from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class AdminPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.admin = {
            "admin_dropdown": (By.XPATH, '//li[@class="dropdown dropdown-user"]'),
            "my_profile_option": (By.CSS_SELECTOR, 'a[routerlink="Employee/ProfileMain"]'),
            "user_profile_header": (By.CSS_SELECTOR, 'a[routerlink="UserProfile"]'),
        }

    def verify_user_profile_navigation(self):
        """
        /**
        * @Test7
        * @description This method verifies that the user is successfully navigated to the "User Profile" page 
        *              after selecting the "My Profile" option from the Admin dropdown.
        * @expected
        * Verify that the user is redirected to the "User Profile" page and the page header or title confirms this.
        */
        """
        try:
            # Click on Admin dropdown
            admin_dropdown = self.wait.until(EC.visibility_of_element_located(self.admin["admin_dropdown"]))
            time.sleep(10)
            admin_dropdown.click()

            # Select "My Profile" option
            my_profile_option = self.wait.until(EC.element_to_be_clickable(self.admin["my_profile_option"]))
            my_profile_option.click()

            # Wait for User Profile page to load
            time.sleep(2)

            # Verify that the User Profile page is displayed
            header_text = self.driver.find_element(*self.admin["user_profile_header"]).text.strip()

            if header_text == "User Profile":
                return True
            else:
                print(f"Expected 'User Profile', but found '{header_text}'")
                return False

        except Exception as e:
            print(f"Test failed due to error: {e}")
            return False
