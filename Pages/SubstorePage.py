import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from datetime import datetime

class SubstorePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)

        self.substore = {
            "substore_link": (By.CSS_SELECTOR, 'a[href="#/WardSupply"]'),
            "select_substore": (By.XPATH, '(//span[@class="report-name"])[1]'),
            "inventory_requisition": (By.CSS_SELECTOR, 'a[href="#/WardSupply/Inventory/InventoryRequisitionList"]'),
            "consumption": (By.CSS_SELECTOR, 'a[href="#/WardSupply/Inventory/Consumption"]'),
            "reports": (By.CSS_SELECTOR, 'a[href="#/WardSupply/Inventory/Reports"]'),
            "patient_consumption": (By.CSS_SELECTOR, 'a[href="#/WardSupply/Inventory/PatientConsumption"]'),
            "return": (By.CSS_SELECTOR, 'a[href="#/WardSupply/Inventory/Return"]'),
            "inventory": (By.CSS_SELECTOR, 'ul.page-breadcrumb a[href="#/WardSupply/Inventory"]'),
            "signout_cursor": (By.CSS_SELECTOR, 'i.fa-sign-out'),
            "tooltip": (By.CSS_SELECTOR, 'div.modal-content h6'),
        }

    def verify_navigation_between_submodules(self):
        """
        /**
        * @Test11
        * @description : This method verifies that the user is able to navigate between the sub modules.
        * @expected : Ensure that it should navigate to each section of the "substore" module.
        */
        """
        try:
            # Navigate to the substore
            self.wait.until(EC.element_to_be_clickable(self.substore["substore_link"])).click()

            # Select the substore
            self.wait.until(EC.element_to_be_clickable(self.substore["select_substore"])).click()

            # Define expected URL mappings
            submodules = {
                "inventory_requisition": "Inventory/InventoryRequisitionList",
                "consumption": "Inventory/Consumption/ConsumptionList",
                "reports": "Inventory/Reports",
                "patient_consumption": "Inventory/PatientConsumption/PatientConsumptionList",
                "return": "Inventory/Return"
            }

            # Navigate through each submodule and verify URL
            for key, expected_url in submodules.items():
                self.wait.until(EC.element_to_be_clickable(self.substore[key])).click()
                if expected_url not in self.driver.current_url:
                    return False

            return True

        except Exception as e:
            print(f"Test failed due to error: {e}")
            return False

    def verify_tooltip_text(self):
        """
        /**
        * @Test12
        * @description This method verifies the tooltip text displayed when hovering over the cursor icon in the Inventory tab.
        * @expected
        * Tooltip text should contain: **"To change, you can always click here."**
        */
        """
        try:
            # Navigate to the substore
            self.wait.until(EC.element_to_be_clickable(self.substore["substore_link"])).click()

            # Select the substore
            self.wait.until(EC.element_to_be_clickable(self.substore["select_substore"])).click()

            # Click on the Inventory tab
            self.wait.until(EC.element_to_be_clickable(self.substore["inventory"])).click()

            # Hover over the cursor icon
            signout_cursor = self.wait.until(EC.visibility_of_element_located(self.substore["signout_cursor"]))
            self.actions.move_to_element(signout_cursor).perform()

            # Verify the tooltip text
            tooltip_text = self.wait.until(EC.visibility_of_element_located(self.substore["tooltip"])).text.strip()
            return "To change, you can always click here." in tooltip_text

        except Exception as e:
            print(f"Test failed due to error: {e}")
            return False

    def capture_inventory_requisition_screenshot(self):
        """
        /**
        * @Test13
        * @description This method navigates to the Inventory Requisition section, captures a screenshot of the page,
        *              and saves it in the screenshots folder.
        * @expected
        * Screenshot of the page is captured and saved successfully.
        */
        """
        try:
            # Create a timestamp for the screenshot filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = os.path.join(os.path.dirname(__file__),
                                           f"../screenshots/inventory-requisition-{timestamp}.png")

            # Navigate to the substore
            self.wait.until(EC.element_to_be_clickable(self.substore["substore_link"])).click()

            # Select the substore
            self.wait.until(EC.element_to_be_clickable(self.substore["select_substore"])).click()

            # Click on the Inventory tab
            self.wait.until(EC.element_to_be_clickable(self.substore["inventory"])).click()

            # Click on the Inventory Requisition section
            self.wait.until(EC.element_to_be_clickable(self.substore["inventory_requisition"])).click()

            # Verify the URL contains the expected path
            if "Inventory/InventoryRequisitionList" not in self.driver.current_url:
                return False

            # Take a screenshot of the current page
            screenshot_success = self.driver.save_screenshot(screenshot_path)

            return screenshot_success

        except Exception as e:
            print(f"Test failed due to error: {e}")
            return False
