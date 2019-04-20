
import os
import datetime
import pytz
import json



def get_current_time():
	tz = pytz.timezone('Europe/Berlin')
	t = datetime.datetime.now(tz)
	return t.strftime("%Y-%m-%d %H:%M:%S %Z")


def read_config():
	config_default = '{ "team": "Your Team", "refresh_interval": 15, "api_key": "KDDhzT5FvHzxqs2f-77QNysPgh0iughuj-xULyaYEkav9oeLT7", "links": { "team": "https://yourteam" } }'
	config = os.environ.get('STATUS_CONFIG', config_default)
	return json.loads(config)



config = read_config()
print("*CONFIGURATION LOADED*")
print(json.dumps(config, sort_keys=True, indent=4))

