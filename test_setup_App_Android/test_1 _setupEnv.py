import sys
import os

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)



from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
from selenium.webdriver.support.ui import WebDriverWait


from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from util.Helper import Helper
#from util.ScreenShotCount import * 
from checking import *

# Appium server URL
APPIUM_SERVER_URL = "http://127.0.0.1:4723" # Default Appium server port

def setup_appium_driver():
  


    options = UiAutomator2Options()
    

    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("platformName", "Android")
    options.set_capability("platformVersion", "14")
    options.set_capability("deviceName", "R3CWA07WE6R") 
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
        print("Specified app opened, will remain open for 3 seconds...")
        time.sleep(3) 
        
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

        app_settings = {
    'OCL Host': 'MARIO', 
    'OCL War': 'VC', 
    'OOS Host': 'INTEGRATION', 
    'OOS Path': 'WILDFLY_7201', 
    'PTS Host': 'UAT', 
    'Webserver Host': 'OCL_WEBSERVER', 
    'Captcha': 'Disable', 
    'Check Root': 'Disable', 
    'Loyalty Host': 'PRE_STAGE', 
    'AO Host': 'SIT', 
    'AO Is Submit Log': 'Enable'
        }
            
        driver = setup_appium_driver()
        if driver:
            print("Appium session executed successfully!")
            time.sleep(1)  # Wait for the app to load
            wait = WebDriverWait(driver, 2)
            skip_button = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@resource-id, 'skip_btn')]")))
            skip_button.click()
            time.sleep(3)  # Wait for the skip sign-in loading
            # Call the static method directly on the Helper class
            is_alive = Helper.is_app_alive_reliable(driver, "com.octopuscards.nfc_reader")
            print(f"Is app alive: {is_alive}")
            time.sleep(1)  # Wait for the skip sign-in loading
            Helper.handle_permissions(driver)
            start_button = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@resource-id, 'start_btn')]")))
            start_button.click()
            image_setting_button = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@resource-id, 'guideline_logo_imageview')]")))
            image_setting_button.click()
            App_Setting = Helper.set_Backend_attributes(driver,app_settings)
            print(f"App Setting: {App_Setting}")
            App_Setting = Helper.extract_setting_attributes(driver)
            print(f"App Setting: {App_Setting}")
            
    finally:
        tear_down_driver(driver)
        print("Script execution finished.")