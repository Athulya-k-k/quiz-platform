# quiz_app/permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access certain views
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow admin users full access and normal users read-only access
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow owners or admin users to access/modify objects
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can access everything
        if request.user.is_admin:
            return True
        # Check if user is the owner of the object
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return False