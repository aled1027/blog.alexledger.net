# Custom Markdown Site Generator

This repository tests out website infrastructure with some basic, near-minimal dependencies (i.e., no hugo, jekyll, javascript, or third party build system).

1. Posts go in the `posts/` directory as markdown files with yaml metadata at the top
2. Run `poetry run build.py` to build the site
3. The site is output to `site/` as a set of HTML files

This is pretty basic. Right now the metadata from the files is generally ignored and there's no table of contents for navigating the posts from the root.

## Running Locally

```bash
poetry install
poetry run python build.py
open site/index.html
```

## Deploying

Deployments are automated with the github action `deploy.yml` to netlify.

The only configuration needed in the action is to update the URL to include your project id and add your netlify token to the actions secret.

## Resources

- [Pandoc](https://pandoc.org/demos.html)
- [Jinja](https://realpython.com/primer-on-jinja-templating/)
