import datetime
import glob
import os

import pandoc
import pydantic
import yaml
from pandoc.types import *
from slugify import slugify

post_filenames = glob.glob("blog/*.md")


class MarkdownMetadata(pydantic.BaseModel):
    tags: list[str] | None
    title: str
    date: datetime.date


class MarkdownContent:
    metadata_marker = "---"

    def __init__(self, filename: str, contents: str) -> None:
        self.filename = filename
        self.contents = contents
        self.metadata = self.parse_metadata(contents)
        self.body = self.parse_body(contents)

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
        options = ["-s"]
        return pandoc.write(doc, format="html", options=options)

    def to_html_file(self, filename: str) -> None:
        """
        https://boisgera.github.io/pandoc/api/
        """
        html_contents = self.to_html()
        with open(filename, "w") as file_handle:
            file_handle.write(html_contents)

    def __str__(self) -> str:
        return self.contents


posts: list[MarkdownContent] = []

for post_filename in post_filenames:
    with open(post_filename) as file_handle:
        mc = MarkdownContent(post_filename, file_handle.read())
        posts.append(mc)

for post in posts:
    slugged_date = slugify(str(post.metadata.date).strip())
    slugged_title = slugify(post.metadata.title)
    filename = os.path.join("site", f"{slugged_date}-{slugged_title}.html")
    post.to_html_file(filename)
