import math
import re
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from alertaemail import send_mail
from funcoes import remove_duplicado


url = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

# Configurações iniciais
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(60)  # seconds
driver.get(url)
# driver.maximize_window()

# Opções do site da caixa para busca de imóveis
estado = driver.find_element(By.ID, "cmb_estado")
select = Select(estado)
select.select_by_value("GO")
time.sleep(5)

cidade = driver.find_element(By.ID, 'cmb_cidade')
select = Select(cidade)
select.select_by_value("2327")

time.sleep(2)

modalidade = driver.find_element(By.ID, 'cmb_modalidade')
select = Select(modalidade)
select.select_by_visible_text("Selecione")

time.sleep(2)

# Seleção de bairros na página
bairros = driver.find_element(By.ID, 'cmb_bairro')

# Setor norte
try:
    norte = bairros.find_element(By.XPATH, "//input[@value='03004||SETOR NORTE']")
    norte.click()
except NoSuchElementException:
    pass

time.sleep(2)

# Setor leste
try:
    leste = bairros.find_element(By.XPATH, "//input[@value='03000||SETOR LESTE']")
    leste.click()
except NoSuchElementException:
    pass

time.sleep(2)

# Santa rita
try:
    santa_rita = bairros.find_element(By.XPATH, "//input[@value='33987||SANTA RITA']")
    santa_rita.click()
except NoSuchElementException:
    pass

time.sleep(2)

driver.find_element(By.ID, 'btn_next0').click()

time.sleep(2)

## Opções para buscar imóveis específicos
# tipo_imovel = Select(driver.find_element(By.NAME, 'cmb_tp_imovel'))
# tipo_imovel.select_by_visible_text("Indiferente")
# quartos = Select(driver.find_element(By.NAME, 'cmb_quartos'))
# quartos.select_by_visible_text("Indiferente")
# vagas_garagem = Select(driver.find_element(By.NAME, 'cmb_vg_garagem'))
# vagas_garagem.select_by_visible_text("Indiferente")
# area_util = Select(driver.find_element(By.NAME, 'cmb_area_util'))
# area_util.select_by_visible_text("Indiferente")
# faixa_valor = Select(driver.find_element(By.NAME, 'cmb_faixa_vlr'))
# faixa_valor.select_by_visible_text("Indiferente")

driver.find_element(By.ID, 'btn_next1').click()

time.sleep(30)

# Quatindade de imóveis encontrados
qtd_imoveis = driver.find_element(By.ID, 'listaimoveis')
qtd = qtd_imoveis.text[18:-9]
ultima_pagina = math.ceil(int(qtd) / 10)

lista_geral_enderecos = []


# Função usada para buscar os dados dos imóveis
def busca_endereco():
    element = driver.find_element(By.ID, 'listaimoveispaginacao')
    imoveis = element.find_elements(By.XPATH, '//ul[@class="control-group no-bullets"]')
    for imovel in imoveis:
        link_foto_imovel = imovel.find_element(By.TAG_NAME, 'img').get_attribute('src')
        dados_imovel = imovel.find_element(By.CLASS_NAME, 'dadosimovel-col2')
        dados_imovel_refinado = dados_imovel.find_element(By.TAG_NAME, 'li').text
        dados_imovel_numero = dados_imovel.find_element(By.TAG_NAME, 'a').get_attribute('onclick')
        numero_imovel = re.findall(r"[0-9]+", dados_imovel_numero)
        lista_geral_enderecos.append([link_foto_imovel, dados_imovel_refinado, numero_imovel[0]])


busca_endereco()

# Mudança de página
paginas = driver.find_element(By.ID, 'paginacao')
for i in range(2, ultima_pagina + 1):
    paginas.find_element(By.XPATH, f'a[{i}]').click()
    time.sleep(30)
    busca_endereco()

imoveis_selecionados = []

