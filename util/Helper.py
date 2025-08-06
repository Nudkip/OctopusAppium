# coding=utf-8
import pytest
import os
import time
import shutil, sys   
import logging
from time import sleep
import base64
from PIL import Image
from pathlib import Path
import sys

from .VisualComparison import VisualComparison
from .Constant import Constant

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.actions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import *
from functools import cache

# generate html code
from appium.webdriver import * 
from dominate.tags import *

logging.basicConfig(level=logging.CRITICAL)

from typing import Dict, Optional


class Helper:
	# _instance = None

	# def __new__(cls, *args, **kwargs):
	# 	if cls._instance is None:
	# 		cls._instance = super().__new__(cls)
	# 	return cls._instance

	def __init__(self):
		self.id = id(self)
		self.compareArray = []
		self.diffFound = False
		self.driver = webdriver

	def add_to_compare_array(self, dic):
		self.compareArray.append(dic)

	def get_compare_array(self):
		return self.compareArray

	def clear_compare_array(self):
		return self.compareArray.clear

	@staticmethod
	def tap(driver, start_x, start_y):
		actions = ActionChains(driver)

		# Add a pointer input of type 'touch'
		finger = actions.w3c_actions.add_pointer_input('touch', 'finger')

		# Move to the specified coordinates (relative to the viewport)
		finger.create_pointer_move(x=int(start_x), y=int(start_y), origin='viewport')

		# Simulate the tap action (pointer down and pointer up)
		finger.create_pointer_down(button=0)
		finger.create_pointer_up(button=0)

		# Execute the action
		actions.perform()

	@staticmethod
	def swipe(driver, start_x, start_y, end_x, end_y):
		# Determine actual coordinates to use
		_start_x, _start_y, _end_x, _end_y = 0,0,0,0

		# If start_x is None, assume a generic swipe to scroll content down
		# (finger moves from a lower y to a higher y on screen).
		if start_x is None:
			size = driver.get_window_size()
			width = size['width']
			height = size['height']
			_start_x = width // 2
			_start_y = int(height * 0.6) # Start lower on screen
			_end_x = width // 2
			_end_y = int(height * 0.4)   # End higher on screen (finger moves up)
		else:
			# Use provided coordinates
			_start_x = start_x
			_start_y = start_y
			_end_x = end_x
			_end_y = end_y
		# Corrected swipe implementation using W3C Actions
		actions = ActionChains(driver)
		finger = actions.w3c_actions.add_pointer_input('touch', 'finger')
		finger.create_pointer_move(x=int(_start_x), y=int(_start_y), duration=0, origin='viewport')
		finger.create_pointer_down(button=0)
		finger.create_pause(0.1) 
		finger.create_pointer_move(x=int(_end_x), y=int(_end_y), duration=250, origin='viewport')
		finger.create_pointer_up(button=0)
		
		actions.perform()

	@staticmethod
	def scroll_until_elementXPATH_found(driver, xpath, max_attempts=5):
		attempt_timeout = 3  # seconds
		for i in range(max_attempts):
			try:
				element = WebDriverWait(driver, attempt_timeout).until(
					EC.element_to_be_clickable((By.XPATH, xpath))
				)
				print(f"scroll_until_elementXPATH_found: Element '{xpath}' found and clickable in attempt {i + 1}.")
				return element
			except TimeoutException:
				print(f"scroll_until_elementXPATH_found: Element '{xpath}' not visible/clickable within {attempt_timeout}s (attempt {i + 1}/{max_attempts}). Swiping down.")
				if i < max_attempts - 1:
					Helper.swipe(driver, None, None, None, None) # Use generic swipe
		raise Exception(f"Element with XPATH '{xpath}' not found or not clickable after {max_attempts} attempts with {attempt_timeout}s timeout per attempt.")

	@staticmethod
	def scroll_until_iOSPredicateString_element_found(driver, predicateString, max_attempts=5):
		attempt_timeout = 3  # seconds
		for i in range(max_attempts):
			try:
				element = WebDriverWait(driver, attempt_timeout).until(
					EC.element_to_be_clickable((AppiumBy.IOS_PREDICATE, predicateString))
				
				)
				print(f"scroll_until_iOSPredicateString_element_found: Element '{predicateString}' found and clickable in attempt {i + 1}.")
				return element
			except TimeoutException:
				print(f"scroll_until_iOSPredicateString_element_found: Element '{predicateString}' not visible/clickable within {attempt_timeout}s (attempt {i + 1}/{max_attempts}). Swiping down.")
				if i < max_attempts - 1:
					Helper.swipe(driver, None, None, None, None) # Use generic swipe
		raise Exception(f"Element with iOS Predicate String '{predicateString}' not found or not clickable after {max_attempts} attempts with {attempt_timeout}s timeout per attempt.")

	@staticmethod
	def scroll_until_accessibilityID_element_found(driver, ID, max_attempts=5):
		attempt_timeout = 3  # seconds
		for i in range(max_attempts):
			try:
				element = WebDriverWait(driver, attempt_timeout).until(
					EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, ID))
				)
				print(f"scroll_until_accessibilityID_element_found: Element '{ID}' found and clickable in attempt {i + 1}.")
				return element
			except TimeoutException:
				print(f"scroll_until_accessibilityID_element_found: Element '{ID}' not visible/clickable within {attempt_timeout}s (attempt {i + 1}/{max_attempts}). Swiping down.")
				if i < max_attempts - 1:
					Helper.swipe(driver, None, None, None, None) # Use generic swipe
		raise Exception(f"Element with Accessibility ID '{ID}' not found or not clickable after {max_attempts} attempts with {attempt_timeout}s timeout per attempt.")

	@staticmethod
	def scroll_until_elementID_found(driver, ID, max_attempts=5):
		attempt_timeout = 3  # seconds
		for i in range(max_attempts):
			try:
				element = WebDriverWait(driver, attempt_timeout).until(
					EC.element_to_be_clickable((By.ID, ID))
				)
				print(f"scroll_until_elementID_found: Element '{ID}' found and clickable in attempt {i + 1}.")
				return element
			except TimeoutException:
				print(f"scroll_until_elementID_found: Element '{ID}' not visible/clickable within {attempt_timeout}s (attempt {i + 1}/{max_attempts}). Swiping down.")
				if i < max_attempts - 1:
					Helper.swipe(driver, None, None, None, None) # Use generic swipe
		raise Exception(f"Element with ID '{ID}' not found or not clickable after {max_attempts} attempts with {attempt_timeout}s timeout per attempt.")

	@staticmethod
	def scroll_until_appiumBY_found(driver, appiumBy, max_attempts=5):
		# Define a timeout for each attempt to find the element before scrolling
		attempt_timeout = 3  # seconds
		for i in range(max_attempts):
			try:
				# EC.element_to_be_clickable checks for both visibility and enabled state.
				# It returns the element if the condition is met.
				element = WebDriverWait(driver, attempt_timeout).until(
					EC.element_to_be_clickable((AppiumBy.IOS_CLASS_CHAIN, appiumBy))
				)
				print(f"scroll_until_appiumBY_found: Element '{appiumBy}' found and clickable in attempt {i + 1}.")
				return element
			except TimeoutException:
				print(f"scroll_until_appiumBY_found: Element '{appiumBy}' not visible/clickable within {attempt_timeout}s (attempt {i + 1}/{max_attempts}). Swiping down.")
				if i < max_attempts - 1:  # Avoid swiping on the last attempt before raising the final exception
					Helper.swipe(driver, None, None, None, None) # Use generic swipe
		# If the loop finishes without returning, the element was not found.
		raise Exception(f"Element '{appiumBy}' not found or not clickable after {max_attempts} attempts with {attempt_timeout}s timeout per attempt.")

	@staticmethod
	def scroll_until_text_element_found(driver, text: str, max_attempts: int = 5) -> Optional:
		"""
		Scrolls until a TextView with the specified text is found and clickable.
		
		Args:
			driver: Appium WebDriver instance.
			text: Text attribute of the TextView to locate.
			max_attempts: Maximum number of scroll attempts.
		
		Returns:
			WebElement if found and clickable, None otherwise.s
		"""
		attempt_timeout = 1  # seconds
		for i in range(max_attempts):
			try:
				element = WebDriverWait(driver, attempt_timeout).until(
					EC.element_to_be_clickable((AppiumBy.XPATH, f"//android.widget.TextView[@text='{text}']"))
				)
				print(f"scroll_until_text_element_found: Element with text '{text}' found and clickable in attempt {i + 1}.")
				return element
			except TimeoutException:
				print(f"scroll_until_text_element_found: Element with text '{text}' not visible/clickable within {attempt_timeout}s (attempt {i + 1}/{max_attempts}). Swiping down.")
				if i < max_attempts - 1:
					# Use shorter swipe for precision
					size = driver.get_window_size()
					width = size['width']
					height = size['height']
					Helper.swipe(driver, None, None, None, None) # Use generic swipe
		
		# Log all TextView texts for debugging
		try:
			text_views = driver.find_elements(AppiumBy.XPATH, "//android.widget.TextView")
			texts = [tv.get_attribute("text") for tv in text_views if tv.get_attribute("text")]
			print(f"scroll_until_text_element_found: Available TextView texts: {texts}")
		except Exception as e:
			print(f"scroll_until_text_element_found: Error listing TextView texts: {str(e)}")
		
		print(f"scroll_until_text_element_found: Element with text '{text}' not found after {max_attempts} attempts.")
		return None



	def captureScreenFYR(self, appium_driver, directory, screenShotCount, remarks):
		screenSize = appium_driver.get_window_size()
		sleep(2)
		reminder = str(screenShotCount.getCounter()) + '_' + remarks
		basePath = str(directory)[:-len(str(time.strftime("%Y%m%d_%H_%M")))-1] + 'Source/' + pytest.global_device + '/'
		print(basePath)

		baseScreenShotPath = basePath + str(screenShotCount.getCounter()) + '_' + remarks + '.png'
		testingScreenShotPath = directory + str(screenShotCount.getCounter()) + '_' + remarks + '.png'
		
		# Save the screenshot
		appium_driver.save_screenshot(testingScreenShotPath)
		print(testingScreenShotPath)

		# Open the screenshot
		screenshotImage = Image.open(testingScreenShotPath)

		# Resize the image to 20%
		new_width = int(screenshotImage.width * 0.2)
		new_height = int(screenshotImage.height * 0.2)
		resizedImage = screenshotImage.resize((new_width, new_height))

		# Calculate the scaled top 40 pixels based on the screen size ratio
		scaleRate = new_height / screenSize['height']
		scaled_top = int(40 * scaleRate)

		# Define the crop area (left, upper, right, lower)
		crop_area = (0, scaled_top, new_width, new_height)  # Crop based on scaled top

		# Crop the resized image
		croppedScreenshotImage = resizedImage.crop(crop_area)
		
		# Save the cropped image
		croppedScreenshotImage.save(testingScreenShotPath)

		# Prepare the dictionary for comparison
		dic = {
			Constant.TESTING_METHOD: reminder,
			Constant.BASE_SCREEN_SHOT: baseScreenShotPath,
			Constant.TESTING_SCREENSHOT: testingScreenShotPath,
			Constant.DIFF: ""
		}
		
		# Use the Helper instance to add to compareArray
		self.add_to_compare_array(dic)

		# Update the screenshot counter
		screenShotCount.setCounter(screenShotCount.getCounter() + 1)

	@staticmethod
	def createDirectory(className, methodName):
		directory = '%s/../testResult/%s/%s/%s/%s/' % (os.path.dirname(__file__),Constant.SCREEN_SHOT, className , methodName, time.strftime("%Y%m%d_%H_%M"))
		
		if (os.path.isdir(directory)) :
			print('\n%s %s' % (directory, 'is existing'))
			try:
				# remove all screen caps in directory
				shutil.rmtree(directory)
				os.makedirs(directory, 0o755)
				print('\n%s %s' % (directory, 'all screen caps are removed'))
			except Exception as e:
				print('\n%s shutil.rmtreeError: %s' % (directory, e))
		else:
			print('\n%s %s' % (directory, 'is not existing'))
			try:
				# create a directory to store screen cap
				os.makedirs( directory, 0o755 )
				print('%s %s' % (directory, 'is created'))
			except Exception as e:
				print('\n%s mkdirError: %s' % (directory, e))
		return directory	

	@staticmethod
	def convertpngToBase64Html(imagePath):
		encodedImage = base64.b64encode(open(imagePath, "rb").read()).decode('ascii')
		return 'data:image/png;base64,%s' % encodedImage

	def createVisualComparisonTable(self):# The above code snippet is creating a visual comparison table for
	# comparing screenshots. It iterates through a list of
	# dictionaries called `compareArray`, where each dictionary
	# contains information about testing and base screenshots.


		print("createVisualComparisonTable")

		for dictionary in self.compareArray:
			dictionary['Diff'] = VisualComparison().analyze(dictionary['TestingScreenShot'], dictionary['BaseScreenShot'])

		td1 = td("Testing Method (Screenshot Name)" ,style= "width:150px")
		td2 = td(Constant.BASE_SCREEN_SHOT ,style= "width:240px")
		td3 = td(Constant.TESTING_SCREENSHOT,style= "width:240px")
		td4 = td(Constant.DIFF,style= "width:240px")
		tr1 = tr(td1, td2, td3, td4)
		table1 = table(tr1, align = "center", border="1")
		for dictionary in self.compareArray:
			trow = tr()
			tdName = td(dictionary[Constant.TESTING_METHOD] ,style= "width:150px")
			# Set max-width and max-height to ensure aspect fit
			tdBaseScreenShot = td(img(style="max-width:240px; max-height:480px;", src=Helper().convertpngToBase64Html(dictionary[Constant.BASE_SCREEN_SHOT])))
			tdTestingScreenShot = td(img(style="max-width:240px; max-height:480px;", src=Helper().convertpngToBase64Html(dictionary[Constant.TESTING_SCREENSHOT])))
			if dictionary[Constant.DIFF] is not None:
				tdDiff = td(img(style="max-width:240px; max-height:480px;", src=Helper().convertpngToBase64Html(dictionary["Diff"])))
				trow = tr(tdName, tdBaseScreenShot, tdTestingScreenShot, tdDiff, bgcolor="#fff200")
			else:
				tdDiff = td(font("✅",size = "20" ) , style="max-width:240px; max-height:480px;" , align= "center")
				trow = tr(tdName, tdBaseScreenShot, tdTestingScreenShot, tdDiff)
			table1.add(trow)

		p1 = p(table1)
		# reset array
		self.compareArray = []
		return str(p1)
