import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PatientPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.patient = {
            "patient_link": (By.CSS_SELECTOR, 'a[href="#/Patient"]'),
            "register_patient": (By.CSS_SELECTOR, 'ul.page-breadcrumb a[href="#/Patient/RegisterPatient"]'),
            "new_photo_button": (By.XPATH, '//button[contains(text(),"New Photo")]'),
            "upload_button": (By.CSS_SELECTOR, 'label[for="fileFromLocalDisk"]'),
            "done_button": (By.XPATH, '//button[text()="Done"]'),
            "uploaded_img": (By.CSS_SELECTOR, 'div.wrapper img'),
            "profile_picture_icon": (By.CSS_SELECTOR, 'a[title="Profile Picture"]'),
        }

    def upload_profile_picture(self):
        """
        /**
        * @Test8
        * @description This method verifies the successful upload of a profile picture for a patient by navigating to the "Register Patient" tab
        *              and completing the upload process.
        * @expected
        * Verify that the uploaded image is displayed successfully in the patient's profile.
        */
        """
        try:
            # Define the path to the image
            image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestImage/UploadImage.png"))

            # Click on the Patient link
            self.wait.until(EC.element_to_be_clickable(self.patient["patient_link"])).click()

            # Click on the "Register Patient" tab
            self.wait.until(EC.element_to_be_clickable(self.patient["register_patient"])).click()

            # Select the Profile Picture icon
            self.wait.until(EC.element_to_be_clickable(self.patient["profile_picture_icon"])).click()

            # Click on "New Photo" button
            self.wait.until(EC.element_to_be_clickable(self.patient["new_photo_button"])).click()

            # Upload image
            upload_button = self.wait.until(EC.presence_of_element_located(self.patient["upload_button"]))
            upload_button.click()  # Click the label to open the file dialog
            self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(
                image_path)  # Send the file path to the file input

            time.sleep(2)  # Wait for the upload to process (consider replacing with a more robust wait)

            # Click on the "Done" button
            self.wait.until(EC.element_to_be_clickable(self.patient["done_button"])).click()

            # Verify that the uploaded image is displayed successfully
            uploaded_img = self.wait.until(EC.visibility_of_element_located(self.patient["uploaded_img"]))

            return uploaded_img.is_displayed()

        except Exception as e:
            print(f"Test failed due to error: {e}")
            return False

