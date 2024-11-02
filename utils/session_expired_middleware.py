from django.contrib import messages
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import reverse

class SessionExpiredMiddleware(MiddlewareMixin):

    def process_request(self, request):
        login_url = settings.LOGIN_URL
        # passa primeiro por esse if para ver se a requisição é de login
        if request.path == login_url or request.path.startswith('/static/'):
            return
        # se não for requsição de login e o usuário não estiver autenticado
        if not request.user.is_authenticated:
            messages.warning(request, "Sua sessão expirou, por favor, faça login novamente.")
            return redirect(login_url)

