from django.contrib import messages
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import reverse

class SessionExpiredMiddleware(MiddlewareMixin):

    def process_request(self, request):
        
        login_url = settings.LOGIN_URL
        # passa primeiro por esse if para ver se a requisição é de login
        # salva a ultima url acessada na sessão exeto para requisições de login e statics
        if request.path != login_url and not request.path.startswith('/static/'):
            if 'url_stack' not in request.session:
                request.session['url_stack'] = []

            # Atualiza a pilha de URLs
            url_stack = request.session['url_stack']
            # Não adiciona duplicatas consecutivas ou a própria página "Voltar"
            if not url_stack or url_stack[-1] != request.path:
                url_stack.append(request.path)
                request.session['url_stack'] = url_stack  # Salva a pilha
        # se não for requsição de login e o usuário não estiver autenticado
        if not request.user.is_authenticated and request.path != login_url:
            messages.warning(request, "Sua sessão expirou, por favor, faça login novamente.")
            return redirect(login_url)

