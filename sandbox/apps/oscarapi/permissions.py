from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwnerOrStaff(IsAuthenticated):
    """
    Permission that checks if this object has a foreign key pointing to the
    authenticated user of this request
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
