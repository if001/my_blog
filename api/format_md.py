import datetime
import os
import re
import subprocess
from conf import Conf


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
    def __init__(self, conf):
        self.conf = conf

    def test_create(self):
        print("test create")
        res = self.create("Title title!", "title", [
                          "tag1", "tag2"], "body", True)
        print(res)

    def test_dir(self):
        now = datetime.datetime.now()
        print("test dir")
        print(self.__dirStr(now))

    def create(self, title, slug, tags, body, draft):
        now = datetime.datetime.now()
        # 日付からディレクトリを生成
        md_dir = os.path.join(
            self.conf.base_dir, self.conf.create_dir, self.__dirStr(now))

        # # slug(url)の作成
        # slug = self.__to_slug(title)
        md_file_name = slug + ".md"

        md_str = FormatMd().format(now, draft, title, slug, tags, body)
        print("md_str:", md_str.encode('utf-8'))

        # mdの作成
        cmd = 'hugo new ' + \
            os.path.join("post", self.__dirStr(now), md_file_name) + "--log"
        cwd = os.path.join(self.conf.base_dir)
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
    pass


if __name__ == "__main__":
    main()
