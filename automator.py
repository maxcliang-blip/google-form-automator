import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def fill_form(driver, config):
    driver.get(config["form_url"])
    time.sleep(2)

    fields = config.get("fields", {})
    for field_name, value in fields.items():
        try:
            inputs = driver.find_elements(By.NAME, field_name)
            if inputs:
                inputs[0].send_keys(value)
                continue

            labels = driver.find_elements(By.XPATH, f"//label[contains(text(), '{field_name}')]")
            if labels:
                label = labels[0]
                container = label.find_element(By.XPATH, "./ancestor::div[contains(@class, 'freebirdFormviewerViewItemsItem')]")
                input_field = container.find_element(By.TAG_NAME, "input")
                input_field.send_keys(value)
        except Exception as e:
            print(f"Error filling field {field_name}: {e}")

    try:
        submit_btn = driver.find_element(By.XPATH, "//span[text()='Submit']/ancestor::button")
        submit_btn.click()
        print("Form submitted successfully!")
    except Exception as e:
        print(f"Error submitting form: {e}")

def main():
    config = load_config()
    driver = setup_driver()
    try:
        fill_form(driver, config)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()