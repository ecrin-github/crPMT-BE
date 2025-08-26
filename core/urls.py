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
    path('studies', study_list),
    path('studies/<int:pk>', study_detail),
    path('studies/<int:pk>/study-countries', study_country_list),
    path('studies/<int:sId>/study-countries/<int:pk>', study_country_detail),
    path('studies/<int:pk>/study-ctus', study_ctu_list),
    path('studies/<int:sId>/study-ctus/<int:pk>', study_ctu_detail),
    path('studies/<int:pk>/centres', centre_list),
    path('studies/<int:sId>/centres/<int:pk>', centre_detail),
    path('studies/<int:pk>/visits', visit_list),
    path('studies/<int:sId>/visits-ctus/<int:pk>', visit_detail),
    path('study-countries', study_country_list),
    path('study-countries/<int:pk>', study_country_detail),
    path('study-countries/<int:pk>/study-ctus', study_ctu_list),
    path('study-countries/<int:scId>/study-ctus/<int:pk>', study_ctu_detail),
    path('study-ctus', study_ctu_list),
    path('study-ctus/<int:pk>', study_ctu_detail),
    path('study-ctus/<int:pk>/visits', visit_list),
    path('study-ctus/<int:sctuId>/visits/<int:pk>', visit_detail),
    path('study-ctus/<int:pk>/centres', centre_list),
    path('study-ctus/<int:sctuId>/centres/<int:pk>', centre_detail),
    path('centres', centre_list),
    path('centres/<int:pk>', centre_detail),
    path('centres/<int:pk>/visits', visit_list),
    path('centres/<int:cId>/visits/<int:pk>', visit_detail),
    path('visits', visit_list),
    path('visits/<int:pk>', visit_detail),
    path('reference-count-by-class/<class_name>/<obj_id>', ReferenceCountByClass.as_view()),
]