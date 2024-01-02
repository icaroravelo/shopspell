import re 
from playwright.sync_api import sync_playwright, expect
import time 

with sync_playwright() as p:
    # Set up the browser
    browser = p.chromium.launch(headless=False)

    # Create a new page
    page = browser.new_page()

    # Go to the Pingo Doce's website
    page.goto("https://www.pingodoce.pt/")

    # Locate, click and fill the search text input
    page.locator('xpath=/html/body/div[1]/div[2]/div[3]/div/form/div[1]/input').click()
    page.fill('xpath=/html/body/div[1]/div[2]/div[3]/div/form/div[1]/input', "arroz")

    # Click in the search button
    page.locator('xpath=/html/body/div[1]/div[2]/div[3]/div/form/div[1]/button').click()

    # Click in the "Ver todos" option
    page.locator('xpath=/html/body/div[5]/div[2]/div[1]/div[1]/div[1]').click()
    time.sleep(5)
    
    # Close browser
    browser.close()