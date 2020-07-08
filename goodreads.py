import sys
import xmltodict
import requests
from rauth.service import OAuth1Service
from requests_oauthlib import OAuth1
import webbrowser
from bs4 import BeautifulSoup

import config
import objects
import data_outputs

class GoodreadsAPI:
	# Returns the response from goodreads API
	@staticmethod
	def make_goodreads_api_request(url, params, key = config.goodreads_api_key):
		params["key"] = key							# add the required API authentication key to params
		return requests.get(url, params = params)


	# Returns the response from a goodreads API that requires OAuth
	# See OAuth1 documentation: https://requests.readthedocs.io/en/master/user/authentication/#oauth-1-authentication
	@staticmethod
	def make_goodreads_api_request_with_auth(url, params, access_token, access_token_secret, key = config.goodreads_api_key, secret = config.goodreads_api_secret):
		params["key"] = key
		auth = OAuth1(key, secret, access_token, access_token_secret)
		return requests.get(url, params = params, auth = auth)


	# Get authroization via OAuth (some Goodreads APIs require OAuth)
	# Code from: https://www.goodreads.com/api/oauth_example#python
	@staticmethod
	def get_goodreads_access():
		goodreads = OAuth1Service(
			consumer_key = config.goodreads_api_key,
			consumer_secret = config.goodreads_api_secret,
			name = "goodreads",
			request_token_url="https://www.goodreads.com/oauth/request_token",
			authorize_url = "https://www.goodreads.com/oauth/authorize",
			access_token_url = "https://www.goodreads.com/oauth/access_token",
			base_url="https://www.goodreads.com/"
			)

		# head_auth=True is important here; this doesn't work with oauth2 for some reason
		request_token, request_token_secret = goodreads.get_request_token(header_auth = True)

		authorize_url = goodreads.get_authorize_url(request_token)
		print ("If a webpage doesn't open up, visit this URL in your browser: \n" + authorize_url)
		print("Note: copy and paste the URL using your mouse, not keyboard.\n")
		webbrowser.open(authorize_url, new = 2) # open up a new tab
		accepted = "n"
		while accepted.lower() == "n":
			# you need to access the authorize_link via a browser,
			# and proceed to manually authorize the consumer
			accepted = input("Have you authorized me? (y/n) ")

		session = goodreads.get_auth_session(request_token, request_token_secret)
		return session


class GoodreadsData:
	# Gets and adds the books in the specified bookshelf to the User's Bookshelf object
	@staticmethod
	def get_books_in_bookshelf_from_goodreads(user_id, shelf_name):
		try:
			print("Getting authorization to access your '" + shelf_name + "' bookshelf")
			session = GoodreadsAPI.get_goodreads_access()
			ACCESS_TOKEN = session.access_token
			ACCESS_TOKEN_SECRET = session.access_token_secret

			bookshelf = objects.Bookshelf(shelf_name)

			data_outputs.PrintOperations.print_header("FINDING BOOKS IN GOOGLE BOOKS API", "=", 10)

			page_num = 1
			while True:
				url = "https://www.goodreads.com/review/list?v=2"
				params = {
					"v":2,
					"id": user_id,
					"shelf": shelf_name,
					"per_page": 200,
					"page": page_num
					}
				response = GoodreadsAPI.make_goodreads_api_request_with_auth(url, params, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
				books = GoodreadsData.parse_goodreads_bookshelf_xml(response)
				if len(books) == 0:
					break

				bookshelf.add_books(books)
				page_num += 1
			
			return bookshelf
			
		except KeyError as err:
			print("Error: Failed to get authorization. Try again and approve authorization by visiting the given url.")
			print("Error details: ", err)
			return -1
	
	
	# Helper function for get_books_in_bookshelf_from_goodreads(...).
	# Parses the xml into a list of books.
	@staticmethod
	def parse_goodreads_bookshelf_xml(response):
		books = []
		# Parse the HTML returned using BeautifulSoup
		soup = BeautifulSoup(response.text, 'html.parser')
		books_table = soup.find(id = "books") 						# the books are listed in <table id= "books"> 
		rows = books_table.findChildren(["th", "tr"])
		for row in rows:
			bookname, author, isbn = "", "", ""

			bookname_cell = row.find("td", ["title"])
			author_cell = row.find("td", ["author"])
			isbn_cell = row.find("td", ["isbn"])

			if bookname_cell: 
				bookname = bookname_cell.find("a")["title"]			# Alternatively: bookname_cell.find("a").text.strip()
			
			if author_cell:
				author = author_cell.find("a").text.strip() 		# Alternatively: author_cell.find("a").string

			if isbn_cell:
				isbn = isbn_cell.find("div").text.strip() 			# Alternatively: isbn_cell.find("div").string.strip()				
			
			if (not bookname) or (bookname == "") or (not author) or (author == ""): 	# Cannot add/find this book if we do not have both the bookname and author information
				continue 
			elif (isbn) and (isbn != ""): 							# If there is an isbn
				new_book = objects.Book.create_new_book_object(bookname, author, isbn)
				books.append(new_book)
			else: 													# If there is no isbn
				new_book = objects.Book.create_new_book_object(bookname, author)
				books.append(new_book)

		return books


	# Returns a dictionary mapping the Goodreads user's bookshelf names (string) to the number of books in bookshelf (string number)
	@staticmethod
	def get_user_shelves_from_goodreads(user_id):
		url = "https://www.goodreads.com/shelf/list.xml"
		params = {
			'user_id': user_id
		}

		response = GoodreadsAPI.make_goodreads_api_request(url, params)

		if not response.ok:
			sys.exit("Goodreads API could not find book or user")

		json_data = xmltodict.parse(response.content)

		# for analyzing purposes
		# data_outputs.FileOperations.output_json_to_file(json_data, "goodreads_data.txt")

		if ("Request" in json_data["GoodreadsResponse"]) and (json_data["GoodreadsResponse"]["Request"]["authentication"] == False):
			sys.exit("Goodreads API could not authenticate the request")

		goodreads_user_shelves = json_data["GoodreadsResponse"]["shelves"]["user_shelf"]
		user_shelves = {}
		for goodreads_shelf in goodreads_user_shelves:
			shelf_name = goodreads_shelf["name"]
			shelf_size = goodreads_shelf["book_count"]["#text"]
			user_shelves[shelf_name] = shelf_size

		return user_shelves
