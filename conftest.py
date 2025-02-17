# coding=utf-8
from py.xml import html as pyhtml
import pytest
import os
import time
import shutil, sys   
import logging
from time import sleep
import base64
import sys

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "./util"))))
# compare screenShot class
from VisualComparison import *
# screenShot Counter class
from ScreenShotCount import *
from Helper import Helper
from Constant import *

from appium.webdriver import Remote
from appium.options.common.base import AppiumOptions

# For W3C actions
from selenium.webdriver.support.ui import WebDriverWait

# generate html code
import dominate
from dominate.tags import *

logging.basicConfig(level=logging.CRITICAL)

diffFound = False

# --------------------- @pytest.fixture ---------------------
@pytest.fixture(scope="session")
def helper_instance():
	instance = Helper()
	return instance


@pytest.fixture(scope="function")
def webDriverTimeoutOctopusFullReset(appium_driverOctopusFullReset):
	return WebDriverWait(appium_driverOctopusFullReset, 20)

@pytest.fixture(scope="function")
def webDriverTimeoutOctopusNoReset(appium_driverOctopusNoReset):
	return WebDriverWait(appium_driverOctopusNoReset, 20)

@pytest.fixture(scope="function")
def webDriverTimeoutSetting(appium_driverSetting):
	return WebDriverWait(appium_driverSetting, 20)

@pytest.fixture(scope="module")
def appium_driverSetting():
	options = AppiumOptions()
	options.load_capabilities({
		"platformName": "iOS",
		"appium:deviceName": "iPhone 15",
		"appium:platformVersion": "17.2",
		"appium:includeNonModalElements": True,  # Critical for system elements
		"appium:noReset": False,
		"appium:app": "com.apple.Preferences",
		"appium:automationName": "XCUITest",
		"appium:includeSafariInWebviews": True,
		"appium:newCommandTimeout": 3600,
		"appium:connectHardwareKeyboard": True
	})

	driver = Remote("http://127.0.0.1:4723", options=options)

	driver.implicitly_wait(20)
	return driver

@pytest.fixture(scope="module")
def appium_driverFullReset():
	options = AppiumOptions()
	options.load_capabilities({
		"platformName": "iOS",
		"appium:deviceName": "iPhone 15",
		"appium:platformVersion": "17.2",
		"appium:includeNonModalElements": True,  # Critical for system elements
		"appium:noReset": True,
			"appium:app": "/Users/raymondchan/Documents/Appium/OctopusQuickBuild.app",
		"appium:automationName": "XCUITest",
		"appium:includeSafariInWebviews": True,
		"appium:newCommandTimeout": 3600,
		"appium:connectHardwareKeyboard": True
	})

	driver = Remote("http://127.0.0.1:4723", options=options)

	driver.implicitly_wait(20)

	return driver

@pytest.fixture(scope="module")
def appium_driverNoReset():
	options = AppiumOptions()
	options.load_capabilities({
		"platformName": "iOS",
		"appium:deviceName": "iPhone 15",
		"appium:platformVersion": "17.2",
		"appium:includeNonModalElements": True,  # Critical for system elements
		"appium:noReset": True,
			"appium:app": "/Users/raymondchan/Documents/Appium/OctopusQuickBuild.app",
		"appium:automationName": "XCUITest",
		"appium:includeSafariInWebviews": True,
		"appium:newCommandTimeout": 3600,
		"appium:connectHardwareKeyboard": True
	})

	driver = Remote("http://127.0.0.1:4723", options=options)

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
		default="iPhone 15",
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

#====================== pytest html report ======================
@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
	cells.pop(3)
	cells.insert(3, pyhtml.th("Pass Diff?"))

@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
	cells.pop(3)
	print("pytest_html_results_table_row")
	global diffFound
	if diffFound:
		cells.insert(3, pyhtml.td('❌'))
	else:
		cells.insert(3, pyhtml.td('✅'))
	diffFound = False


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    pytest_html = item.config.pluginmanager.get_plugin('html')
    extras = getattr(report, 'extra', [])

    if pytest_html is not None:
        if report.when in ('call', 'setup'):
            xfail = hasattr(report, 'wasxfail')
            if (report.skipped and xfail) or (report.failed and not xfail):
                screenshot = driver.get_screenshot_as_base64()
                html = f'<p><img src="data:image/png;base64,{screenshot}" alt="screenshot" style="width:270px;height:480px;" align="left"/></p>'
                extras.append(pytest_html.extras.html(html))
        elif report.passed and report.when != 'setup':
            helper_instance = Helper()
            htmlCode = helper_instance.createVisualComparisonTable()
            extras.append(pytest_html.extras.html(htmlCode))
            helper_instance.clear_compare_array()

    report.extra = extras
    return report
#====================== pytest html report ======================


 
