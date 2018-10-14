import json
import falcon
from falcon.http_error import HTTPError
import falcon.status_codes as status
from format_md import CreateMd
import os
import subprocess
import base64
from conf import Conf

TOKEN = "aG9nZWhvZ2U=".encode('utf-8')


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
    print("hugahuga")
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
        cmd = 'hugo'
        cwd = os.path.join(Conf.base_dir)

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
    article_body = data['body']
    return title, slug, tags, article_body


def to_array(st):
    tmp = st[1:-1]
    if "," in tmp:
        return tmp.split(",")
    else:
        return [tmp]


@falcon.before(check_token)
class AddArticle(object):
    def on_post(self, req, resp):
        title, slug, tags, body = article_article_parse(req)
        # todo tagのフォーマットが間違っていたら、エラーリスポンスを返す
        tags_str = to_array(tags)
        CreateMd().create(title, slug, tags_str, body, draft="false")
        resp.body = to_resp(200, "create article")


@falcon.before(check_token)
class AddDraftArticle(object):
    def on_post(self, req, resp):
        title, slug, tags, body = article_article_parse(req)
        CreateMd().create(title, slug, tags, body, draft="true")
        resp.body = to_resp(200, "create draft article")


def handle_404(req, resp):
    resp.body = to_resp(400, "not found end point")


app = falcon.API(middleware=[CORSMiddleware()])
app.add_route("/", HealthCheck())
app.add_route("/build", Build())
app.add_route("/article", AddArticle())
app.add_route("/article/draft", AddDraftArticle())
app.add_sink(handle_404, '')


if __name__ == "__main__":
    from wsgiref import simple_server
    print("start server")
    # host = os.getenv("HOST", "0.0.0.0")
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", 8000)
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
