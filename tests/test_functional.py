import pathlib
import time
import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.LoginPage import LoginPage
from Pages.AppointmentPage import AppointmentPage
from Pages.OperationTheatrePage import OperationTheatrePage
from Pages.DoctorPage import DoctorPage
from Pages.ProcurementPage import ProcurementPage
from Pages.AdminPage import AdminPage
from Pages.PatientPage import PatientPage
from Pages.IncentivePage import IncentivePage
from Pages.SettingsPage import SettingsPage
from Pages.SubstorePage import SubstorePage
from Pages.ADTPage import ADTPage
from Pages.UtilitiesPage import UtilitiesPage
from tests.TestUtils import TestUtils


# Fixture to set up the WebDriver for each test function
@pytest.fixture(scope="function")
def setup_driver():
    """
    Initializes the WebDriver for Chrome and navigates to the application URL.
    Ensures the driver is properly closed after each test execution.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get('https://healthapp.yaksha.com/')
    driver.implicitly_wait(15)
    driver.maximize_window()
    yield driver
    driver.quit()

# Reusable login function to be called before each test
def login_to_application(driver):
    """
    Logs in to the application before each test.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        test_credentials (dict): Dictionary containing username and password.
    """
    login_page = LoginPage(driver)
    login_page.perform_login()
    time.sleep(5)

@pytest.mark.order(1)
def test_verification_module(setup_driver):
    """
    Test Case: Verify the presence of Visit Type drop down by selecting "New patient" option.

    Expected Result:
    - The 'Visit Type' column should contain only patients in the "new visit" category.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    appointment_page = AppointmentPage(driver)
    testResult =  appointment_page.verify_visit_type_dropdown()
    time.sleep(5)
    verificationResult = verify_visit_type(driver)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_verification_module", True, "Functional")
        print("test_verification_module = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_verification_module", False, "Functional")
        print("test_verification_module = Failed")


@pytest.mark.order(2)
def test_ot_booking_alert(setup_driver):
    """
    Test Case: Handle Alert for OT Booking Without Patient Selection.

    Expected Result:
    - An alert with the message "Patient not Selected! Please Select the patient first!" is displayed and handled.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    ot_page = OperationTheatrePage(driver)
    testResult = ot_page.handle_ot_booking_alert()
    is_ot_booking_modal_displayed(driver)
    time.sleep(5)
    verificationResult = verify_visit_type(driver)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_ot_booking_alert", True, "Functional")
        print("test_ot_booking_alert = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_ot_booking_alert", False, "Functional")
        print("test_ot_booking_alert = Failed")


@pytest.mark.order(3)
def test_verify_patient_overview(setup_driver):
    """
        Test Case: Verify Patient Overview Page Displays information Correctly

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/Doctors/OutPatientDoctor/NewPatient
        2. Click on the In Patient Department Tab.
        3. In the search bar, enter the patient name "Devid8 Roy8" and perform the search.
        4. Locate the patient in the results and click on the Preview icon under the Actions column.

        Expected Result:
        - Verify the same patient overview page is displayed with the same patient name.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    doctor_page = DoctorPage(driver)
    testResult = doctor_page.verify_patient_overview()
    verificationResult = verify_user_is_on_correct_url(driver,"Doctors/PatientOverviewMain/PatientOverview")
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_verify_patient_overview", True, "Functional")
        print("test_verify_patient_overview = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_verify_patient_overview", False, "Functional")
        print("test_verify_patient_overview = Failed")

@pytest.mark.order(4)
def test_add_progress_note_for_patient(setup_driver):
    """
        Test Case: Add Progress Note for In Patient

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/Doctors/OutPatientDoctor/NewPatient
        2. Click on the In Patient Department Tab.
        3. In the search bar, enter the patient name "Devid173 Roy8" and perform the search.
        4. On the Patient Overview page, click on the Notes section..
        5. Now click on "Add Notes" button.
        6. Select Template as "Progress Note" from dropdown.
        7, Enter subjective Notes as "Test Notes" and click on save button.

        Expected Result:
        - A success confirmation popup with the message: "Progress Note Template added." should appear.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    doctor_page = DoctorPage(driver)
    testResult = doctor_page.add_progress_note_for_patient()
    verificationResult = verify_user_is_on_correct_url(driver,"Doctors/PatientOverviewMain/NotesSummary/NotesList")
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_add_progress_note_for_patient", True, "Functional")
        print("test_add_progress_note_for_patient = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("TestValidLogin", False, "Functional")
        print("test_add_progress_note_for_patient = Failed")

@pytest.mark.order(5)
def test_add_currency_and_verify(setup_driver):
    """
        Test Case: Add and Verify New Currency in Settings

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/ProcurementMain/PurchaseRequest/PurchaseRequestList
        2. Click on the Settings tab then click on currency.
        3. Click on add currency button.
        4. Enter a unique currecny code and fill description .
        5. Now click on "Add Currency" button.

        Expected Result:
        - The new currency should be added successfully and displayed in the table with the correct currency code and description.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    procurement_page = ProcurementPage(driver)
    testResult = procurement_page.add_currency_and_verify()
    verificationResult = verify_user_is_on_correct_url(driver,"ProcurementMain/Settings/CurrencyList")
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_add_currency_and_verify", True, "Functional")
        print("test_add_currency_and_verify = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_add_currency_and_verify", False, "Functional")
        print("test_add_currency_and_verify = Failed")

