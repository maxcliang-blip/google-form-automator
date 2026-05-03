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
        page.wait_for_load_state("networkidle")

        fields = config.get("fields", {})
        for field_name, value in fields.items():
            try:
                label = page.locator(f"label:has-text('{field_name}')").first
                if label.count() > 0:
                    container = label.locator("xpath=ancestor::div[contains(@class, 'quantumWizTextinputPaperinputContainer')]")
                    input_field = container.locator("input")
                    if input_field.count() > 0:
                        input_field.fill(value)
                        continue

                inputs = page.locator(f"input[name='{field_name}']")
                if inputs.count() > 0:
                    inputs.first.fill(value)
            except Exception as e:
                print(f"Error filling field {field_name}: {e}")

        try:
            page.click("button:has-text('Submit')")
            print("Form submitted successfully!")
        except Exception as e:
            print(f"Error submitting form: {e}")

        browser.close()

if __name__ == "__main__":
    config = load_config()
    fill_form(config)