"""
python3 md_article_request.py target.md

md format is 
title=title
slug=slug
tags=tag1,tag2
body
"""

# import urllib.request
import requests
import json
import sys
import re
import json
import argparse
import os


# headers = {'content-type': 'application/x-www-form-urlencoded'}


class Requester():
    def __init__(self, token):
        # self.host = "127.0.0.1"
        # self.host = "35.221.100.217"
        self.host = "www.if-blog.site"
        self.port = "8000"
        self.base_url = "http://" + self.host + ":" + self.port
        self.headers = {'content-type': 'application/json'}
        self.img_headers = {'Content-Type': 'multipart/form-data'}
        self.token = token

    def gen_url(self, uri):
        return self.base_url + uri + "?password=" + self.token

    def post(self, uri, json_data):
        url = self.gen_url(uri)
        print("repuest to " + url)
        response = requests.post(url, json_data, headers=self.headers)
        return response

    def post_img(self, uri, image_name, image):
        url = self.gen_url(uri)
        print("repuest to " + url)
        files = {'file': (image_name, image)}
        response = requests.post(url, files=files)
        return response

    def get(self, uri):
        url = self.gen_url(uri)
        print("repuest to " + url)
        response = requests.get(url, headers=self.headers)
        return response


def get_param(key, line):
    if key in line:
        raw_title = line
        tmp_title = re.sub('\n', '', raw_title)
        param = tmp_title.split("=")[-1]
        return param
    else:
        raise ValueError("key must be set!!")


def get_images(body):
    figure_line = list()
    for b in body.split("\n"):
        # 先頭にスラッシュがあるとエスケープ
        if ("figure src=" in b) and (b[0] != "\\"):
            figure_line.append(b)

    images = list()
    for l in figure_line:
        tmp = l.split(" ")
        for t in tmp:
            if "src" in t:
                # imageの先頭のスラッシュを一つ取り除く
                images.append(t.split("=")[-1][2:-1])
    return images


def request_md(requester, file_name, draft_flag):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    title = get_param('title', lines[0])
    slug = get_param('slug', lines[1])
    tags = get_param('tag', lines[2])
    body = "".join(lines[3:])
    json_data = json.dumps({'title': title,
                            'slug': slug,
                            'tags': tags,
                            'body': body}).encode("utf-8")
    # 画像のアップロード
    image_files = get_images(body)
    for img in image_files:
        try:
            print(img)
            with open(img, "rb") as f:
                uri = "/image"
                response = requester.post_img(uri, img, f)
                print(response.headers)
                print(response.text)
        except IOError:
            print("image open error " + img)

    if draft_flag == "false":
        response = requester.post("/article", json_data)
    elif draft_flag == "true":
        response = requester.post("/article/draft", json_data)
    else:
        build_request(requester)
    print(response.text)


def build_request(requester):
    response = requester.get("/build")
    print(response.text)


def main():
    parser = argparse.ArgumentParser(description='hugo request')
    parser.add_argument('--token', '-t', type=str, required=True)
    parser.add_argument('--source', '-s', type=str, default="none")
    parser.add_argument('--draft', '-d', type=str, default="false")
    args = parser.parse_args()

    requester = Requester(args.token)
    if args.source == "none":
        build_request(requester)
    else:
        if args.draft == "false":
            request_md(requester, args.source, args.draft)
        elif args.draft == "true":
            request_md(requester, args.source, args.draft)
        else:
            raise ValueError("draft flag invalid")
        build_request(requester)


if __name__ == "__main__":
    main()