@pytest.mark.order(6)
def test_verify_mandatory_fields_warning(setup_driver):
    """
        Test Case: Verify Warning Popup for Mandatory Fields in Scheme Refund

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/Utilities
        2. Click on the Scheme Refund Tab.
        3. Click on "New scheme Refund Entry" button.
        4. Now click on save without entering value in any field.

        Expected Result:
        - A warning popup with the message: "Please fill all the mandatory fields."
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    utilities_page = UtilitiesPage(driver)
    testResult = utilities_page.verify_mandatory_fields_warning()
    verificationResult = verify_user_is_on_correct_url(driver,"/Utilities/SchemeRefund")
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_verify_mandatory_fields_warning", True, "Functional")
        print("test_verify_mandatory_fields_warning = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_verify_mandatory_fields_warning", False, "Functional")
        print("test_verify_mandatory_fields_warning = Failed")

@pytest.mark.order(7)
def test_verify_user_profile_navigation(setup_driver):
    """
        Test Case: Verify Navigation to User Profile Page

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/
        2. Click on the Admin dropdown.
        3. Select the "My Profile" option.

        Expected Result:
        - Verify that the user is redirected to the "User Profile" page and the page header or title confirms this.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    admin_page = AdminPage(driver)
    testResult = admin_page.verify_user_profile_navigation()
    verificationResult = verify_user_is_on_correct_url(driver,"Employee/ProfileMain/UserProfile")
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_verify_user_profile_navigation", True, "Functional")
        print("test_verify_user_profile_navigation = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_verify_user_profile_navigation", False, "Functional")
        print("test_verify_user_profile_navigation = Failed")

@pytest.mark.order(8)
def test_upload_profile_picture(setup_driver):
    """
        Test Case: Verify Patient Profile Picture Upload

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/Patient/SearchPatient
        2. Click on Register Patient Tab.
        3. Select the Profile Picture icon.
        4. Click on the "New Photo" button.
        5. Upload an image and click on the "Done" button.

        Expected Result:
        - Verify that the uploaded image is displayed successfully in the patient's profile.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    patient_page = PatientPage(driver)
    testResult = patient_page.upload_profile_picture()
    verificationResult = verify_image_is_uploaded(driver)
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_upload_profile_picture", True, "Functional")
        print("test_upload_profile_picture = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_upload_profile_picture", False, "Functional")
        print("test_upload_profile_picture = Failed")

@pytest.mark.order(9)
def test_edit_tds_for_employee(setup_driver):
    """
        Test Case: Verify TDS Percent update for an employee

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/Incentive/Transactions/InvoiceLevel
        2. Click on the "Settings" tab.
        3. Locate the row corresponding to the specified employee name.
        4. Click the "Edit TDS%" button within the located row.
        5. In the "Edit TDS Percent" modal, enter the updated TDS% value.
        6. Click on the "Update TDS" button.
        7. Verify that the updated TDS% value is correctly displayed in the table.

        Expected Result:
        - The updated TDS% value is displayed correctly in the corresponding row of the table.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    inc_page = IncentivePage(driver)
    testResult = inc_page.edit_tds_for_employee()
    verificationResult = verify_tds_test(driver)
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_edit_tds_for_employee", True, "Functional")
        print("Ttest_edit_tds_for_employee = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_edit_tds_for_employee", False, "Functional")
        print("test_edit_tds_for_employee = Failed")

