from datetime import date, timedelta
from tabulate import tabulate
import pickle
import validators
import difflib
from collections import Counter

def validate_member(email, password):
    email_address = validators.email(email)
    if not email_address:
        print("Invalid email format.")
        return False
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    if not any(char.isdigit() for char in password):
        print("Password must contain at least one digit.")
        return False
    if not any(char.isupper() for char in password):
        print("Password must contain at least one uppercase letter.")
        return False
    return True

login = {
    "email": "admin@gmail.com",
    "password": "Admin@123"
}

def forgot_password(library):
    email = input("Enter your email: ")
    if user := library.search_member(email):
        new_password = input("Enter new password: ")
        user.change_password(new_password, library)
    else:
        print("Member not found.")

def signin(library):
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    if email == login["email"] and password == login["password"]:
        print("Login successful!")
        return library.librarian
    member = library.search_member(email, password)
    if member:
        print("Login successful!")
        return member
    print("Invalid email or password.")
    return None

class User:
    def __init__(self, name, age, email, password):
        self.name = name
        self.age = age
        self.email = email
        self.password = password

    def __str__(self):
        return f"User(name={self.name}, age={self.age}, email={self.email})"
    def change_password(self, new_password, library):
        if not validate_member(self.email, new_password):
            return
        self.password = new_password
        print("Password changed successfully.")

class Book:
    def __init__(self, title, author, isbn, genre, description=None, borrowed=False):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.description = description
        self.borrowed = borrowed

    def __str__(self):
        return f"Book(title={self.title}, author={self.author}, isbn={self.isbn}, genre={self.genre}, description={self.description})"


class Member(User):
    def __init__(self, name, age, email, password):
        self.borrowed_books = []
        self.transactions = []
        super().__init__(name, age, email, password)

 
    def search_book(self, title, library):
        if book := library.search_book(title):
            print(f"Found book: {book}")
        else:
            print(f"The book '{title}' is not available at the moment.")

    
    def add_borrowed_book(self, book):
        self.borrowed_books.append(book)

    def remove_borrowed_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def view_borrowed_books(self):
        if not self.borrowed_books:
            print("You have not borrowed any books.")
        else:
            print("Borrowed books:")
            for book in self.borrowed_books:
                print(f" - {book.title} by {book.author}")

    def view_pending_dues(self):
        if not self.transactions:
            print("You have no pending dues.")
            return
        print("Pending dues:")
        for transaction in self.transactions:
      
            fine = transaction.calculate_fine(date.today())
            print(f"Book: {transaction.book.title}, Due Date: {transaction.due_date}, Fine: ${fine:.2f}")



