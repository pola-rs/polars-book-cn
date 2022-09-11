import difflib
import re
import token
import tokenize
import os

from pathlib import Path
from typing import TextIO
from urllib.parse import quote

contains_zh = re.compile("[\u4e00-\u9fa5]+")

polars_book_dir = "./tmp/polars-book"
polars_book_cn_file_url = "https://github.com/pola-rs/polars-book-cn/blob/main/"

# functional tools (single file), no need to translate
# will directly replace the original file
scripts = [
    "Makefile",
    "generate_data.py",
    "tasks.sh",
    "user_guide/preprocessor/",
    "user_guide/data/",
]

# may contain translated comments
# if there exists chinese characters in the original file, will be skipped and print the diff in the log
codes = [
    "user_guide/src/examples/",
]


def remove_comments(fname):
    """https://stackoverflow.com/questions/1769332/script-to-remove-python-comments-docstrings"""
    res = ""
    with open(fname, "r", encoding="utf-8") as source:
        prev_toktype = token.INDENT
        first_line = None
        last_lineno = -1
        last_col = 0

        tokgen = tokenize.generate_tokens(source.readline)
        for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
            if slineno > last_lineno:
                last_col = 0
            if scol > last_col:
                res += " " * (scol - last_col)
            if toktype == token.STRING and prev_toktype == token.INDENT:
                pass  # docstring
            elif toktype == tokenize.COMMENT:
                pass  # comment
            else:
                res += ttext

            prev_toktype = toktype
            last_col = ecol
            last_lineno = elineno

    return "\n".join(l.rstrip() for l in res.split("\n") if l.strip())


def sync(targets, force, log: TextIO):
    def sync_file(file):
        print(f"\n>>> sync {file}")
        with open(f"{polars_book_dir}/{file}", "r", encoding="utf-8") as new:
            if force or not os.path.exists(file):
                path = file.split("/")
                if len(path) > 0:
                    Path("/".join(path[:-1])).mkdir(parents=True, exist_ok=True)
                with open(file, "w", encoding="utf-8") as old:
                    old.write(new.read())
            else:
                old_clean = remove_comments(file)
                new_clean = remove_comments(f"{polars_book_dir}/{file}")
                if old_clean != new_clean:
                    with open(file, "r", encoding="utf-8") as old:
                        old_text = old.readlines()
                    if all(not contains_zh.search(o) for o in old_text):
                        with open(file, "w", encoding="utf-8") as old:
                            old.write(new.read())
                    else:
                        diff = "".join(difflib.unified_diff(a=new.readlines(), b=old_text, n=0))
                        print(diff)
                        log.write(
                            f"<details>"
                            f'<summary><a href="{polars_book_cn_file_url}/{quote(file)}">{file}</a></summary>'
                            f"<br>"
                            f"<pre>{diff}</pre>"
                            f"</details>"
                        )

    for target in targets:
        if os.path.isfile(f"{polars_book_dir}/{target}"):
            sync_file(target)
        elif os.path.isdir(f"{polars_book_dir}/{target}"):
            for root, _, fs in os.walk(f"{polars_book_dir}/{target}"):
                for f in fs:
                    sync_file(os.path.join(root, f)[18:])  # removing './tmp/polars-book/' prefix


if __name__ == "__main__":
    with open("diffs.log", "w", encoding="utf-8") as log:
        sync(scripts, True, log)
        sync(codes, False, log)

    with open("diffs.log", "r", encoding="utf-8") as log:
        # to set a multiline file's context as github output, replace \n as <br>
        context = "<br>".join([l.rstrip() for l in log.readlines()])
    with open("diffs.log", "w", encoding="utf-8") as log:
        log.write(context)
