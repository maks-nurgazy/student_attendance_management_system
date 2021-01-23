from rest_framework import permissions
from rest_framework.permissions import BasePermission


class TeacherOnly(BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            user = request.user
            role = user
            print(role)
            if role is not None:
                return user.role == 2
        else:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
