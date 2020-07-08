import requests
import data_outputs

class GoogleBooksAPI:
	# Returns a list of genres of the given book
	@staticmethod
	def make_google_api_request(book):
		# Example URL 1: "https://www.googleapis.com/books/v1/volumes?q=The+Prohpet+inauthor:Kahlil+Gibran+isbn:9780646266428" 
		# Example URL 2: "https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes"
		url = GoogleBooksAPI.create_url_request_string(book.title, book.author, book.isbn)
		return requests.get(url = url)


	# Helper method create_url_request_string(...)
	@staticmethod
	def parse_for_url_request(s):
		return s.replace(" ", "+")


	@staticmethod
	def create_url_request_string(bookname, author = "", isbn = ""):
		if (bookname is None) or (bookname == ""):
			return -1

		parsed_bookname = GoogleBooksAPI.parse_for_url_request(bookname)
		base_url = "https://www.googleapis.com/books/v1/volumes?q="
		url = base_url + "+" + parsed_bookname

		if author != "":
			url += "+inauthor:" + GoogleBooksAPI.parse_for_url_request(author)

		if isbn != "":
			url += "+isbn:" + GoogleBooksAPI.parse_for_url_request(isbn)

		return url


class GoogleBooksData:
	# Returns a list of genres (strings) that the book belongs to (according to the Google Books API)
	@staticmethod
	def get_book_genres(book):
		response = GoogleBooksAPI.make_google_api_request(book)

		if not response.ok:
			print("Invalid Google Books API request")
			return []

		data = response.json()

		data_outputs.FileOperations.output_json_to_file(data, "raw_data_google_books.txt")

		if ("items" not in data) or (len(data["items"]) < 1):
			print("[NOT FOUND] " + book.get_book_info_string())
			return ["Uncategorized"]

		# Otherwise, pick the 1st book in the list and use it
		print("[FOUND] " + book.get_book_info_string())
		current_book = data["items"][0]

		try:
			current_book_genres = current_book["volumeInfo"]["categories"]
		except:
			current_book_genres = ["Uncategorized"]
		finally:
			return current_book_genres 

