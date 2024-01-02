from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # Set up browser
    browser = p.chromium.launch(headless=False)

    # Create a new page
    page = browser.new_page()

    # Go to Continente's website
    page.goto("https://www.continente.pt/")

    # Accept all cookies
    page.locator('xpath=//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()

    # Locate, click and fill the search text input
    page.locator('xpath=//*[@id="input-custom-label-search"]').click()
    page.fill('xpath=//*[@id="input-custom-label-search"]', "arroz")
    page.locator('xpath=//*[@id="brand-header"]/nav/div/div[1]/div[1]/div[3]/form/div/div[1]/button[1]').click()

    time.sleep(2)

    # Close browser
    browser.close()