# digital_text_libary
In this repo I'll make a python console app that willbe able to add, read, lend out and delete books from a database
![image](https://github.com/Shift-Happens/digital_text_libary/assets/90008035/35e162f0-4a2c-4ca3-8eee-a027f0070f6a)
<br>
This project is a simple library management system implemented in Python. It allows users to perform various operations such as adding books to the library, borrowing books, returning books, and checking the history of a book. The program uses CSV files to store book, reader, and history data.

The main features of the program include:

Book Class: Represents a book with attributes such as ID, title, author, publication year, and status. It provides methods to check if the book is available, mark it as available, and mark it as borrowed.

Reader Class: Represents a reader with attributes like reader number, first name, last name, and number of books borrowed. It includes methods to add or subtract books from the reader's count.

Library Class: Manages the library operations and user interactions. It provides functionalities to add books, borrow books, return books, and check the history of a book. The class also includes a daily random quote feature for inspiration.

The project also includes exception classes for handling specific situations, such as when a book is already borrowed or not found.

The program starts by checking the existence of CSV files for books, readers, and history. If any file is missing, the program creates a new file with the required header.

![image](https://github.com/Shift-Happens/digital_text_libary/assets/90008035/c6521786-99bb-4f16-96eb-96c38d559815)
![image](https://github.com/Shift-Happens/digital_text_libary/assets/90008035/ac74d445-873a-43af-8700-93601b3d0f95)


The user is presented with a menu to select from various options, including adding a book, borrowing a book, returning a book, checking the history of a book, and exiting the program. Each operation is validated and appropriate actions are performed, such as updating the book status, adding or subtracting books from the reader's count, and logging the history of transactions.

The program saves the data back to the CSV files before exiting to ensure data persistence.

Overall, this project provides a basic library management system that allows users to manage books and readers efficiently.

