from flask import Flask, jsonify, request

app = Flask(__name__)


books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]

@app.route('/')
def home():
    return "Welcome to the Book API!"


@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():

    if request.method == 'POST':
        data = request.get_json()
        new_book = {
            "id": len(books) + 1,
            "title": data.get("title"),
            "author": data.get("author")
        }
        books.append(new_book)
        return jsonify(new_book), 201

    else:
        return jsonify(books)


def find_book_by_id(book_id):
    """ Find the book with the id `book_id`.
    If there is no book with this id, return None. """
    for book in books:
        if book["id"] == book_id:
            return book

    return None


@app.route("/api/books/<int:id>", methods=['PUT', 'DELETE'])
def update_book(id):
    global books
    book = find_book_by_id(id)
    if book is None:
        return '', 404
    if request.method == "PUT":
        new_data = request.get_json()
        book.update(new_data)

        return jsonify(book)

    if request.method == "DELETE":
        books = [book for book in books if book['id'] != id]
        return jsonify(book), 200


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5017)
