# from django.contrib import messages
# from django.shortcuts import redirect
# from django.utils.deprecation import MiddlewareMixin
# from django.conf import settings

# class SessionExpiredMiddleware(MiddlewareMixin):
#     def precessar_request(self, request):
#         if not request.user.is_authenticated and request.path != settings.LOGIN_URL:
#             messages.warning(request, "Sua sessão expirou, por favor, faça login novamente.")
#             return redirect('login')

