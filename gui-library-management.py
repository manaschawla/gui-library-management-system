import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import smtplib
import os

# Email needs
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"

# File paths
BOOKS_FILE = "books.txt"
USERS_FILE = "users.txt"
HISTORY_FILE = "borrow_history.txt"

# Global variable to store current user
current_user = None


# Utility Functions
def send_email(subject, body, recipient):
    """Send an email notification."""
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(EMAIL_ADDRESS, recipient, message)
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


def load_books():
    """Load books from the file and populate the listbox."""
    listbox_books.delete(0, tk.END)
    try:
        with open(BOOKS_FILE, "r") as file:
            for line in file:
                listbox_books.insert(tk.END, line.strip())
    except FileNotFoundError:
        open(BOOKS_FILE, "w").close()  # Create the file if it doesn't exist


def save_books():
    """Save books to the file."""
    with open(BOOKS_FILE, "w") as file:
        for book in listbox_books.get(0, tk.END):
            file.write(book + "\n")


def add_book():
    """Add a new book to the library."""
    title, author, isbn = entry_title.get(), entry_author.get(), entry_isbn.get()
    if title and author and isbn:
        book_info = f"{title} by {author} (ISBN: {isbn}) - Available"
        listbox_books.insert(tk.END, book_info)
        entry_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
        entry_isbn.delete(0, tk.END)
        save_books()
        messagebox.showinfo("Success", "Book added!")
    else:
        messagebox.showwarning("Error", "All fields are required.")


def borrow_book_by_details():
    """Borrow a book by providing details."""
    title, author, isbn = entry_title.get(), entry_author.get(), entry_isbn.get()
    if not (title and author and isbn):
        messagebox.showwarning("Error", "Please provide the title, author, and ISBN to borrow a book.")
        return

    for index in range(listbox_books.size()):
        book = listbox_books.get(index)
        if f"{title} by {author} (ISBN: {isbn})" in book and "Available" in book:
            borrow_date = datetime.now().strftime("%Y-%m-%d")
            updated_book = book.replace("Available", f"Borrowed on {borrow_date}")
            listbox_books.delete(index)
            listbox_books.insert(index, updated_book)
            save_books()
            with open(HISTORY_FILE, "a") as file:
                file.write(f"Borrowed: {book} on {borrow_date}\n")

            send_email("Book Borrowed", f"You have borrowed: {book}", entry_user_email.get())
            messagebox.showinfo("Success", "Book borrowed successfully!")
            return

    messagebox.showwarning("Error", "The book is either not available or doesn't exist.")


def borrow_book_from_list():
    """Borrow a selected book from the list."""
    try:
        selected_index = listbox_books.curselection()[0]
        book = listbox_books.get(selected_index)
        if "Available" in book:
            borrow_date = datetime.now().strftime("%Y-%m-%d")
            updated_book = book.replace("Available", f"Borrowed on {borrow_date}")
            listbox_books.delete(selected_index)
            listbox_books.insert(selected_index, updated_book)
            save_books()
            with open(HISTORY_FILE, "a") as file:
                file.write(f"Borrowed: {book} on {borrow_date}\n")

            send_email("Book Borrowed", f"You have borrowed: {book}", entry_user_email.get())
            messagebox.showinfo("Success", "Book borrowed successfully!")
        else:
            messagebox.showwarning("Error", "This book is not available for borrowing.")
    except IndexError:
        messagebox.showwarning("Error", "No book selected.")


def return_book():
    """Return a selected borrowed book."""
    try:
        selected_index = listbox_books.curselection()[0]
        book = listbox_books.get(selected_index)
        if "Borrowed on" in book:
            updated_book = book.split(" - Borrowed on")[0] + " - Available"
            listbox_books.delete(selected_index)
            listbox_books.insert(selected_index, updated_book)
            save_books()
            with open(HISTORY_FILE, "a") as file:
                file.write(f"Returned: {book}\n")

            messagebox.showinfo("Success", "Book returned successfully!")
        else:
            messagebox.showwarning("Error", "This book is not currently borrowed.")
    except IndexError:
        messagebox.showwarning("Error", "No book selected.")


def send_available_books():
    """Email the list of available books."""
    available_books = [book for book in listbox_books.get(0, tk.END) if "Available" in book]
    if available_books:
        books_list = "\n".join(available_books)
        send_email("Available Books", f"Here is the list of available books:\n\n{books_list}", entry_user_email.get())
        messagebox.showinfo("Success", "Available books emailed!")
    else:
        messagebox.showwarning("Error", "No available books.")


# User Authentication Functions
def register():
    """Register a new user."""
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        with open(USERS_FILE, "a") as file:
            file.write(f"{username},{password}\n")
        messagebox.showinfo("Success", "User registered successfully!")
    else:
        messagebox.showwarning("Error", "All fields are required.")


def login():
    """Log in an existing user."""
    global current_user
    username = entry_username.get()
    password = entry_password.get()
    try:
        with open(USERS_FILE, "r") as file:
            users = file.readlines()
            for user in users:
                stored_username, stored_password = user.strip().split(",")
                if username == stored_username and password == stored_password:
                    current_user = username
                    messagebox.showinfo("Success", "Logged in successfully!")
                    show_library_ui()
                    return
        messagebox.showwarning("Error", "Invalid credentials.")
    except FileNotFoundError:
        open(USERS_FILE, "w").close()
        messagebox.showwarning("Error", "No users registered yet.")


def logout():
    """Log out the current user."""
    global current_user
    current_user = None
    messagebox.showinfo("Success", "Logged out successfully!")
    show_login_ui()


# UI Functions
def show_login_ui():
    """Display the login page."""
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Login", font=("Arial", 18)).pack(pady=10)
    tk.Label(root, text="Username").pack()
    global entry_username
    entry_username = tk.Entry(root)
    entry_username.pack()

    tk.Label(root, text="Password").pack()
    global entry_password
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    tk.Button(root, text="Login", command=login).pack(pady=5)
    tk.Button(root, text="Register", command=register).pack()


def show_library_ui():
    """Display the library management page."""
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Welcome, {current_user}!", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Logout", command=logout).pack(pady=5)

    global listbox_books
    listbox_books = tk.Listbox(root, width=80)
    listbox_books.pack()

    tk.Label(root, text="Title:").pack()
    global entry_title
    entry_title = tk.Entry(root)
    entry_title.pack()

    tk.Label(root, text="Author:").pack()
    global entry_author
    entry_author = tk.Entry(root)
    entry_author.pack()

    tk.Label(root, text="ISBN:").pack()
    global entry_isbn
    entry_isbn = tk.Entry(root)
    entry_isbn.pack()

    tk.Label(root, text="User Email:").pack()
    global entry_user_email
    entry_user_email = tk.Entry(root)
    entry_user_email.pack()

    tk.Button(root, text="Add Book", command=add_book).pack()
    tk.Button(root, text="Borrow by Book Details", command=borrow_book_by_details).pack()
    tk.Button(root, text="Borrow from List", command=borrow_book_from_list).pack()
    tk.Button(root, text="Return Book", command=return_book).pack()
    tk.Button(root, text="Email Available Books", command=send_available_books).pack()

    load_books()


# Main Application
root = tk.Tk()
root.title("Library Management System")
root.geometry("600x600")
show_login_ui()
root.mainloop()