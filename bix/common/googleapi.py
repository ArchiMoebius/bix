from base64 import b64encode
from functools import lru_cache

import requests


@lru_cache(maxsize=512)
def searchBookByISBN(isbn):
    response = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    )

    if not response.ok:
        return False

    data = response.json()
    ret = False

    if hasattr(data, "items") and len(data["items"]) > 0:
        info = data["items"][0].get("volumeInfo", False)

        if info:
            ret = {}

            ret["title"] = info.get("title", "")
            ret["description"] = info.get("description", "")
            ret["author"] = ",".join(info.get("authors", []))
            ret["publisher"] = info.get("publisher", "")
            ret["publish_date"] = info.get("publishedDate", "")
            ret["lexile"] = f"https://hub.lexile.com/find-a-book/book-details/{isbn}"

            identifiers = info.get("industryIdentifiers", False)

            if identifiers and len(identifiers) > 0:
                for identifier in identifiers:
                    if identifier.get("type", False) == "ISBN_10":
                        ret["isbn10"] = identifier.get("identifier", "")

                    if identifier.get("type", False) == "ISBN_13":
                        ret["isbn13"] = identifier.get("identifier", "")

            images = info.get("imageLinks", False)

            if images and len(images) > 0:
                small_thumbnail_link = images.get("smallThumbnail", False)

                if small_thumbnail_link:
                    response = requests.get(small_thumbnail_link)

                    if response.ok:
                        ret["image"] = (
                            f"data:image/png;base64,{b64encode(response.content).decode('ascii')}"
                        )

    return ret
