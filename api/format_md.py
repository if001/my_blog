import datetime
import os
import re
import subprocess

base_dir = "/work/blog/"
create_dir = "content/post"


class FormatMd():
    def __header(self, time, draft, title, slug, tags):
        header_prefix = "+++"
        h = """{}
date = \"{}\"
draft = {}
title = \"{}\"
slug = \"{}\"
tags = {}
{}""".format(header_prefix, time, draft, title, slug, tags, header_prefix)
        return h

    def format(self, time, draft, title, slug, tags_str, body):
        header = self.__header(time, draft, title, slug, tags_str)
        return header + "\n" + body


class CreateMd():
    def test_create(self):
        print("test create")
        res = self.create("Title title!", ["tag1", "tag2"], "body", True)
        print(res)

    def test_dir(self):
        now = datetime.datetime.now()
        print("test dir")
        print(self.__dirStr(now))

    def create(self, title, tags, body, draft):
        now = datetime.datetime.now()
        # 日付からディレクトリを生成
        md_dir = os.path.join(
            base_dir, create_dir, self.__dirStr(now))

        # # ディレクトリの存在確認 なければ作成
        # if not(os.path.exists(md_dir)):
        #     os.makedirs(md_dir)
        #     print("create " + md_dir)

        # slug(url)の作成
        slug = self.__to_slug(title)
        md_file_name = slug + ".md"

        md_str = FormatMd().format(now, draft, title, slug, tags, body)
        print("md_str:", md_str)

        # mdの作成
        cmd = 'hugo new ' + \
            os.path.join("post", self.__dirStr(now), md_file_name) + "--log"
        cwd = os.path.join(base_dir, "blog")
        res = subprocess.call(cmd.split(), cwd=cwd)

        if res == 0:
            with open(os.path.join(md_dir, md_file_name), "w") as f:
                f.writelines(md_str)
        return md_str

    def __dirStr(self, now):
        return str(now.year) + "/" + str(now.month)

    def __to_slug(self, title):
        tmp_title = title.lower()
        tmp_title = re.sub(re.compile("[!-/:-@[-`{-~]"), '', tmp_title)
        splited_title = tmp_title.split(" ")
        slug = "-".join(splited_title)
        return slug


def main():
    CreateMd().test_dir()
    CreateMd().test_create()


if __name__ == "__main__":
    main()
