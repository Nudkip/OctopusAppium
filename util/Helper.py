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
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import *
from functools import cache

# generate html code
from appium.webdriver import * 
from dominate.tags import *

logging.basicConfig(level=logging.CRITICAL)


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
		actions = ActionChains(driver)
		finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
		finger1.create_pointer_move(x=start_x, y=start_y)
		finger1.create_pointer_move(x=end_x, y=end_y)
		actions.perform()
	

	@staticmethod
	def scroll_until_element_found(driver, xpath, max_attempts=5):
		for _ in range(max_attempts):
			try:
				element = WebDriverWait(driver, 0.1).until(EC.visibility_of_element_located((By.XPATH, xpath)))
				print("Element found! %s" % xpath)
				return element
			except:
				print("Element not found, swiping down...")
				Helper().swipe(driver, 200, 600, 200, 200)
		raise Exception("Element not found after max attempts")

	@staticmethod
	def scroll_until_iOSPredicateString_element_found(driver, predicateString, max_attempts=5):
		for _ in range(max_attempts):
			try:
				element = WebDriverWait(driver, 0.1).until(EC.visibility_of_element_located((AppiumBy.IOS_PREDICATE, predicateString)))
				print("Element found! %s" % predicateString)
				return element
			except:
				print("Element not found, swiping down...")
				Helper().swipe(driver, 200, 600, 200, 200)
		raise Exception("Element not found after max attempts")

	@staticmethod
	def scroll_until_accessibilityID_element_found(driver, ID, max_attempts=5):
		for _ in range(max_attempts):
			try:
				element = WebDriverWait(driver, 0.1).until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, ID)))
				print("Element found! %s" % ID)
				return element
			except:
				print("Element not found, swiping down...")
				Helper().swipe(driver, 200, 600, 200, 200)
		raise Exception("Element not found after max attempts")

	@staticmethod
	def scroll_until_elementID_found(driver, id, max_attempts=5):
		for _ in range(max_attempts):
			try:
				element = WebDriverWait(driver, 0.1).until(EC.visibility_of_element_located((By.ID, id)))
				print("Element found! %s" % id)
				return element
			except:
				print("Element not found, swiping down...")
				Helper().swipe(driver, 200, 600, 200, 200)
		raise Exception("Element not found after max attempts")

	@staticmethod
	def scroll_until_appiumBY_found(driver, appiumBy, max_attempts=5):
		for _ in range(max_attempts):
			try:
				element = WebDriverWait(driver, 0.1).until(EC.visibility_of_element_located((AppiumBy.IOS_CLASS_CHAIN, appiumBy)))
				print("Element found! %s" % id)
				return element
			except:
				print("Element not found, swiping down...")
				Helper().swipe(driver, 200, 600, 200, 200)
		raise Exception("Element not found after max attempts")

	def captureScreenFYR(self, appium_driver, directory, screenShotCount, remarks):
		screenSize = appium_driver.get_window_size()
		sleep(1)
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

		# Resize the image to 50%
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
