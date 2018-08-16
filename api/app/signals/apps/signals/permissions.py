from rest_framework import permissions


class StatusPermission(permissions.BasePermission):
    """
    Permission check for status.
    """
    def has_permission(self, request, view):
        if request.user:
            if request.method == 'POST' and not request.user.has_perm('signals.add_status'):
                return False
            return True
        else:
            return False


class CategoryPermission(permissions.BasePermission):
    """
    Permission check for status.
    """
    def has_permission(self, request, view):
        if request.user:
            if request.method == 'POST' and not request.user.has_perm('signals.add_category'):
                return False
            return True
        else:
            return False


class LocationPermission(permissions.BasePermission):
    """
    Permission check for status.
    """
    def has_permission(self, request, view):
        if request.user:
            if request.method == 'POST' and not request.user.has_perm('signals.add_location'):
                return False
            return True
        else:
            return False


class ReporterPermission(permissions.BasePermission):
    """
    Permission check for status.
    """
    def has_permission(self, request, view):
        if request.user:
            if request.method == 'POST' and not request.user.has_perm('siognals.add_reporter'):
                return False
            return True
        else:
            return False