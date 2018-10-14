import os


class Conf():
    def __init__(self, mode):
        if mode == "prob":
            self.base_dir = "/work/blog/"
            self.create_dir = "content/post"
            self.host = "0.0.0.0"
            self.port = 8000
            # 環境変数から読み込む場合
            # host = os.getenv("HOST", "0.0.0.0")
            # port = os.getenv("PORT", 8000)
        elif mode == "dev":
            self.base_dir = "/Users/issei/prog/go_lang/my_blog/blog"
            self.create_dir = "content/post"
            self.host = "0.0.0.0"
            self.port = 8000
        else:
            raise ValueError("invalid mode")
