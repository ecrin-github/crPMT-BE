from django.contrib import admin

from users.models.profiles import UserProfiles
from users.models.users import Users


admin.site.register(Users)
admin.site.register(UserProfiles)
