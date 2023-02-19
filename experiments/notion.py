import os
from notion_client import Client

# 1. Create integration
# 2. Go to page and connect
#   https://www.notion.so/help/add-and-manage-connections-with-the-api#add-connections-to-pages
# 3. Confirm by hitting the Search API
#   https://restless-meadow-422171.postman.co/workspace/sxm-workspace~af728e2f-360f-46c9-93f3-8eb7ab3f5d9d/request/5251691-a7e602c0-d6a3-4948-91f1-118359e42893

# Initialize a new Notion client with your API key
NOTION_TOKEN = ""
notion = Client(auth=NOTION_TOKEN)

page_id = ""

# Get the ID of the database you want to retrieve notes from
# https://www.notion.so/d7507c6bbdbe4977a1282873332eb7b5?v=74f2ebed7ed547e3992beb1fdc30a237
# DATABASE_ID = ""

# Retrieve all pages (notes) from the database
query_params = {"database_id": DATABASE_ID}
response = notion.databases.query(**query_params)

# # Write each page to a separate file on disk
# for page in response["results"]:
#     print(page)
#     # file_name = page["properties"]["Name"]["title"][0]["text"]["content"] + ".md"
#     # file_content = page["properties"]["Note"]["rich_text"][0]["text"]["content"]
