# common_checking.py

import time
from typing import List, Tuple
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput

class CommonChecking:
    """
    A collection of common utility functions for Appium tests in Python.
    """

    def is_element_present(self, by: AppiumBy, locator: str, driver: AppiumDriver) -> bool:
        """
        Checks for the presence of an element on the screen.

        :param by: The method to locate the element (e.g., AppiumBy.ID).
        :param locator: The locator string.
        :param driver: The Appium driver instance.
        :return: True if the element is found, False otherwise.
        """
        try:
            driver.find_element(by, locator)
            return True
        except NoSuchElementException:
            return False

    def is_element_present_with_timeout(self, by: AppiumBy, locator: str, driver: AppiumDriver, timeout_in_seconds: int) -> bool:
        """
        Checks for the presence of an element, waiting up to a specified timeout.

        :param by: The method to locate the element.
        :param locator: The locator string.
        :param driver: The Appium driver instance.
        :param timeout_in_seconds: The maximum time to wait in seconds.
        :return: True if the element is found within the timeout, False otherwise.
        """
        end_time = time.time() + timeout_in_seconds
        while time.time() < end_time:
            try:
                driver.find_element(by, locator)
                return True  # Element found
            except NoSuchElementException:
                # Element not found, print message and wait
                print("Still waiting for the element to be present...")
                time.sleep(1)
        
        print(f"Timeout of {timeout_in_seconds} seconds exceeded. Element not found.")
        return False  # Timeout exceeded

    def check_snackbar(self, driver: AppiumDriver) -> None:
        """
        Finds the snackbar element and prints its text.

        :param driver: The Appium driver instance.
        """
        try:
            # Note: In Python, it's more common to use find_element with AppiumBy
            snackbar_element = driver.find_element(AppiumBy.XPATH, "//*[contains(@resource-id, 'snackbar_text')]")
            print(f"Snackbar text is: {snackbar_element.text}")
        except NoSuchElementException:
            print("No Snackbar found.")
        except Exception as e:
            print(f"An error occurred while checking for snackbar: {e}")

    def check_and_close_image_view_ad(self, driver: AppiumDriver) -> None:
        """
        Checks for an image view ad and clicks the collapse button if found.

        :param driver: The Appium driver instance.
        """
        try:
            # First, check if the ad image view is present
            driver.find_element(AppiumBy.XPATH, "//*[contains(@resource-id, 'image_view')]")
            print("Image view ADs found.")
            
            # If found, click the collapse button
            driver.find_element(AppiumBy.XPATH, "//*[contains(@resource-id, 'collapse_button')]").click()
            print("Closed ADs.")
        except NoSuchElementException:
            print("No image view ADs found.")
        except Exception as e:
            print(f"An error occurred while handling the ad: {e}")

    def is_app_in_foreground(self, package_name: str, driver: AppiumDriver) -> bool:
        """
        Checks if the current foreground activity belongs to the specified package.
        Note: This is an Android-specific method.

        :param package_name: The package name of the application.
        :param driver: The Appium driver instance.
        :return: True if the app is in the foreground, False otherwise.
        """
        try:
            current_package = driver.current_package
            return current_package == package_name
        except Exception as e:
            print(f"Could not get current package: {e}")
            # Fallback for some driver versions
            current_activity = driver.current_activity
            return package_name in current_activity


    def tap_multiple_times(self, driver: AppiumDriver, x: int, y: int, times: int, delay_millis: float) -> None:
        """
        Performs a tap action at a specific coordinate multiple times using W3C Actions.

        :param driver: The Appium driver instance.
        :param x: The x-coordinate.
        :param y: The y-coordinate.
        :param times: The number of times to tap.
        :param delay_millis: The delay in milliseconds between taps.
        """
        for i in range(times):
            print(f"Tapping at ({x}, {y}) - Repetition {i + 1}/{times}")
            
            # W3C Actions are the modern way to perform gestures
            actions = ActionChains(driver)
            finger = PointerInput(interaction.POINTER_TOUCH, "finger")
            
            # Create a sequence of actions for a single tap
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            actions.w3c_actions.pointer_action.pointer_down()
            # A brief pause to simulate a real tap
            actions.w3c_actions.pointer_action.pause(0.1) 
            actions.w3c_actions.pointer_action.pointer_up()
            
            # Perform the tap
            actions.perform()

            # Wait for the specified delay before the next tap
            if i < times - 1: # No need to wait after the last tap
                time.sleep(delay_millis / 1000.0)