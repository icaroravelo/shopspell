from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    # Set up browser
    browser = p.chromium.launch(headless=False)

    # Create a new page
    page = browser.new_page()

    # Go to Continente's website
    page.goto("https://www.continente.pt/")

    # Accept cookies if necessary
    try:
        page.wait_for_selector(
            "xpath=//*[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']",
            timeout=1000  # Increase timeout to 5 seconds if necessary
        ).click()
    except:
        pass

    # Fill the search text input and press Enter
    search_input = page.wait_for_selector(
        "xpath=//*[@id='input-custom-label-search']",
        timeout=5000  # Increase timeout to 5 seconds (5000ms)
    )
    search_input.click()
    search_input.fill("arroz")
    search_input.press("Enter")

    # Selector -> Name of the product
    name_selector = 'xpath=//*[@id="product-search-results"]/div/div[2]/div[3]/div[1]/div/div/div/div[2]/div[1]'

    # Selector -> Price of the product
    price_selector = '//*[@id="product-search-results"]/div/div[2]/div[3]/div[1]/div/div/div/div[2]/div[2]/div[1]/div/div[1]'

    # Wait for the product name and price to load on the page
    name_element = page.wait_for_selector(name_selector)
    price_element = page.wait_for_selector(price_selector)

    # Get the text of the product name and price
    product_name = name_element.inner_text()
    product_price = price_element.inner_text()

    # Create a dictionary with the information collected
    product_info = {
        "name": product_name,
        "price": product_price
    }

    # Saving information in a JSON file
    with open('product_info.json', 'w') as json_file:
        json.dump(product_info, json_file)

    print(product_info)

    # Closing the browser