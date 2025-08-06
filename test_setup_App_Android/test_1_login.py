from appium import webdriver
from appium.options.android import UiAutomator2Options
import time


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
from util.checking import *
#import all pytest.fixture
# from Helper import *
from conftest import *

def setup_module(module):
	print()
	print(f"-------------- setup_module before {module.__name__} --------------")

def teardown_module(module):
	print()
	print(f"-------------- teardown_module after {module.__name__} --------------")

class TestGoThroughTutorial():
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

	@pytest.mark.run(order=2)
	def test_GoThroughTour(self, appium_Android_driverNoReset):
		pytest.sharedHelper.driver = appium_Android_driverNoReset
		self.log.log(msg="test_GoThroughTour", level=logging.INFO)
		#pytest.sharedHelper.captureScreenFYR(appium_Android_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.SPLASH.value)
		sleep(1)
  
		#pytest.sharedHelper.captureScreenFYR(appium_Android_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.TOUR_1.value)
		sleep(1)
		
		wait = WebDriverWait(appium_Android_driverNoReset, 5)
		sign_in_button = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@resource-id, 'sign_in_btn_layout')]")))
		sign_in_button.click()
		connecting = True
		while connecting:
			# Check for the presence of the "Connecting..." text
			connecting = CommonChecking().isElementPresent(By.xpath("//*[contains(@text, '連接中...')]"), appium_Android_driverNoReset, 1)
			sleep(1)
			self.log.info(f"Waiting for connection to complete... {connecting}")


		pytest.sharedHelper.captureScreenFYR(appium_Android_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.TOUR_1.value)
		el = appium_Android_driverNoReset.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
		el[0].click()
		el[0].send_keys("99000067")
		if len(el) > 1:
			print("Captral is disable password is needed")
			el[1].click()
			el[1].send_keys("aaaa1111")
		else:
			print("Captral is enable, not able to proceed")
		
		Next = appium_Android_driverNoReset.findElement(AppiumBy.xpath("//*[contains(@resource-id, 'login_button')]"))
		Next.click()

		pytest.sharedHelper.captureScreenFYR(appium_Android_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.OFFER_NOTIFICATION.value)
		thanksBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_Android_driverNoReset, 'label CONTAINS "Yes"')
		thanksBtn.click()
