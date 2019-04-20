# statusboard



# key features

* Web Ui which is showing
    * message of the day (motd)
	* status of services
	* events
* REST API to 
	* CRUD motd
	* CRUD status of services
	* CRUD events
	* import / export motd, status and events
* Testcases for every REST call
* configurable using an environment variable



# How to


## install the needed software

```
pip install -U -r requirements.txt
```


## How to run for development?

```
export STATUS_CONFIG='{ "team": "Authentication Delivery Center", "refresh_interval": 15, "api_key": "1111111", "links": { "team": "https://adc" } }'
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```


## How to run for production?

```
export STATUS_CONFIG='{ "team": "Authentication Delivery Center", "refresh_interval": 15, "api_key": "1111111", "links": { "team": "https://adc" } }'
export FLASK_ENV=production
flask run
```


## How to unit test the software?

```
export STATUS_CONFIG='{ "team": "Authentication Delivery Center", "refresh_interval": 15, "api_key": "1111111", "links": { "team": "https://adc" } }'
export FLASK_ENV=production
flask run
```



# planned features

* protected REST API with API key
* packaged with docker container
* RSS feed
* desktop notification
* mail notification

