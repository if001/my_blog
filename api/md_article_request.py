"""
python3 md_article_request.py target.md

md format is 
title=title
tags=tag1,tag2
body
"""

import urllib.request
import json
import sys
import re
import json


host = "127.0.0.1"
host = "35.221.100.217"
port = "8000"
url = "http://" + host + ":" + port
headers = {'content-type': 'application/json'}
# headers = {'content-type': 'application/x-www-form-urlencoded'}


def get_param(key, line):
    if key in line:
        raw_title = line
        tmp_title = re.sub('\n', '', raw_title)
        param = tmp_title.split("=")[-1]
        return param
    else:
        raise ValueError("key must be set!!")


def request_md(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    title = get_param('title', lines[0])
    tags = get_param('tag', lines[1])
    body = "".join(lines[2:])
    json_data = json.dumps({'title': title, 'tags': tags,
                            'body': body}).encode("utf-8")
    print(json_data)
    post_url = url + "/article"
    request = urllib.request.Request(
        post_url, data=json_data, method="POST", headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)


def build_request():
    post_url = url + "/"
    request = urllib.request.Request(
        post_url, method="GET", headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)


def main():
    if len(sys.argv) != 2:
        print("invalid argument")
        exit(-1)
    file_name = sys.argv[-1]
    request_md(file_name)
    build_request()


if __name__ == "__main__":
    main()
