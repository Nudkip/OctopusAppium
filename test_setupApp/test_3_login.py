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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from util.Helper import *
from util.ScreenShotCount import * 
#import all pytest.fixture
# from Helper import *
from conftest import *

def setup_module(module):
	print()
	print(f"-------------- setup_module before {module.__name__} --------------")

def teardown_module(module):
	print()
	print(f"-------------- teardown_module after {module.__name__} --------------")

class TestLogin():
	class _ScreenShotName(Enum):
		PROFILE = "PROFILE"
		PROFILE_LOGIN_PAGE = "PROFILE_LOGIN_PAGE"
		PROFILE_LOGIN = "PROFILE_LOGIN"
		INPUT_MOBILE_NUMBER = "INPUT_MOBILE_NUMBER"
		TAP_LOGIN_BUTTON = "TAP_LOGIN_BUTTON"
		IGNORE_SAVE_PASSWORD = "IGNORE_SAVE_PASSWORD"
		INPUT_OTP = "INPUT_OTP"
		LOGIN_COMPLETE = "LOGIN_COMPLETE"
		TAP_FINISH = "TAP_FINISH"

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
		print(pytest.sharedHelper.clear_compare_array())
		print(pytest.sharedHelper.get_compare_array())
		print(f"************** teardown_method after {method.__name__} **************")

	@pytest.mark.run(order=4)
	def test_Login(self, appium_driverNoReset):
		pytest.sharedHelper.driver = appium_driverNoReset
		self.log.log(msg="test_Login", level=logging.INFO)
		profileBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'name == "Profile and Settings"')
		profileBtn.click()
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLogin._ScreenShotName.PROFILE.value)

		signUploginBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'name == "Sign up / Login" AND label == "Sign up / Login" AND value == "Sign up / Login"')
		signUploginBtn.click()
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLogin._ScreenShotName.PROFILE_LOGIN_PAGE.value)

		loginBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'name == "Login"')
		loginBtn.click()
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLogin._ScreenShotName.PROFILE_LOGIN.value)

		mobileNumberTxtField = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'label CONTAINS "Enter Mobile Number"')
		mobileNumberTxtField.send_keys(f"{pytest.global_walletMobileNo}")
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLogin._ScreenShotName.INPUT_MOBILE_NUMBER.value)

		loginBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'name == "Login"')
		loginBtn.click()
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLogin._ScreenShotName.IGNORE_SAVE_PASSWORD.value)

		# If a "Save Password" system alert appears, it needs to be handled.
		# Example:
		otp = pytest.global_otp

		otp0TxtField = Helper().scroll_until_accessibilityID_element_found(appium_driverNoReset, 'Verification Code, 1st digit')
		# WebDriverWait(appium_driverNoReset, 10).until(
		# 		EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Verification Code, 1st digit'))
		# )
		otp0TxtField.click()
		otp0TxtField.send_keys(f"{otp[0]}")

		otp1TxtField = Helper().scroll_until_accessibilityID_element_found(appium_driverNoReset, '2nd digit')
		otp1TxtField.send_keys(f"{otp[1]}")

		otp2TxtField = Helper().scroll_until_accessibilityID_element_found(appium_driverNoReset, '3rd digit')
		otp2TxtField.send_keys(f"{otp[2]}")

		otp3TxtField = Helper().scroll_until_accessibilityID_element_found(appium_driverNoReset, '4th digit')
		otp3TxtField.send_keys(f"{otp[3]}")

		otp4TxtField = Helper().scroll_until_accessibilityID_element_found(appium_driverNoReset, '5th digit')
		otp4TxtField.send_keys(f"{otp[4]}")

		otp5TxtField = Helper().scroll_until_accessibilityID_element_found(appium_driverNoReset, '6th digit')
		otp5TxtField.send_keys(f"{otp[5]}")
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLogin._ScreenShotName.LOGIN_COMPLETE.value)

		finishBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'name == "Finish" AND label == "Finish" AND value == "Finish"')
		finishBtn.click()
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLogin._ScreenShotName.TAP_FINISH.value)
