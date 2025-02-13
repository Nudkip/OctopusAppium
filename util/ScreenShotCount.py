class ScreenShotCount:
	def __init__(self,counter=1):
		self.counter= counter

	def setCounter(self, newCounter):
		self.counter= newCounter
		
	def getCounter(self):
		return self.counter
