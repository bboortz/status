import datetime

from app import app
from app import repo
from app.utils import get_current_time, config

from flask import render_template

from markupsafe import Markup



##
## *Web methods*
##

#
# index
#


# CURL: curl -i -X GET http://localhost:5000/
# NO INPUT
# OUTPUT: HTML
@app.route('/')
def index():
	status = "OK"
	status_ico = "ok.svg"
	for s in repo.services:
		if s['score'] != 100:
			status = "WARNING"
			status_ico = "warning.png"
			break

	repo.events.sort(key=lambda item:item['updated'], reverse=True)

	return render_template('index.html',
		config=config,
		links=config['links'],
		status=status,
		status_ico=status_ico,
		motd=repo.motd,
		services=repo.services,
		events=repo.events)
