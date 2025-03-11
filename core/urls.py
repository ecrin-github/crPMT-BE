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


urlpatterns = [
    path('projects', project_list),
    path('projects/<int:pk>', project_detail),
    path('studies', study_list),
    path('studies/<int:pk>', study_detail),
    path('studies/<int:studyId>/study-countries', study_country_list),
    path('studies/<int:studyId>/study-countries/<int:pk>', study_country_detail),
]