from django.urls import path

from core.views.views import *


project_list = ProjectView.as_view({
    'get': 'list',
    'post': 'create'
})
project_detail = ProjectView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

reporting_period_list = ReportingPeriodView.as_view({
    'get': 'list',
    'post': 'create'
})
reporting_period_detail = ReportingPeriodView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

study_list = StudyView.as_view({
    'get': 'list',
    'post': 'create'
})
study_detail = StudyView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

study_country_list = StudyCountryView.as_view({
    'get': 'list',
    'post': 'create'
})
study_country_detail = StudyCountryView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

notification_list = NotificationView.as_view({
    'get': 'list',
    'post': 'create'
})
notification_detail = NotificationView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

safety_notification_list = SafetyNotificationView.as_view({
    'get': 'list',
    'post': 'create'
})
safety_notification_detail = SafetyNotificationView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

submission_list = SubmissionView.as_view({
    'get': 'list',
    'post': 'create'
})
submission_detail = SubmissionView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

study_ctu_list = StudyCTUView.as_view({
    'get': 'list',
    'post': 'create'
})
study_ctu_detail = StudyCTUView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

ctu_agreement_list = CTUAgreementView.as_view({
    'get': 'list',
    'post': 'create'
})
ctu_agreement_detail = CTUAgreementView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

ctu_agreement_amendment_list = CTUAgreementAmendmentView.as_view({
    'get': 'list',
    'post': 'create'
})
ctu_agreement_amendment_detail = CTUAgreementAmendmentView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

centre_list = CentreView.as_view({
    'get': 'list',
    'post': 'create'
})
centre_detail = CentreView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

visit_list = VisitView.as_view({
    'get': 'list',
    'post': 'create'
})
visit_detail = VisitView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('projects', project_list),
    path('projects/<int:pk>', project_detail),
    path('projects-by-funding-source/<fs_id>', ProjectsByFundingSource.as_view()),
    path('projects-by-organisation/<org_id>', ProjectsByOrganisation.as_view()),
    path('projects-by-service/<s_id>', ProjectsByService.as_view()),
    path('reporting-periods', reporting_period_list),
    path('reporting-periods/<int:pk>', reporting_period_detail),
    path('studies', study_list),
    path('studies/<int:pk>', study_detail),
    path('studies/<int:pk>/study-countries', study_country_list),
    path('studies/<int:pk>/study-ctus', study_ctu_list),
    path('studies/<int:pk>/centres', centre_list),
    path('studies/<int:pk>/visits', visit_list),
    path('study-countries', study_country_list),
    path('study-countries/<int:pk>', study_country_detail),
    path('study-countries/<int:pk>/notifications', notification_list),
    path('study-countries/<int:pk>/study-ctus', study_ctu_list),
    path('study-countries/<int:pk>/submissions', submission_list),
    path('notifications', notification_list),
    path('notifications/<int:pk>', notification_detail),
    path('safety-notifications', safety_notification_list),
    path('safety-notifications/<int:pk>', safety_notification_detail),
    path('study-ctus', study_ctu_list),
    path('study-ctus/<int:pk>', study_ctu_detail),
    path('study-ctus/<int:pk>/visits', visit_list),
    path('study-ctus/<int:pk>/centres', centre_list),
    path('study-ctus/<int:pk>/ctu-agreements', ctu_agreement_list),
    path('ctu-agreements', ctu_agreement_list),
    path('ctu-agreements/<int:pk>', ctu_agreement_detail),
    path('ctu-agreements', ctu_agreement_list),
    path('ctu-agreements/<int:pk>/ctu-agreement-amendments', ctu_agreement_amendment_list),
    path('ctu-agreement-amendments/<int:pk>', ctu_agreement_amendment_detail),
    path('ctu-agreement-amendments', ctu_agreement_amendment_list),
    path('submissions', submission_list),
    path('submissions/<int:pk>', submission_detail),
    path('centres', centre_list),
    path('centres/<int:pk>', centre_detail),
    path('centres/<int:pk>/visits', visit_list),
    path('visits', visit_list),
    path('visits/<int:pk>', visit_detail),
    path('reference-count-by-class/<class_name>/<obj_id>', ReferenceCountByClass.as_view()),
]