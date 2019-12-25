#!/bin/bash


#
# confg
#
HOST="${1:-localhost}"
PORT="${2:-5000}"
CURL="curl --fail --silent -o /dev/null -w %{http_code}"
API_KEY="KDDhzT5FvHzxqs2f-77QNysPgh0iughuj-xULyaYEkav9oeLT7"
ERRORS=0



#
# method
#
do_curl() {
	local with_api_key="${1}"
	local option="${2}"
	local url="${3}"
	local content_type="${4}"
	local expected_code="${5}"
	shift
	shift
	shift
	shift
	shift
	local data="$@"

	curl_cmd="$CURL -X ${option} ${url}"

	local http_code
	if [ "${with_api_key}" == "1" ]; then
		set -x
		http_code=$( ${curl_cmd} -H "Content-Type: ${content_type}" -d "${data}" -H "X-API_KEY: ${API_KEY}" )
		set +x
	else
		if [ "${option}" == "POST" ]; then
			set -x
			http_code=$( ${curl_cmd} -H "Content-Type: ${content_type}" -H "Content-Length: 0")
			set +x
		else
			set -x
			http_code=$( ${curl_cmd} -H "Content-Type: ${content_type}" )
			set +x
		fi
	fi
	echo "  http_code: ${http_code}"
	if [ "${http_code}" != "${expected_code}" ]; then
		let ERRORS=$ERRORS+1
		echo "  ERROR!"
		echo "    http_code: ${http_code} != ${expected_code}"
	else
		echo "  SUCCESS!"
	fi
}



if [ "${HOST}" == "localhost" ]; then
	#
	# prepare
	#
	source .venv/bin/activate



	#
	# pytest
	#
	echo -e "\nRUNNING PYTEST UNIT TESTS"
	cd app
	pytest
	cd ..



	#
	# running application in dev mode
	#
	echo -e "\nRUNNING THE APPLICATION"
	DEV=1 timeout 10 ./run.sh > testrun.log 2>&1 &
fi



#
# test run
#
echo -e "\nSIMULATING TESTS"
sleep 1
do_curl "0" "GET"    "http://${HOST}:${PORT}"              "text/html"        "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/"             "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "0" "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "403"
do_curl "1" "DELETE" "http://${HOST}:${PORT}/api/motd"     "application/json" "200"

sleep 1
do_curl "0" "POST"   "http://${HOST}:${PORT}/api/services" "application/json" "405"
do_curl "0" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "403"
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services are ok" }'
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "1" "DELETE" "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services are still ok" }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/event"    "application/json" "201" '{ "title": "change scheduled", "description": "A change has been scheduled." }'
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service2", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services are still ok" }'
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service2", "score": 50 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services2 is broken" }'
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service2", "score": 50 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services2 is broken" }'
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service2", "score": 100 }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/event"    "application/json" "201" '{ "title": "service2 had an outage", "description": "After the change service2 was broken. Now it is repaired again." }'
do_curl "1" "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services are ok again" }'
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "0" "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "1" "GET"    "http://${HOST}:${PORT}/api/export"   "application/json" "200"
do_curl "1" "POST"    "http://${HOST}:${PORT}/api/import"  "application/json" "201" '{
  "events": [
    {
      "description": "A change has been scheduled.", 
      "title": "change scheduled", 
      "updated": "2019-04-20 18:27:21 CEST"
    }, 
    {
      "description": "After the change service2 was broken. Now it is repaired again.", 
      "title": "service2 had an outage", 
      "updated": "2019-04-20 18:27:25 CEST"
    }
  ], 
  "motd": {
    "message": "services are ok again", 
    "updated": "2019-04-20 18:27:25 CEST"
  }, 
  "services": [
    {
      "name": "service0", 
      "score": 100, 
      "updated": "2019-04-20 18:27:25 CEST"
    }, 
    {
      "name": "service1", 
      "score": 100, 
      "updated": "2019-04-20 18:27:25 CEST"
    }, 
    {
      "name": "service2", 
      "score": 100, 
      "updated": "2019-04-20 18:27:25 CEST"
    }
  ]
}'
do_curl "1" "POST"    "http://${HOST}:${PORT}/api/import"  "application/json" "201" '{
  "events": [
  ], 
  "motd": {
  }, 
  "services": [
  ]
}'
do_curl "1" "POST"    "http://${HOST}:${PORT}/api/import"  "application/json" "201" '{
  "events": [
    {
      "description": "A change has been scheduled.", 
      "title": "change scheduled", 
      "updated": "2019-04-20 18:27:21 CEST"
    }, 
    {
      "description": "After the change service2 was broken. Now it is repaired again.", 
      "title": "service2 had an outage", 
      "updated": "2019-04-20 18:27:25 CEST"
    }
  ], 
  "motd": {
    "message": "services are ok again", 
    "updated": "2019-04-20 18:27:25 CEST"
  }, 
  "services": [
    {
      "name": "service0", 
      "score": 100, 
      "updated": "2019-04-20 18:27:25 CEST"
    }, 
    {
      "name": "service1", 
      "score": 100, 
      "updated": "2019-04-20 18:27:25 CEST"
    }, 
    {
      "name": "service2", 
      "score": 100, 
      "updated": "2019-04-20 18:27:25 CEST"
    }
  ]
}'



#
# finalize
#
if [ "${HOST}" == "localhost" ]; then
	deactivate
fi
echo -e "\n\n$ERRORS ERRORS FOUND!"
exit $ERRORS
