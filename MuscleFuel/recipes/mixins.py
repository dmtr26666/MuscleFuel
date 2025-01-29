from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RecipePermissionMixin(UserPassesTestMixin):
    """
    Mixin to check if a user has permission to edit or delete an object.
    Permissions:
        - User is the object owner (author)
        - User is in a specific group (e.g., moderator)
        - User is a superuser
    """

    permission_group = 'Moderator'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user

        if obj.user == user or user.groups.filter(name=self.permission_group).exists() or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        raise PermissionDenied("You are not authorized to access this page.")