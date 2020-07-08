import config
import google_books
import goodreads

class Book:
	def __init__(self, title, author, isbn = ""):
		self.title = title
		self.author = author
		self.isbn = isbn
		self.genres = set()

	def set_isbn(self, isbn):
		self.isbn = isbn

	def add_genre(self, genre):
		self.genres.add(genre)

	def get_book_info_string(self):
		return self.title + " | " + self.author + " | " + self.isbn
	
	# Retrieves the genres of the book from the Google Books API,
	# and adds them to the book object.
	def get_and_add_book_genres(self):
		genres = google_books.GoogleBooksData.get_book_genres(self)
		for genre in genres:
			self.add_genre(genre.upper())		# upper case to normalize all the strings	

	def get_title(self):
		return self.title
	
	def get_author(self):
		return self.author
	
	def get_isbn(self):
		return self.isbn
	
	def get_genres(self):
		return self.genres

	# Returns the newly created Book object with all its genres
	@staticmethod
	def create_new_book_object(bookname, author, isbn = ""):
		book = Book(bookname, author, isbn)
		book.get_and_add_book_genres()
		return book	
	

class User:
	def __init__(self, user_id):
		self.user_id = user_id
		self.shelves = {} 			# empty dictionary mapping bookshelf names (string) to Bookshelf objects

	def add_shelf(self, shelf_name, bookshelf):
		self.shelves[shelf_name] = bookshelf
	
	def create_shelf(self, shelf_name):
		return goodreads.GoodreadsData.get_books_in_bookshelf_from_goodreads(self.user_id, shelf_name)
	
	def create_and_add_shelf(self, shelf_name):
		bookshelf = self.create_shelf(shelf_name)
		self.add_shelf(shelf_name, bookshelf)
	
	# Returns a list of names of shelves in the user's Goodreads account (using the Goodreads API)
	def get_user_shelf_names(self):
		return goodreads.GoodreadsData.get_user_shelves_from_goodreads(self.user_id).keys()
	
	# Returns a dictionary mapping the shelf names to shelf size.
	# Gets the size of each of the user's bookshelves without going through each book in the shelf.
	def get_user_shelf_sizes(self):
		return goodreads.GoodreadsData.get_user_shelves_from_goodreads(self.user_id)	
	
	def get_user_id(self):
		return self.user_id
	
	def get_shelves(self):
		return self.shelves

	# Returns the newly created User object 
	@staticmethod
	def create_new_user_object(user_id):
		return User(user_id)


class Bookshelf:
	def __init__(self, name):
		self.name = name
		self.items = set() 			# set of Books

	def add_book(self, book):
		self.items.add(book)
	
	def add_books(self, books):
		self.items.update(set(books))	
	
	def get_bookshelf_name(self):
		return self.name
	
	def get_books(self):
		return self.items
	
	# Retrieves the genres of a book from the Google Books API,
	# and adds them to the book object, for all books in the bookshelf
	def get_and_add_genres_for_all_bookshelf_books(self):
		for book in self.items:
			book.get_and_add_book_genres()

	# Returns a dictionary mapping a genre (string) to a set of books of that genre (set of Book objects)
	def categorize_bookshelf_books_into_genres(self):
		genre_to_books = {} 		
		for book in self.items:
			for genre in book.genres:
				if genre in genre_to_books.keys():
					genre_to_books[genre].add(book)
				else:
					genre_to_books[genre] = {book}
		return genre_to_books
	