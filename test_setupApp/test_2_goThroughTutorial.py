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

class TestGoThroughTutorial():
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
		HIGHLIGHT_5 = "HIGHLIGHT_5"
		NOTIFICATION = "NOTIFICATION"
		APP_TRACK = "APP_TRACK"
		HOME = "HOME"

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
	def test_GoThroughTour(self, appium_driverNoReset):
		pytest.sharedHelper.driver = appium_driverNoReset
		self.log.log(msg="test_GoThroughTour", level=logging.INFO)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.SPLASH.value)
		sleep(3)
  
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.TOUR_1.value)
		sleep(1)
	
		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		# Consider replacing magic numbers in swipe with descriptive helper methods if this is a common gesture like "swipe left"
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.TOUR_2.value)
		sleep(1)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.TOUR_3.value)
		sleep(1)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.TOUR_4.value)
		sleep(1)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.TOUR_5.value)
		sleep(1)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.TOUR_6.value)
		sleep(1)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.TOUR_7.value)
		sleep(1)

		Helper().swipe(appium_driverNoReset, 500, 200, 0, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.TOUR_8.value)
		sleep(1)

		# Ensure "Start" button is present and clickable
		# WebDriverWait(appium_driverNoReset, 10).until(
		# 	EC.element_to_be_clickable((AppiumBy.IOS_PREDICATE, 'name == "Start"'))
		# )
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.START.value)
		startBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'name == "Start"')
		startBtn.click()
  
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.SKIP.value)
		skipBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'name == "Skip"')
		skipBtn.click()

		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.OFFER_NOTIFICATION.value)
		thanksBtn = Helper().scroll_until_iOSPredicateString_element_found(appium_driverNoReset, 'label CONTAINS "Yes"')
		thanksBtn.click()

	@pytest.mark.run(order=3)
	def test_GoThroughHighlight(self, appium_driverNoReset):
		pytest.sharedHelper.driver = appium_driverNoReset
		self.log.log(msg="test_GoThroughHighlight", level=logging.INFO)

		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.HIGHLIGHT_1.value)

		# WARNING: Tapping by coordinates is highly brittle and should be avoided.
		# Prefer finding and tapping a specific UI element.
		Helper().tap(appium_driverNoReset, 200, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.HIGHLIGHT_2.value)

		# WARNING: Tapping by coordinates is highly brittle.
		Helper().tap(appium_driverNoReset, 200, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.HIGHLIGHT_3.value)

		# WARNING: Tapping by coordinates is highly brittle.
		Helper().tap(appium_driverNoReset, 200, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.HIGHLIGHT_4.value)

		# WARNING: Tapping by coordinates is highly brittle.
		Helper().tap(appium_driverNoReset, 200, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.HIGHLIGHT_5.value)

		# WARNING: Tapping by coordinates is highly brittle.
		Helper().tap(appium_driverNoReset, 200, 200)
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.NOTIFICATION.value)

		notificationAlert = WebDriverWait(appium_driverNoReset, 5).until(EC.alert_is_present()) # Increased timeout slightly for alert
		print(f"Alert text: {notificationAlert.text}")
		notificationAlert.accept()
		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.APP_TRACK.value)

		allowTrackingAlert = WebDriverWait(appium_driverNoReset, 3).until(EC.alert_is_present())
		print(f"Alert text: {allowTrackingAlert.text}")
		allowTrackingAlert.accept()

		pytest.sharedHelper.captureScreenFYR(appium_driverNoReset, self.directory, self.screenShotCounter, TestGoThroughTutorial._ScreenShotName.HOME.value)
