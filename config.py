class Config:
	def __init__(self):
		self.MONGO_URI: str = "mongodb://root:password@localhost:27017/"
		self.queue_name = 'web-8'
