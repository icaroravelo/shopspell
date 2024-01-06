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

                # Accept cookies if necessary
                try:
                    page.wait_for_selector(
                        "xpath=//*[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']",
                        timeout=10000
                    ).click()
                except:
                    pass

                # Fill the search text input and press Enter
                search_input = page.wait_for_selector(
                    "xpath=//*[@id='input-custom-label-search']",
                    timeout=5000
                )
                search_input.click()
                search_input.fill("arroz")
                search_input.press("Enter")

                time.sleep(2)

                # Wait for the product links to load
                page.wait_for_selector(
                    "xpath=//*[@id='product-search-results']/div/div[2]/div[3]",
                    timeout=10000
                )

                # Click in "Ver mais produtos" while it is visible
                while page.locator('xpath=//*[@id="product-search-results"]/div/div[2]/div[3]/div[25]/div[3]/button').is_visible():
                    page.locator('xpath=//*[@id="product-search-results"]/div/div[2]/div[3]/div[25]/div[3]/button').click()
                

                # Get product links
                product_links = page.evaluate('''() => {
                    const cards = Array.from(document.querySelectorAll('.ct-image-container a'));
                    return cards.map(card => card.getAttribute('href'));
                }''')

                time.sleep(2)

                # Create a variable to store the search results
                products_data = []

                # Iterate through each product link
                for link in product_links:
                    page.goto(link)

                    # Wait for the product details to load
                    page.locator(".row.no-gutter.ct-pdp--name")
                    price = page.wait_for_selector(".prices-wrapper")

                    # Get the name and price of the product
                    product_info = page.evaluate('''() => {
                        const title = document.querySelector('.pwc-h3.col-h3.product-name.pwc-font--primary-extrabold.mb-0').innerText.trim();
                        const price = document.querySelector('.prices-wrapper').innerText.trim();
                        return { title, price };
                    }''')

                    # Append the product info to the list
                    products_data.append(product_info)

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
