from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
from selenium.webdriver.support.ui import WebDriverWait


from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#from util.Helper import *
#from util.ScreenShotCount import * 
from checking import *

# Appium server URL
APPIUM_SERVER_URL = "http://127.0.0.1:4723" # Default Appium server port

def setup_appium_driver():
  
    options = UiAutomator2Options()
    

    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("platformName", "Android")
    options.set_capability("platformVersion", "14")
    options.set_capability("deviceName", "R3CWA03FA0K") 
    options.set_capability("appPackage", "com.octopuscards.nfc_reader")
    options.set_capability("appActivity", "com.octopuscards.nfc_reader.ui.login.activities.OctopusFullLoginActivity")
    # ==========================

    # Optional capability: maximum duration (in milliseconds) to wait for the app to launch
    options.set_capability("appWaitDuration", 30000) # Wait 30 seconds for the app to launch

    print(f"Connecting to Appium server: {APPIUM_SERVER_URL}")
    print(f"Capabilities being used: {options.capabilities}")

    driver = None
    try:
        driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
        
        # Set an implicit wait, so it waits for elements to appear for a certain period
        driver.implicitly_wait(10) # Wait up to 10 seconds to find elements

        print("Appium Android driver initialized successfully!")
        print(f"Session ID: {driver.session_id}")
        print(f"Current Context: {driver.context}") # Usually NATIVE_APP

        # Simple interaction example: wait a few seconds, then close the app
        print("Specified app opened, will remain open for 5 seconds...")
        time.sleep(5) 
        
        return driver

    except Exception as e:
        print(f"Error initializing Appium driver: {e}")
        print("Please confirm the following:")
        print("1. Is the Appium server running at 'http://127.0.0.1:4723'?")
        print(f"2. Is device '{options.get_capability('deviceName')}' connected and recognized by ADB?")
        print(f"3. Is device '{options.get_capability('deviceName')}' running platform version '{options.get_capability('platformVersion')}'?")
        print(f"4. Are the app package name '{options.get_capability('appPackage')}' and activity name '{options.get_capability('appActivity')}' correct?")
        print("   (If the app is not installed, or the package/activity name is wrong, it may cause launch failure)")
        if driver:
            driver.quit() # If an error occurs, try to close the driver
        return None

def tear_down_driver(driver):
    """Closes the Appium driver."""
    if driver:
        print("Closing Appium driver...")
        driver.quit()
        print("Appium driver closed.")
    else:
        print("Driver not initialized, no need to close.")

# Main execution block
if __name__ == "__main__":
    driver = None
    try:
        driver = setup_appium_driver()
        if driver:
            print("Appium session executed successfully!")
            time.sleep(1)  # Wait for the app to load
            wait = WebDriverWait(driver, 2)
            sign_in_button = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@resource-id, 'sign_in_btn_layout')]")))
            sign_in_button.click()
            time.sleep(2)  # Wait for the sign-in process to complete
            el = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            el[0].click()
            el[0].send_keys("99000067")
            if len(el) > 1:
                print("Captral is disable password is needed")
                el[1].click()
                el[1].send_keys("aaaa1111")
            else:
                print("Captral is enable, not able to proceed")

            login_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@resource-id, 'login_button')]")
            login_button.click()
            try:
                CommonChecking.check_snackbar(driver)
            except Exception as e: 
                print(f"An error occurred while checking for snackbar: {e}")

            
            # You can add your test operations here, e.g., clicking buttons, entering text
            # Example: If you know an element's ID or accessibility ID in your app
            # try:
            #     some_element = driver.find_element("accessibility id", "Some Button Text")
            #     some_element.click()
            #     print("Successfully clicked an element.")
            #     time.sleep(2)
            # except Exception as e:
            #     print(f"Could not find or click element: {e}")

    finally:
        tear_down_driver(driver)
        print("Script execution finished.")

"""

venvjeffreychan@jeffreys-MacBook-Air OctopusAppium % python3 ./test_setup_App_Android/test_1.py
Connecting to Appium server: http://127.0.0.1:4723
Capabilities being used: {'automationName': 'UIAutomator2', 'platformName': 'Android', 'appium:automationName': 'UiAutomator2', 'appium:platformVersion': '14', 'appium:deviceName': 'R3CWA03FA0K', 'appium:appPackage': 'com.octopuscards.nfc_reader', 'appium:appActivity': 'com.octopuscards.nfc_reader.ui.login.activities.OctopusFullLoginActivity', 'appium:appWaitDuration': 30000}
Appium Android driver initialized successfully!
Session ID: 230a223b-3fe3-4eab-8966-fbae5ab173d2
Current Context: NATIVE_APP
Specified app opened, will remain open for 5 seconds...
Appium session executed successfully!
Closing Appium driver...
Appium driver closed.
Script execution finished.
"""
