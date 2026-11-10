from datetime import date, datetime, time, timedelta

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models.reporting_period import ReportingPeriod
from core.models.study import Study
from core.models.submission import Submission


# Groups of the "Studies by status" chart, in display order, with the Study.status values they contain.
# Study.status is free text whose possible values are listed in the front-end (STUDY_STATUSES in src/assets/js/constants.ts)
STATUS_GROUPS = [
    ("Start-up", ["Start-up phase"]),
    ("Running", [
        "Running phase: Regulatory & ethical approvals",
        "Running phase: Follow up",
        "Running phase: Organisation of close-out",
    ]),
    ("Completion", ["Completion & termination phase"]),
    ("Completed", ["Completed"]),
    ("Stopped", ["Withdrawn", "On hold"]),
]
STATUS_OTHER = "Other"       # Status not in the list above (e.g. renamed status)
STATUS_NOT_SET = "Not set"   # Empty status
STATUS_GROUP_NAMES = [group for group, _ in STATUS_GROUPS] + [STATUS_OTHER, STATUS_NOT_SET]

_GROUP_OF_STATUS = {status: group for group, statuses in STATUS_GROUPS for status in statuses}


# Date counted for each series of the "Regulatory submissions" chart
SUBMISSION_DATE_FIELDS = {"submitted": "submission_date", "approved": "approval_date"}


def get_dashboard_submissions():
    """Submissions counted by the "Regulatory submissions" chart and listed when clicking on it: all but not applicable"""
    return Submission.objects.filter(not_applicable=False)


def get_status_group(status):
    """Status group of a Study.status value. Single place of this rule, used by the chart and by its study list"""
    status = (status or "").strip()
    if not status:
        return STATUS_NOT_SET
    return _GROUP_OF_STATUS.get(status, STATUS_OTHER)

SUBMISSIONS_MONTHS = 6       # Number of months of the "Regulatory submissions" chart, current month included
DEADLINES_LIMIT = 5          # Number of items of the "Upcoming deadlines" list
DEADLINES_DAYS = 60          # Only the deadlines of the next DEADLINES_DAYS days, today included


class DashboardView(APIView):
    """
    Data of the dashboard of the internal main page (#36), computed by the database (COUNT / GROUP BY)
    instead of sending every study to the front-end. Fixed number of SQL queries whatever the amount of data.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "studies_by_status": self.get_studies_by_status(),
            "submissions_by_month": self.get_submissions_by_month(),
            "upcoming_deadlines": self.get_upcoming_deadlines(),
        })

    def get_studies_by_status(self):
        """Number of studies per status group, every group included (even with 0 studies) to keep a stable order"""
        counts = {group: 0 for group in STATUS_GROUP_NAMES}

        # 1 query: SELECT status, COUNT(id) FROM studies GROUP BY status
        for row in Study.objects.values("status").annotate(count=Count("id")).order_by():
            counts[get_status_group(row["status"])] += row["count"]

        return [{"name": name, "value": value} for name, value in counts.items()]

    def get_submissions_by_month(self):
        """
        Number of submissions sent and approved per month over the last SUBMISSIONS_MONTHS months.
        Every type of submission is counted (initial, amendments, other notifications), except the not applicable ones.
        """
        months = self.get_last_months(SUBMISSIONS_MONTHS)
        start = timezone.make_aware(datetime.combine(months[0], time.min))
        submissions = get_dashboard_submissions()

        submitted = self.count_per_month(submissions, SUBMISSION_DATE_FIELDS["submitted"], start)
        approved = self.count_per_month(submissions, SUBMISSION_DATE_FIELDS["approved"], start)

        return [{
            "month": month.strftime("%Y-%m"),
            "submitted": submitted.get(month, 0),
            "approved": approved.get(month, 0),
        } for month in months]

    def get_upcoming_deadlines(self):
        """Next DEADLINES_LIMIT ends of reporting periods in the next DEADLINES_DAYS days, closest first"""
        today = timezone.make_aware(datetime.combine(timezone.localdate(), time.min))
        end = today + timedelta(days=DEADLINES_DAYS + 1)   # Midnight after the last day of the window

        # 1 query, the project of each reporting period is loaded with a join
        reporting_periods = (ReportingPeriod.objects
                             .filter(end__gte=today, end__lt=end)
                             .select_related("project")
                             .order_by("end")[:DEADLINES_LIMIT])

        return [{
            "title": "Reporting period",
            "details": self.get_reporting_period_details(rp),
            "date": timezone.localtime(rp.end).date().isoformat(),
        } for rp in reporting_periods]

    @staticmethod
    def get_last_months(number):
        """First day of each of the last `number` months, oldest first, current month included"""
        today = timezone.localdate()
        months = []
        year, month = today.year, today.month
        for _ in range(number):
            months.append(date(year, month, 1))
            month -= 1
            if month == 0:
                month, year = 12, year - 1
        return list(reversed(months))

    @staticmethod
    def count_per_month(queryset, date_field, start):
        """{first day of the month: number of rows whose date_field is in that month}, from start"""
        # 1 query: SELECT DATE_TRUNC('month', date_field), COUNT(id) ... GROUP BY 1
        rows = (queryset
                .filter(**{f"{date_field}__gte": start})
                .annotate(month=TruncMonth(date_field))
                .values("month")
                .annotate(count=Count("id"))
                .order_by())
        return {timezone.localtime(row["month"]).date(): row["count"] for row in rows}

    @staticmethod
    def get_reporting_period_details(rp):
        """'Project short name · Period 2' of a reporting period, with what is available"""
        parts = []
        if rp.project:
            parts.append(rp.project.short_name or rp.project.name or "")
        if rp.stage is not None:
            parts.append(f"Period {rp.stage}")
        return " · ".join(part for part in parts if part)


class DashboardStudiesView(APIView):
    """
    Studies of one status group of the "Studies by status" chart, with their project, shown when clicking on the chart.
    GET core/dashboard/studies?status_group=Running
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        status_group = request.query_params.get("status_group")
        if status_group not in STATUS_GROUP_NAMES:
            return Response({"error": f"status_group must be one of: {', '.join(STATUS_GROUP_NAMES)}"}, status=400)

        # 1 query with the project joined. The group is computed in Python with the same function as the chart,
        # so that the list always matches the number shown on the chart (e.g. for "Other" or statuses with spaces)
        studies = Study.objects.values(
            "id", "short_title", "title", "status", "project_id", "project__short_name", "project__name"
        ).order_by("short_title", "id")

        return Response({"studies": [{
            "id": study["id"],
            "short_title": study["short_title"] or study["title"] or "",
            "status": study["status"],
            "project": {
                "id": study["project_id"],
                "short_name": study["project__short_name"] or study["project__name"] or "",
            } if study["project_id"] else None,
        } for study in studies if get_status_group(study["status"]) == status_group]})