# Busca imóvel específico dentro da lista
for e in lista_geral_enderecos:
    # Início de busca de uma quadra
    if 'Q2 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q-2 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q 2 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q02 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q-02 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q 02 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD2 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD-2 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD 2 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD02 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD-02 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD 02 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA2 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA-2 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA 2 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA02 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA-02 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA 02 ' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q2,' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q-2,' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q 2,' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q02,' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q-02,' in e[1]:
        imoveis_selecionados.append(e)
    if 'Q 02,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD2,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD-2,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD 2,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD02,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD-02,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QD 02,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA2,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA-2,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA 2,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA02,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA-02,' in e[1]:
        imoveis_selecionados.append(e)
    if 'QUADRA 02,' in e[1]:
        imoveis_selecionados.append(e)
    # Fim de busca de uma quadra
    # Início de busca de uma quadra
    if 'Q7' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'Q-7' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'Q 7' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'Q07' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'Q-07' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'Q 07' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QD7' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QD-7' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QD 07' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QD07' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QD-07' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QD 07' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QUADRA7' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QUADRA-7' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QUADRA 7' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QUADRA07' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QUADRA-07' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    if 'QUADRA 07' in e[1]:
        a1 = e[1]
        if 'SETOR LESTE' in a1:
            imoveis_selecionados.append(e)
    # Fim de busca de uma quadra
    if 'SANTA RITA' in e[1]:
        imoveis_selecionados.append(e)
    if 'SANTA-RITA' in e[1]:
        imoveis_selecionados.append(e)

# Imoveis selecionados sem repetição
imoveis_selecionados_refinado = []
remove_duplicado(imoveis_selecionados, imoveis_selecionados_refinado)

# # Imoveis ignorados
# imovel_ignorado1 = "PLANALTINA - Res. Toronto  Valor de avaliação: R$ 125.000,00Valor mínimo de venda à vista: " \
#                    "R$ 51.787,50 ( desconto de 58,57%)Casa - 2 quarto(s) - Venda OnlineNúmero do imóvel: " \
#                    "878770108536-7QD-02 CH-21 CH. SANTA MARIA,N. 43, SETOR NORTE Detalhes do " \
#                    "imóvel   Corretores credenciados"
# imovel_ignorado2 = "PLANALTINA - Res. Toronto  Valor de avaliação: R$ 117.200,00Valor mínimo de venda: " \
#                    "R$ 64.952,24 ( desconto de 44,58%)Valor mínimo de venda à vista: R$ 48.555,96 " \
#                    "( desconto de 58,57%)Casa - 2 quarto(s) - Venda Direta OnlineQD-02 CH-21 rua 21,N. 51 " \
#                    "Chácaras Santa Maria, SETOR NORTE Detalhes do imóvel   Corretores credenciados"
# imovel_ignorado3 = "PLANALTINA - RES PIZZATO | R$ 122.500,00  Casa - 2 quarto(s) - 1º " \
#                   "Leilão SFI 3027/0223-CPA/RERUA O CASA 4B QD 07 LT 4, SANTA RITA Detalhes do imóvel"
#
#
# if imovel_ignorado1 in imoveis_selecionados_b:
#     imoveis_selecionados_b.remove(imovel_ignorado1)
# if imovel_ignorado2 in imoveis_selecionados_b:
#     imoveis_selecionados_b.remove(imovel_ignorado2)
# if imovel_ignorado3 in imoveis_selecionados_b:
#     imoveis_selecionados_b.remove(imovel_ignorado3)

# Organização dos imóveis selecionados e refinamento dos endereços
body = []