class Library:
    def __init__(self):
        self.members = []
        self.books = []
        self.librarian = None
        self.transactions = []

    def print_users(self):
        table = [[u.name, u.age, u.email] for u in self.members]
        print(tabulate(table, headers=["Name", "Age", "Email"]))

    def print_books(self):
        table = [[b.title, b.author, b.isbn, "Yes" if b.borrowed else "No"] for b in self.books]
        print(tabulate(table, headers=["Title", "Author", "ISBN", "Borrowed"]))

    def search_book(self, query):
        q = str(query).strip().lower()
        results = []
        for book in self.books:
            if (q in book.title.lower() or q in book.author.lower()
                or q in book.isbn.lower() or q in book.genre.lower()):
                results.append(book)

            if not results:
                titles = [book.title for book in self.books]
                close_matches = difflib.get_close_matches(q, titles, n=5, cutoff=0.5)
                for match in close_matches:
                    results.extend([b for b in self.books if b.title == match])

        return results if results else None

    def search_member(self, query):
        q = query.strip.lower()
        results = [m for m in self.members if q in m.name.lower() or q in m.email.lower()]

        if not results:
            names = [m.name for m in self.members]
            close_matches = difflib.get_close_matches(q, names, n=5, cutoff=0.5)
            for match in close_matches:
                results.extend([m for m in self.members if m.name == match])

        return results if results else None
    
    

 
    def _add_member(self, user):
      
        if self.search_member(user.email) is not None:
            print("Member with this email already exists.")
            return
        self.members.append(user)

    def _add_book(self, book):

        if any(b.isbn == book.isbn for b in self.books):
            print("A book with this ISBN already exists.")
            return
        self.books.append(book)

    def _remove_member(self, user):
        if user in self.members:
            self.members.remove(user)

    def _remove_book(self, book):
        if book in self.books:
            self.books.remove(book)

    def _add_transaction(self, transaction):
        self.transactions.append(transaction)
        print(f"Transaction added: {transaction}")

    def _view_transactions(self):
        table = [[t.member.name, t.book.title, t.book.isbn, t.borrow_date, t.return_date, t.due_date] for t in self.transactions]
        print(tabulate(table, headers=["Member", "Title", "ISBN", "Borrow Date", "Return Date", "Due Date"]))

    def _view_books(self):
        self.print_books()

    def save_library(self):
        try:
            with open('library.pkl', 'wb') as file:
                pickle.dump(self, file)
            print("Library saved.")
        except Exception as e:
            print("Error saving library:", e)

    def retrieve_library(self):
        try:
            with open('library.pkl', 'rb') as file:
                loaded_library = pickle.load(file)
                self.members = loaded_library.members
                self.books = loaded_library.books
                self.transactions = loaded_library.transactions
                print("Library restored from file.")
        except FileNotFoundError:
            print("No saved library found.")
        except Exception as e:
            print("Error loading library:", e)

    
    def borrow_book(self, member, title_or_isbn):
        if book := self.search_book(title_or_isbn):
            if book.borrowed:
                print(f"The book '{book.title}' is currently borrowed.")
                return
           
            for t in member.transactions:
                if t.return_date is None and t.calculate_fine(date.today()) > 0:
                    print(f"Cannot borrow: outstanding fine ${t.calculate_fine(date.today()):.2f} for {t.book.title}")
                    return
            book.borrowed = True
            transaction = Transaction(member, book, date.today())
            self._add_transaction(transaction)
            member.add_borrowed_book(book)
            member.add_transaction(transaction)
            print(f"{member.name} has successfully borrowed '{book.title}'.")
        else:
            print(f"The book '{title_or_isbn}' is not available at the moment.")

    def return_book(self, member, title_or_isbn):
        if book := self.search_book(title_or_isbn):
            if not book.borrowed:
                print(f"The book '{book.title}' was not borrowed.")
                return
           
            transaction = next((t for t in self.transactions if t.member == member and t.book == book and t.return_date is None), None)
            if not transaction:
                print("No open borrowing record found for this member/book.")
                return
       
            today = date.today()
            transaction.return_date = today
            if today > transaction.due_date:
                fine = transaction.calculate_fine(today)
                print(f"A fine of ${fine:.2f} is due.")
            else:
                print("Book returned on time. No fine.")
            book.borrowed = False
            member.remove_borrowed_book(book)
          
        else:
            print(f"The book '{title_or_isbn}' is not available at the moment.")

    def recommend_books(self, member=None,mode="generic", query_title=None, n=3):
        if not self.books:
            return []
        
        if mode == "generic":
            if not query_title:
                return []
            titles = [book.title for book in self.books]
            close_matches = difflib.get_close_matches(query_title, titles, n=n, cutoff=0.3)
            return close_matches
        elif mode == "personalized" and member:
            if not member.borrowed_books:
                return []
            genres = [book.genre for book in member.borrowed_books if book.genre]
            fav_genre = Counter(genres).most_common(1)[0][0]

            recs = [book.title for book in self.books if book.genre == fav_genre and book not in self.borrowed_books]
            return recs[:3]
        return []
    
    

    

class Librarian(User):
    def __init__(self, name, age, email, password, library):
        super().__init__(name, age, email, password)
        self.library = library

    def __str__(self):
        return f"Librarian(name={self.name}, age={self.age}, email={self.email})"

    def register_member(self, name, age, email, password):
       
        if not validate_member(email, password):
            print("Member not registered: invalid email/password format.")
            return None
        member = Member(name, age, email, password)
        self.library._add_member(member)
        print(f"Member '{name}' registered successfully.")
        return member

    def add_book(self, book):
        self.library._add_book(book)

    def remove_member(self, member):
        self.library._remove_member(member)

    def remove_book(self, book):
        self.library._remove_book(book)


