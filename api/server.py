import json
import falcon
from format_md import CreateMd
import os
import subprocess

base_dir = "/Users/issei/prog/go_lang/my_blog/"


def to_resp(status_code, contents):
    resp = {
        "status": status_code,
        "contents": contents
    }
    return json.dumps(resp)


class HealthCheck(object):
    def on_get(self, req, resp):
        resp.body = to_resp(200, "ok")


class Build(object):
    def on_get(self, req, resp):
        cmd = 'hugo'
        cwd = os.path.join(base_dir, "blog")
        res = subprocess.call(cmd.split(), cwd=cwd)
        # todo ビルドに失敗したらエラーリスポンスを返す
        if res == 0:
            resp.body = to_resp(200, "ok")
        if res == 0:
            resp.body = to_resp(500, "build error")


def article_article_parse(req):
    body = req.stream.read().decode("utf-8")
    data = json.loads(body)
    title = data['title']
    tags = data['tags']
    article_body = data['body']
    return title, tags, article_body


def to_array(st):
    tmp = st[1:-1]
    if "," in tmp:
        return tmp.split(",")
    else:
        return [tmp]


class AddArticle(object):
    def on_post(self, req, resp):
        title, tags, body = article_article_parse(req)
        # todo tagのフォーマットが間違っていたら、エラーリスポンスを返す
        tags_str = to_array(tags)
        CreateMd().create(title, tags_str, body, draft="false")
        resp.body = to_resp(200, "create article")


class AddDraftArticle(object):
    def on_post(self, req, resp):
        title, tags, body = article_article_parse(req)
        CreateMd().create(title, tags, body, draft="true")
        resp.body = to_resp(200, "create draft article")


def handle_404(req, resp):
    resp.body = to_resp(400, "not found end point")


app = falcon.API()
app.add_route("/", HealthCheck())
app.add_route("/build", Build())
app.add_route("/article", AddArticle())
app.add_route("/article/draft", AddDraftArticle())
app.add_sink(handle_404, '')


if __name__ == "__main__":
    from wsgiref import simple_server
    print("start server")
    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", 8000)
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
