from pathlib import Path
import re
import unicodedata

import pandas as pd
from rapidfuzz import fuzz

from context.models.ctu import CTU
from context.models.country import Country


def get_ctu_csv_path():
    """
    Return the path of the CSV export used for bulk CTU synchronization.

    This CSV-based sync is currently optional / secondary, since the application
    now mainly relies on on-demand synchronization at save time.
    """
    base_dir = Path(__file__).resolve().parents[2]
    return base_dir / "scripts" / "data" / "ctus_service_providers_with_ids.csv"


def normalize_country_to_iso2(raw_country: str | None) -> str | None:
    """
    Normalize a country code received from SharePoint / CSV to ISO2 format.

    Supported inputs:
    - ISO2 (example: FR)
    - ISO3 (example: FRA)

    Returns:
        ISO2 code or None if the value cannot be mapped.
    """
    if not raw_country:
        return None

    raw = str(raw_country).strip().upper()

    iso3_to_iso2 = {
        "AUT": "AT",
        "BEL": "BE",
        "BGR": "BG",
        "HRV": "HR",
        "CYP": "CY",
        "CZE": "CZ",
        "DNK": "DK",
        "EST": "EE",
        "FIN": "FI",
        "FRA": "FR",
        "DEU": "DE",
        "GRC": "GR",
        "HUN": "HU",
        "IRL": "IE",
        "ITA": "IT",
        "LVA": "LV",
        "LTU": "LT",
        "LUX": "LU",
        "MLT": "MT",
        "NLD": "NL",
        "POL": "PL",
        "PRT": "PT",
        "ROU": "RO",
        "SVK": "SK",
        "SVN": "SI",
        "ESP": "ES",
        "SWE": "SE",
        "CHE": "CH",
        "NOR": "NO",
        "ISL": "IS",
        "GBR": "GB",
    }

    if len(raw) == 2:
        return raw

    return iso3_to_iso2.get(raw)


def normalize_text(value: str | None) -> str:
    """
    Normalize text for robust comparison.

    Transformations:
    - lowercase
    - remove accents
    - remove punctuation
    - collapse multiple spaces

    Example:
        "CHU GRENOBLE-ALPES" -> "chu grenoble alpes"
    """
    if not value:
        return ""

    value = str(value).strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def canonicalize_name(value: str | None) -> str:
    """
    Build a canonical version of a name by sorting normalized words alphabetically.

    This helps match names with the same words in a different order.

    Example:
        "CHU ALPES GRENOBLE" -> "alpes chu grenoble"
        "CHU GRENOBLE ALPES" -> "alpes chu grenoble"
    """
    normalized = normalize_text(value)
    tokens = normalized.split()
    tokens.sort()
    return " ".join(tokens)


def exact_canonical_match(left: str | None, right: str | None) -> bool:
    """
    Compare two names using their canonical representation.

    Returns True only if both canonical values are non-empty and identical.
    """
    left_canonical = canonicalize_name(left)
    right_canonical = canonicalize_name(right)

    return bool(left_canonical) and left_canonical == right_canonical


def fuzzy_name_match(left: str | None, right: str | None, threshold: int = 95) -> bool:
    """
    Compare two names using a fuzzy token-based similarity score.

    We use canonicalized names and token_sort_ratio to make the comparison
    robust to word order differences.

    Example:
        "CHU ALPES GRENOBLE"
        "CHU GRENOBLE ALPES"
    -> very high score

    The threshold is intentionally high to reduce false positives.
    """
    left_canonical = canonicalize_name(left)
    right_canonical = canonicalize_name(right)

    if not left_canonical or not right_canonical:
        return False

    score = fuzz.token_sort_ratio(left_canonical, right_canonical)
    return score >= threshold


def find_matching_ctu_by_business_rules(name, short_name, country):
    """
    Fallback CTU matching strategy when no SharePoint ID link exists yet.

    Matching order:
    1. Same country + exact canonical short_name
    2. Same country + exact canonical name
    3. Same country + fuzzy short_name
    4. Same country + fuzzy name

    Why country is checked first:
    It prevents linking CTUs from different countries that happen to have
    similar names.

    Returns:
        Matching CTU instance or None.
    """
    if not country:
        return None

    candidates = CTU.objects.filter(country=country)

    # 1. Strong fallback on exact canonical short_name
    if short_name:
        for candidate in candidates:
            if exact_canonical_match(candidate.short_name, short_name):
                return candidate

    # 2. Exact canonical match on full name
    if name:
        for candidate in candidates:
            if exact_canonical_match(candidate.name, name):
                return candidate

    # 3. Fuzzy match on short_name
    if short_name:
        for candidate in candidates:
            if fuzzy_name_match(candidate.short_name, short_name, threshold=95):
                return candidate

    # 4. Fuzzy match on full name
    if name:
        for candidate in candidates:
            if fuzzy_name_match(candidate.name, name, threshold=95):
                return candidate

    return None


