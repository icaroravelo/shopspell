from playwright.sync_api import sync_playwright
import json
import time

def scrape_continente(productsContinente, ws):
    with sync_playwright() as p:
        
        # Set up browser
        browser = p.chromium.launch(headless=False)

        # Create a new page
        page = browser.new_page()

        # Go to Continente's website
        page.goto("https://www.continente.pt/")
        
        for product in productsContinente:
            try:
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
                search_input.fill(product)
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
                        const price = document.querySelector('.sales.pwc-tile--price-primary.col-tile--price-primary').innerText.trim();
                        return { title, price };
                    }''')
                    
                    # Append the product info to the list
                    products_data.append(product_info)

                for product in products_data:
                    ws.append([product['title'], product['price'], 'Continente'])
            
            except Exception as e:
                print(f"Erro ao fazer raspagem dos produtos {product}: {e}")
        