from pingo_doce import scrape_pingo_doce
from continente import scrape_continente
from openpyxl import Workbook

# List of products for Pingo Doce
with open('produtos.txt', 'r') as file:
    productsPingoDoce = [product.strip() for product in file.readlines()]

# List of products for Continente
with open('produtos.txt', 'r') as file:
    productsContinente = [product.strip() for product in file.readlines()]

wb = Workbook()
ws = wb.active
ws.title = 'Resultados da pesquisa'
ws.append(['Produto', 'Preço', 'Mercado'])

# Scraping Pingo Doce
scrape_pingo_doce(productsPingoDoce, ws)

# Scraping Continente
scrape_continente(productsContinente, ws)

try:
    wb.save('lista.xlsx')
    print("Dados salvos com sucesso no arquivo 'lista.xlsx'")
except Exception as e:
    print(f"Erro ao salvar dados no arquivo: {str(e)}")
