import re 
from playwright.sync_api import sync_playwright
from openpyxl import Workbook
import time

with open('produtos.txt', 'r') as file:
    productList = [product.strip() for product in file.readlines()]

pingo_doce = 'https://www.pingodoce.pt/'
continente = 'https://www.continente.pt/'
aldi = 'https://www.aldi.pt/'
minipreco = 'https://www.minipreco.pt/'

wb = Workbook()
ws = wb.active
ws.title = 'Resultados da pesquisa'
ws.append(['Produto', 'Preço'])

with sync_playwright() as p:
    # Set up browser
    browser = p.chromium.launch()

    for product in productList:
        for url in [pingo_doce, continente, aldi, minipreco]:
            # Create a new page
            page = browser.new_page()

            # Navigate to the supermarkets pages
            page.goto(url)

            # Scrapping based on the current page URL
            if 'pingodoce.pt' in page.url:
                # Locate, click and fill the search text input
                page.locator('xpath=/html/body/div[1]/div[2]/div[3]/div/form/div[1]/input').click()
                page.fill('xpath=/html/body/div[1]/div[2]/div[3]/div/form/div[1]/input', product)

                # Click in the search button
                page.locator('xpath=/html/body/div[1]/div[2]/div[3]/div/form/div[1]/button').click()

                # Click in the "Ver todos" option
                time.sleep(2)
                page.locator('xpath=/html/body/div[5]/div[2]/div[1]/div[1]/div[1]').click()

                # Get infos from the caroussel/cards itens
                product_links = page.evaluate('''() => {
                    const cards = Array.from(document.querySelectorAll('.cards.js-search-cards-container a.search-card.product'));
                    return cards.map(card => card.getAttribute('href'));
                }''')

                # Create a variable to put the search in
                products_data = []

                for link in product_links:
                    page.goto(link)

                    page.locator('xpath=//*[@id="maincontent"]/div[2]/div[1]/div/div/div[1]/div[1]/div/div[1]/h1')
                    price = page.locator('xpath=//*[@id="maincontent"]/div[2]/div[1]/div/div/div[1]/div[1]/div/div[2]/span')

                    product_info = page.evaluate('''() => {
                        const title = document.querySelector('.product-details__title').innerText.trim();
                        const price = document.querySelector('.product-details_price').innerText.trim();

                        return { title, price };
                    }''')

                    # Append the search into the variable to send to the spreadsheet
                    products_data.append(product_info)

                time.sleep(2)
            
            elif 'continente.pt' in page.url:
                # Your scraping logic for Continente

                # Accept cookies button
                page.locator('xpath=//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()

                # Locate, click and fill the search text input
                page.locator('xpath=//*[@id="input-custom-label-search"]').click()
                page.fill('xpath=//*[@id="input-custom-label-search"]', product)
                page.locator('xpath=//*[@id="brand-header"]/nav/div/div[1]/div[1]/div[3]/form/div/div[1]/button[1]').click()

                # Click on the "Ver mais Produtos" button
                while page.locator('xpath=//*[@id="product-search-results"]/div/div[2]/div[3]/div[49]/div[3]/button').is_visible():
                    page.locator('xpath=//*[@id="product-search-results"]/div/div[2]/div[3]/div[49]/div[3]/button').click()

                # Get infos from the caroussel/cards itens
                product_links = page.evaluate('''() => {
                    const cards = Array.from(document.querySelectorAll('.row .product-grid a.intrinsic intrinsic--square'));
                    return cards.map(card => card.getAttribute('href'));
                }''')

                product_info = page.evaluate('''() => {
                    const title = document.querySelector('.product-name').innerText.trim();                        
                    const price = document.querySelector('.prices-wrapper').innerText.trim();  

                    return { title, price };                      
                }''')
                time.sleep(2)

            # elif 'aldi.pt' in page.url:
            #     # Your scraping logic for Aldi
            #     page.locator('xpath=//*[@id="autocomplete-1-input"]').click()
            #     page.fill('xpath=//*[@id="autocomplete-1-input"]', product)
            #     page.locator('xpath=//*[@id="autocomplete-1-input"]').press("Enter")
            #     time.sleep(2)

            # elif 'minipreco.pt' in page.url:
            #     # Your scraping logic for Minipreco
            #     page.locator('xpath=//*[@id="search"]').click()
            #     page.fill('xpath=//*[@id="search"]', product)
            #     page.locator('xpath=//*[@id="search"]').press("Enter")
            #     time.sleep(2)
            time.sleep(2)

            for product in products_data:
                ws.append([product['title'], product['price']])

    browser.close()

wb.save('products_data.xlsx')
