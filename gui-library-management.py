import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# File paths
books_file = "books.txt"
users_file = "users.txt"
history_file = "borrow_history.txt"

# Global variable to store current user
current_user = None

# Load books from the file
def load_books():
    listbox_books.delete(0, tk.END)
    try:
        with open(books_file, 'r') as file:
            for line in file:
                listbox_books.insert(tk.END, line.strip())
    except FileNotFoundError:
        open(books_file, 'w').close()  # Create file if it doesn't exist

# Save books to the file
def save_books():
    with open(books_file, 'w') as file:
        for book in listbox_books.get(0, tk.END):
            file.write(book + "\n")

# Add a book
def add_book():
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

# Borrow or return a book
def update_book_status(operation):
    pass

# Remove a book
def remove_book():
    pass

# Authorize a user
def authenticate_user():
    global current_user
    username, password = entry_username.get(), entry_password.get()
    try:
        with open(users_file, 'r') as file:
            for line in file:
                user, pwd = line.strip().split(',')
                if user == username and pwd == password:
                    current_user = username
                    messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                    login_frame.pack_forget()
                    main_frame.pack()
                    load_books()
                    return
    except FileNotFoundError:
        pass
    messagebox.showwarning("Error", "Invalid username or password.")

# Register a new user
def register_user():
    username, password = entry_username.get(), entry_password.get()
    if username and password:
        with open(users_file, 'a') as file:
            file.write(f"{username},{password}\n")
        messagebox.showinfo("Success", "User registered!")
    else:
        messagebox.showwarning("Error", "Enter both username and password.")


# Logout and return to login screen
def logout():
    pass


# Initialize the main window
root = tk.Tk()
root.title("Library Management System")
root.geometry("500x600")

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack()

tk.Label(login_frame, text="Username:").pack()
entry_username = tk.Entry(login_frame)
entry_username.pack()

tk.Label(login_frame, text="Password:").pack()
entry_password = tk.Entry(login_frame, show="*")
entry_password.pack()

tk.Button(login_frame, text="Login", command=authenticate_user).pack()
tk.Button(login_frame, text="Register", command=register_user).pack()

# Main Frame
main_frame = tk.Frame(root)

tk.Label(main_frame, text="Title:").pack()
entry_title = tk.Entry(main_frame)
entry_title.pack()

tk.Label(main_frame, text="Author:").pack()
entry_author = tk.Entry(main_frame)
entry_author.pack()

tk.Label(main_frame, text="ISBN:").pack()
entry_isbn = tk.Entry(main_frame)
entry_isbn.pack()

tk.Button(main_frame, text="Add Book", command=add_book).pack()
tk.Button(main_frame, text="Borrow Book", command=lambda: update_book_status("borrow")).pack()
tk.Button(main_frame, text="Return Book", command=lambda: update_book_status("return")).pack()
tk.Button(main_frame, text="Remove Book", command=remove_book).pack()

listbox_books = tk.Listbox(main_frame, width=80)
listbox_books.pack()

tk.Button(main_frame, text="Log Out", command=logout).pack()

# Start with login frame visible
root.mainloop()