def update_ctu_from_sharepoint_fields(
    ctu: CTU, sharepoint_fields: dict, sharepoint_item_id=None
) -> CTU:
    """
    Update a CTU instance with the fields received from SharePoint.

    Only fields explicitly present in the payload and different from the current
    DB values are updated.

    Also ensures:
    - the CTU is marked as non-manual when linked/synced from SharePoint
    - the SharePoint ID is stored when provided

    Returns:
        Updated CTU instance.
    """
    fields_to_update = []

    if sharepoint_item_id and ctu.sharepoint_item_id != sharepoint_item_id:
        ctu.sharepoint_item_id = sharepoint_item_id
        fields_to_update.append("sharepoint_item_id")

    for field_name, new_value in sharepoint_fields.items():
        # Only update fields actually sent by SharePoint / frontend.
        # This avoids overwriting existing local values with None.
        if new_value is not None:
            current_value = getattr(ctu, field_name)
            if current_value != new_value:
                setattr(ctu, field_name, new_value)
                fields_to_update.append(field_name)

    if ctu.manual_add:
        ctu.manual_add = False
        fields_to_update.append("manual_add")

    if fields_to_update:
        fields_to_update = list(dict.fromkeys(fields_to_update))
        ctu.save(update_fields=fields_to_update)

    return ctu


def resolve_ctu_from_sharepoint(data):
    """
    Resolve a SharePoint CTU into a local DB CTU.

    Main strategy:
    1. Try to match by SharePoint item ID (strongest match)
    2. If not found, try business fallback matching:
       - same country
       - exact canonical match
       - then fuzzy match with a high threshold
    3. If still not found, create a new CTU

    Whenever a match is found, DB fields are updated with the latest SharePoint data
    for all fields included in the payload.
    """
    sp_id = data.get("sharepoint_item_id")
    name = data.get("name")
    short_name = data.get("short_name")
    country = data.get("country")

    sharepoint_fields = {
        "name": name,
        "short_name": short_name,
        "country": country,
        "address_info": data.get("address_info"),
        "contact": data.get("contact"),
    }

    # 1. Strongest match: already linked by SharePoint item ID.
    if sp_id:
        existing = CTU.objects.filter(sharepoint_item_id=sp_id).first()
        if existing:
            return update_ctu_from_sharepoint_fields(
                ctu=existing,
                sharepoint_fields=sharepoint_fields,
                sharepoint_item_id=sp_id,
            )

    # 2. Business fallback using same-country normalized / fuzzy matching.
    existing = find_matching_ctu_by_business_rules(
        name=name,
        short_name=short_name,
        country=country,
    )
    if existing:
        return update_ctu_from_sharepoint_fields(
            ctu=existing,
            sharepoint_fields=sharepoint_fields,
            sharepoint_item_id=sp_id,
        )

    # 3. No match found: create a new CTU from SharePoint data.
    return CTU.objects.create(
        sharepoint_item_id=sp_id or None,
        name=name,
        short_name=short_name,
        country=country,
        address_info=data.get("address_info"),
        contact=data.get("contact"),
        manual_add=False,
    )


def sync_ctus_from_sharepoint():
    """
    Bulk synchronize CTUs from the SharePoint CSV export.

    This function:
    - reads the CSV file
    - resolves each SharePoint row against the local CTU table
    - creates missing CTUs
    - updates existing ones when differences are detected

    Returns a summary dictionary for logging / command output.
    """
    csv_path = get_ctu_csv_path()

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path, sep=",", dtype=str, na_filter=False)

    required_columns = [
        "sharepoint_item_id",
        "short_name",
        "name",
        "country_iso2",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required CSV columns: {missing_columns}")

    processed = 0
    skipped = 0
    created = 0
    updated = 0

    for index, row in df.iterrows():
        raw_country = row.get("country_iso2")
        country_iso2 = normalize_country_to_iso2(raw_country)
        country = (
            Country.objects.filter(iso2=country_iso2).first() if country_iso2 else None
        )

        if not country:
            skipped += 1
            print(f"SKIP row {index + 1}: country not found for '{raw_country}'")
            continue

        sharepoint_item_id = (row.get("sharepoint_item_id") or "").strip() or None
        name = (row.get("name") or "").strip() or None
        short_name = (row.get("short_name") or "").strip() or None

        before_existing = None
        if sharepoint_item_id:
            before_existing = CTU.objects.filter(
                sharepoint_item_id=sharepoint_item_id
            ).first()

        fallback_existing = None
        if not before_existing:
            fallback_existing = find_matching_ctu_by_business_rules(
                name=name,
                short_name=short_name,
                country=country,
            )

        payload = {
            "sharepoint_item_id": sharepoint_item_id,
            "name": name,
            "short_name": short_name,
            "country": country,
        }

        ctu = resolve_ctu_from_sharepoint(payload)

        if before_existing:
            updated += 1
            print(
                f"UPDATED row {index + 1}: existing SharePoint-linked CTU "
                f"sharepoint_item_id={sharepoint_item_id} -> CTU id={ctu.id}"
            )
        elif fallback_existing:
            updated += 1
            print(
                f"UPDATED row {index + 1}: matched existing CTU id={ctu.id} "
                f"and linked sharepoint_item_id={sharepoint_item_id}"
            )
        else:
            created += 1
            print(
                f"CREATED row {index + 1}: CTU id={ctu.id}, "
                f"sharepoint_item_id={sharepoint_item_id}"
            )

        processed += 1

    return {
        "processed": processed,
        "skipped": skipped,
        "created": created,
        "updated": updated,
        "csv_path": str(csv_path),
    }