@pytest.mark.order(10)
def test_toggle_price_category_status(setup_driver):
    """
        Test Case: Verify Price Category Enable/Disable

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/Settings
        2. Click on more... and select "Price Category" tab.
        3. Click on Disable button to disable any Code in the table.
        4. Verify a success message appears with the message "Deactivated.".
        5. Activate the same code and verify the success message.

        Expected Result:
        - A success message is displayed for both actions: "Deactivated." for disabling and "Activated." for enabling.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    setting_page = SettingsPage(driver)
    testResult = setting_page.toggle_price_category_status()
    verificationResult = verify_user_is_on_correct_url(driver,"Settings/PriceCategory")
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_toggle_price_category_status", True, "Functional")
        print("Ttest_toggle_price_category_status = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_toggle_price_category_status", False, "Functional")
        print("test_toggle_price_category_status = Failed")

@pytest.mark.order(11)
def test_verify_navigation_between_submodules(setup_driver):
    """
        Test Case: Verify to navigate to each sections which are present in the "Inventory" sub-module

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/WardSupply
        2. Click on the "Inventory Requisition" section
        3. Click on the "Stock"
        4. Click on the "Consumption"
        5. Click on the " Reports"
        6. Click on the "Patient Consumption"
        7. Click on the "Return"
        8. Naviaget back to the "Inventory Requisition" section

        Expected Result:
        - Ensure that it should navigate to each sections of the "Inventory" module
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    substore_page = SubstorePage(driver)
    testResult = substore_page.verify_navigation_between_submodules()
    verificationResult = verify_user_is_on_correct_url(driver,"Inventory/Return")
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_verify_navigation_between_submodules", True, "Functional")
        print("test_verify_navigation_between_submodules = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_verify_navigation_between_submodules", False, "Functional")
        print("test_verify_navigation_between_submodules = Failed")

@pytest.mark.order(12)
def test_verify_tooltip_text(setup_driver):
    """
        Test Case: Verify tooltip text on hover in Substore > Inventory tab

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/WardSupply
        2. Click on Inventory tab.
        3. Hover over the cursor icon located at the top-right corner.
        4. Capture the tooltip text displayed on hover.

        Expected Result:
        - The tooltip text displayed on hover should contain: "To change, you can always click here."
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    substore_page = SubstorePage(driver)
    testResult = substore_page.verify_tooltip_text()
    verificationResult = is_tooltip_displayed(driver)
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("TestValidLogin", True, "Functional")
        print("TestValidLogin = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("TestValidLogin", False, "Functional")
        print("TestValidLogin = Failed")

@pytest.mark.order(13)
def test_capture_inventory_requisition_screenshot(setup_driver):
    """
        Test Case: Verify to navigate to each sections which are present in the "Inventory" sub-module

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/WardSupply
        2. Select any substore from the list.
        3. Click on the "Inventory Requisition" section.
        4. Take a screenshot of the current page and save it in the screenshots folder.

        Expected Result:
        - The screenshot of the Inventory Requisition page is captured and saved under the screenshots folder.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    substore_page = SubstorePage(driver)
    testResult = substore_page.capture_inventory_requisition_screenshot()
    verificationResult = verify_user_is_on_correct_url(driver,"Inventory/InventoryRequisitionList")
    time.sleep(5)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_capture_inventory_requisition_screenshot", True, "Functional")
        print("test_capture_inventory_requisition_screenshot = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_capture_inventory_requisition_screenshot", False, "Functional")
        print("TestValidLogin = Failed")

