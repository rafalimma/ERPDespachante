
def validador(cpf_cnpj):
    tamanho = len(cpf_cnpj)
    if tamanho == 14:
        return validar_cpf(cpf_cnpj)
    else:
        return validar_cnpj(cpf_cnpj)


def validar_cpf(cpf):
    cpf = cpf.replace('.', '')
    cpf = cpf.replace('-', '')
    digitos9 = cpf[:9] #tirando os 9 primeiros digts para multiplicar
    contador_reg1 = 10
    resultado1 = 0

    for digito in digitos9:
        resultado1 += int(digito) *  contador_reg1
        contador_reg1 -= 1
#Fora do for:
    firstdigit = (resultado1 * 10) % 11
    firstdigit = firstdigit if firstdigit <= 9 else 0

#segundo digito do cpf: #inclua o firstdigit na contagem reg e no cpf:
    digitos10 = digitos9 + str(firstdigit)
    contador_reg2 = 11
    resultado2 = 0

    for digito in digitos10:
        resultado2 += int(digito) *contador_reg2
        contador_reg2 -= 1
#outside for:
    seconddigit = (resultado2 * 10) % 11
    seconddigit = seconddigit if seconddigit <= 9 else 0

    cpf_gerado = f'{digitos9}{firstdigit}{seconddigit}'
    print(cpf)
    print('cpf gerado:', cpf_gerado)
    
    return cpf == cpf_gerado

def validar_cnpj(cnpj):
    # Remove caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))
    
    # Verifica se o CNPJ tem 14 dígitos
    if len(cnpj) != 14:
        return False

    # Evita CNPJs inválidos comuns (ex: 00000000000000)
    if cnpj in (c * 14 for c in "1234567890"):
        return False

    # Primeira parte: cálculo do primeiro dígito verificador
    digitos12 = cnpj[:12]
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    resultado1 = sum(int(digito) * peso for digito, peso in zip(digitos12, pesos1))
    
    primeiro_digito = (resultado1 % 11)
    primeiro_digito = 0 if primeiro_digito < 2 else 11 - primeiro_digito

    # Segunda parte: cálculo do segundo dígito verificador
    digitos13 = digitos12 + str(primeiro_digito)
    pesos2 = [6] + pesos1
    resultado2 = sum(int(digito) * peso for digito, peso in zip(digitos13, pesos2))
    
    segundo_digito = (resultado2 % 11)
    segundo_digito = 0 if segundo_digito < 2 else 11 - segundo_digito

    # Verifica se os dígitos finais do CNPJ conferem com os calculados
    cnpj_gerado = f"{digitos12}{primeiro_digito}{segundo_digito}"
    return cnpj == cnpj_gerado