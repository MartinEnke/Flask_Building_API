import requests

BASE_URL = "http://127.0.0.1:5019/api/books"
page = 1
limit = 5

while True:
    response = requests.get(BASE_URL, params={"page": page, "limit": limit})
    books = response.json()

    if not books:
        break

    print(f"\n📘 Page {page}")
    for book in books:
        print(f"{book['id']}: {book['title']} by {book['author']}")

    page += 1
