from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class UtilitiesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.utilities = {
            "utilities_link": (By.XPATH, "//span[text()='Utilities']"),
            "scheme_refund_tab": (By.CSS_SELECTOR, 'ul.page-breadcrumb a[href="#/Utilities/SchemeRefund"]'),
            "counter_item": (By.XPATH, "//div[@class='counter-item']"),
            "new_scheme_refund_entry_button": (By.XPATH, "//a[contains(text(),'New Scheme Refund Entry')]"),
            "save_scheme_refund_button": (By.CSS_SELECTOR, "button#savebutton"),
            "warning_popup": (By.XPATH, "//p[contains(text(),'warning')]/../p[contains(text(),'Please fill all the mandatory fields.')]"),
        }

    def verify_mandatory_fields_warning(self):
        """
        /**
        * @Test6
        * @description This method verifies that a warning popup is displayed when attempting to save a new
        *              Scheme Refund Entry without filling in mandatory fields.
        * @expected
        * A warning popup should appear with the message: "Please fill all the mandatory fields."
        */
        """
        try:
            # Navigate to Utilities and open Scheme Refund tab
            self.wait.until(EC.element_to_be_clickable(self.utilities["utilities_link"])).click()
            self.wait.until(EC.element_to_be_clickable(self.utilities["scheme_refund_tab"])).click()

            # Select first counter item if available
            time.sleep(3)  # Wait for the counter items to load
            counter_items = self.wait.until(EC.presence_of_all_elements_located(self.utilities["counter_item"]))
            counter_count = len(counter_items)
            print("Counter count is " + str(counter_count))

            if counter_count > 0:
                counter_items[0].click()
            else:
                print("No counter items available")

            # Click "New Scheme Refund Entry" button
            self.wait.until(EC.element_to_be_clickable(self.utilities["new_scheme_refund_entry_button"])).click()

            # Click Save without filling any fields
            self.wait.until(EC.element_to_be_clickable(self.utilities["save_scheme_refund_button"])).click()

            # Wait for warning popup
            warning_popup = self.wait.until(EC.visibility_of_element_located(self.utilities["warning_popup"]))

            # Verify warning message
            popup_message = warning_popup.text.strip()
            if popup_message == "Please fill all the mandatory fields.":
                return True
            else:
                print(f"Expected warning message not found. Found: {popup_message}")
                return False

        except Exception as e:
            print(f"Test failed due to error: {e}")
            return False
