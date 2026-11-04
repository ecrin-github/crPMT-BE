"""
Querysets loading in a fixed number of queries everything the nested output serializers render,
instead of one query per related object (N+1), see #125.

Each function mirrors a serializer: when a serializer gets a new nested field, the matching lookup must be added here,
otherwise the response stays correct but that field goes back to one query per object.
"""
from django.db.models import Prefetch

from core.models.centre import Centre
from core.models.ctu_agreement import CTUAgreement
from core.models.project import Project
from core.models.study import Study
from core.models.study_country import StudyCountry
from core.models.study_ctu import StudyCTU

# Foreign keys rendered by StudyMainDetailsSerializer and StudyMainDetailsNoProjectSerializer
STUDY_MAIN_DETAILS_SELECT = ["c_euco__country", "coordinating_country", "sponsor_country", "sponsor_organisation__country"]
# Foreign keys rendered by StudyOutputSerializer
STUDY_OUTPUT_SELECT = STUDY_MAIN_DETAILS_SELECT + [
    "complex_trial_type", "ecrin_contracting_entity", "lead_ctu__country", "coordinating_investigator__country"]
# Foreign keys rendered by ProjectMainDetailsSerializer and ProjectOutputSerializer
PROJECT_MAIN_DETAILS_SELECT = ["coordinating_institution__country", "coordinator__country"]


def study_country_main_details_prefetches(lookup):
    """StudyCountryMainDetailsSerializer, for the study countries at this lookup"""
    return [
        Prefetch(lookup, queryset=StudyCountry.objects.select_related("country")),
        f"{lookup}__safety_notifications",
        Prefetch(f"{lookup}__study_ctus", queryset=StudyCTU.objects.select_related("ctu__country")),
    ]


def study_country_output_prefetches(lookup):
    """StudyCountryOutputSerializer, for the study countries at this lookup"""
    return [
        Prefetch(lookup, queryset=StudyCountry.objects.select_related("country")),
        f"{lookup}__safety_notifications",
        f"{lookup}__notifications",
        f"{lookup}__submissions",
        Prefetch(f"{lookup}__study_ctus", queryset=StudyCTU.objects.select_related(
            "ctu__country", "contact_person__country", "ctu_contracting_entity")),
        f"{lookup}__study_ctus__services",
        Prefetch(f"{lookup}__study_ctus__centres", queryset=Centre.objects.select_related("hospital__country", "pi__country")),
        f"{lookup}__study_ctus__centres__visits",
        Prefetch(f"{lookup}__study_ctus__ctu_agreements", queryset=CTUAgreement.objects.select_related("ctu_status")),
        f"{lookup}__study_ctus__ctu_agreements__ctu_agreement_amendments",
    ]


def project_main_details_prefetches(prefix=""):
    """ProjectMainDetailsSerializer, for the project at this prefix ("" for a Project queryset)"""
    return [
        f"{prefix}funding_sources",
        f"{prefix}reporting_periods",
        Prefetch(f"{prefix}studies", queryset=Study.objects.select_related(*STUDY_MAIN_DETAILS_SELECT)),
        *study_country_main_details_prefetches(f"{prefix}studies__study_countries"),
    ]


def study_output_prefetches(prefix=""):
    """StudyOutputSerializer, for the studies at this prefix ("" for a Study queryset)"""
    return [
        f"{prefix}medical_fields",
        f"{prefix}populations",
        f"{prefix}regulatory_framework_details",
        f"{prefix}services",
        f"{prefix}satisfaction_surveys",
        f"{prefix}study_agreements__study_agreement_amendments",
        *study_country_output_prefetches(f"{prefix}study_countries"),
    ]


def study_output_queryset():
    """Studies rendered with StudyOutputSerializer (study page)"""
    return (
        Study.objects
        .select_related(*STUDY_OUTPUT_SELECT, *[f"project__{field}" for field in PROJECT_MAIN_DETAILS_SELECT])
        .prefetch_related(*study_output_prefetches(), *project_main_details_prefetches("project__"))
    )


def project_main_details_queryset():
    """Projects rendered with ProjectMainDetailsSerializer (project list)"""
    return (
        Project.objects
        .select_related(*PROJECT_MAIN_DETAILS_SELECT)
        .prefetch_related(*project_main_details_prefetches())
    )


def project_output_queryset():
    """Projects rendered with ProjectOutputSerializer (project page)"""
    return (
        Project.objects
        .select_related(*PROJECT_MAIN_DETAILS_SELECT)
        .prefetch_related(
            "funding_sources",
            "reporting_periods",
            "publications",
            Prefetch("studies", queryset=Study.objects.select_related(*STUDY_OUTPUT_SELECT)),
            *study_output_prefetches("studies__"),
        )
    )


def with_study_country_main_details(queryset):
    """Items rendering their study_country with StudyCountryMainDetailsSerializer (notifications, submissions)"""
    return queryset.select_related("study_country__country").prefetch_related(
        "study_country__safety_notifications",
        Prefetch("study_country__study_ctus", queryset=StudyCTU.objects.select_related("ctu__country")),
    )


def link_study_ctus_to_studies(studies):
    """
    Prefetching a study's study countries then their study CTUs only links each study CTU to its study country,
    so rendering study_ctu.study would query the study again, and then everything nested in it.
    Links each prefetched study CTU to its already loaded study instead.
    """
    study_field = StudyCTU._meta.get_field("study")
    for study in studies:
        for study_country in study.study_countries.all():
            for study_ctu in study_country.study_ctus.all():
                if study_ctu.study_id == study.id:
                    study_field.set_cached_value(study_ctu, study)
