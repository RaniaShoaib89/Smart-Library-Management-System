Library Management System

Video demo:  
A **Python-based Library Management System** built using Object-Oriented Programming (OOP).
This program allows librarians to manage books and members, while members can borrow, return, and search books. It also supports password validation, fine calculation, and persistent storage with pickle`.

##  Features

###  Librarian
- Register new members with validation (email + password rules).
- Add and remove books from the library.
- Add and remove memmbers of the library.
- View all members and books.
- Issue and return books to/from members.
- View all transactions (borrow/return history).
- save and retrieve library objects using pickle

###  Member
- Borrow and return books.
- Search for books by title or ISBN.
- View currently borrowed books.
- View pending dues (fines are calculated at $0.50/day overdue).
- Change password securely.
- Receive **book recommendations** based on previously borrowed authors.

---

## Technologies Used
- **tabulate** → for displaying books, users, and transactions in tables.
- **validators** → for email validation.
- **pickle** → for saving & restoring library data between runs.

---

##  Project Structure

LibrarySystem/
│
├── main.py              # Entry point (contains menus and logic)
├── library.pkl          # Auto-generated file (saves library state)
└── README.md            # Project documentation
```

---

```bash
pip install tabulate validators
```

3. Run the program:

```bash
python main.py
```

---

##  Login

- **Admin/Librarian Login:**
  ```
  Email: admin@gmail.com
  Password: Admin@123
  ```
- Members must be registered by the librarian before logging in. (The admin credentials are hardcoded, a functionality that can be improved)

---

##  Usage

- On start, you’ll be prompted to login (`l`), quit (`q`), or reset password (`fp`).
- Depending on whether you login as librarian or member, you’ll see the relevant menu.
- There are two menus, one for librarian and one for members. Members aren't given the authority to join the LMS on their own nor can they self-issue books. These rights to restricted to the admin, as common in a typical library.

---

##  Example Workflows

### Librarian
1. Login with `admin@gmail.com` / `Admin@123`.
2. Add books and register members.
3. Issue books to members.
4. Track transactions and pending dues.
5. Search members,books
6. Remove members,books

### Member
1. Login with your registered email/password.
2. Borrow available books (if no pending fines).
3. Return books before the due date to avoid fines.
4. Change password anytime.
5. Get recommendations for similar books.
5. View pending dues

---

##  Notes & Limitations
- Uses `pickle` for persistence (not safe for untrusted files).
- Currently, there is no borrow limit (members can borrow unlimited books).
- Recommendations are only based on previously borrowed authors.
- Admin credentials have been hardcoded

---

##  Future Improvements
- Replace `pickle` with JSON or a database for safer storage.
- Add more attributes for books such as genre,description etc
- Add borrow limits per member.
- Improve book recommendation logic (genres, most borrowed, etc.).
- GUI or web-based interface.


---

##  Author
Developed as a Python OOP project for practicing **classes, inheritance, a small degree of exception handlng, and validation**.
github: https://github.com/RaniaShoaib89
email: raniashoaib8@gmail.com
