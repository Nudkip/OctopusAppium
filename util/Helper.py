# coding=utf-8
from appium import webdriver
from py.xml import html as pyhtml
import pytest
import os
import time
import shutil, sys   
import logging
from time import sleep
import base64
from io import BytesIO
import inspect
from PIL import Image
from pathlib import Path
import sys
import configparser

# sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "./utils"))))
# compare screenShot class
from VisualComparison import *
# screenShot Counter class
from ScreenShotCount import *

import Constant
from selenium.webdriver.support import expected_conditions as ec 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.webdriver import WebDriver

# generate html code
import dominate
from dominate.tags import *

logging.basicConfig(level=logging.CRITICAL)

diffFound = False

class Helper:
	@staticmethod
	def swipe_down(driver, start_x, start_y, end_x, end_y):
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
				Helper.swipe_down(driver, 200, 600, 200, 200)
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
				Helper.swipe_down(driver, 200, 600, 200, 200)
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
				Helper.swipe_down(driver, 200, 600, 200, 200)
		raise Exception("Element not found after max attempts")

	@staticmethod
	def captureScreenFYR(appium_driver,directory,screenShotCount, remarks):
		# statusBar = appium_driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStatusBar')

		# screenSize = appium_driver.get_window_size()
		sleep(1)
		reminder = str(screenShotCount.getCounter())+ '_' + remarks
		# print(reminder)
		basePath = str(directory)[:-len(str(time.strftime("%Y%m%d_%H_%M")))-1] + 'Source/' + pytest.global_device + '/'
		baseScreenShotPath = basePath + str(screenShotCount.getCounter()) +'_'+ remarks +'.png'
		testingScreenShotPath = directory + str(screenShotCount.getCounter()) +'_'+ remarks +'.png'
		appium_driver.save_screenshot(testingScreenShotPath)
		print(testingScreenShotPath)

		# screenshotImage = Image.open(testingScreenShotPath)
		# screenshotImageWidth, screenshotImageHeight = screenshotImage.size
		# scaleRate = screenshotImageWidth/screenSize['width']

		# resized = (0, \
		# 	statusBar.size.get("height") * scaleRate, \
		# 		screenSize['width'] *scaleRate, \
		# 			(screenSize['height'] * scaleRate))

		# croppedScreenshotImage = screenshotImage.crop(resized)
		# croppedScreenshotImage.save(testingScreenShotPath)

		dic = {Constant.TESTING_METHOD:reminder,\
			Constant.BASE_SCREEN_SHOT:baseScreenShotPath,\
				Constant.TESTING_SCREENSHOT:testingScreenShotPath,\
					Constant.DIFF:""}
		# compareArray.append(dic)

		screenShotCount.setCounter(screenShotCount.getCounter()+1)

	@staticmethod
	def createDirectory(className, methodName):
		directory = '%s/test/%s/%s/%s/%s/' % (os.path.dirname(__file__),Constant.SCREEN_SHOT, className , methodName, time.strftime("%Y%m%d_%H_%M"))
		
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