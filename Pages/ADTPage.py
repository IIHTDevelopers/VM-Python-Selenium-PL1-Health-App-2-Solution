import time
import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ADTPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Construct the correct path for the JSON file
        base_path = os.path.dirname(os.path.abspath(__file__))  # Current script directory
        json_path = os.path.join(base_path, "..", "Data", "PatientName.json")  # Adjusted path

        # Load test data from JSON
        try:
            with open(json_path, "r") as f:
                self.test_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found at {json_path}")

        self.ADT = {
            "ADT_link": (By.CSS_SELECTOR, 'a[href="#/ADTMain"]'),
            "search_bar": (By.CSS_SELECTOR, "#quickFilterInput"),
            "admitted_patients_tab": (By.CSS_SELECTOR, 'ul.page-breadcrumb a[href="#/ADTMain/AdmittedList"]'),
            "more_options_button": (By.XPATH, "//button[contains(text(),'...')]"),
            "change_doctor_option": (By.CSS_SELECTOR, 'a[danphe-grid-action="changedr"]'),
            "change_doctor_modal": (By.CSS_SELECTOR, 'div.modelbox-div'),
            "update_button": (By.XPATH, '//button[text()="Update"]'),
            "field_error_message": (By.XPATH, "//span[text()='Select doctor from the list.']"),
            "counter_item": (By.XPATH, "//div[@class='counter-item']"),
        }

    def verify_field_level_error_message(self):
        """
        /**
        * @Test14
        * @description This test verifies that the error message "Select doctor from the list." is displayed
        *              when the user attempts to update the doctor without selecting a value.
        * @expected The error message "Select doctor from the list." is shown near the field.
        */
        """
        try:
            patient_name = self.test_data['PatientNames'][0]['Patient1'] or ""

            # Click on the ADT link
            self.wait.until(EC.element_to_be_clickable(self.ADT["ADT_link"])).click()

            # Wait for counter items to load
            time.sleep(3)  # Consider replacing with an explicit wait
            counter_items = self.wait.until(EC.presence_of_all_elements_located(self.ADT["counter_item"]))

            if counter_items:
                counter_items[0].click()
            else:
                print("No counter items available")
                return False

            # Navigate to "Admitted Patients" tab
            self.wait.until(EC.element_to_be_clickable(self.ADT["admitted_patients_tab"])).click()

            # Search for the patient
            search_bar = self.wait.until(EC.visibility_of_element_located(self.ADT["search_bar"]))
            search_bar.clear()
            search_bar.send_keys(patient_name)
            search_bar.send_keys("\n")  # Press Enter

            # Click on the "..." button for the patient
            self.wait.until(EC.element_to_be_clickable(self.ADT["more_options_button"])).click()

            # Select "Change Doctor" from the options
            self.wait.until(EC.element_to_be_clickable(self.ADT["change_doctor_option"])).click()

            # Wait for the "Change Doctor" modal to appear
            self.wait.until(EC.visibility_of_element_located(self.ADT["change_doctor_modal"]))

            # Click on the "Update" button without selecting a doctor
            self.wait.until(EC.element_to_be_clickable(self.ADT["update_button"])).click()

            # Verify the error message is displayed
            error_message = self.wait.until(EC.visibility_of_element_located(self.ADT["field_error_message"]))

            return error_message.is_displayed() and error_message.text.strip() == "Select doctor from the list."

        except Exception as e:
            print(f"Test failed due to error: {e}")
            return False