class Transaction:
    def __init__(self, member, book, borrow_date, return_date=None):
        self.member = member
        self.book = book
        self.borrow_date = borrow_date
        self.return_date = return_date 
        self.due_date = borrow_date + timedelta(days=14)
   
        if self.return_date is None:
            self.book.borrowed = True

    def __str__(self):
        return f"Transaction(member={self.member.name}, book={self.book.title}, borrow_date={self.borrow_date}, return_date={self.return_date})"

    def calculate_fine(self, current_date):
 
        if self.return_date and self.return_date > self.due_date:
            days_overdue = (self.return_date - self.due_date).days
            return days_overdue * 0.5
        elif not self.return_date and current_date > self.due_date:
            days_overdue = (current_date - self.due_date).days
            return days_overdue * 0.5
        return 0


def library_menu(library, librarian):
    while True:
        print("\n--- Librarian Menu ---")
        print("1.Register Member")
        print("2.Add book")
        print("3.Remove member")
        print("4.Remove book")
        print("5.View transactions")
        print("6.View books")
        print("7.View members")
        print("8.Search books")
        print("9.Search member")
        print("10.Allot book (issue)")
        print("11.Return book")
        print("12.Logout\n")

        match input("Enter your choice: "):
            case "1":
                name = input("Enter member name: ")
                age = int(input("Enter member age: "))
                email = input("Enter member email: ")
                password = input("Enter member password: ")
                librarian.register_member(name, age, email, password)
            case "2":
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                isbn = input("Enter book ISBN: ")
                book = Book(title, author, isbn)
                librarian.add_book(book)
            case "3":
                email = input("Enter member email to remove: ")
                member = next((m for m in library.members if m.email == email), None)
                if member:
                    librarian.remove_member(member)
                else:
                    print("Member not found.")
            case "4":
                isbn = input("Enter book ISBN to remove: ")
                book = next((b for b in library.books if b.isbn == isbn), None)
                if book:
                    librarian.remove_book(book)
                else:
                    print("Book not found.")
            case "5":
                library._view_transactions()
            case "6":
                library._view_books()
            case "7":
                library.print_users()
            case "8":
                query = input("Enter query to search book: ")
                results = library.search_book(query)
                if results:
                    print("Search results:")
                    for book in results:
                        print(f" - {book.title} (ISBN: {book.isbn})")
                else:
                    print("No results found.")

            case "9":
                query = input("Enter query to search member: ")
                results = library.search_member(query)
                if results:
                    print("Search results:")
                    for member in results:
                        print(f" - {member.name} (Email: {member.email})")
                else:
                    print("No results found.")

            case "10":
                email = input("Enter member email: ")
                title = input("Enter book title or ISBN: ")
                member = next((m for m in library.members if m.email == email), None)
                if member:
                    library.borrow_book(member, title)
                else:
                    print("Invalid member or book.")
            case "11":
                email = input("Enter member email: ")
                title = input("Enter book title or ISBN: ")
                member = next((m for m in library.members if m.email == email), None)
                if member:
                    library.return_book(member, title)
                else:
                    print("Invalid member or book.")
            case "12":
                print("Logging out...")
                return
            case _:
                print("Invalid choice")
                continue

def member_menu(library, member):
    while True:
        print("\n--- Member Menu ---")
        print("1.View Borrowed Books")
        print("2.Search Books")
        print("3.View pending dues")
        print("4.Change password")
        print("5.Logout")

        match input("Enter your choice: "):
            case "1":
                member.view_borrowed_books()
            case "2":
                title = input("Enter book title to search: ")
                member.search_book(title, library)
            case "3":
                member.view_pending_dues()
            case "4":
                forgot_password(library)
            case "5":
                print("Logging out...")
                return
            case _:
                print("Invalid choice.")
                continue

def main():
    library = Library()
    library.retrieve_library()
    librarian = Librarian("Alice", 40, "alice@gmail.com", "Admin@123", library)
    library.librarian = librarian   

    print("Library Management System")
    running = True

    while running:
        choice = input("\nLogin (l) or quit (q) forgot password (fp): ")
        if choice.lower() == "l":
            user = signin(library)
            if not user:
                continue
            print(f"Welcome, {user.name}!")
            if user == library.librarian:
                library_menu(library, user)
            else:
                member_menu(library, user)

        elif choice.lower() == "q":
            running = False
            print("Exiting...")
            library.save_library()
        elif choice.lower() == "fp":
            forgot_password(library)
                
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
