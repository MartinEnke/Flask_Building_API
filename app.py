from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
import os


app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)
# Limiter(...) connects the limiter to your Flask app.
# ensures rate limits apply per IP address (each visitor gets their own quota).

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Create a logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging to file
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=3)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
file_handler.setFormatter(formatter)

''' check logs via - cat logs/app.log - in the terminal '''


# Attach handler to Flask's logger
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


@app.route('/')
def home():
    app.logger.info("🏠 Home page accessed from %s", request.remote_addr)
    return "Welcome to the Book API!"


def validate_book_data(data):
    if "title" not in data or "author" not in data:
        return False
    return True


@app.route('/api/books', methods=['GET', 'POST'])
@limiter.limit("10/minute")  # Limit to 10 requests per minute
def handle_books():          # If limit is exceeded, server will return a 429 Too Many Requests error.
    # filtering books by f.e. author or title OR return all books via GET
    if request.method == "GET":
        app.logger.info("✅ GET request to /api/books from %s", request.remote_addr)
        author = request.args.get('author')
        title = request.args.get('title')

        filtered_books = books
        if author:
            filtered_books = [book for book in filtered_books if book["author"].lower() == author.lower()]
            app.logger.info("🔍 Filtered by author: %s", author)
        if title:
            filtered_books = [book for book in filtered_books if book["title"].lower() == title.lower()]
            app.logger.info("🔍 Filtered by title: %s", title)

        # pagination
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        start_index = (page - 1) * limit
        end_index = start_index + limit

        paginated_books = filtered_books[start_index:end_index] # if not filtered return all books paginated

        app.logger.info("📄 Returned page %s with limit %s", page, limit)
        return jsonify(paginated_books)

    # or add new book if POST
    elif request.method == 'POST':
        data = request.get_json()
        if not validate_book_data(data):
            app.logger.warning("❌ Invalid book data received: %s", data)
            return jsonify({"error": "Invalid Book Data"}), 400

        new_book = {
            "id": len(books) + 1,
            "title": data.get("title"),
            "author": data.get("author")
        }
        books.append(new_book)
        app.logger.info("✅ New book added: %s", new_book)
        return jsonify(new_book), 201


def find_book_by_id(book_id):
    """ Find the book with the id `book_id`.
    If there is no book with this id, return None. """
    for book in books:
        if book["id"] == book_id:
            return book
    app.logger.warning("🔎 Book with ID %s not found", book_id)
    return None


@app.route("/api/books/<int:id>", methods=['PUT', 'DELETE'])
def update_book(id):
    global books
    book = find_book_by_id(id)
    if book is None:
        app.logger.warning("❌ Attempt to access non-existent book with ID %s", id)
        return '', 404

    if request.method == "PUT":
        new_data = request.get_json()
        book.update(new_data)
        app.logger.info("✏️ Book with ID %s updated: %s", id, new_data)
        return jsonify(book)

    if request.method == "DELETE":
        books = [book for book in books if book['id'] != id]
        app.logger.info("🗑️ Book with ID %s deleted", id)
        return jsonify(book), 200


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error("🚫 404 error - page not found: %s", request.path)
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    app.logger.error("🚫 405 error - method not allowed: %s %s", request.method, request.path)
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
    app.run(host="0.0.0.0", port=5019)
