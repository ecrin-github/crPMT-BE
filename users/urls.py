from django.urls import path

from users.views.views import *


users_login = UserView.as_view({
    'post': 'create'
})

users_detail = UserView.as_view({
    'get': 'retrieve',
    'post': 'create',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# user_profiles_detail = UserProfilesList.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })


urlpatterns = [
    path('', UsersList.as_view()),
    path('login', users_login),
    path('by-name', UsersByName.as_view()),
    # path('by-ls-aai-id', UserByLsAaiId.as_view()),
    # path('by-email', UserByEmail.as_view()),

    # path('users-to-notify/<sd_oid>', UsersToNotify.as_view()),

    path('<uuid:pk>', users_detail),

    # path('<uuid:userId>/profile/<uuid:pk>', user_profiles_detail),
]
