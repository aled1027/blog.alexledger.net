import datetime
import glob
import os
import shutil

from jinja2 import Environment, FileSystemLoader
import pandoc
from pydantic import BaseModel

import pandoc
import pydantic
import yaml
from pandoc.types import *
from slugify import slugify


class MarkdownMetadata(pydantic.BaseModel):
    tags: list[str] | None
    title: str
    date: datetime.date


class MarkdownContent:
    metadata_marker = "---"
    jinja_templates_dir = "templates/"

    def __init__(self, filename: str, contents: str) -> None:
        self.filename = filename
        self.contents = contents
        self.metadata = self.parse_metadata(contents)
        self.body = self.parse_body(contents)

        self.jinja_env = Environment(loader=FileSystemLoader(self.jinja_templates_dir))
        self.post_template = self.jinja_env.get_template("post.html")

    def parse_body(self, contents: str) -> str:
        if not contents.startswith(self.metadata_marker):
            return contents

        end_idx = contents.find(self.metadata_marker, len(self.metadata_marker))
        if end_idx < 0:
            raise ValueError("Unable to find end of metadata section")

        body = self.contents[end_idx + len(self.metadata_marker) :]
        return body

    def parse_metadata(self, contents: str) -> MarkdownMetadata:
        if not contents.startswith(self.metadata_marker):
            return MarkdownMetadata(**{})

        start_idx = len(self.metadata_marker)
        end_idx = contents.find(self.metadata_marker, len(self.metadata_marker))

        if end_idx < 0:
            raise ValueError("Unable to find end of metadata section")

        metadata_section = self.contents[start_idx:end_idx]
        metadata = yaml.safe_load(metadata_section)
        return MarkdownMetadata(**metadata)

    def to_html(self) -> str:
        """
        https://boisgera.github.io/pandoc/api/
        """
        doc = pandoc.read(self.body)
        html_body: str = pandoc.write(doc, format="html")

        render_in: dict[str, str] = {"title": self.metadata.title, "body": html_body}
        content = self.post_template.render(render_in)
        return content

    def to_html_file(self, filename: str) -> None:
        """
        https://boisgera.github.io/pandoc/api/
        """
        html_contents = self.to_html()
        with open(filename, "w") as file_handle:
            file_handle.write(html_contents)

    def __str__(self) -> str:
        return self.contents


if __name__ == "__main__":
    build_dir = "site"

    try:
        shutil.rmtree(build_dir)
    except FileNotFoundError:
        # Ignore if the directory doesn't exist
        pass

    os.makedirs(build_dir, exist_ok=True)

    posts: list[MarkdownContent] = []

    post_filenames = glob.glob("posts/*.md")
    for post_filename in post_filenames:
        with open(post_filename) as file_handle:
            mc = MarkdownContent(post_filename, file_handle.read())
            posts.append(mc)

    for post in posts:
        slugged_title = slugify(post.metadata.title)
        filename = os.path.join(build_dir, f"{slugged_title}.html")
        post.to_html_file(filename)
