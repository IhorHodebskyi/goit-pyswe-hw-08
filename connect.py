from mongoengine import connect
from config import Config


config = Config()

connect(db="dbname", host=config.MONGO_URI)






