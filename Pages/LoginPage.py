import json
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)

        # Construct the correct path for the JSON file
        base_path = os.path.dirname(os.path.abspath(__file__))  # Current script directory
        json_path = os.path.join(base_path, "..", "Data", "ValidLogin.json")  # Adjusted path

        # Load test data from JSON
        try:
            with open(json_path, "r") as f:
                self.test_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found at {json_path}")

        self.username_input = (By.CSS_SELECTOR, "#username_id")
        self.password_input = (By.CSS_SELECTOR, "#password")
        self.login_button = (By.CSS_SELECTOR, "#login")
        self.login_error_message = (By.XPATH, '//div[contains(text(),"Invalid credentials !")]')
        self.admin = (By.XPATH, '//li[@class="dropdown dropdown-user"]')
        self.log_out = (By.XPATH, "//a[text() = ' Log Out ']")

    def perform_login(self):
        """
        /**
        * @Test1 This method logs in the user with valid credentials.
        *
        * @description This method performs the login operation using the provided valid credentials. It highlights the input
        *              fields for better visibility during interaction and fills the username and password fields. After submitting
        *              the login form by clicking the login button, it validates the success of the login process. The login is
        *              considered successful if there are no errors.
        */
        """
        try:
            valid_username = self.test_data['ValidLogin'][0]['ValidUser Name']
            valid_password = self.test_data['ValidLogin'][1]['ValidPassword']

            # Highlight and fill the username field
            username_field = self.wait.until(EC.visibility_of_element_located(self.username_input))
            username_field.clear()
            username_field.send_keys(valid_username)

            # Highlight and fill the password field
            password_field = self.wait.until(EC.visibility_of_element_located(self.password_input))
            password_field.clear()
            password_field.send_keys(valid_password)

            # Highlight and click the login button
            login_btn = self.wait.until(EC.element_to_be_clickable(self.login_button))
            login_btn.click()

            # Verify successful login by checking if 'admin' element is visible
            admin_element = self.wait.until(EC.visibility_of_element_located(self.admin))
            assert admin_element.is_displayed(), "Admin element is not visible after login."
        except Exception as e:
            print("Error during login:", e)

    def verify_logout_functionality(self):
        """
        /**
        * @Test15
        * @description This method verifies the logout functionality from the Admin dropdown.
        * @expected
        * User is logged out successfully and the login page is displayed.
        */
        """
        try:
            time.sleep(10)  # Consider replacing with an explicit wait

            # Click the admin dropdown
            admin_element = self.wait.until(EC.element_to_be_clickable(self.admin))
            admin_element.click()

            # Click the logout button
            log_out_element = self.wait.until(EC.element_to_be_clickable(self.log_out))
            log_out_element.click()

            # Verify that the login button is visible after logout
            login_btn = self.wait.until(EC.visibility_of_element_located(self.login_button))

            return login_btn.is_displayed()

        except Exception as e:
            print(f"Test failed due to error: {e}")
            return False
