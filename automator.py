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
        
        for field_label, value in fields.items():
            try:
                label = page.locator(f"label:has-text('{field_label}')").first
                if label.count() > 0:
                    container = label.locator("xpath=ancestor::div[@data-item-id]").first
                    if container.count() > 0:
                        input_field = container.locator("input, textarea, select")
                        if input_field.count() > 0:
                            input_field.first.fill(value)
                            continue
                        
                        role_group = container.locator("div[role='listbox']")
                        if role_group.count() > 0:
                            page.locator(f"div[role='listbox']:has-text('{field_label}')").click()
                            page.wait_for_timeout(500)
                            page.locator(f"div[role='option']:has-text('{value}')").click()
                            continue
                    
                    freebird = label.locator("xpath=ancestor::div[contains(@class, 'freebirdFormviewerViewItemsItem')]").first
                    if freebird.count() > 0:
                        input_field = freebird.locator("input, textarea").first
                        if input_field.count() > 0:
                            input_field.fill(value)
                            continue
                        
                        select_button = freebird.locator("div[role='button']").first
                        if select_button.count() > 0:
                            select_button.click()
                            page.wait_for_timeout(500)
                            page.locator(f"div[role='option']:has-text('{value}')").click()
            except Exception as e:
                print(f"Error filling field '{field_label}': {e}")

        try:
            page.click("button:has-text('Submit')")
            page.wait_for_timeout(1000)
            print("Form submitted successfully!")
        except Exception as e:
            print(f"Error submitting form: {e}")

        browser.close()

if __name__ == "__main__":
    config = load_config()
    fill_form(config)