class DashboardSubmissionsView(APIView):
    """
    Submissions of one bar of the "Regulatory submissions" chart, shown when clicking on it.
    GET core/dashboard/submissions?month=2026-06&series=submitted (or approved)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        series = request.query_params.get("series")
        if series not in SUBMISSION_DATE_FIELDS:
            return Response({"error": f"series must be one of: {', '.join(SUBMISSION_DATE_FIELDS)}"}, status=400)
        try:
            first_day = datetime.strptime(request.query_params.get("month") or "", "%Y-%m").date()
        except ValueError:
            return Response({"error": "month must be in the YYYY-MM format"}, status=400)

        # Same month boundaries as TruncMonth in the chart: from the 1st of the month to the 1st of the next one
        next_month = date(first_day.year + first_day.month // 12, first_day.month % 12 + 1, 1)
        date_field = SUBMISSION_DATE_FIELDS[series]

        # 1 query, with the authority, country, study and project joined
        submissions = (get_dashboard_submissions()
                       .filter(**{
                           f"{date_field}__gte": timezone.make_aware(datetime.combine(first_day, time.min)),
                           f"{date_field}__lt": timezone.make_aware(datetime.combine(next_month, time.min)),
                       })
                       .select_related("authority", "study_country__country", "study_country__study__project")
                       .order_by(date_field, "id"))

        return Response({"submissions": [self.serialize(submission, date_field) for submission in submissions]})

    @staticmethod
    def serialize(submission, date_field):
        sc = submission.study_country
        study = sc.study if sc else None
        project = study.project if study else None

        if submission.is_amendment:
            submission_type = "Amendment"
        elif submission.is_other_notification:
            submission_type = "Other notification"
        else:
            submission_type = "Initial submission"

        return {
            "id": submission.id,
            "date": timezone.localtime(getattr(submission, date_field)).date().isoformat(),
            "type": submission_type,
            "authority": submission.authority.code if submission.authority else None,
            "country": sc.country.name if sc and sc.country else None,
            "study": {"id": study.id, "short_title": study.short_title or study.title or ""} if study else None,
            "project": {"id": project.id, "short_name": project.short_name or project.name or ""} if project else None,
        }
