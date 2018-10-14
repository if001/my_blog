"""
python3 md_article_request.py target.md

md format is 
title=title
slug=slug
tags=tag1,tag2
body
"""

import urllib.request
import json
import sys
import re
import json
import argparse

# headers = {'content-type': 'application/x-www-form-urlencoded'}


class Requester():
    def __init__(self, token):
        self.host = "127.0.0.1"
        # self.host = "35.221.100.217"
        # self.host = "www.if-blog.site"
        self.port = "8000"
        self.base_url = "http://" + self.host + ":" + self.port
        self.headers = {'content-type': 'application/json'}
        self.token = token

    def gen_url(self, uri):
        return self.base_url + uri + "?password=" + self.token

    def post(self, uri, json_data):
        url = self.gen_url(uri)
        print("repuest to " + url)
        request = urllib.request.Request(
            url, data=json_data, method="POST", headers=self.headers)
        return request

    def get(self, uri):
        url = self.gen_url(uri)
        print("repuest to " + url)
        request = urllib.request.Request(
            url, method="GET", headers=self.headers)
        return request


def get_param(key, line):
    if key in line:
        raw_title = line
        tmp_title = re.sub('\n', '', raw_title)
        param = tmp_title.split("=")[-1]
        return param
    else:
        raise ValueError("key must be set!!")


def request_md(requester, file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    title = get_param('title', lines[0])
    slug = get_param('slug', lines[1])
    tags = get_param('tag', lines[2])
    body = "".join(lines[3:])
    json_data = json.dumps({'title': title,
                            'slug': slug,
                            'tags': tags,
                            'body': body}).encode("utf-8")
    print(json_data)
    request = requester.post("/article", json_data)

    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print("response:", response_body)


def build_request(requester):
    request = requester.get("/build")
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print("response:", response_body)


def main():
    parser = argparse.ArgumentParser(description='hugo request')
    parser.add_argument('--token', '-t', type=str, required=True)
    parser.add_argument('--source', '-s', type=str, default="none")
    args = parser.parse_args()

    requester = Requester(args.token)
    if args.source == "none":
        build_request(requester)
    else:
        request_md(requester, args.source)
        build_request(requester)


if __name__ == "__main__":
    main()
