from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminForCreator(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method in ('POST', 'DELETE'):
            if request.user.is_anonymous:
                return False
            return request.user.role == 'admin' or request.user.is_superuser
        else:
            return True


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_anonymous:
            return False
        return request.user.role == 'moderator' or request.user.is_superuser


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin' or request.user.is_superuser


class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_anonymous:
            return False
        return request.user.role == 'user'

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.role == 'moderator'  # TODO: заменить на .is_staff