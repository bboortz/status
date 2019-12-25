#!/bin/sh


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
	local option="$1"
	local url="$2"
	local content_type="${3}"
	local expected_code="${4}"
	shift
	shift
	shift
	shift
	local data="$@"

	curl_cmd="$CURL -X ${option} ${url}"

	local http_code
	if [ -z "${data}" ]; then
		echo -e "\nCURL: ${curl_cmd}" -H "Content-Type: ${content_type}"
		http_code=$( ${curl_cmd} -H "Content-Type: ${content_type}" )
	else
		echo -e "\nCURL: ${curl_cmd}" -H "Content-Type: ${content_type} -d ${data}"
		http_code=$( ${curl_cmd} -H "Content-Type: ${content_type}" -d "${data}" -H "X-API_KEY: ${API_KEY}" )
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
do_curl "GET"    "http://${HOST}:${PORT}"              "text/html"        "200"
do_curl "GET"    "http://${HOST}:${PORT}/"             "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "403"
do_curl "DELETE" "http://${HOST}:${PORT}/api/motd"     "application/json" "200" '1'

sleep 1
do_curl "POST"   "http://${HOST}:${PORT}/api/services" "application/json" "405"
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "403"
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services are ok" }'
do_curl "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "DELETE" "http://${HOST}:${PORT}/api/motd"     "application/json" "200" '1'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services are still ok" }'
do_curl "POST"   "http://${HOST}:${PORT}/api/event"    "application/json" "201" '{ "title": "change scheduled", "description": "A change has been scheduled." }'
do_curl "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service2", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services are still ok" }'
do_curl "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service2", "score": 50 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services2 is broken" }'
do_curl "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service2", "score": 50 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services2 is broken" }'
do_curl "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service0", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service1", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/service"  "application/json" "201" '{ "name": "service2", "score": 100 }'
do_curl "POST"   "http://${HOST}:${PORT}/api/event"    "application/json" "201" '{ "title": "service2 had an outage", "description": "After the change service2 was broken. Now it is repaired again." }'
do_curl "POST"   "http://${HOST}:${PORT}/api/motd"     "application/json" "201" '{ "message": "services are ok again" }'
do_curl "GET"    "http://${HOST}:${PORT}/api/motd"     "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/services" "application/json" "200"
do_curl "GET"    "http://${HOST}:${PORT}/api/events"   "application/json" "200"

sleep 1
do_curl "GET"    "http://${HOST}:${PORT}/api/export"   "application/json" "200" '1'
do_curl "POST"    "http://${HOST}:${PORT}/api/import"  "application/json" "201" '{
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
do_curl "POST"    "http://${HOST}:${PORT}/api/import"  "application/json" "201" '{
  "events": [
  ], 
  "motd": {
  }, 
  "services": [
  ]
}'
do_curl "POST"    "http://${HOST}:${PORT}/api/import"  "application/json" "201" '{
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
