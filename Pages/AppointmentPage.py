from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class AppointmentPage:
    def __init__(self, driver):
        self.driver = driver
        self.appointment = {
            "appointment_link": (By.CSS_SELECTOR, 'a[href="#/Appointment"]'),
            "counter_item": (By.XPATH, "//div[@class='counter-item']"),
            "appointment_booking_list": (By.CSS_SELECTOR, "ul.page-breadcrumb li a[href='#/Appointment/ListAppointment']"),
            "visit_type_dropdown": (By.NAME, "VistType"),
            "from_date": (By.XPATH, "(//input[@id='date'])[1]"),
            "show_patient": (By.XPATH, "//button[contains(text(),'Show Patient')]"),
            "visit_type_column": (By.XPATH, "//div[@col-id='AppointmentType']"),
        }

    def verify_visit_type_dropdown(self):
        """
        /**
        * @Test1
        * @description This method verifies the 'Visit Type' dropdown functionality and validates 'New Visit' patients.
        */
        """
        driver = self.driver
        try:
            # Click Appointment link
            driver.find_element(*self.appointment["appointment_link"]).click()

            # Wait for counter items to load
            time.sleep(10)
            counter_items = driver.find_elements(*self.appointment["counter_item"])
            counter_count = len(counter_items)
            print(f"Counter count is {counter_count}")

            if counter_count > 0:
                counter_items[0].click()
                driver.find_element(*self.appointment["appointment_link"]).click()
            else:
                print("No counter items available")

            driver.find_element(*self.appointment["appointment_booking_list"]).click()

            # Select "New Patient" from the dropdown
            visit_dropdown = Select(driver.find_element(*self.appointment["visit_type_dropdown"]))
            visit_dropdown.select_by_visible_text("New Patient")

            # Enter "January 2024" in the FROM date field
            from_date_element = driver.find_element(*self.appointment["from_date"])
            from_date_element.clear()
            from_date_element.send_keys("01-01-2024")

            # Click "Show Patient" button
            driver.find_element(*self.appointment["show_patient"]).click()
            time.sleep(2)

            # Validate "Visit Type" column contains only "New Visit"
            visit_type_cells = driver.find_elements(*self.appointment["visit_type_column"])
            visit_type_count = len(visit_type_cells)
            print(f"Visit count >> {visit_type_count}")

            for i in range(1, visit_type_count):
                visit_type_text = visit_type_cells[i].text.strip()
                if "New" not in visit_type_text:
                    print(f"Visit type mismatch at index {i}: {visit_type_text}")
                    return False

            return True

        except Exception as e:
            print(f"Exception occurred: {e}")
            return False
