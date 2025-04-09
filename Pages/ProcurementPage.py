from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

class ProcurementPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.procurement = {
            "procurement_link": (By.CSS_SELECTOR, 'a[href="#/ProcurementMain"]'),
            "settings": (By.XPATH, '//a[contains(text(),"Settings")]'),
            "currency_sub_tab": (By.CSS_SELECTOR, 'a[routerlink="CurrencyList"]'),
            "add_currency_button1": (By.CSS_SELECTOR, 'input[value="Add Currency"]'),
            "add_currency_button2": (By.CSS_SELECTOR, 'input#AddCurrency'),
            "currency_code": (By.CSS_SELECTOR, 'input#CurrencyCode'),
            "currency_description_field": (By.CSS_SELECTOR, 'input#Description'),
            "search_bar": (By.CSS_SELECTOR, 'input#quickFilterInput'),
            "currency_code_column": (By.CSS_SELECTOR, 'div[col-id="CurrencyCode"]'),
        }

    def add_currency_and_verify(self):
        """
        /**
        * @Test5
        * @description This method navigates to the Purchase Request page, accesses the Currency Settings,
        *              adds a new currency with a unique code and description, and verifies that the new
        *              currency is successfully added to the table.
        *
        * @expected
        * The new currency should be added successfully and displayed in the table with the correct currency
        * code and description.
        */
        """
        try:
            unique_currency_code = f"CURR_{random.randint(0, 9999)}"  # Generate a unique currency code
            description = "Test Currency Description"

            # Navigate to the Currency Settings
            self.wait.until(EC.element_to_be_clickable(self.procurement["procurement_link"])).click()
            self.wait.until(EC.element_to_be_clickable(self.procurement["settings"])).click()
            self.wait.until(EC.element_to_be_clickable(self.procurement["currency_sub_tab"])).click()

            # Click "Add Currency" button
            self.wait.until(EC.element_to_be_clickable(self.procurement["add_currency_button1"])).click()

            # Fill in currency details
            self.wait.until(EC.visibility_of_element_located(self.procurement["currency_code"])).send_keys(
                unique_currency_code)
            self.wait.until(EC.visibility_of_element_located(self.procurement["currency_description_field"])).send_keys(
                description)

            # Click "Add Currency"
            self.wait.until(EC.element_to_be_clickable(self.procurement["add_currency_button2"])).click()

            # Wait for table to load
            time.sleep(2)  # You can replace this with a more robust wait if needed

            # Search for the newly added currency
            search_bar = self.wait.until(EC.visibility_of_element_located(self.procurement["search_bar"]))
            search_bar.clear()
            search_bar.send_keys(unique_currency_code)
            time.sleep(2)  # Wait for the search results to update

            # Verify newly added currency is in the table
            currency_rows = self.wait.until(
                EC.presence_of_all_elements_located(self.procurement["currency_code_column"]))
            if currency_rows[1].text == unique_currency_code:
                return True
            else:
                print(f"Expected {unique_currency_code}, but found {currency_rows[1].text}")
                return False

        except Exception as e:
            print(f"Test failed due to error: {e}")
            return False

