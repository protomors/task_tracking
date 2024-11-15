from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


# class UserIsOwnerMixin(object):
#     def dispatch(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.user == request.user:
#             return super().dispatch(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
        
class RedirectAuthenticatedUserMixin(AccessMixin):
    """Міксин для перенаправлення залогінених користувачів."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Змінити 'home' на вашу URL-іменну сторінку
        return super().dispatch(request, *args, **kwargs)