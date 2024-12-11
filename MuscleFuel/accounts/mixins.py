from django.core.exceptions import PermissionDenied


class CheckUserAuthorization:
    def dispatch(self, request, *args, **kwargs):
        # Fetch the user object
        user = self.get_object()

        # Check if the current user is the profile owner
        if user != self.request.user.profile:
            raise PermissionDenied("You are not authorized to edit this recipe.")  # Return 403 Forbidden

        return super().dispatch(request, *args, **kwargs)