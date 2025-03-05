# coding=utf-8
import pytest
import os
import sys   
import logging
from time import sleep
import sys
import pytest_html
from dominate.tags import *

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "./util"))))
from Helper import Helper

from appium.webdriver import Remote
from appium.options.common.base import AppiumOptions

logging.basicConfig(level=logging.CRITICAL)

diffFound = False

# --------------------- @pytest.fixture ---------------------
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
		"appium:noReset": False,
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
	owPath = config.getoption('--owPath')
	pytest.global_owPath = owPath
	oosPath = config.getoption('--oosPath')
	pytest.global_oosPath = oosPath
 
	config.option.html_show_all = True  # Show extras for all tests

	pytest.sharedHelper = Helper()


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

@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
	cells.pop(3)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
	outcome = yield
	report = outcome.get_result()
	extras = getattr(report, "extras", [])

	# if report.when in ('call', 'setup'):
	xfail = hasattr(report, "wasxfail")
	if (report.skipped and xfail) or (report.failed and not xfail):
		screenshot = pytest.sharedHelper.driver.get_screenshot_as_base64()
		html = f'<p><img src="data:image/png;base64,{screenshot}" alt="screenshot" style="width:270px;height:480px;" align="left"/></p>'
		extras.append(pytest_html.extras.html(html))
	elif report.passed and report.when != 'setup':
		htmlCode = pytest.sharedHelper.createVisualComparisonTable()  # Ensure this function returns valid HTML
		extras.append(pytest_html.extras.html(htmlCode))
	report.extras = extras

	return report

#====================== pytest html report ======================


 
