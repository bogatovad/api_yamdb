from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminForCreator(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('POST', 'DELETE'):
            if request.user.is_anonymous:
                return False
            return request.user.role == 'admin' or request.user.is_superuser
        else:
            return True

