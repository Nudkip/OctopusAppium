# coding=utf-8
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

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "./util"))))
# compare screenShot class
from VisualComparison import *
# screenShot Counter class
from ScreenShotCount import *
from Constant import *

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait

# generate html code
import dominate
from dominate.tags import *

logging.basicConfig(level=logging.CRITICAL)

diffFound = False

# --------------------- @pytest.fixture ---------------------
@pytest.fixture(scope="module")
def webDriverTimeoutOctopusFullReset(appium_driverOctopusFullReset):
	return WebDriverWait(appium_driverOctopusFullReset, 20)

@pytest.fixture(scope="module")
def webDriverTimeoutOctopusNoReset(appium_driverOctopusNoReset):
	return WebDriverWait(appium_driverOctopusNoReset, 20)

@pytest.fixture(scope="function")
def webDriverTimeoutSetting(appium_driverSetting):
	return WebDriverWait(appium_driverSetting, 20)

@pytest.fixture(scope="function")
def appium_driverSetting():
	global driver
	global compareArray
	global diffFound
	compareArray = []
	options = AppiumOptions()
	options.load_capabilities({
		"platformName": "iOS",
		"appium:deviceName": "iPhone 15",
		"appium:platformVersion": "17.2",
		"appium:noReset": False,
		"appium:app": "com.apple.Preferences",
		"appium:automationName": "XCUITest",
		"appium:includeSafariInWebviews": True,
		"appium:newCommandTimeout": 3600,
		"appium:connectHardwareKeyboard": True
	})

	driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

	driver.implicitly_wait(20)
	return driver

@pytest.fixture(scope="module")
def appium_driverFullReset():
	global driver
	global compareArray
	global diffFound
	compareArray = []
	options = AppiumOptions()
	options.load_capabilities({
		"platformName": "iOS",
		"appium:deviceName": "iPhone 15",
		"appium:platformVersion": "17.2",
		"appium:noReset": True,
			"appium:app": "/Users/raymondchan/Documents/Appium/OctopusQuickBuild.app",
		"appium:automationName": "XCUITest",
		"appium:includeSafariInWebviews": True,
		"appium:newCommandTimeout": 3600,
		"appium:connectHardwareKeyboard": True
	})

	driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

	driver.implicitly_wait(20)

	return driver

@pytest.fixture(scope="module")
def appium_driverNoReset():
	global driver
	global compareArray
	global diffFound
	compareArray = []
	options = AppiumOptions()
	options.load_capabilities({
		"platformName": "iOS",
		"appium:deviceName": "iPhone 15",
		"appium:platformVersion": "17.2",
		"appium:noReset": True,
			"appium:app": "/Users/raymondchan/Documents/Appium/OctopusQuickBuild.app",
		"appium:automationName": "XCUITest",
		"appium:includeSafariInWebviews": True,
		"appium:newCommandTimeout": 3600,
		"appium:connectHardwareKeyboard": True
	})

	driver = webdriver.Remote("http://127.0.0.1:4723", options=options)


	driver.implicitly_wait(20)
	return driver

# --------------------- @pytest.fixture ---------------------

# ````````````````````` pytest_configure `````````````````````

def pytest_configure(config):

	fullReset = config.getoption('--fullReset')
	pytest.global_fullReset = fullReset
	device = config.getoption('--device')
	pytest.global_device = device
	environment = config.getoption('--environment')
	pytest.global_environment = environment
	environment = config.getoption('--owPath')
	pytest.global_owPath = environment
	environment = config.getoption('--oosPath')
	pytest.global_oosPath = environment


def pytest_addoption(parser):
    # Use hyphens for CLI arguments (e.g., --full-reset)
    parser.addoption(
        "--fullReset",
        metavar="FULL_RESET",
        default="False",
        type=str,
        help="True: Run full reset, False: No reset"
    )
    parser.addoption(
        "--device",
        metavar="DEVICE",
        default="iPhone7_8_Plus",
        type=str,
        help="Device type (e.g., iPhone7_8_Plus)"
    )
    parser.addoption(
        "--environment",
        metavar="ENVIRONMENT",
        default="Kirby",
        type=str,
        help="Environment name (e.g., Zaku, Gouf)"
    )
    parser.addoption(
        "--owPath",
        metavar="OWPath",
        default="/ow_owallet_ws/rest/",
        type=str,
        help="/ow_owallet_ws_xxxxxx/rest/"
    )
    parser.addoption(
        "--oosPath",
        metavar="OOSPath",
        default="/wildfly/7301/",
        type=str,
        help="/wildfly/7301/"
    )


# ````````````````````` pytest_configure `````````````````````

#////////////////////// Common function //////////////////////

def createDirectory(className, methodName):
	directory = '%s/test/%s/%s/%s/%s/' % (os.path.dirname(__file__),Constant.SCREEN_SHOT, className , methodName, time.strftime("%Y%m%d_%H_%M"))
	
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

