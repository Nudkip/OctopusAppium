# coding=utf-8
# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from time import sleep

import os
import logging
import sys
import pytest
from enum import Enum
from appium.webdriver.common.appiumby import AppiumBy

from util.ScreenShotCount import *
# from Helper import *
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))))
from conftest import *

def setup_module(module):
	print()
	print(f"-------------- setup_module before {module.__name__} --------------")

def teardown_module(module):
	print()
	print(f"-------------- teardown_module after {module.__name__} --------------")

class TestSetupAppEnv():
	class _ScreenShotName(Enum):
		SELECT_APP = "SELECT_APP"
		SELECT_SEVER = "SELECT_SEVER"
		DID_SELECT_SEVER = "DID_SELECT_SEVER"
		DID_SET_OWPATH = "DID_SET_OWPATH"
		DID_SET_OOSPATH = "DID_SET_OOSPATH"
		DID_SET_CUSTOM_PATH = "DID_SET_CUSTOM_PATH"

	def setup_class(self):
		print()
		print(f"~~~~~~~~~~~~~~ setup_class before {self.__name__} ~~~~~~~~~~~~~~")

	def teardown_class(self):
		print()
		print(f"~~~~~~~~~~~~~~ teardown_class after {self.__name__} ~~~~~~~~~~~~~~")

	def setup_method(self,method):
		print()
		self.log = logging.getLogger(method.__name__)
		self.directory = Helper().createDirectory(self.__class__.__name__, method.__name__)
		self.screenShotCounter = ScreenShotCount(1)
		print(f"************** setup_method before {method.__name__} **************")

	def teardown_method(self, method):
		print()
		print(f"************** teardown_method after {method.__name__} **************")

	@pytest.mark.skipif(pytest.global_fullReset == "False", reason="Only run after FullReset")
	@pytest.mark.run(order=0)
	def test_fullResetApp(self, appium_driverFullReset):
		print("full reset App")

	@pytest.mark.run(order=1)
	def test_setupEnvironment(self, appium_driverSetting):
		pytest.sharedHelper.driver = appium_driverSetting

		appCell = Helper().scroll_until_iOSPredicateString_element_found(appium_driverSetting, 'name == "Apps"')
		appCell.click()

		octopusCell = Helper().scroll_until_iOSPredicateString_element_found(appium_driverSetting, 'name == "com.octopuscards.octopus"')
		Helper().swipe(appium_driverSetting, 200, 300, 200, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.SELECT_APP.value)
		# sleep(10) # Consider removing if next action waits, or replace with explicit wait for next screen element
		octopusCell.click()

		serverCell = Helper().scroll_until_iOSPredicateString_element_found(appium_driverSetting, 'name == "Server"')
		pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.SELECT_SEVER.value)
		serverCell.click()

		self.log.info(f"Setting environment to: {pytest.global_environment}")

		envCell = Helper().scroll_until_elementXPATH_found(
			appium_driverSetting,
			f'//XCUIElementTypeButton[@name="{pytest.global_environment}"]',
		)
		# It's good practice to ensure element is clickable if there are fast transitions
		pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.DID_SELECT_SEVER.value)
		envCell.click()

		backBtn = Helper().scroll_until_elementXPATH_found(appium_driverSetting, '//XCUIElementTypeButton[@name="Octopus"]')
		backBtn.click()

		customOWPathTextField = Helper().scroll_until_elementXPATH_found(appium_driverSetting, '//XCUIElementTypeTextField[@name="PSTextFieldSpecifier.SB_CUS_OW_PATH"]')
		customOWPathTextField.clear()
		customOWPathTextField.send_keys(f"{pytest.global_owPath}")
		pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.DID_SET_OWPATH.value)

		returnBtn = Helper().scroll_until_elementXPATH_found(appium_driverSetting, '//XCUIElementTypeButton[@name="Return"]')
		returnBtn.click()

		customOOSPathTextField = Helper().scroll_until_elementXPATH_found(appium_driverSetting, '//XCUIElementTypeTextField[@name="PSTextFieldSpecifier.SB_CUS_OOS_PATH"]')
		customOOSPathTextField.clear()                                                          

		customOOSPathTextField.send_keys(f"{pytest.global_oosPath}")
		pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.DID_SET_OOSPATH.value)

		sleep(1)
		returnBtn.click()

		# Attempt to find the specific "Custom WAR" switch and turn it on if it's off.
		# WARNING: The XPath (//XCUIElementTypeSwitch[@value="0"])[2] is brittle.
		# It assumes the target is the *second* switch on the screen AND it's currently OFF.
		# A more robust locator (e.g., accessibility ID or unique name for the switch) is highly recommended.
		try:
			customWARSwitch = Helper().scroll_until_elementXPATH_found(appium_driverSetting, '(//XCUIElementTypeSwitch[@value="0"])[2]')
			switch_state = customWARSwitch.get_attribute("value")
			print(f"click the switch now {switch_state}")
			customWARSwitch.click()  # Turn the switch on
			pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.DID_SET_CUSTOM_PATH.value)
		except:
			print("customWARSwitch is on now")
			pytest.sharedHelper.captureScreenFYR(appium_driverSetting, self.directory, self.screenShotCounter, TestSetupAppEnv._ScreenShotName.DID_SET_CUSTOM_PATH.value)

		print(pytest.sharedHelper.get_compare_array())

		appium_driverSetting.quit()
