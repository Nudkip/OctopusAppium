# coding=utf-8
from appium import webdriver
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

# sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "./utils"))))
# compare screenShot class
from VisualComparison import *
# screenShot Counter class
from ScreenShotCount import *

import Constant
from selenium.webdriver.support import expected_conditions as ec 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# generate html code
import dominate
from dominate.tags import *

logging.basicConfig(level=logging.CRITICAL)

diffFound = False

class Helper:
	def swipe_down(driver, start_x, start_y, end_x, end_y):
		actions = ActionChains(driver)
		#创建输入设备
		finger1 = actions.w3c_actions.add_pointer_input('touch','finger1')
		#输入设备移动
		finger1.create_pointer_move(x=start_x,y=start_y)
		#输入设备移动
		finger1.create_pointer_move(x=end_x,y=end_y)
		#按下输入设备的鼠标左键
		#执行actions对象的动作序列
		actions.perform()

	def printLog():
		print("on99")

	def scroll_until_element_found(driver, xpath, max_attempts=5):
		for _ in range(max_attempts):
			try:
				element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
				print("Element found!")
				return element
			except:
				print("Element not found, swiping down...")
				swipe_down(driver, 200, 600, 200, 200, duration=800)
		raise Exception("Element not found after max attempts")
