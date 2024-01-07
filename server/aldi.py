from playwright.sync_api import sync_playwright
import json
import time

with sync_playwright() as p:
    # Set up browser
    browser = p.chromium.launch(headless=False)

    # Create a new page
    page = browser.new_page()

    # Go to Continente's website
    page.goto("https://www.aldi.pt/")

    # Accept cookies (if necessary)
    try:
        page.locator(
            'xpath=//*[@id="focus-lock-id"]/div/div/div[2]/div/div/div[2]/div/button[3]'
        ).click()
    except:
        pass

    # Fill the search text input and press Enter
    search_input = page.locator(
        '//*[@id="autocomplete-1-input"]'
    )
    search_input.click()
    search_input.fill("arroz")
    search_input.press("Enter")

    # Wait for the product links to load
    page.locator(
        '.tiles-grid'
    )

    # Get product links
    product_links = page.evaluate('''() => {
        const cards = Array.from(document.querySelectorAll('.tiles-grid a'));
        return cards.map(card => card.getAttribute('href'));
    }''')

    # Create a variable to store the search results
    products_data = []

    # Iterate through each product link
    for link in product_links:
        page.goto(link)

        # Wait for the product details to load
        page.locator('.tiles-grid')
        price = page.locator('.price__label')

        # Get the name and price of the product
        product_info = page.evaluate('''() => {
            const title = document.querySelector('.mod-article-intro__header-headline').innerText.trim();
            const price = document.querySelector('price__label').innerText.trim();

            return { title, price };
        }''')

        # Append the product info to the list
        products_data.append(product_info)

    # Output the collected data
    print(products_data)

    # Saving information in a JSON file
    with open('product_info.json', 'w') as json_file:
        json.dump(products_data, json_file)