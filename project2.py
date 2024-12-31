from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Set up the WebDriver and launch the URL
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

# Test Case: TC_PIM_01 - Forgot Password Link Validation
def test_forgot_password():
    print("Executing TC_PIM_01 - Forgot Password Link Validation")
    try:
        # Locate and click on the 'Forgot Password' link
        forgot_password_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Forgot your password?"))
        )
        forgot_password_link.click()

        # Check for the presence of the username textbox and reset password button
        username_textbox = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        username_textbox.send_keys("Admin")
        reset_password_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Reset Password')]")
        reset_password_button.click()

        # Validate the successful reset password message
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Reset Password link sent successfully')]"))
        )
        assert success_message.is_displayed(), "Success message not displayed"
        print("TC_PIM_01 - Passed")

    except Exception as e:
        print("TC_PIM_01 - Failed", e)

# Test Case: TC_PIM_02 - Header Validation on Admin Page
def test_admin_page_header_validation():
    print("Executing TC_PIM_02 - Header Validation on Admin Page")
    try:
        # Login as Admin
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("Admin")
        driver.find_element(By.NAME, "password").send_keys("admin123" + Keys.RETURN)

        # Navigate to Admin page
        admin_page_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/web/index.php/admin/viewAdminModule']"))
        )
        admin_page_link.click()

        # Validate the page title
        assert driver.title == "OrangeHRM", "Admin Page Title Validation Failed"

        # Validate Admin page headers
        headers_to_validate = [
            "User Management", "Job", "Organization", "Qualifications", "Nationalities", 
            "Corporate Banking", "Configuration"
        ]
        for header in headers_to_validate:
            header_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//h6[contains(text(), '{header}')]"))
            )
            assert header_element.is_displayed(), f"{header} not found on Admin Page"

        print("TC_PIM_02 - Passed")

    except Exception as e:
        print("TC_PIM_02 - Failed", e)

# Test Case: TC_PIM_03 - Main Menu Validation on Admin Page
def test_admin_page_main_menu_validation():
    print("Executing TC_PIM_03 - Main Menu Validation on Admin Page")
    try:
        # Go to the Admin page
        admin_page_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/web/index.php/admin/viewAdminModule']"))
        )
        admin_page_link.click()

        # Validate menu items on the left side panel
        menu_items_to_validate = [
            "Admin", "PIM", "Leave", "Time", "Recruitment", "Info",
            "Performance", "Dashboard", "Directory", "Maintenance", "Buzz"
        ]
        for item in menu_items_to_validate:
            menu_item_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(), '{item}')]"))
            )
            assert menu_item_element.is_displayed(), f"{item} not found on Admin Page Menu"

        print("TC_PIM_03 - Passed")

    except Exception as e:
        print("TC_PIM_03 - Failed", e)

# Run test cases
test_forgot_password()
time.sleep(2)  # Adding delay between test cases
test_admin_page_header_validation()
time.sleep(2)
test_admin_page_main_menu_validation()

# Close the driver
driver.quit()
