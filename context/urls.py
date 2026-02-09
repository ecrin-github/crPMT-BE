from django.urls import path

from context.views.views import *


authority_list = AuthorityView.as_view({
    'get': 'list',
    'post': 'create'
})
authority_detail = AuthorityView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


complex_trial_type_list = ComplexTrialTypeView.as_view({
    'get': 'list',
    'post': 'create'
})
complex_trial_type_detail = ComplexTrialTypeView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

country_list = CountryView.as_view({
    'get': 'list',
})
country_detail = CountryView.as_view({
    'get': 'retrieve',
})

ctu_list = CTUView.as_view({
    'get': 'list',
    'post': 'create'
})
ctu_detail = CTUView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

ctu_status_list = CTUStatusView.as_view({
    'get': 'list',
    'post': 'create'
})
ctu_status_detail = CTUStatusView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

hospital_list = HospitalView.as_view({
    'get': 'list',
    'post': 'create'
})
hospital_detail = HospitalView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

funding_source_list = FundingSourceView.as_view({
    'get': 'list',
    'post': 'create'
})
funding_source_detail = FundingSourceView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

medical_field_list = MedicalFieldView.as_view({
    'get': 'list',
    'post': 'create'
})
medical_field_detail = MedicalFieldView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

organisation_list = OrganisationView.as_view({
    'get': 'list',
    'post': 'create'
})
organisation_detail = OrganisationView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

person_list = PersonView.as_view({
    'get': 'list',
    'post': 'create'
})
person_detail = PersonView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

population_list = PopulationView.as_view({
    'get': 'list',
    'post': 'create'
})
population_detail = PopulationView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

regulatory_framework_detail_list = RegulatoryFrameworkDetailView.as_view({
    'get': 'list',
    'post': 'create'
})
regulatory_framework_detail_detail = RegulatoryFrameworkDetailView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

safety_notification_type_list = SafetyNotificationTypeView.as_view({
    'get': 'list',
    'post': 'create'
})
safety_notification_type_detail = SafetyNotificationTypeView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

service_list = ServiceView.as_view({
    'get': 'list',
    'post': 'create'
})
service_detail = ServiceView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

study_status_list = StudyStatusView.as_view({
    'get': 'list',
    'post': 'create'
})
study_status_detail = StudyStatusView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

visit_type_list = VisitTypeView.as_view({
    'get': 'list',
    'post': 'create'
})
visit_type_detail = VisitTypeView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('complex-trial-types', complex_trial_type_list),
    path('complex-trial-types/<int:pk>', complex_trial_type_detail),
    path('countries', country_list),
    path('countries/<int:pk>', country_detail),
    path('ctus', ctu_list),
    path('ctus/<int:pk>', ctu_detail),
    path('ctu-statuses', ctu_status_list),
    path('ctu-statuses/<int:pk>', ctu_status_detail),
    path('hospitals', hospital_list),
    path('hospitals/<int:pk>', hospital_detail),
    path('funding-sources', funding_source_list),
    path('funding-sources/<int:pk>', funding_source_detail),
    path('medical-fields', medical_field_list),
    path('medical-fields/<int:pk>', medical_field_detail),
    path('organisations', organisation_list),
    path('organisations/<int:pk>', organisation_detail),
    path('persons', person_list),
    path('persons/<int:pk>', person_detail),
    path('populations', population_list),
    path('populations/<int:pk>', population_detail),
    path('regulatory-framework-details', regulatory_framework_detail_list),
    path('regulatory-framework-details/<int:pk>', regulatory_framework_detail_detail),
    path('safety-notification-types', safety_notification_type_list),
    path('safety-notification-types/<int:pk>', safety_notification_type_detail),
    path('services', service_list),
    path('services/<int:pk>', service_detail),
    path('visit-types', visit_type_list),
    path('visit-types/<int:pk>', visit_type_detail),
]