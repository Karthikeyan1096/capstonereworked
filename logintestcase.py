from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the driver (replace with the path to your own WebDriver executable)
driver = webdriver.Chrome()

# URL of the Grange-+RM System
url = "http://opensource-Demo.orangehrmlive.com/web/index.php/auth/login"  # Replace with actual URL

# Open the website
driver.get(url)
driver.maximize_window()

# Test case ID: TC_Login_01 - Successful Employee Login
def test_login_successful():
    try:
        driver.get(url)
        driver.find_element(By.ID, "txtUsername").send_keys("Admin")  # Replace with actual username field ID
        driver.find_element(By.ID, "txtPassword").send_keys("admin123")  # Replace with actual password field ID
        driver.find_element(By.ID, "btnLogin").click()  # Replace with actual login button ID

        # Wait until the dashboard page is loaded
        WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
        print("Login successful - Test Passed")
    except Exception as e:
        print("Login successful - Test Failed", e)

# Test case ID: TC_Login_02 - Invalid Employee Login
def test_login_invalid():
    try:
        driver.get(url)
        driver.find_element(By.ID, "txtUsername").send_keys("Admin")  # Replace with actual username field ID
        driver.find_element(By.ID, "txtPassword").send_keys("invalidPassword")  # Replace with actual password field ID
        driver.find_element(By.ID, "btnLogin").click()  # Replace with actual login button ID

        # Check for invalid login message
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "spanMessage"))  # Replace with actual error message ID
        ).text
        assert error_message == "Invalid credentials", "Test Failed: Unexpected error message"
        print("Invalid login - Test Passed")
    except Exception as e:
        print("Invalid login - Test Failed", e)

# Test case ID: TC_PIM_01 - Add a new employee in the PIM module
def test_add_employee():
    try:
        # Log in first (assume login was successful)
        test_login_successful()
        
        # Navigate to PIM module
        driver.find_element(By.ID, "menu_pim_viewPimModule").click()  # Replace with actual PIM menu ID
        driver.find_element(By.ID, "btnAdd").click()  # Replace with actual "Add" button ID
        
        # Fill in employee details
        driver.find_element(By.ID, "firstName").send_keys("John")  # Replace with actual first name field ID
        driver.find_element(By.ID, "lastName").send_keys("Doe")  # Replace with actual last name field ID
        driver.find_element(By.ID, "btnSave").click()  # Replace with actual save button ID
        
        # Confirm successful addition
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "successMessage"))  # Replace with actual success message ID
        ).text
        assert "Successfully Saved" in success_message, "Test Failed: Employee addition was unsuccessful"
        print("Add employee - Test Passed")
    except Exception as e:
        print("Add employee - Test Failed", e)

# Test case ID: TC_PIM_02 - Edit an existing employee in the PIM module
def test_edit_employee():
    try:
        # Log in and navigate to PIM module
        test_login_successful()
        driver.find_element(By.ID, "menu_pim_viewPimModule").click()
        
        # Select an employee from the list and click Edit
        driver.find_element(By.XPATH, "//a[text()='John Doe']").click()  # Replace with actual employee name link
        driver.find_element(By.ID, "btnSave").click()
        
        # Edit employee details
        driver.find_element(By.ID, "middleName").clear()
        driver.find_element(By.ID, "middleName").send_keys("Michael")  # Replace with actual middle name field ID
        driver.find_element(By.ID, "btnSave").click()
        
        # Confirm successful edit
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "successMessage"))
        ).text
        assert "Successfully Saved" in success_message, "Test Failed: Employee edit was unsuccessful"
        print("Edit employee - Test Passed")
    except Exception as e:
        print("Edit employee - Test Failed", e)

# Test case ID: TC_PIM_03 - Delete an existing employee in the PIM module
def test_delete_employee():
    try:
        # Log in and navigate to PIM module
        test_login_successful()
        driver.find_element(By.ID, "menu_pim_viewPimModule").click()
        
        # Select an employee checkbox and delete
        driver.find_element(By.XPATH, "//a[text()='John Doe']/../preceding-sibling::td/input").click()
        driver.find_element(By.ID, "btnDelete").click()
        
        # Confirm deletion in dialog
        driver.find_element(By.ID, "dialogDeleteBtn").click()  # Replace with actual confirm delete button ID

        # Confirm successful deletion
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "successMessage"))
        ).text
        assert "Successfully Deleted" in success_message, "Test Failed: Employee deletion was unsuccessful"
        print("Delete employee - Test Passed")
    except Exception as e:
        print("Delete employee - Test Failed", e)

# Run test cases
test_login_successful()
test_login_invalid()
test_add_employee()
test_edit_employee()
test_delete_employee()

# Close the browser
driver.quit()
