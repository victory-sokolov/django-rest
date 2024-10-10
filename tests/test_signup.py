from playwright.sync_api import sync_playwright

BASE_URL = "http://0.0.0.0:8000"
HEADLESS = False


with sync_playwright() as p:
    browser = p.chromium.launch(headless=HEADLESS)
    browser.is_connected()

    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/auth/signup/")

    csrf_token = page.locator("//input[@name='csrfmiddlewaretoken']").get_attribute(
        "value",
    )
    page.evaluate(f"document.cookie = 'csrftoken={csrf_token}; path=/;'")

    page.locator("//input[@id='name']").fill("testuser")
    page.locator("//input[@id='email']").fill("testuser@gmail.com")
    page.locator("//input[@id='password']").fill("password123")
    page.locator("//button[@type='submit']").click()

    browser.close()
