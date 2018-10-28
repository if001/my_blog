import json
import falcon
from falcon.http_error import HTTPError
import falcon.status_codes as status
from format_md import CreateMd
from falcon_multipart.middleware import MultipartMiddleware

import os
import subprocess
import base64
from conf import Conf
import argparse


TOKEN = "aG9nZWhvZ2U=".encode('utf-8')
BASE_DIR = ""
CREATE_DIR = ""
CREATEMD = None


class CORSMiddleware:
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')


def to_resp(status_code, contents):
    resp = {
        "status": status_code,
        "contents": contents
    }
    return json.dumps(resp)


# class MyHTTPError(Exception):
#     def __init__(self, status, status_code, contents=None):
#         self.status = status
#         self.status_code = status_code
#         self.contents = contents


# class BadAuthToken(MyHTTPError):
#     def __init__(self, status_code, contents):
#         super(BadAuthToken, self).__init__(
#             status.HTTP_200, status_code, contents)

def check_token(req, resp, resource, params):
    params = req.params
    if 'password' not in params.keys():
        raise falcon.HTTPBadRequest('Token not found', "")
    password = params['password']
    enc_token = base64.b64encode(password.encode('utf-8'))
    if enc_token != TOKEN:
        raise falcon.HTTPBadRequest('Invalid Token', "")
        # raise BadAuthToken("200", "invalid token")


@falcon.before(check_token)
class HealthCheck(object):
    def on_get(self, req, resp):
        resp.body = to_resp(200, "ok")


@falcon.before(check_token)
class Build(object):
    def on_get(self, req, resp):
        cmd = 'hugo -t hugo-theme-geppaku'
        cwd = os.path.join(BASE_DIR)
        # todo ビルドに失敗したらエラーリスポンスを返す
        try:
            res = subprocess.check_call(cmd.split(), cwd=cwd)
            resp.body = to_resp(200, str(res))
        except subprocess.CalledProcessError:
            resp.body = to_resp(500, "build error")


def article_article_parse(req):
    body = req.stream.read().decode("utf-8")
    data = json.loads(body)
    title = data['title']
    slug = data['slug']
    tags = data['tags']
    description = data['description']
    article_body = data['body']
    return title, slug, tags, description, article_body


def to_array(st):
    tmp = st[1:-1]
    if "," in tmp:
        return tmp.split(",")
    else:
        return [tmp]


@falcon.before(check_token)
class AddArticle(object):
    def on_post(self, req, resp):
        title, slug, tags, description, body = article_article_parse(req)
        # todo tagのフォーマットが間違っていたら、エラーリスポンスを返す
        tags_str = to_array(tags)
        CREATEMD.create(title, slug, tags_str, description, body, draft="false")
        resp.body = to_resp(200, "create article")


@falcon.before(check_token)
class AddDraftArticle(object):
    def on_post(self, req, resp):
        title, slug, tags, body = article_article_parse(req)
        CREATEMD.create(title, slug, tags, body, draft="true")
        resp.body = to_resp(200, "create draft article")


@falcon.before(check_token)
class UploadImage(object):
    def on_post(self, req, resp):
        image = req.get_param('file')
        raw = image.file.read()
        image_name = image.filename
        filepath = os.path.join(BASE_DIR, "static", image_name)
        try:
            with open(filepath, 'wb') as f:
                f.write(raw)
        except IOError:
            print("save file faild :" + filepath)
        resp.body = to_resp(200, "save img " + filepath)


def handle_404(req, resp):
    resp.body = to_resp(400, "not found end point")


def handle_200(req, resp):
    resp.body = to_resp(200, "ok")


app = falcon.API(middleware=[CORSMiddleware(), MultipartMiddleware()])
app.add_route("/", HealthCheck())
app.add_route("/build", Build())
app.add_route("/article", AddArticle())
app.add_route("/article/draft", AddDraftArticle())
app.add_route("/image", UploadImage())
app.add_sink(handle_200, "/.well-known/acme-challenge/.*")
app.add_sink(handle_404, '')


if __name__ == "__main__":
    from wsgiref import simple_server
    parser = argparse.ArgumentParser(description='api server for hugo')
    parser.add_argument('--mode', '-m', type=str, required=True)
    args = parser.parse_args()

    print("start server")
    print("server mode " + args.mode)
    conf = Conf(args.mode)
    CREATEMD = CreateMd(conf)

    BASE_DIR = conf.base_dir
    CREATE_DIR = conf.create_dir
    httpd = simple_server.make_server(conf.host, conf.port, app)
    httpd.serve_forever()
