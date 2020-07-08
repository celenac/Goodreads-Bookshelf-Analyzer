
import config
import objects
import data_outputs
import goodreads
import google_books

commands_dict = {
	0: "bookshelf genres breakdown",
	1: "bookshelf books",
	2: "bookshelf books with genres",
	3: "all bookshelf sizes",
	4: "all bookshelf names"
}

class Examples():
	test_bookshelf = objects.Bookshelf("read")
	test_user = objects.User("example")

	def __init__(self):
		test_book_1 = objects.Book("Slumber Party", "Pike, Christopher")
		test_book_2 = objects.Book("Weekend", "Pike, Christopher", "0590442562")
		test_book_3 = objects.Book("The Stranger", "Camus, Albert")
		test_book_4 = objects.Book("The Allegory of the Cave", "Plato")
		test_book_5 = objects.Book("The Prophet", "Kahlil Gibran", "9780646266428")
		Examples.test_bookshelf.add_book(test_book_1)
		Examples.test_bookshelf.add_book(test_book_2)
		Examples.test_bookshelf.add_book(test_book_3)
		Examples.test_bookshelf.add_book(test_book_4)
		Examples.test_bookshelf.add_book(test_book_5)		
		Examples.test_user.add_shelf("read", Examples.test_bookshelf)
	
	def test_with_examples(self):
		if (config.command == ""):
			print("Please specify the command you want to run in the config.py file.")
		elif (config.command == commands_dict[0]):
			Examples.test_bookshelf.get_and_add_genres_for_all_bookshelf_books()
			data_outputs.PrintOperations.print_bookshelf_genres_breakdown(Examples.test_bookshelf)
			data_outputs.FileOperations.export_genres_breakdown_to_excel(Examples.test_bookshelf)
		elif (config.command == commands_dict[1]): # "bookshelf books"
			data_outputs.PrintOperations.print_bookshelf_books(Examples.test_bookshelf)
			data_outputs.FileOperations.export_bookshelf_books_to_file(Examples.test_bookshelf)
		elif (config.command == commands_dict[2]): # "bookshelf books with genres"
			Examples.test_bookshelf.get_and_add_genres_for_all_bookshelf_books()
			data_outputs.PrintOperations.print_bookshelf_books_with_genres(Examples.test_bookshelf)
			data_outputs.FileOperations.export_bookshelf_books_with_genres_to_file(Examples.test_bookshelf)
		elif (config.command == commands_dict[3]): # "all bookshelf sizes"
			data = []
			data_outputs.PrintOperations.print_header("USER'S BOOKSHELF SIZES", "-", 5)
			for shelf_name, bookshelf in Examples.test_user.get_shelves().items():
				bookshelf_size = len(bookshelf.get_books())
				line = shelf_name + " " + str(bookshelf_size)
				print(line)
				data.append(line)
			data_outputs.FileOperations.output_to_file(data, config.export_filename + ".txt")
		elif (config.command == commands_dict[4]): # "all bookshelf names"
			data = []
			data_outputs.PrintOperations.print_header("USER'S BOOKSHELFS", "-", 5)
			for shelf_name in Examples.test_user.get_shelves().keys():
				print(shelf_name)
				data.append(shelf_name)
			data_outputs.FileOperations.output_to_file(data, config.export_filename + ".txt")
		else:
			print("Command not recognized: \"" + config.command + "\". Please see the documentation or the README.txt file for a list of valid commands.")


def main():
	user = objects.User.create_new_user_object(config.goodreads_user_id)

	if (config.command == ""):
		print("Please specify the command you want to run in the config.py file.")
	elif (config.goodreads_user_id == "example"):
		data_outputs.PrintOperations.print_header("RUNNING EXAMPLE", "=", 5)
		Examples().test_with_examples()
	elif (config.command == commands_dict[0]): # "bookshelf genres breakdown"
		user.create_and_add_shelf(config.bookshelf)
		data_outputs.PrintOperations.print_bookshelf_genres_breakdown(user.shelves[config.bookshelf])
		data_outputs.FileOperations.export_genres_breakdown_to_excel(user.shelves[config.bookshelf])
	elif (config.command == commands_dict[1]): # "bookshelf books"
		user.create_and_add_shelf(config.bookshelf)
		bookshelf = user.shelves[config.bookshelf]
		data_outputs.PrintOperations.print_bookshelf_books(bookshelf)
		data_outputs.FileOperations.export_bookshelf_books_to_file(user.shelves[config.bookshelf])
	elif (config.command == commands_dict[2]): # "bookshelf books with genres"
		user.create_and_add_shelf(config.bookshelf)
		bookshelf = user.shelves[config.bookshelf]
		data_outputs.PrintOperations.print_bookshelf_books_with_genres(bookshelf)
		data_outputs.FileOperations.export_bookshelf_books_with_genres_to_file(user.shelves[config.bookshelf])
	elif (config.command == commands_dict[3]): # "all bookshelf sizes"
		data_outputs.PrintOperations.print_user_shelf_sizes(user)
		data_outputs.FileOperations.export_user_bookshelf_sizes_to_file(user)
	elif (config.command == commands_dict[4]): # "all bookshelf names"
		data_outputs.PrintOperations.print_user_shelf_names(user)
		data_outputs.FileOperations.export_user_bookshelf_names_to_file(user)
	else:
		print("Command not recognized: \"" + config.command + "\". Please see the documentation/README.txt file for a list of valid commands.")


if __name__ == "__main__":
	main()









