# About
This program both prints the results in the terminal and outputs the results in an excel spreadsheet file. 

# How to use
1. __Edit config.py__: See "Configuration file details" below to learn more about the variables. 
    - If you want to run an example first, set the `goodreads_user_id` variable to `"example"`. 
2. __Run the program__: open the terminal and go to the directory with the python files. In the terminal, type "python main.py".
3. __Give Goodreads authorization__: For certain commands (e.g. "bookshelf genres breakdown"), you will need to give authorization to Goodreads. When this is required, a browser window will open up. After giving authorization, type 'y' in the terminal. ![terminal authorization](/screenshots/goodreads_authorization_terminal.jpg)
4. __See the outputted results__: the results will be printed to the terminal and outputted to a file.

_! Note_: It may be the case that not all your Goodreads books are found and displayed. This python program uses Google Books API, so if your Goodreads book is not found in the Google Books API, you will see "[NOT FOUND]" in the termianl when this program is running and getting your Goodreads information.

# Configuration file details (config.py)
- __goodreads_user_id__: Your Goodreads user ID. To find your user id, click [here](https://help.goodreads.com/s/article/Where-can-I-find-my-user-ID). You can also use another user's user id to get the breakdown of their bookshelf.
- __goodreads_api_key__: Your Goodreads API key. Can be created and found [here](https://www.goodreads.com/api/keys). This is needed to make requests to the Goodreads API.
- __goodreads_api_secret__: Your Goodreads API secret. Can be created and found [here](https://www.goodreads.com/api/keys). This is needed to make requests to the Goodreads API.
- **command**: What you want the program to do. 
    - "bookshelf genres breakdown": Outputs the genre breakdown of the "bookshelf" you specify in the `config.py` file. Prints in the terminal and exports to a .xlsx file.
    - "bookshelf books": Outputs the book information for all books in the "bookshelf" you specify in the config.py file. The information is formatted like: <title> | <author> | <isbn>. Prints in the terminal and exports to a .txt file.
    - "bookshelf books with genres": Outputs the book information _and_ genres for all books in the "bookshelf" you specify in the config.py file. Prints in the terminal and exports to a .txt file.
    - "all bookshelf sizes": Outputs the names and sizes of the user's bookshelfs. The size of a bookshelf is the number of books in it. Prints in the terminal and exports to a .txt file.
    - "all bookshelf names": Outputs the names of all the user's bookshelfs. Prints in the terminal and exports to a .txt file.
    - If you're curious, the source of all the commands is the `commands_dict` variable in `main.py`.
- **bookshelf**: The name of the bookshelf on your profile that you want to get information on. If the name given is not an actual bookshelf on your profile, it defaults to retrieving information on the "read" bookshelf.
- **export_filename**: The name of the output file _without_ the file extension. 
    - If a file with that name already exists, the old file will be deleted.
    - If using an existing filename, please make sure that the file is not open before running this program.
- **primary_color_hex**: (for the "bookshelf genres breakdown" command) The hex color of the top row of the output excel file.
- **secondary_color_hex**: (for the "bookshelf genres breakdown" command) The hex color of the 2nd row of the output excel file.

## config.py
```
# DO NOT DELETE ANY VARIABLES OR CHANGE THE VARIABLE NAMES, EVEN IF THE COMMAND DOESN'T USE THEM

# Your Goodreads credentials. Your API key and API secret are used to make requests to the Goodreads API.
# Find your API key and secret at https://www.goodreads.com/api/keys.
goodreads_api_key = "<your api key>"
goodreads_api_secret = "<your api secret>"

command = "bookshelf genres breakdown"       
goodreads_user_id = "<your goodreads user id>"         
export_filename = "bookshelf_genres_breakdown"    

# Name of the specific bookshelf you want to get information on
# For the commands: "bookshelf genres breakdown", "bookshelf books", "bookshelf books with genres"
bookshelf = "read"                   

# For the command: "bookshelf genres breakdown"
# Excel output file customization 
primary_color_hex = "#c4d79b"  
secondary_color_hex  = "#d8e4bc"
```

## Other examples for config.py file
```
...
command = "bookshelf genres breakdown"
bookshelf = "to-read"
export_filename = "genres_breakdown"
...
```

```
...
command = "bookshelf books"
bookshelf = "read"
export_filename = "bookshelf_books"
...
```


# Screenshots
## "bookshelf genres breakdown"
![bookshelf genres breakdown details](/screenshots/bookshelf_genres_breakdown_1.jpg)

![bookshelf genres breakdown overview](/screenshots/bookshelf_genres_breakdown_2.jpg)

In the exported excel file, there are 2 sheets, Details and Overview. 
### "Details" sheet 
- The 1st row lists the genres (according to Google Books)
- The 2nd row lists the size of each genre (in percentages)
- The 3rd row and onwards list the books under the respective genres as <title> - <author>.

### "Overview" sheet 
In Overview, expand the pie chart to see as many genres as you want (i.e. adjust the chart with and height by dragging any edge or corner).

- __Number of books in bookshelf__: the number of books you have in all bookshelves, including duplicates (some books can be catergorized under multiple genres).
- __Number of genres__: the total number of genres.
- __Number of book instances__: the _unique_ number of books in all your bookshelves.

## "bookshelf books"
![bookshelf books](/screenshots/bookshelf_books.jpg)

## "bookshelf books with genres"
![bookshelf books with genres](/screenshots/bookshelf_books_with_genres.jpg)

## "all bookshelf names"
![all bookshelf names](/screenshots/all_bookshelf_names.jpg)

## "all bookshelf sizes"
![all bookshelf sizes](/screenshots/all_bookshelf_sizes.jpg)
