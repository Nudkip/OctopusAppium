from PIL import Image,ImageDraw,ImageFont
import os
import sys
import logging
import Constant
import shutil
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))))
from conftest import *

class VisualComparison:

	def analyze(self, screenShotTestingPath, screenShotSourcePath):
		diffFound = False
		screenShotTesting = Image.open(screenShotTestingPath)
		screenShotSource = Image.open(screenShotSourcePath)
		path, fileName = os.path.split(screenShotTestingPath)
		diffDirectoryPath = "%s/diff" % (path)
		if not (os.path.isdir(diffDirectoryPath)) :
			os.makedirs( diffDirectoryPath, 0o755 )
			print('\n%s %s' % (diffDirectoryPath, 'diff directory is created'))

		diffFullPath = '%s/%s' %(diffDirectoryPath, fileName)
		comparisonResultPath = str(diffFullPath).replace(".png", "Diff.png")
		shutil.copy(screenShotTestingPath, comparisonResultPath)
		comparisonResultImg = Image.open(comparisonResultPath)
		
		screen_width, screen_height = screenShotTesting.size

		block_width = 10
		block_height = 10
			
		for y in range(0, screen_height, block_height+1):
			for x in range(0, screen_width, block_width+1):
				region_staging = self.process_region(screenShotTesting, x, y, block_width, block_height)
				region_production = self.process_region(screenShotSource, x, y, block_width, block_height)

				if region_staging is not None and region_production is not None and region_production != region_staging:
					diffFound = True
					draw = ImageDraw.Draw(comparisonResultImg)
					draw.rectangle((x, y, x+block_width, y+block_height), outline = "red")

		comparisonResultImg.save(comparisonResultPath)

		if diffFound:
			conftest.diffFound = True
			print("Found Diff")
			return comparisonResultPath
		else:
			print("No Diff")
			return None

	def process_region(self, image, x, y, width, height):
		region_total = 0

		# This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
		factor = 1000

		for coordinateY in range(y, y+height):
			for coordinateX in range(x, x+width):
				try:
					pixel = image.getpixel((coordinateX, coordinateY))
					region_total += sum(pixel)/4
				except:
					return

		return region_total/factor
