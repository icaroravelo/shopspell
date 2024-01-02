import re 
from playwright.sync_api import sync_playwright, expect
import time 

with sync_playwright() as p:
    # Set up the browser
    browser = p.chromium.launch(headless=False)

    # Create a new page
    page = browser.new_page()

    # Go to the Pingo Doce's website
    page.goto("https://www.minipreco.pt/")

    # Locate, click and fill the search text input
    page.locator('xpath=//*[@id="search"]').click()
    page.fill('xpath=//*[@id="search"]', "arroz")

    # Click in the search button
    page.locator('xpath=//*[@id="search"]').press("Enter")

    time.sleep(5)
    
    # Close browser
    browser.close()