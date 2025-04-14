from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the Book API!"


def validate_book_data(data):
    if "title" not in data or "author" not in data:
        return False
    return True


@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    # filtering books by f.e. author or title OR return all books via GET
    if request.method == "GET":
        author = request.args.get('author')
        title = request.args.get('title')

        filtered_books = books
        if author:
            filtered_books = [book for book in filtered_books if book["author"].lower() == author.lower()]
        if title:
            filtered_books = [book for book in filtered_books if book["title"].lower() == title.lower()]

        # pagination
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        start_index = (page - 1) * limit
        end_index = start_index + limit

        paginated_books = filtered_books[start_index:end_index] # if not filtered return all books paginated

        return jsonify(paginated_books)

    # or add new book if POST
    elif request.method == 'POST':
        data = request.get_json()
        if not validate_book_data(data):
            return jsonify({"error": "Invalid Book Data"}), 400

        new_book = {
            "id": len(books) + 1,
            "title": data.get("title"),
            "author": data.get("author")
        }
        books.append(new_book)
        return jsonify(new_book), 201


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


books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald"
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell"
    },
    {
        "id": 3,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee"
    },
    {
        "id": 4,
        "title": "Brave New World",
        "author": "Aldous Huxley"
    },
    {
        "id": 5,
        "title": "Moby-Dick",
        "author": "Herman Melville"
    },
    {
        "id": 6,
        "title": "Pride and Prejudice",
        "author": "Jane Austen"
    },
    {
        "id": 7,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger"
    },
    {
        "id": 8,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien"
    },
    {
        "id": 9,
        "title": "The Brothers Karamazov",
        "author": "Fyodor Dostoevsky"
    },
    {
        "id": 10,
        "title": "Don Quixote",
        "author": "Miguel de Cervantes"
    },
    {
        "id": 11,
        "title": "Beloved",
        "author": "Toni Morrison"
    },
    {
        "id": 12,
        "title": "Jane Eyre",
        "author": "Charlotte Bront\u00eb"
    },
    {
        "id": 13,
        "title": "The Divine Comedy",
        "author": "Dante Alighieri"
    },
    {
        "id": 14,
        "title": "The Iliad",
        "author": "Homer"
    },
    {
        "id": 15,
        "title": "The Sun Also Rises",
        "author": "Ernest Hemingway"
    },
    {
        "id": 16,
        "title": "Things Fall Apart",
        "author": "Chinua Achebe"
    },
    {
        "id": 17,
        "title": "The Trial",
        "author": "Franz Kafka"
    },
    {
        "id": 18,
        "title": "White Teeth",
        "author": "Zadie Smith"
    },
    {
        "id": 19,
        "title": "A Clockwork Orange",
        "author": "Anthony Burgess"
    },
    {
        "id": 20,
        "title": "Siddhartha",
        "author": "Hermann Hesse"
    }
]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5018)
