from rest_framework.permissions import BasePermission


class AdminForCreator(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('POST', 'DELETE'):
            if request.user.is_anonymous:
                return False
            return request.user.role == 'admin' or request.user.is_superuser
        else:
            return True


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'moderator' or request.user.is_superuser


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin' or request.user.is_superuser


class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'user'