###########################ANDROID HELPER########################################
	@staticmethod
	def is_app_alive_reliable(driver, package_name):
		"""
		Reliably checks if an app is alive based on its state.
		- Returns True if the app is running in the foreground.
		- If the app is running in the background (state code 2 or 3), it automatically
		  brings it to the foreground and returns True.
		- Returns False if the app is not running, not installed, or an error occurs.

		App State Codes:
		- 0: Not installed.
		- 1: Not running.
		- 2: Running in the background or suspended.
		- 3: Running in the background.
		- 4: Running in the foreground.

		Returns:
		- True: The app is running (and is brought to the foreground if needed).
		- False: The app is not running, not installed, or an error occurred.
		"""
		try:
			app_state = driver.query_app_state(package_name)

			if app_state == 4:  # App is running in the foreground
				print(f"App '{package_name}' is already running in the foreground.")
				return True

			elif app_state in [2, 3]:  # App is running in the background
				print(f"App '{package_name}' is running in the background. Bringing it to the foreground...")
				driver.activate_app(package_name)
				# Wait a few seconds to ensure the app has fully resumed
				time.sleep(3)
				print(f"App '{package_name}' has been successfully brought to the foreground.")
				return True

			elif app_state == 1:  # App is not running
				print(f"App '{package_name}' is not running.")
				return False

			elif app_state == 0:  # App is not installed
				print(f"App '{package_name}' is not installed.")
				return False

			else:  # Unknown state
				print(f"App '{package_name}' is in an unknown state (code: {app_state}).")
				return False

		except Exception as e:
			# An exception often indicates that the connection to the app was lost,
			# which is a strong sign that the app has terminated.
			print(f"An error occurred while checking app state: {e}")
			return False

	@staticmethod
	def handle_permissions(driver):
		"""
		Locates the Android permission dialog and clicks the 'Allow' button.
		This function handles multiple languages and will not fail if the dialog is not present.
		
		Args:
			driver: The Appium WebDriver instance.
		"""
		try:
			# 1. Define locators for the dialog and the allow button
			permission_dialog_id = "com.android.permissioncontroller:id/grant_dialog"
			allow_button_id = "com.android.permissioncontroller:id/permission_allow_button"
			
			# 2. Use WebDriverWait to wait for the dialog to appear.
			# Use a short timeout since it usually appears quickly.
			wait = WebDriverWait(driver, 5)
			wait.until(EC.presence_of_element_located((AppiumBy.ID, permission_dialog_id)))
			print("Permission dialog located by ID.")

			# 3. Attempt to find and click the 'Allow' button by its ID.
			try:
				allow_button = driver.find_element(AppiumBy.ID, allow_button_id)
				allow_button.click()
				print("Clicked the 'Allow' button by ID.")
			except NoSuchElementException:
				# 4. Fallback if the button ID is not found.
				# This handles cases where the text might be different or the ID is missing.
				print("Could not find 'Allow' button by ID. Attempting to locate by text.")
				allow_button_locators = [
					AppiumBy.XPATH, "//*[contains(@text, 'Allow') or contains(@text, '允許') or contains(@text, '允许')]"
				]
				allow_button = driver.find_element(*allow_button_locators)
				allow_button.click()
				print("Clicked the 'Allow' button by text.")
			# 5. Add a small pause after clicking to let the dialog disappear
			time.sleep(1)

		except (NoSuchElementException, TimeoutException):
			print("Permission dialog or 'Allow' button was not found. Continuing test.")
		except Exception as e:
			print(f"An unexpected error occurred while handling permissions: {e}")

	@staticmethod
	def extract_setting_attributes(driver) -> Dict[str, Optional[str]]:
		"""
		Extracts UI attributes from an Android app using Appium by locating attribute names
		and capturing the values of subsequent input elements (Spinner, RadioGroup, EditText).
		
		Args:
			driver: Appium WebDriver instance.
		
		Returns:
			Dict[str, Optional[str]]: Dictionary containing mapped attributes and their values.
		"""
		# Initialize the result dictionary
		attributes = {
			"OCL Host": None,
			"OCL War": None,
			"OOS Host": None,
			"OOS Path": None,
			"PTS Host": None,
			"Webserver Host": None,
			"Captcha": None,
			"Check Root": None,
			"Loyalty Host": None,
			"AO Host": None,
			"AO Is Submit Log": None
		}
		
		try:
			# Initialize WebDriverWait
			wait = WebDriverWait(driver, 3)  # 3-second timeout for initial attempt
			
			# Define attribute names to locate
			attribute_names = list(attributes.keys())
			
			for attr_name in attribute_names:
				try:
					# Try to find the TextView immediately
					try:
						text_view = wait.until(
							EC.presence_of_element_located((AppiumBy.XPATH, f"//android.widget.TextView[@text='{attr_name}']"))
						)
						if text_view.is_displayed():
							print(f"Immediate find: Element with text '{attr_name}' found and fully visible.")
						else:
							print(f"Immediate find: Element with text '{attr_name}' found but not fully visible. Attempting to scroll.")
							text_view = Helper.scroll_until_text_element_found(driver, attr_name)
							if not text_view:
								print(f"Error: TextView for '{attr_name}' not found after scrolling.")
								attributes[attr_name] = None
								continue
					except TimeoutException:
						print(f"Immediate find: Element with text '{attr_name}' not found. Attempting to scroll.")
						text_view = Helper.scroll_until_text_element_found(driver, attr_name)
						if not text_view:
							print(f"Error: TextView for '{attr_name}' not found after scrolling.")
							attributes[attr_name] = None
							continue
					
					# Determine the input element type and locate the next input element
					if attr_name == "OOS Path":
						try:
							input_element = driver.find_element(
								AppiumBy.XPATH,
								f"//android.widget.TextView[@text='{attr_name}']/preceding-sibling::android.widget.EditText[1]"
							)
							attributes[attr_name] = input_element.get_attribute("text") or "Empty"
						except Exception as e:
							print(f"Error locating EditText for '{attr_name}': {str(e)}")
							attributes[attr_name] = None
					
					elif attr_name in ["Captcha", "Check Root", "AO Is Submit Log"]:
						try:
							radio_group = driver.find_element(
								AppiumBy.XPATH,
								f"//android.widget.TextView[@text='{attr_name}']/following-sibling::android.widget.RadioGroup[1]"
							)
							selected_radio = radio_group.find_element(
								AppiumBy.XPATH,
								".//android.widget.RadioButton[@checked='true']"
							)
							attributes[attr_name] = selected_radio.get_attribute("text")
						except Exception as e:
							print(f"Error locating RadioGroup or selected RadioButton for '{attr_name}': {str(e)}")
							attributes[attr_name] = None
					
					else:
						try:
							spinner = driver.find_element(
								AppiumBy.XPATH,
								f"//android.widget.TextView[@text='{attr_name}']/following-sibling::android.widget.Spinner[1]"
							)
							selected_item = spinner.find_element(
								AppiumBy.XPATH,
								".//android.widget.CheckedTextView"
							)
							attributes[attr_name] = selected_item.get_attribute("text")
						except Exception as e:
							print(f"Error locating Spinner or selected item for '{attr_name}': {str(e)}")
							attributes[attr_name] = None
				
				except Exception as e:
					print(f"Error processing '{attr_name}': {str(e)}")
					attributes[attr_name] = None
			
			return attributes
		
		except Exception as e:
			print(f"Error extracting attributes: {str(e)}")
			return attributes

	@staticmethod
	def set_Backend_attributes(driver, attributes_json: Dict[str, str]) -> Dict[str, Optional[str]]:
		"""
		Sets UI attributes in an Android app using Appium based on a JSON input.
		Radio button attributes are set by selecting the corresponding RadioButton.
		Other attributes are set by selecting values from a ListView within a Spinner.
		Scrolls the ListView if the value is not found, returning an error if not found after reaching the bottom.
		
		Args:
			driver: Appium WebDriver instance.
			attributes_json: Dictionary of attribute names and desired values.
		
		Returns:
			Dict[str, Optional[str]]: Dictionary with attribute names as keys and success/error messages as values.
		"""
		# Initialize result dictionary
		result = {attr: None for attr in attributes_json.keys()}
		
		try:
			for attr_name, attr_value in attributes_json.items():
				try:
					# Locate the TextView label
					text_view = Helper.scroll_until_text_element_found(driver, attr_name)
					if not text_view:
						result[attr_name] = f"Error: TextView for '{attr_name}' not found after scrolling."
						continue
					
					# Handle radio button attributes
					if attr_name in ["Captcha", "Check Root", "AO Is Submit Log"]:
						try:
							radio_group = driver.find_element(
								AppiumBy.XPATH,
								f"//android.widget.TextView[@text='{attr_name}']/following-sibling::android.widget.RadioGroup[1]"
							)
							radio_button = radio_group.find_element(
								AppiumBy.XPATH,
								f".//android.widget.RadioButton[@text='{attr_value}']"
							)
							if not radio_button.is_selected():
								radio_button.click()
								time.sleep(0.5)  # Wait for UI update
								print(f"set_Backend_attributes: Selected RadioButton '{attr_value}' for '{attr_name}'.")
							else:
								print(f"set_Backend_attributes: RadioButton '{attr_value}' for '{attr_name}' already selected.")
							result[attr_name] = f"Success: Set to '{attr_value}'."
						except Exception as e:
							print(f"set_Backend_attributes: Error setting RadioButton for '{attr_name}': {str(e)}")
							result[attr_name] = f"Error: Failed to set '{attr_value}' - {str(e)}"
					
					# Handle Spinner (ListView) attributes
					else:
						try:
							spinner = driver.find_element(
								AppiumBy.XPATH,
								f"//android.widget.TextView[@text='{attr_name}']/following-sibling::android.widget.Spinner[1]"
							)
							spinner.click()
							print(f"set_Backend_attributes: Tapped Spinner for '{attr_name}'.")
							time.sleep(1)  # Wait for ListView to open
							
							# Scroll and select value in ListView
							max_scroll_attempts = 5
							for attempt in range(max_scroll_attempts):
								try:
									checked_text_view = driver.find_element(
										AppiumBy.XPATH,
										f"//android.widget.ListView//android.widget.CheckedTextView[@text='{attr_value}']"
									)
									checked_text_view.click()
									time.sleep(0.5)  # Wait for selection
									print(f"set_Backend_attributes: Selected '{attr_value}' for '{attr_name}' in attempt {attempt + 1}.")
									result[attr_name] = f"Success: Set to '{attr_value}'."
									break
								except Exception:
									if attempt < max_scroll_attempts - 1:
										try:
											list_view = driver.find_element(AppiumBy.XPATH, "//android.widget.ListView")
											bounds = list_view.get_attribute("bounds")
											# Parse bounds: [x1,y1][x2,y2]
											x1, y1, x2, y2 = map(int, bounds.strip("[]").replace("][", ",").split(","))
											# Swipe within ListView: from 75% to 25% of height
											start_y = y1 + int((y2 - y1) * 0.75)
											end_y = y1 + int((y2 - y1) * 0.25)
											center_x = (x1 + x2) // 2
											# Check for bottom of ListView
											initial_content = driver.page_source
											Helper.swipe(driver, center_x, start_y, center_x, end_y)
											time.sleep(1)  # Wait for scroll
											new_content = driver.page_source
											if new_content == initial_content:
												print(f"set_Backend_attributes: Reached bottom of ListView for '{attr_name}' in attempt {attempt + 1}.")
												result[attr_name] = f"Error: Value '{attr_value}' not found in ListView."
												break
											print(f"set_Backend_attributes: Scrolled ListView for '{attr_name}' in attempt {attempt + 1}.")
										except Exception as e:
											print(f"set_Backend_attributes: Error scrolling ListView for '{attr_name}': {str(e)}")
											result[attr_name] = f"Error: Failed to scroll ListView - {str(e)}"
											break
							else:
								result[attr_name] = f"Error: Value '{attr_value}' not found in ListView after {max_scroll_attempts} attempts."
						except Exception as e:
							print(f"set_Backend_attributes: Error setting Spinner for '{attr_name}': {str(e)}")
							result[attr_name] = f"Error: Failed to set '{attr_value}' - {str(e)}"
				
				except Exception as e:
					print(f"set_Backend_attributes: Error processing '{attr_name}': {str(e)}")
					result[attr_name] = f"Error: Failed to process '{attr_name}' - {str(e)}"
			
			return result
		
		except Exception as e:
			print(f"set_Backend_attributes: General error: {str(e)}")
			return result