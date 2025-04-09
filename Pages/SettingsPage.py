from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SettingsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        self.settings = {
            "settings_link": (By.CSS_SELECTOR, 'a[href="#/Settings"]'),
            "more_dropdown": (By.XPATH, '//a[contains(text(),"More...")]'),
            "price_category_tab": (By.CSS_SELECTOR, 'ul.dropdown-menu a[href="#/Settings/PriceCategory"]'),
            "activate_success_message": (By.XPATH, '//p[contains(text(),"success")]/../p[text()="Activated."]'),
            "deactivate_success_message": (By.XPATH, '//p[contains(text(),"success")]/../p[text()="Deactivated."]'),
        }

    def disable_button(self, code: str):
        return (By.XPATH, f'//div[text()="{code}"]/../div/span/a[@danphe-grid-action="deactivatePriceCategorySetting"]')

    def enable_button(self, code: str):
        return (By.XPATH, f'//div[text()="{code}"]/../div/span/a[@danphe-grid-action="activatePriceCategorySetting"]')

    def toggle_price_category_status(self):
        """
        /**
        * @Test10
        * @description This method verifies disabling and enabling a price category code in the table.
        * @expected
        * A success message is displayed for both actions: "Deactivated." for disabling and "Activated." for enabling.
        */
        """
        try:
            # Step 1: Click on the Settings link
            self.wait.until(EC.element_to_be_clickable(self.settings["settings_link"])).click()

            # Step 2: Open the "more..." dropdown and select the "Price Category" tab
            self.wait.until(EC.element_to_be_clickable(self.settings["more_dropdown"])).click()
            self.wait.until(EC.element_to_be_clickable(self.settings["price_category_tab"])).click()

            # Step 3: Disable the specified code
            self.wait.until(EC.element_to_be_clickable(self.disable_button("NHIF-1"))).click()

            # Step 4: Verify the "Deactivated." success message
            deactivate_message = self.wait.until(
                EC.visibility_of_element_located(self.settings["deactivate_success_message"])).text.strip()
            if deactivate_message != "Deactivated.":
                return False

            # Step 5: Enable the same code
            self.wait.until(EC.element_to_be_clickable(self.enable_button("NHIF-1"))).click()

            # Step 6: Verify the "Activated." success message
            activate_message = self.wait.until(
                EC.visibility_of_element_located(self.settings["activate_success_message"])).text.strip()
            return activate_message == "Activated."

        except Exception as e:
            print(f"Test failed due to error: {e}")
            return False
