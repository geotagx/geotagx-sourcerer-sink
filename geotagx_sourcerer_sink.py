#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
import sys
import time
import datetime
import base64
import json
import random

from pybossa.core import db, create_app, sentinel
from pybossa.model.task import Task
from pybossa.model.category import Category
from pybossa.model.project import Project

TIME_DELAY = 1 # 0.5 seconds, or check every half a second
DELIMITER = "%%%%"

def _now():
	return datetime.datetime.utcnow()

def main():
	app = create_app(run_as_server=False)
	with app.app_context():
		def timer_function():
			#Continue code here
			image_source = sentinel.slave.lpop("GEOTAGX-SOURCERER-QUEUE")
			if image_source:
				split_image_source = image_source.split(DELIMITER)
				base64Data = split_image_source[-1]
				decodedJSONString = base64.b64decode(base64Data)
				parsedJSONObject = json.loads(decodedJSONString)

				if parsedJSONObject['source'] == 'geotagx-chrome-sourcerer':
					#Handle Chrome Sourcerer
					#TODO : Refactor into an OOP based implementation
					
					SOURCE_URI = parsedJSONObject['source_uri']
					IMAGE_URL = parsedJSONObject['image_url']
					print SOURCE_URI, IMAGE_URL
					for category in parsedJSONObject['categories']:
						category_objects = Category.query.filter(Category.short_name == category)
						for category_object in category_objects:
							related_projects = Project.query.filter(Project.category == category_object)
							for related_project in related_projects:
								print related_project.name

								# Start building Task Object
								_task_object = Task()
								_task_object.project_id = related_project.id

								# Build Info Object from whatever data we have
								_info_object = {}
								_info_object['image_url'] = IMAGE_URL
								_info_object['source_uri'] = SOURCE_URI
								_info_object['id'] = parsedJSONObject['source'] + "_" + \
													''.join(random.choice('0123456789ABCDEF') for i in range(16))

								_task_object.info = _info_object

								db.session.add(_task_object)
								db.session.commit()
								print _now(), _task_object								
			else:
				print _now(), "GEOTAGX-SOURCERER-QUEUE Empty....."

	while True:
		timer_function()
		time.sleep(TIME_DELAY)


main()