for imovel in imoveis_selecionados_refinado:
    imagem_imovel = imovel[0]
    # dados_imovel = imovel[1]
    numero_imovel = imovel[2]

    cidade_titulo = re.findall(r'^PLANALTINA.*\S', imovel[1])

    valor_avaliacao = re.findall(r'Valor de avaliação.*\S', imovel[1])

    valor_venda = re.findall(r'Valor m.*\S', imovel[1])

    caracteristicas_imovel = re.findall(r'Apartamento.*\S', imovel[1])

    caracteristicas_imovel_alterantivo = re.findall(r'Casa.*\S', imovel[1])
    if not caracteristicas_imovel:
        caracteristicas_imovel = caracteristicas_imovel_alterantivo
    else:
        '-'

    tipo_venda = re.findall(r'Venda O.*\S', imovel[1])

    tipo_venda_alternativo = re.findall(r'Venda D.*\S', imovel[1])

    tipo_venda_alternativo_dois = re.findall(r'Leiloeir.*\S', imovel[1])
    if not tipo_venda:
        tipo_venda = tipo_venda_alternativo
    if not tipo_venda or not tipo_venda_alternativo:
        tipo_venda = tipo_venda_alternativo_dois
    else:
        '-'

    numero_do_imovel = re.findall(r'Número do i.*\S', imovel[1])

    endereco_imovel = re.findall(r'\bQ.*\S', imovel[1][150:])
    endereco_imovel_dois = re.findall(r'\bRUA.*\S', imovel[1][150:])
    endereco_imovel_tres = re.findall(r'\bAV.*\S', imovel[1][150:])
    endereco_imovel_quatro = re.findall(r'\bCH.*\S', imovel[1][150:])
    endereco_imovel_cinco = re.findall(r'\bCO.*\S', imovel[1][150:])
    endereco_imovel_seis = re.findall(r'\bLOT.*\S', imovel[1][150:])
    endereco_imovel_sete = re.findall(r'\bMR.*\S', imovel[1][150:])
    if not endereco_imovel:
        endereco_imovel = endereco_imovel_dois
    if not endereco_imovel and not endereco_imovel_dois:
        endereco_imovel = endereco_imovel_tres
    if not endereco_imovel and not endereco_imovel_dois and not endereco_imovel_tres:
        endereco_imovel = endereco_imovel_quatro
    if not endereco_imovel and not endereco_imovel_dois and not endereco_imovel_tres and not endereco_imovel_quatro:
        endereco_imovel = endereco_imovel_cinco
    if not endereco_imovel and not endereco_imovel_dois and not endereco_imovel_tres and not endereco_imovel_quatro and not endereco_imovel_cinco:
        endereco_imovel = endereco_imovel_seis
    if not endereco_imovel and not endereco_imovel_dois and not endereco_imovel_tres and not endereco_imovel_quatro and not endereco_imovel_cinco and not endereco_imovel_seis:
        endereco_imovel = endereco_imovel_sete

    try:
        body.append(f'<div id="listaimoveispaginacao" class="control-item control-span-12_12"><ul class="control-group '
                    f'no-bullets" style="width:100%;background:#f3f4f6;"><li class="group-block-item;"><div '
                    f'class="fotoimovel-col1"><a '
                    f'href="https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnOrigem=index&hdnimovel='
                    f'{numero_imovel}"><img src="{imagem_imovel}"alt="Consulte detalhes do imóvel" title="Consulte '
                    f'detalhes do imóvel" class="fotoimovel"onclick="javascript:detalhe_imovel('
                    f'8444422892646);"></div><div class="dadosimovel-col2"><ul class="form-set inside-set no-bullets"><li '
                    f'class="form-row clearfix" style="margin-bottom:0.5em;"><div class="control-item '
                    f'control-span-12_12"><span><strong><font style="font-size:0.80em;"><a '
                    f'href="https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnOrigem=index&hdnimovel='
                    f'{numero_imovel}"onclick="javascript:detalhe_imovel(8444422892646); return false;">'
                    f'{cidade_titulo[0]}</a></font></strong></span><a href="#" onclick="javascript:favoritos('
                    f'8444422892646); return false;" alt="favoritos"><i class="fa fa-heart-o" alt="icone favoritos" '
                    f'title="Adicionar à lista de favoritos"></i></a><br><span><font style="font-size:0.80em;">'
                    f'{valor_avaliacao[0]}<br><b>{str(*valor_venda)}</font></span><br><span><font '
                    f'style="font-size:0.75em;">{str(caracteristicas_imovel[0])}<br>{str(tipo_venda[0])}<br>'
                    f'{numero_do_imovel[0]}<br>{endereco_imovel[0]}</font></span></div></li><li class="form-row '
                    f'clearfix"><div class="control-item control-span-5_12" style="margin-bottom:0.1em;"><span><a '
                    f'href="https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnOrigem=index&hdnimovel='
                    f'{numero_imovel}" onclick="javascript:detalhe_imovel(8444422892646); return false;" style="color: '
                    f'#ff7200; font-size:0.80em;"><i class="fa fa-caret-right"></i>Detalhes do '
                    f'imóvel</a></span></div></li></ul></div></li></ul><br></div>')
    except:
        ...


body_replace = str(body)[2:-2].replace("', '", '')

if len(imoveis_selecionados_refinado) == 0:
    send_mail(f'<h2><font color="red">Busca de imóveis site Caixa</font></h2><font color="blue">Bairros de busca: Q.2 '
              f'- Setor norte, Q.7 - Setor Leste e Santa Rita<br />Todas as opções marcadas como "Indiferentes"<br '
              f'/>Foram encontrados <b>{qtd}</b> imóveis.</font><br /><br />Nenhum mais próximo do centro '
              f'encontrado.</html>')
else:
    send_mail(f'<h2><font color="red">Busca de imóveis Caixa</font></h2><font color="blue">Bairros de busca: Q.2 - '
              f'Setor norte, Q.7 - Setor Leste e Santa Rita<br />Todas as opções marcadas como "Indiferentes"<br '
              f'/>Foram encontrados <b>{qtd}</b> imóveis.</font><br /><br>{body_replace}<br>Caso deseje tirar algum '
              f'desses imóveis de sua busca,<br> por gentileza, enviar mensagem no WhatsApp (61) 98556-4096')

driver.quit()
