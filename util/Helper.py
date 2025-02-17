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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.actions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from functools import cache

# generate html code
import dominate
from dominate.tags import *

logging.basicConfig(level=logging.CRITICAL)

diffFound = False

class Helper:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		self.id = id(self)
		self.compareArray = []

	def add_to_compare_array(self, dic):
		self.compareArray.append(dic)

	def get_compare_array(self):
		return self.compareArray

	def clear_compare_array(self):
		return self.compareArray.clear

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
				Helper().swipe_down(driver, 200, 600, 200, 200)
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
				Helper().swipe_down(driver, 200, 600, 200, 200)
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
				Helper().swipe_down(driver, 200, 600, 200, 200)
		raise Exception("Element not found after max attempts")

	def captureScreenFYR(self, appium_driver,directory, screenShotCount, remarks):
		screenSize = appium_driver.get_window_size()
		sleep(1)
		reminder = str(screenShotCount.getCounter())+ '_' + remarks
		# print(reminder)
		basePath = str(directory)[:-len(str(time.strftime("%Y%m%d_%H_%M")))-1] + 'Source/' + pytest.global_device + '/'
		print(basePath)

		baseScreenShotPath = basePath + str(screenShotCount.getCounter()) +'_'+ remarks +'.png'
		testingScreenShotPath = directory + str(screenShotCount.getCounter()) +'_'+ remarks +'.png'
		appium_driver.save_screenshot(testingScreenShotPath)
		print(testingScreenShotPath)

		screenshotImage = Image.open(testingScreenShotPath)
		screenshotImageWidth, screenshotImageHeight = screenshotImage.size
		scaleRate = screenshotImageWidth/screenSize['width']

		resized = (0, \
			40 * scaleRate, \
				screenSize['width'] *scaleRate, \
					(screenSize['height'] * scaleRate))

		croppedScreenshotImage = screenshotImage.crop(resized)
		croppedScreenshotImage.save(testingScreenShotPath)

		dic = {Constant.TESTING_METHOD:reminder,\
			Constant.BASE_SCREEN_SHOT:baseScreenShotPath,\
				Constant.TESTING_SCREENSHOT:testingScreenShotPath,\
					Constant.DIFF:""}
		# Use the Helper instance to add to compareArray
		self.add_to_compare_array(dic)

		screenShotCount.setCounter(screenShotCount.getCounter()+1)

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
		td2 = td(Constant.BASE_SCREEN_SHOT ,style= "width:270px")
		td3 = td(Constant.TESTING_SCREENSHOT,style= "width:270px")
		td4 = td(Constant.DIFF,style= "width:270px")
		tr1 = tr(td1, td2, td3, td4)
		table1 = table(tr1, align = "center", border="1")
		for dictionary in self.compareArray:
			trow = tr()
			tdName = td(dictionary[Constant.TESTING_METHOD] ,style= "width:150px")
			tdBaseScreenShot = td(img(style="width:270px;height:480px;", src = Helper().convertpngToBase64Html(dictionary[Constant.BASE_SCREEN_SHOT])))
			tdTestingScreenShot = td(img(style="width:270px;height:480px;", src = Helper().convertpngToBase64Html(dictionary[Constant.TESTING_SCREENSHOT])))
			if dictionary[Constant.DIFF] is not None:
				tdDiff = td(img(style="width:270px;height:480px;", src = Helper().convertpngToBase64Html(dictionary["Diff"])))
				trow = tr(tdName, tdBaseScreenShot, tdTestingScreenShot, tdDiff, bgcolor = "#fff200")
			else:
				tdDiff = td(font("✅",size = "20" ) , style="width:270px;height:480px;" , align= "center")
				trow = tr(tdName, tdBaseScreenShot, tdTestingScreenShot, tdDiff)
			table1.add(trow)

		p1 = p(table1)
		return str(p1)
