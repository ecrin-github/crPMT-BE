from django.urls import path

from context.views.views import *


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


urlpatterns = [
    path('countries', country_list),
    path('countries/<int:pk>', country_detail),
    path('ctus', ctu_list),
    path('ctus/<int:pk>', ctu_detail),
    path('funding-sources', funding_source_list),
    path('funding-sources/<int:pk>', funding_source_detail),
    path('persons', person_list),
    path('persons/<int:pk>', person_detail),
    path('services', service_list),
    path('services/<int:pk>', service_detail),
    path('study-statuses', study_status_list),
    path('study-statuses/<int:pk>', study_status_detail),
]