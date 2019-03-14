#!/usr/bin/env python3

import os
import json
from aliyunsdkcore import client
from aliyunsdkcms.request.v20180308 import QueryMetricListRequest
import time

ACCESS_KEY = os.environ.get('ALICLOUD_ACCESS_KEY')
SECRET_KEY = os.environ.get('ALICLOUD_SECRET_KEY')
REGION 	   = os.environ.get('ALICLOUD_REGION')


def get_client():
	return client.AcsClient(ACCESS_KEY, SECRET_KEY, REGION)

def get_dimensions_json():
	return json.dumps({
		'cenId': 'cen-io8olhs9j9bquumh9l',
		'geographicSpanId': 'China'
	})

def get_request(dimensions_json):
	request = QueryMetricListRequest.QueryMetricListRequest()
	request.set_accept_format('json')
	request.set_Project('acs_cen')
	request.set_Metric('InternetOutRatePercentByConnectionRegion')
	start_time = "2019-03-01 10:00:00"
	timestamp_start = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) * 1000
	request.set_StartTime(timestamp_start)
	request.set_Dimensions(dimensions_json)
	request.set_Period('60')

	return request

if __name__ == '__main__':
	client = get_client()
	dimensions_json = get_dimensions_json()
	request = get_request(dimensions_json)
	result = client.do_action_with_exception(request)
	print(result)