def captureScreenFYR(appium_driver,directory,screenShotCount, remarks):

	statusBar = appium_driver.find_element_by_xpath("//XCUIElementTypeStatusBar")
	screenSize = appium_driver.get_window_size()
	sleep(1)
	reminder = str(screenShotCount.getCounter())+ '_' + remarks
	print(reminder)
	basePath = str(directory)[:-len(str(time.strftime("%Y%m%d_%H_%M")))-1] + 'Source/' + pytest.global_device + '/'
	baseScreenShotPath = basePath + str(screenShotCount.getCounter()) +'_'+ remarks +'.png'
	testingScreenShotPath = directory + str(screenShotCount.getCounter()) +'_'+ remarks +'.png'
	appium_driver.save_screenshot(testingScreenShotPath)

	screenshotImage = Image.open(testingScreenShotPath)
	screenshotImageWidth, screenshotImageHeight = screenshotImage.size
	scaleRate = screenshotImageWidth/screenSize['width']

	resized = (0, \
		statusBar.size.get("height") * scaleRate, \
			screenSize['width'] *scaleRate, \
				(screenSize['height'] * scaleRate))

	croppedScreenshotImage = screenshotImage.crop(resized)
	croppedScreenshotImage.save(testingScreenShotPath)

	dic = {Constant.TESTING_METHOD:reminder,\
		Constant.BASE_SCREEN_SHOT:baseScreenShotPath,\
			Constant.TESTING_SCREENSHOT:testingScreenShotPath,\
				Constant.DIFF:""}
	compareArray.append(dic)

	screenShotCount.setCounter(screenShotCount.getCounter()+1)
	

# def moveUISlider(driver, slider, increase):
# 	Y = slider.location.get("y")
# 	height = slider.size.get("height")
# 	startX = slider.size.get("width") 
# 	endX = slider.location.get("x")

# 	if increase:
# 		TouchAction(driver).press(x= endX +12, y= Y).wait(1000).move_to(x= startX + 39, y= Y).wait(2000).release().perform()
# 	else:
# 		TouchAction(driver).press(x= startX, y= Y).wait(1000).move_to(x= 0, y= Y).wait(2000).release().perform()

# def convertpngToBase64Html(imagePath):
# 	encodedImage = base64.b64encode(open(imagePath, "rb").read()).decode('ascii')
# 	return 'data:image/png;base64,%s' % encodedImage

# def createVisualComparisonTable():

# 	# print("createVisualComparisonTable")

# 	for dictionary in compareArray:
# 		dictionary['Diff'] = VisualComparison().analyze(dictionary['TestingScreenShot'], dictionary['BaseScreenShot'])

# 	td1 = td("Testing Method (Screenshot Name)" ,style= "width:150px")
# 	td2 = td(Constant.BASE_SCREEN_SHOT ,style= "width:270px")
# 	td3 = td(Constant.TESTING_SCREENSHOT,style= "width:270px")
# 	td4 = td(Constant.DIFF,style= "width:270px")
# 	tr1 = tr(td1, td2, td3, td4)
# 	table1 = table(tr1, align = "center", border="1")
# 	for dictionary in compareArray:
# 		trow = tr()
# 		tdName = td(dictionary[Constant.TESTING_METHOD] ,style= "width:150px")
# 		tdBaseScreenShot = td(img(style="width:270px;height:480px;", src = convertpngToBase64Html(dictionary[Constant.BASE_SCREEN_SHOT])))
# 		tdTestingScreenShot = td(img(style="width:270px;height:480px;", src = convertpngToBase64Html(dictionary[Constant.TESTING_SCREENSHOT])))
# 		if dictionary[Constant.DIFF] is not None:
# 			tdDiff = td(img(style="width:270px;height:480px;", src = convertpngToBase64Html(dictionary["Diff"])))
# 			trow = tr(tdName, tdBaseScreenShot, tdTestingScreenShot, tdDiff, bgcolor = "#fff200")
# 		else:
# 			tdDiff = td(font("✅",size = "20" ) , style="width:270px;height:480px;" , align= "center")
# 			trow = tr(tdName, tdBaseScreenShot, tdTestingScreenShot, tdDiff)
# 		table1.add(trow)

# 	p1 = p(table1)
# 	return str(p1)

#////////////////////// Common function //////////////////////

#====================== pytest html report ======================
# @pytest.mark.optionalhook
# def pytest_html_results_table_header(cells):
# 	cells.pop(3)
# 	cells.insert(3, pyhtml.th("Pass Diff?"))

# @pytest.mark.optionalhook
# def pytest_html_results_table_row(report, cells):
# 	cells.pop(3)
# 	print("pytest_html_results_table_row")
# 	global diffFound
# 	if diffFound:
# 		cells.insert(3, pyhtml.td('❌'))
# 	else:
# 		cells.insert(3, pyhtml.td('✅'))
# 	diffFound = False


# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
# 	"""
# 	Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
# 	:param item:
# 	"""
# 	pytest_html = item.config.pluginmanager.getplugin('html')
# 	outcome = yield
# 	report = outcome.get_result()
# 	extras = getattr(report, 'extra', [])
# 	if report.when == 'call' or report.when == 'setup':
# 		xfail = hasattr(report, 'wasxfail')
# 		if (report.skipped and xfail) or (report.failed and not xfail):
# 			screenshot = driver.get_screenshot_as_base64()
# 			html = '<p><img src="data:image/png;base64,%s" alt="screenshot" style="width:270px;height:480px;" align="left"/></p>' % screenshot
# 			extras.append(pytest_html.extras.html(html))
# 			# extra.append(pytest_html.extras.image(screenshot))
# 			report.extra = extras
# 		elif (report.passed and report.when != 'setup'):
# 			# generate a table in visual testing if testing pass
# 			htmlCode = createVisualComparisonTable()
# 			extras.append(pytest_html.extras.html(htmlCode))
# 			compareArray.clear()
# 			report.extra = extras
			
#====================== pytest html report ======================


 
