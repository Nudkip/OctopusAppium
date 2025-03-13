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

class TestLoginByPTFSS():
	class _ScreenShotName(Enum):
		SPLASH = "SPLASH"
		TOUR_1 = "TOUR_1"
		TOUR_2 = "TOUR_2"
		TOUR_3 = "TOUR_3"
		TOUR_4 = "TOUR_4"
		TOUR_5 = "TOUR_5"
		TOUR_6 = "TOUR_6"
		TOUR_7 = "TOUR_7"
		TOUR_8 = "TOUR_8"
		START = "START"
		SKIP = "SKIP"
		OFFER_NOTIFICATION = "OFFER_NOTIFICATION"
		HIGHLIGHT_1 = "HIGHLIGHT_1"
		HIGHLIGHT_2 = "HIGHLIGHT_2"
		HIGHLIGHT_3 = "HIGHLIGHT_3"
		HIGHLIGHT_4 = "HIGHLIGHT_4"
		NOTIFICATION = "NOTIFICATION"
		APP_TRACK = "APP_TRACK"
		HOME = "HOME"
		PTFSS = "PTFSS"
		PTFSS_LOGIN_PAGE = "PTFSS_LOGIN_PAGE"
		PTFSS_LOGIN = "PTFSS_LOGIN"
		INPUT_MOBILE_NUMBER = "INPUT_MOBILE_NUMBER"
		INPUT_PASSWORD = "INPUT_PASSWORD"
		TAP_LOGIN_BUTTON = "TAP_LOGIN_BUTTON"
		IGNORE_SAVE_PASSWORD = "IGNORE_SAVE_PASSWORD"
		INPUT_OTP = "INPUT_OTP"
		LOGIN_COMPLETE = "LOGIN_COMPLETE"
		TAP_FINISH = "TAP_FINISH"


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
		print(pytest.sharedHelper.clear_compare_array())
		print(pytest.sharedHelper.get_compare_array())
		print("************** teardown_method after %s **************" % method.__name__)

	@pytest.mark.xfail(raises=SystemError)
	@pytest.mark.run(order=3)
	def test_GoThroughTour(self, appium_driverNoReset):
		pytest.sharedHelper.driver = appium_driverNoReset
		self.log.log(msg="test_GoThroughTour", level=0)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.TOUR_1.value)
		sleep(2)
	
		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.TOUR_2.value)
		sleep(2)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.TOUR_3.value)
		sleep(2)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.TOUR_4.value)
		sleep(2)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.TOUR_5.value)
		sleep(2)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.TOUR_6.value)
		sleep(2)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.TOUR_7.value)
		sleep(2)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.TOUR_8.value)
		sleep(2)


	@pytest.mark.xfail(raises=SystemError)
	@pytest.mark.run(order=4)
	def test_GoThroughHighlight(self, appium_driverNoReset):
		pytest.sharedHelper.driver = appium_driverNoReset
		self.log.log(msg="test_GoThroughHighlight", level=0)

	@pytest.mark.xfail(raises=SystemError)
	@pytest.mark.run(order=5)
	def test_Login(self, appium_driverNoReset):
		pytest.sharedHelper.driver = appium_driverNoReset
		self.log.log(msg="test_Login", level=0)
		ptfssBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'name == "Transport Subsidy"')
		ptfssBtn.click()
  
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.PTFSS.value)
		loginCell = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'label CONTAINS "Login/Create"')
		loginCell.click()
  
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.PTFSS_LOGIN_PAGE.value)
		loginBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'name == "Login"')
		loginBtn.click()

		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.PTFSS_LOGIN.value)
		mobileNumberTxtField = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'label CONTAINS "Enter Mobile Number"')
		mobileNumberTxtField.send_keys("%s" % pytest.global_walletMobileNo)

		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.INPUT_MOBILE_NUMBER.value)
		passwordTxtField = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'label CONTAINS "Password"')
		passwordTxtField.send_keys("%s" % pytest.global_walletPassword)

		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.INPUT_PASSWORD.value)
		loginBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'name == "Login"')
		loginBtn.click()
  
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestLoginByPTFSS._ScreenShotName.IGNORE_SAVE_PASSWORD.value)
		savePasswordAlert = WebDriverWait(appium_driverNoReset, 3).until(EC.alert_is_present())
		print(f"Alert text: {savePasswordAlert.text}")
		savePasswordAlert.dismiss
