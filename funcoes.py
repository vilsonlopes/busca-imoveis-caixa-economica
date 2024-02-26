
# Função para retirar endereços duplicados da lista.
def remove_duplicado(lista=list, lista_nova=list):
    for element in lista:
        if element not in lista_nova:
            lista_nova.append(element)