@pytest.mark.order(14)
def test_verify_field_level_error_message(setup_driver):
    """
        Test Case: Verify to navigate to each sections which are present in the "Inventory" sub-module

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/ADTMain/AdmissionSearchPatient
        2. Click on Admitted Patients Tab.
        3. Search for Devid8 Roy8.
        4. Click on ... button from table and click on change doctor.
        5. Change doctor Modal opens and click on update button without filling any value.

        Expected Result:
        - Verify a field level error message appears "Select doctor from the list."
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    adt_page = ADTPage(driver)
    testResult = adt_page.verify_field_level_error_message()
    verificationResult = verify_error_message(driver)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_verify_field_level_error_message", True, "Functional")
        print("test_verify_field_level_error_message = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_verify_field_level_error_message", False, "Functional")
        print("test_verify_field_level_error_message = Failed")

@pytest.mark.order(15)
def test_verify_logout_functionality(setup_driver):
    """
        Test Case: Verify logout functionality from Admin dropdown

        Steps:
        1. Navigate to https://healthapp.yaksha.com/Home/Index#/
        2. Click on the Admin dropdown
        3. Click on logout option.
        4. Verify the user is redirected to the login page.

        Expected Result:
        - User is logged out successfully and the login page is displayed.
    """
    test_obj = TestUtils()
    driver = setup_driver
    login_to_application(driver)  # Perform login before test
    login_page = LoginPage(driver)
    testResult = login_page.verify_logout_functionality()
    verificationResult = verify_user_is_logged_out(driver)
    if (testResult == True and verificationResult == True):
        passed = True
        test_obj.yakshaAssert("test_verify_logout_functionality", True, "Functional")
        print("test_verify_logout_functionality = Passed")
    else:
        passed = False
        test_obj.yakshaAssert("test_verify_logout_functionality", False, "Functional")
        print("test_verify_logout_functionality = Failed")


"""------------------------------------------------- Helper Method------------------------------------------------------------"""


def verify_visit_type(driver):
    """
    /**
    * @Test
    * @description This method verifies that the visit type column has more than one entry.
    * @expected
    * The visit type column should contain more than one entry.
    */
    """
    visit_type_column_locator = (By.XPATH, "//div[@col-id='AppointmentType']")
    try:
        visit_type_cells = driver.find_elements(*visit_type_column_locator)
        return len(visit_type_cells) > 1
    except Exception as e:
        print(f"Visit type verification failed: {e}")
        return False

def is_ot_booking_modal_displayed(driver):
    """
    /**
    * @Test
    * @description This method verifies if the OT Booking Modal is displayed.
    * @expected
    * The OT Booking Modal should be visible on the screen.
    */
    """
    modal_locator = (By.CSS_SELECTOR, "div.modelbox-div")
    try:
        wait = WebDriverWait(driver, 10)
        modal = wait.until(EC.visibility_of_element_located(modal_locator))
        return modal.is_displayed()
    except Exception as e:
        print(f"OT Booking Modal verification failed: {e}")
        return False

def verify_user_is_on_correct_url(driver, expected_url):
    """
    /**
    * @Test
    * @description This method verifies that the user is on the expected URL.
    * @expected
    * The current URL should contain the expected URL.
    */
    """
    try:
        WebDriverWait(driver, 10).until(lambda d: expected_url in d.current_url)
        return expected_url in driver.current_url
    except Exception as e:
        print(f"URL verification failed: {e}")
        return False

def verify_user_is_logged_out(driver):
    """
    /**
    * @Test
    * @description This method verifies that the user is logged out by checking if the login button is visible.
    * @expected
    * The login button should be displayed after logout.
    */
    """
    login_button_locator = (By.CSS_SELECTOR, "#login")

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(login_button_locator))
        return driver.find_element(*login_button_locator).is_displayed()
    except Exception as e:
        print(f"Logout verification failed: {e}")
        return False

def verify_error_message(driver):
    """
    /**
    * @Test
    * @description This method verifies that the error message "Select doctor from the list." is displayed.
    * @expected
    * The error message should be visible near the field.
    */
    """
    try:
        # Wait for the error message to be visible
        error_message_locator = (By.XPATH, "//span[text()='Select doctor from the list.']")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Verify the error message is displayed
        error_message = driver.find_element(*error_message_locator)
        return error_message.is_displayed()

    except Exception as e:
        print(f"Error message verification failed: {e}")
        return False

def is_tooltip_displayed(driver):
    """
    /**
    * @Test
    * @description This method verifies that the tooltip/modal with class 'modal-content' is displayed.
    * @expected
    * The tooltip/modal should be visible on the screen.
    */
    """
    try:
        # Wait for the tooltip/modal to be visible
        tooltip_locator = (By.CSS_SELECTOR, "div.modal-content")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(tooltip_locator))

        # Verify the tooltip/modal is displayed
        tooltip = driver.find_element(*tooltip_locator)
        return tooltip.is_displayed()

    except Exception as e:
        print(f"Tooltip verification failed: {e}")
        return False

def verify_tds_test(driver):
    """
    /**
    * @Test
    * @description This method verifies that the second element in the 'FullName' column contains 'Rakesh'.
    * @expected
    * The second element's text should include 'Rakesh'.
    */
    """
    try:
        # Find all elements with the specified column ID
        pt_names = driver.find_elements(By.CSS_SELECTOR, 'div[col-id="FullName"]')

        # Verify the second element's text contains 'Rakesh'
        return len(pt_names) > 1 and "Rakesh" in pt_names[1].text

    except Exception as e:
        print(f"TDS test verification failed: {e}")
        return False



def verify_image_is_uploaded(driver):
    """
    /**
    * @Test
    * @description This method verifies that an uploaded image is displayed successfully.
    * @expected
    * The uploaded image should be visible on the page.
    */
    """
    try:
        # Wait for the image to be visible
        img_locator = (By.CSS_SELECTOR, "div.wrapper img")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(img_locator))

        # Verify the image is visible
        image = driver.find_element(*img_locator)
        return image.is_displayed()

    except Exception as e:
        print(f"Image upload verification failed: {e}")
        return False
