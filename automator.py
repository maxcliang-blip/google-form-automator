import json
from playwright.sync_api import sync_playwright

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def fill_form(config):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(config["form_url"])
        
        fields = config.get("fields", {})
        
        for field_label, value in fields.items():
            try:
                label = page.get_by_label(field_label, exact=True)
                label.click()
                page.keyboard.type(value, delay=50)
            except Exception as e:
                print(f"Error: {e}")

        page.get_by_role("button", name="Submit").click()
        print("Done!")
        
        browser.close()

if __name__ == "__main__":
    config = load_config()
    fill_form(config)