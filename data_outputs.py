import os
import json
import xlsxwriter

import config
import objects

class FileOperations:
	# ===== Helper file operations =====
	@staticmethod
	def output_json_to_file(data, filename):
		with open(filename, "w") as outfile:
			json.dump(data, outfile, indent = 2)
	

	# Generic helper function that outputs data_list (a list of strings) to a file, line by line.
	# filename is a string including the file extension (e.g. "data.txt")
	@staticmethod
	def output_to_file(data_list, filename):
		FileOperations.remove_file_if_exists(filename)
		file = open(filename, "w", encoding = "utf-8")
		for line in data_list:
			file.write(line + "\n")
		file.close()


	@staticmethod
	def remove_file_if_exists(path):
		if os.path.exists(path):
			os.remove(path)


	# ===== Main file operations =====
	@staticmethod
	def export_genres_breakdown_to_excel(bookshelf):
		genre_to_books = bookshelf.categorize_bookshelf_books_into_genres()
		num_of_genres = len(genre_to_books.keys())
		num_of_book_instances = sum([len(v) for v in genre_to_books.values()])

		xlsx_filename = config.export_filename + ".xlsx"
		FileOperations.remove_file_if_exists(xlsx_filename) # because the xlsxwriter module cannot read or modify existing excel xlsx files

		excel_file = xlsxwriter.Workbook(xlsx_filename)

		# Create sheet1 and cell formats
		sheet1 = excel_file.add_worksheet("Details")
		header_cell_format = excel_file.add_format({'bold': True, 'align': 'left', 'text_wrap': True, 'valign': 'vcenter'})
		header_genre_cell_format = excel_file.add_format({'bold': True, 'align': 'left', 'text_wrap': True, 'valign': 'vcenter', 'bg_color': config.primary_color_hex})
		header_percent_cell_format = excel_file.add_format({'bold': True, 'align': 'left', 'text_wrap': True, 'valign': 'vcenter', 'bg_color': config.secondary_color_hex})
		genre_cell_format = excel_file.add_format({'align': 'center', 'valign': 'vcenter', 'bg_color': config.primary_color_hex})
		percent_cell_format = excel_file.add_format({'num_format': '0.00%', 'align': 'center', 'valign': 'vcenter', 'bg_color': config.secondary_color_hex})
		book_cell_format = excel_file.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})

		# Create header column in sheet1
		sheet1.write("A1", "Genre", header_genre_cell_format)
		sheet1.write("A2", "Percent size of genre", header_percent_cell_format)
		sheet1.write("A3", "Books in genre", header_cell_format)

		# Fill sheet1 with data
		current_column_index = 1
		for genre, books in genre_to_books.items():
			current_column = xlsxwriter.utility.xl_col_to_name(current_column_index)
			genre_cell = current_column + "1"
			percentage_cell = current_column + "2"
			percentage_cell_data = len(books) / num_of_book_instances
			sheet1.write(genre_cell, genre, genre_cell_format)
			sheet1.write(percentage_cell, percentage_cell_data, percent_cell_format)
			current_book_row = 3
			for book in books:
				book_cell = current_column + str(current_book_row)
				book_cell_data = book.title + " - " + book.author
				sheet1.write(book_cell, book_cell_data, book_cell_format)
				current_book_row += 1
			current_column_index += 1
		
		# Format sheet1
		sheet1.set_column(0, 15) 							# set the width of column A to 15
		sheet1.set_column(1, current_column_index, 30) 		# set the width of columns starting from B to 30
		sheet1.freeze_panes(2, 1) 							# freeze the top 2 rows and 1 leftmost column

		# Create pie chart for sheet2
		sheet2 = excel_file.add_worksheet("Overview")
		last_column = xlsxwriter.utility.xl_col_to_name(current_column_index - 1)
		pie_chart = excel_file.add_chart({'type': 'pie'})
		pie_chart.add_series({
			"categories": "=Details!$B$1:$" + last_column + "$1",
			"values": "=Details!$B$2:$" + last_column + "$2"
			})
		sheet2.insert_chart("B6", pie_chart)

		# Fill sheet2 with data
		sheet2.write("B2", "Number of books in bookshelf:")
		sheet2.write("C2", len(bookshelf.items))
		sheet2.write("B3", "Number of genres:")
		sheet2.write("C3", num_of_genres)
		sheet2.write("B4", "Number of book instances:")
		sheet2.write("C4", num_of_book_instances)

		# Format sheet2
		sheet2.set_column(1, 2, 30) 						# set the width of column B to 30

		excel_file.close()
	

	@staticmethod
	def export_bookshelf_books_to_file(bookshelf):
		text_filename = config.export_filename + ".txt"
		FileOperations.remove_file_if_exists(text_filename)
		file = open(text_filename, "w", encoding = "utf-8")

		bookshelf_books = bookshelf.get_books()
		for book in bookshelf_books:
			book_info = book.get_book_info_string()
			file.write(book_info + "\n")
		file.close()


	@staticmethod
	def export_bookshelf_books_with_genres_to_file(bookshelf):
		text_filename = config.export_filename + ".txt"
		FileOperations.remove_file_if_exists(text_filename)
		file = open(text_filename, "w", encoding = "utf-8")

		bookshelf_books = bookshelf.get_books()
		for book in bookshelf_books:
			book_info = book.get_book_info_string()
			file.write(book_info + "\n")
			for genre in book.get_genres():
				file.write("\t" + genre + "\n")
			file.write("\n")
		file.close()

	
	@staticmethod
	def export_user_bookshelf_sizes_to_file(user):
		text_filename = config.export_filename + ".txt"
		FileOperations.remove_file_if_exists(text_filename)
		file = open(text_filename, "w", encoding = "utf-8")

		names_and_sizes = user.get_user_shelf_sizes().items()
		for name, size in names_and_sizes:
			file.write(name + " " + size + "\n")		
		file.close()
	

	@staticmethod
	def export_user_bookshelf_names_to_file(user):
		text_filename = config.export_filename + ".txt"
		FileOperations.remove_file_if_exists(text_filename)
		file = open(text_filename, "w", encoding = "utf-8")

		bookshelf_names = user.get_user_shelf_names()
		for name in bookshelf_names:
			file.write(name + "\n")		
		file.close()
	
        

