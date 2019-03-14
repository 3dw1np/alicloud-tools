#!/usr/bin/env python3

import os
import time
import uuid
import hmac
import base64
import hashlib
import datetime
import urllib.parse

import requests

ACCESS_KEY = os.environ.get('ALICLOUD_ACCESS_KEY')
SECRET_KEY = os.environ.get('ALICLOUD_SECRET_KEY')
REGION     = os.environ.get('ALICLOUD_REGION')

BASE_URL_API = 'https://ecs.aliyuncs.com/'


def get_alicloud_uri(params):
    # Add mandatory parameters:
    params.setdefault('AccessKeyId', ACCESS_KEY)
    params.setdefault('SignatureMethod', 'HMAC-SHA1')
    params.setdefault('SignatureVersion', '1.0')
    params.setdefault('SignatureNonce', str(uuid.uuid4()))
    params.setdefault('Timestamp', datetime.datetime.utcnow().isoformat())
    params.setdefault('Version', '2014-05-26')
    params.setdefault('Format', 'json')

    # Generate the canonicalized query string
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    encoded_params = urllib.parse.urlencode(sorted_params)

    # Generate the Signature
    string_to_sign = 'GET' + '&' + urllib.parse.quote_plus('/') + '&' + urllib.parse.quote(encoded_params)
    h = hmac.new(SECRET_KEY.encode('utf-8') + b'&', string_to_sign.encode('utf-8'), hashlib.sha1)
    signature = base64.encodebytes(h.digest()).strip()

    return '{base_url_api}?{params}&Signature={signature}'.format(base_url_api=BASE_URL_API, params=encoded_params, signature=urllib.parse.quote_plus(signature.decode()))

if __name__ == '__main__':
    answer = requests.get(get_alicloud_uri({'Action': 'DescribeRegions'}))
    answer.raise_for_status()
    print(answer.json())
