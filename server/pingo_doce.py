import re 
from playwright.sync_api import sync_playwright, expect
import time 

def scrape_pingo_doce(productsPingoDoce, ws):
    with sync_playwright() as p:
        # Set up the browser
        browser = p.chromium.launch(headless=False)

        # Create a new page
        page = browser.new_page()

        # Go to the Pingo Doce's website
        page.goto("https://www.pingodoce.pt/")
        
        for product in productsPingoDoce:
            # Locate, click and fill the search text input
            page.locator('xpath=/html/body/div[1]/div[2]/div[3]/div/form/div[1]/input').click()
            page.fill('xpath=/html/body/div[1]/div[2]/div[3]/div/form/div[1]/input', product)

            # Click in the search button
            page.locator('xpath=/html/body/div[1]/div[2]/div[3]/div/form/div[1]/button').click()

            # Click in the "Ver todos" option
            time.sleep(2)
            
            page.locator('xpath=/html/body/div[5]/div[2]/div[1]/div[1]/div[1]').click()
            
            time.sleep(2)

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

                            # Append the product info to the list
                            products_data.append(product_info)
            for product in products_data:
                ws.append([product['title'], product['price'], 'Pingo Doce'])
