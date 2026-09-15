import pandas as pd
import sqlalchemy as db
from pathlib import Path


def main():
    base_dir = Path(__file__).resolve().parent
    ctuFp = base_dir / "data" / "ctus_service_providers_with_ids.csv"

    db_hostname = "localhost"
    db_port = "5432"
    db_name = "crpmt"

    if not ctuFp.exists():
        raise FileNotFoundError(f"CSV file not found: {ctuFp}")

    df = pd.read_csv(ctuFp, sep=",", dtype=str, na_filter=False)

    required_columns = [
        "sharepoint_item_id",
        "short_name",
        "name",
        "country_iso2",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required CSV columns: {missing_columns}")

    # Keep only useful columns for CTU sync
    #)
    df_ctu = df[["sharepoint_item_id", "short_name", "name", "country_iso2"]].copy()
    df_ctu = df_ctu.drop_duplicates()

    user = input("Enter DB user: ")
    password = input("Enter DB password: ")

    engine = db.create_engine(
        f"postgresql+psycopg2://{user}:{password}@{db_hostname}:{db_port}/{db_name}"
    )

    metadata = db.MetaData()
    countries = db.Table("countries", metadata, autoload_with=engine)
    ctus = db.Table("ctus", metadata, autoload_with=engine)

    with engine.connect() as conn:
        for _, row in df_ctu.iterrows():
            sharepoint_item_id = row["sharepoint_item_id"].strip()
            short_name = row["short_name"].strip()
            name = row["name"].strip()
            country_iso2 = row["country_iso2"].strip().upper()

            # find country FK
            stmt_country = db.select(countries.c.iso2).where(countries.c.iso2 == country_iso2)
            res_country = conn.execute(stmt_country).first()

            if not res_country:
                print(f"Couldn't find country from iso2 code {country_iso2}")
                continue

            # 1. exact match by sharepoint_item_id
            existing_by_sp = None
            if sharepoint_item_id:
                stmt_existing_by_sp = db.select(ctus.c.id).where(
                    ctus.c.sharepoint_item_id == sharepoint_item_id
                )
                existing_by_sp = conn.execute(stmt_existing_by_sp).first()

            if existing_by_sp:
                print(
                    f"CTU already linked by sharepoint_item_id={sharepoint_item_id}, skipped: "
                    f"{short_name} - {name}"
                )
                continue

            # 2. fallback by business fields
            stmt_existing_ctu = db.select(ctus.c.id, ctus.c.sharepoint_item_id).where(
                ctus.c.name == name,
                ctus.c.short_name == short_name,
                ctus.c.country_id == country_iso2,
            )
            existing_ctu = conn.execute(stmt_existing_ctu).first()

            if existing_ctu:
                # update sharepoint_item_id if missing
                if sharepoint_item_id and not existing_ctu[1]:
                    stmt_update = (
                        ctus.update()
                        .where(ctus.c.id == existing_ctu[0])
                        .values(sharepoint_item_id=sharepoint_item_id)
                    )
                    conn.execute(stmt_update)
                    conn.commit()
                    print(
                        f"Updated existing CTU with sharepoint_item_id={sharepoint_item_id}: "
                        f"{short_name} - {name}"
                    )
                else:
                    print(f"CTU already exists, skipped: {short_name} - {name}")
                continue

            # 3. create new CTU
            insert_payload = {
                "sharepoint_item_id": sharepoint_item_id or None,
                "name": name,
                "short_name": short_name,
                "country_id": country_iso2,
                "manual_add": False,
            }

            conn.execute(ctus.insert(), insert_payload)
            conn.commit()
            print(f"Inserted CTU: {short_name} - {name}")

    print("Done!")


if __name__ == "__main__":
    main()