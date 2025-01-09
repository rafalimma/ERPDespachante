from login.models import Filial

def filial_context(request):
    try:
        filial = Filial.objects.first()
    except Filial.DoesNotExist:
        print('****CLEINTE NÃO ENCONTRADO****')
    return {'filial': filial}
