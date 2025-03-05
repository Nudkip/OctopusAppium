# coding=utf-8
# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from time import sleep

import os
import logging
import sys
import pytest
import logging
from enum import Enum
from appium.webdriver.common.appiumby import AppiumBy

#import all pytest.fixture
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "./util"))))
from ScreenShotCount import *
# from Helper import *
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))))
from conftest import *

def setup_module(module):
	print()
	print("-------------- setup_module before %s --------------" % module.__name__)

def teardown_module(module):
	print()
	print("-------------- teardown_module after %s --------------" % module.__name__)

class TestSetupAppEnv():
	class _ScreenShotName(Enum):
		SELECT_APP = "SELECT_APP"
		SELECT_SEVER = "SELECT_SEVER"
		DID_SELECT_SEVER = "DID_SELECT_SEVER"
		DID_SET_OWPATH = "DID_SET_OWPATH"
		DID_SET_OOSPATH = "DID_SET_OOSPATH"
		DID_SET_CUSTOM_PATH = "DID_SET_CUSTOM_PATH"

	def setup_class(cls):
		print()
		print("~~~~~~~~~~~~~~ setup_class before %s ~~~~~~~~~~~~~~" % cls.__name__)

	def teardown_class(cls):
		print()
		print("~~~~~~~~~~~~~~ teardown_class after %s ~~~~~~~~~~~~~~" % cls.__name__)

	def setup_method(self,method):
		print()
		self.log = logging.getLogger(method.__name__)
		self.directory = Helper().createDirectory(self.__class__.__name__ , method.__name__)
		self.screenShotCounter = ScreenShotCount(1)
		print("************** setup_method before %s **************" % method.__name__)

	def teardown_method(self, method):
		print()
		print("************** teardown_method after %s **************" % method.__name__)

	@pytest.mark.skipif(pytest.global_fullReset == "False", reason="Only run after FullReset")
	@pytest.mark.run(order=0)
	def test_fullResetApp(self, appium_driverFullReset):
		print("full reset App")

	@pytest.mark.xfail(raises=SystemError)
	@pytest.mark.run(order=1)
	def test_setupEnvironment(self, appium_driverSetting):
		pytest.sharedHelper.driver = appium_driverSetting
		octopusCell = Helper().scroll_until_iOSPredicateString_element_found(appium_driverSetting, 'name == "Octopus"')
		pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.SELECT_APP.value)
		octopusCell.click()

		serverCell = Helper().scroll_until_iOSPredicateString_element_found(appium_driverSetting, 'name == "Server"')
		pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.SELECT_SEVER.value)
		serverCell.click()

		print(pytest.global_environment)
		print(pytest.global_environment)
		print(pytest.global_environment)

		envCell = Helper().scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeCell[@name="%s"]' % pytest.global_environment)
		pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.DID_SELECT_SEVER.value)
		envCell.click()

		backBtn = Helper().scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeButton[@name="Octopus"]')
		backBtn.click()
		
		customOWPathTextField = Helper().scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeTextField[@name="SB_CUS_OW_PATH"]')
		customOWPathTextField.clear()
		customOWPathTextField.send_keys("%s" % pytest.global_owPath)
		pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.DID_SET_OWPATH.value)
  
		returnBtn = Helper().scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeButton[@name="Return"]')
		returnBtn.click()
  
		customOOSPathTextField = Helper().scroll_until_element_found(appium_driverSetting, '//XCUIElementTypeTextField[@name="SB_CUS_OOS_PATH"]')
		customOOSPathTextField.clear()
		customOOSPathTextField.send_keys("%s" % pytest.global_oosPath)
		pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.DID_SET_OOSPATH.value)
		returnBtn.click()

		try:
			customWARSwitch = appium_driverSetting.find_element(by=AppiumBy.IOS_CLASS_CHAIN, value="**/XCUIElementTypeSwitch[`value == \"0\"`][2]")
			switch_state = customWARSwitch.get_attribute("value")
			print("click the switch now")
			customWARSwitch.click()  # Turn the switch on
			pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.DID_SET_CUSTOM_PATH.value)
		except:
			print("customWARSwitch is on now")
			pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.DID_SET_CUSTOM_PATH.value)
				
		print(pytest.sharedHelper.get_compare_array())

		appium_driverSetting.quit()

