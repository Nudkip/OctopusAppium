

lsof -i :4723
kill -9 [PID]

appium --allow-cors
<!-- appium -a 0.0.0.0 -p 4723    -->
WebDriverAgentRunner installation

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

python3 -m venv venv

pip3 install Pillow
pip3 install appium-python-client
pip3 install pytest
pip3 install py
pip3 install dominate