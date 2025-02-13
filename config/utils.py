# coding=utf-8
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
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

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "./utils"))))
# compare screenShot class
from util.VisualComparison import *
# screenShot Counter class
from util.ScreenShotCount import *

import util.Constant
from selenium.webdriver.support import expected_conditions as ec 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# generate html code
import dominate
from dominate.tags import *

logging.basicConfig(level=logging.CRITICAL)

diffFound = False

# --------------------- @pytest.fixture ---------------------
@pytest.fixture(scope="module")
def webDrivertimeoutFullReset(appium_driverFullReset):
	return WebDriverWait(appium_driverFullReset, 20)

@pytest.fixture(scope="module")
def webDrivertimeoutNoReset(appium_driverNoReset):
	return WebDriverWait(appium_driverNoReset, 20)

@pytest.fixture(scope="function")
def webDrivertimeoutGoSetting(appium_driverGoSetting):
	return WebDriverWait(appium_driverGoSetting, 20)

@pytest.fixture(scope="function")
def appium_driverGoSetting():
	global driver
	global compareArray
	global diffFound
	compareArray = []
	driver = webdriver.Remote(
		command_executor='http://localhost:4723/wd/hub',
		desired_capabilities={
			'app': 'settings',
			'platformName': 'iOS',
			'platformVersion': '11.3',
			'deviceName': 'Timothy’s iPhone',
			'noReset': True,
			# 'fullReset': True,
			'newCommandTimeout': '180',
			'xcodeOrgId': 'L62BN6336L',
			'xcodeSigningId': "iPhone Developer",
			'udid':'d2868681650f7719f409679663b4af95f71278be'
		})
	driver.implicitly_wait(20)
	return driver

