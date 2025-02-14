# coding=utf-8
# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from time import sleep

import unittest
import os
import random
import string
import shutil
import logging
import json
import contextlib
import sys
import time
import pytest
import logging
from selenium.webdriver.support import expected_conditions as ec 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.common.actions.pointer_input import PointerInput

#import all pytest.fixture
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "./util"))))
from ScreenShotCount import *
from Helper import *
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))))
from conftest import *

def setup_module(module):
	print()
	print("-------------- setup_module before %s --------------" % module.__name__)

def teardown_module(module):
	print()
	print("-------------- teardown_module after %s --------------" % module.__name__)

class TestSetupAppEnv():
	def setup_class(cls):
		print()
		# self.directory = '%s%s%s%s' % (os.getcwd(),'/', self.__class__.__name__, '/') 
		# if (os.path.isdir(self.directory)) :
		# 	print('\n%s %s' % (self.directory, 'is existing'))
		# 	try:
		# 		# remove all screen caps in directory
		# 		shutil.rmtree(self.directory)
		# 		os.mkdir( self.directory, 0755);
		# 		print('\n%s %s' % (self.directory, 'all screen caps are removed'))
		# 	except Exception as e:
		# 		print('\n%s shutil.rmtreeError: %s' % (self.directory, e))
		# else:
		# 	try:
		# 		# create a directory to store screen cap
		# 		os.mkdir( self.directory, 0755);
		# 		print('%s %s' % (self.directory, 'is created'))
		# 	except Exception as e:
		# 		print('\n%s mkdirError: %s' % (self.directory, e))

		print("~~~~~~~~~~~~~~ setup_class before %s ~~~~~~~~~~~~~~" % cls.__name__)

	def teardown_class(cls):
		print()
		print("~~~~~~~~~~~~~~ teardown_class after %s ~~~~~~~~~~~~~~" % cls.__name__)

	def setup_method(self,method):
		print()
		self.log = logging.getLogger(method.__name__)
		self.directory = Helper.createDirectory(self.__class__.__name__ , method.__name__)
		self.screenShotCounter = ScreenShotCount(1)
		print("************** setup_method before %s **************" % method.__name__)
		self.log = logging.getLogger(method.__name__)

	def teardown_method(self, method):
		print()
		print("************** teardown_method after %s **************" % method.__name__)

	@pytest.mark.skipif(pytest.global_fullReset == "False", reason="Only run after FullReset")
	@pytest.mark.run(order=0)
	def test_fullResetApp(self, appium_driverFullReset):
		print("full reset App")

	@pytest.mark.run(order=1)
	def test_setupEnvironment(self, appium_driverSetting, webDriverTimeoutSetting):
		octopusCell = Helper.scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeCell[@name="Octopus"]')
		Helper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, 'Home')
		octopusCell.click()

		serverCell = Helper.scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeCollectionView/XCUIElementTypeCell[13]')
		serverCell.click()

		envCell = Helper.scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeCell[@name="%s"]' % pytest.global_environment)
		envCell.click()

		backBtn = Helper.scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeButton[@name="Octopus"]')
		backBtn.click()

		
		# customOWPathTextField = Helper.scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeTextField[@name="SB_CUS_OW_PATH"]')
		# customOWPathTextField.clear()
		# customOWPathTextField.send_keys("%s" % pytest.global_owPath)

		# customOOSPathTextField = Helper.scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeTextField[@name="SB_CUS_OOS_PATH"]')
		# customOOSPathTextField.clear()
		# customOOSPathTextField.send_keys("%s" % pytest.global_oosPath)
  
		# try:
		# 	customWARSwitch = appium_driverSetting.find_element(by=AppiumBy.IOS_CLASS_CHAIN, value="**/XCUIElementTypeSwitch[`value == \"0\"`][2]")
		# 	switch_state = customWARSwitch.get_attribute("value")
		# 	print("click the switch now")
		# 	customWARSwitch.click()  # Turn the switch on
		# except:
		# 	print("customWARSwitch is on now")

		appium_driverSetting.quit()