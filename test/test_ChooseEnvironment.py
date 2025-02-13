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

#import all pytest.fixture
from app.conftest import *
from util.ScreenShotCount import *

def setup_module(module):
	print()
	print("-------------- setup_module before %s --------------" % module.__name__)

def teardown_module(module):
	print()
	print("-------------- teardown_module after %s --------------" % module.__name__)

class TestLoginOePay():
	def setup_class(cls):
		print()
		print("~~~~~~~~~~~~~~ setup_class before %s ~~~~~~~~~~~~~~" % cls.__name__)

	def teardown_class(cls):
		print()
		print("~~~~~~~~~~~~~~ teardown_class after %s ~~~~~~~~~~~~~~" % cls.__name__)

	def setup_method(self,method):
		print()
		print("************** setup_method before %s **************" % method.__name__)
		self.log = logging.getLogger(method.__name__)

	def teardown_method(self, method):
		print()
		print("************** teardown_method after %s **************" % method.__name__)

	@pytest.mark.skipif(pytest.global_fullReset == "False", reason="Only run after FullReset")
	@pytest.mark.run(order=0)
	def test_fullResetapp(self, appium_driverFullReset, webDriverTimeoutFullReset):
		print("full reset App")

	@pytest.mark.run(order=1)
	def test_chooseEnvironmrnt(self, driver, webDriver):
		# TouchAction(appium_driverGoSetting).press(x=self.x/2, y=self.y/2).wait(100).move_to(x=self.x/2, y=0).wait(100).release().perform()
		# TouchAction(appium_driverGoSetting).press(x=self.x/2, y=self.y/2).wait(100).move_to(x=self.x/2, y=0).wait(100).release().perform()

		width = driver.get_window_size()['width']
		height = driver.get_window_size()['height']
		driver.swipe(width / 2, height / 4, width / 2, height * 3 / 4, 500)