class PrintOperations:
	# ===== Helper print operations =====
	@staticmethod
	def print_header(banner_text, banner_pattern = "-", banner_length = 8):
		banner_left, banner_right = (banner_pattern * banner_length) + " ", " " + (banner_pattern * banner_length)
		print()
		print(banner_left + banner_text + banner_right)
	

	@staticmethod
	def print_data_items(json_data):
		print("Number of found items: ", json_data["totalItems"])
		for item in json_data["items"]:
			if "volumeInfo" in item:
				print("Title: " + item["volumeInfo"]["title"])
				print("Authors: " + item["volumeInfo"]["authors"][0])
	

	# Prints the book's title, author, and isbn
	@staticmethod
	def print_book_info(book):
		print(book.get_book_info_string())

	
	# ===== Main print operations =====
	@staticmethod
	def print_bookshelf_genres_breakdown(bookshelf):
		genre_to_books = bookshelf.categorize_bookshelf_books_into_genres()
		num_of_genres = len(genre_to_books.keys())
		num_of_book_instances = sum([len(v) for v in genre_to_books.values()])
		max_genre_word_length = max([len(genre) for genre in genre_to_books.keys()])
		
		PrintOperations.print_header("RESULT OVERVIEW", "=", 10)
		print("Number of books in bookshelf:", len(bookshelf.items))
		print("Number of book instances: ", num_of_book_instances)
		print("Number of genres: ", num_of_genres)
		
		PrintOperations.print_header("RESULT DETAILS", "=", 10)
		for genre, books in genre_to_books.items():
			num_of_dots = max_genre_word_length - len(genre) + 3 # pretty print: align the display of percentages
			dots = "." * num_of_dots
			print()
			print(genre + " " + dots + " " + str(len(books) / num_of_book_instances * 100) + "%")
			for book in books:
				print("   " + book.get_title() + " - " + book.get_author())
	

	@staticmethod
	def print_user_shelf_names(user):
		PrintOperations.print_header("USER'S BOOKSHELFS", "-", 5)
		shelf_names = user.get_user_shelf_names()
		for shelf_name in shelf_names:
			print(shelf_name)


	@staticmethod
	def print_user_shelf_sizes(user):
		PrintOperations.print_header("USER'S BOOKSHELF SIZES", "-", 5)
		names_to_sizes = user.get_user_shelf_sizes()
		for shelf_name in names_to_sizes.keys():
			print(shelf_name + " " + names_to_sizes[shelf_name])


	@staticmethod
	def print_bookshelf_books(bookshelf):
		PrintOperations.print_header("BOOKS IN BOOKSHELF: " + bookshelf.get_bookshelf_name(), "-", 5)
		for book in bookshelf.get_books():
			PrintOperations.print_book_info(book)
	

	# Prints the genres of each book, for all books in the bookshelf
	@staticmethod
	def print_bookshelf_books_with_genres(bookshelf):
		PrintOperations.print_header("BOOKS' GENRES", "-", 5)
		for book in bookshelf.get_books():
			print (book.get_book_info_string())
			for genre in book.get_genres():
				print("	" + genre)
			print()
	
	


