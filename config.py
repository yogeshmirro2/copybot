import os

class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
    APP_ID = int(os.environ.get("APP_ID"))
    API_HASH = os.environ.get("API_HASH")
    TO_CHANNEL = int(os.environ.get("CHANNEL_ID"))
    FROM_CHANNEL = int(os.environ.get("FROM_CHANNEL"))
