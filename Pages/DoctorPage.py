from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import json

class DoctorPage:
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

        self.doctor = {
            "doctor_link": (By.CSS_SELECTOR, 'a[href="#/Doctors"]'),
            "in_patient_tab": (By.CSS_SELECTOR, 'ul.page-breadcrumb  a[href="#/Doctors/InPatientDepartment"]'),
            "search_box": (By.CSS_SELECTOR, 'input#quickFilterInput'),
            "actions_preview_icon": (By.CSS_SELECTOR, 'a[title="Preview"]'),
            "patient_name_heading": (By.CSS_SELECTOR, 'h1.pat-name-hd'),
            "notes_section": (By.CSS_SELECTOR, 'a[href="#/Doctors/PatientOverviewMain/NotesSummary"]'),
            "add_notes_button": (By.XPATH, '//a[text()="Add Notes"]'),
            "template_dropdown": (By.CSS_SELECTOR, 'input[value-property-name="TemplateName"]'),
            "subjective_notes_field": (By.XPATH, '//label[text()="Subjective Notes"]/../div/textarea'),
            "success_confirmation_popup": (By.XPATH, '//p[contains(text(),"Success")]/../p[contains(text(),"Progress Note Template added.")]'),
            "save_notes_button": (By.XPATH, '//button[contains(text(),"Save")]'),
            "note_type": (By.CSS_SELECTOR, 'input[placeholder="Select Note Type"]'),
        }

    def verify_patient_overview(self):
        """
        /**
        * @Test3
        * @description This method searches for a patient and verifies their overview page.
        * @param patientName - Name of the patient to search.
        */
        """
        try:
            patient_name = self.test_data['PatientNames'][0]['Patient1'] or ""
            # patient_name = "Devid8 Roy8"

            self.wait.until(EC.element_to_be_clickable(self.doctor["doctor_link"])).click()
            self.wait.until(EC.element_to_be_clickable(self.doctor["in_patient_tab"])).click()

            # Search for the patient
            search_boxes = self.wait.until(EC.presence_of_all_elements_located(self.doctor["search_box"]))
            for search_box in search_boxes:
                if search_box.is_displayed():
                    search_box.clear()
                    search_box.send_keys(patient_name)
                    time.sleep(2)  # Wait for the search to process
                    break

            # Click on the preview icon under Actions
            self.wait.until(EC.element_to_be_clickable(self.doctor["actions_preview_icon"])).click()

            # Verify the patient overview page is displayed with the correct patient name
            self.wait.until(EC.visibility_of_element_located(self.doctor["patient_name_heading"]))
            displayed_patient_name = self.driver.find_element(*self.doctor["patient_name_heading"]).text.strip()
            assert displayed_patient_name.lower() == patient_name.lower(), f"Expected {patient_name}, but found {displayed_patient_name}"

            return True

        except Exception as e:
            print(f"Exception occurred: {e}")
            return False

    def add_progress_note_for_patient(self):
        """
        /**
        * @Test4
        * @description This method searches for a specific patient in the In Patient Department, navigates to the patient's
        *              overview page, and adds a Progress Note. The method ensures that the note is successfully added
        *              and verifies the confirmation message.
        * @expected
        * The method should successfully add a Progress Note for the patient, and a success confirmation message
        * with the text "Progress Note Template added." should be displayed.
        */
        """
        try:
            patient_name = self.test_data['PatientNames'][1]['Patient2'] or ""

            self.wait.until(EC.element_to_be_clickable(self.doctor["doctor_link"])).click()
            self.wait.until(EC.element_to_be_clickable(self.doctor["in_patient_tab"])).click()

            # Search for the patient
            search_boxes = self.wait.until(EC.presence_of_all_elements_located(self.doctor["search_box"]))
            for search_box in search_boxes:
                if search_box.is_displayed():
                    search_box.clear()
                    search_box.send_keys(patient_name)
                    time.sleep(2)  # Wait for the search to process
                    break

            # Click on the preview icon under Actions
            self.wait.until(EC.element_to_be_clickable(self.doctor["actions_preview_icon"])).click()

            # Click on Notes section
            self.wait.until(EC.element_to_be_clickable(self.doctor["notes_section"])).click()

            # Click on Add Notes button
            self.wait.until(EC.element_to_be_clickable(self.doctor["add_notes_button"])).click()

            # Select note type
            note_type_input = self.wait.until(EC.element_to_be_clickable(self.doctor["note_type"]))
            note_type_input.click()
            note_type_input.send_keys("Progress Note")
            note_type_input.send_keys("\n")  # Press Enter

            # Select "Progress Note" from the Template dropdown
            template_input = self.wait.until(EC.element_to_be_clickable(self.doctor["template_dropdown"]))
            template_input.click()

            template_dropdown = "Progress Note"
            for char in template_dropdown:
                template_input.send_keys(char)
                time.sleep(0.1)  # Adjust this delay as needed

            template_input.send_keys("\n")

            subjective_notes = self.wait.until(EC.presence_of_element_located(self.doctor["subjective_notes_field"]))
            subjective_notes.clear()
            subjective_notes.send_keys("Test Notes")

            save_button = self.wait.until(EC.element_to_be_clickable(self.doctor["save_notes_button"]))
            save_button.click()

            success_popup = self.wait.until(EC.visibility_of_element_located(self.doctor["success_confirmation_popup"]))
            assert "Progress Note Template added." in success_popup.text, "Progress Note was not added successfully."

            return True

        except Exception as e:
            print(f"Exception occurred: {e}")
            return False