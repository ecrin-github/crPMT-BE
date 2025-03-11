from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        return False


class WriteOnlyForOwnOrg(BasePermission):
    """ Write permissions for own organisation only """
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # For studies and data objects
            try:
                if request.user.user_profile.organisation.id == obj.organisation.id:
                    return True
            except AttributeError:
                pass

            # For studies sub-objects
            try:
                if request.user.user_profile.organisation.id == obj.study_id.organisation.id:
                    return True
            except AttributeError:
                pass

            # For data objects sub-objects
            try:
                if request.user.user_profile.organisation.id == obj.object_id.organisation.id:
                    return True
            except AttributeError:
                pass
            try:
                if request.user.user_profile.organisation.id == obj.data_object.organisation.id:
                    return True
            except AttributeError:
                pass
        return False


class WriteOnlyForSelf(BasePermission):
    """ Write permissions for own user/user profile only TODO """
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'PUT', 'PATCH']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method in ['PUT', 'PATCH']:
            return False
            # try:
            #     if request.user.id == obj.id:
            #         return True
            # except AttributeError:
            #     pass
        return False