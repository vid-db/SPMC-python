from tkinter import *

from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from product import product


# window positioning to center
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')


# index function - first window to open
def index():
    # when clicked, it will close the login form
    def open_signup_window():
        window.destroy()
        signup()

    def login():
        username = entry_username.get()
        password = entry_password.get()
        try:
            # connection to MySQL database
            conn = mysql.connector.connect(host="localhost", user="root", password="", db="spmc")
            if conn.is_connected():
                pst = conn.cursor()
                sql_query = 'SELECT * FROM user WHERE username=%s AND password=%s'
                pst.execute(sql_query, (username, password))
                result = pst.fetchone()
                if username == "" and password == "":
                    messagebox.showinfo("Error ", "Please enter username and password")
                elif result is None:
                    messagebox.showinfo("Error", "Incorrect username or password")
                else:
                    messagebox.showinfo("Success", "Login Successfully")
                    window.destroy()
                    product()
        except Error as e:
            print(e)

    # GUI title and size
    window = Tk()
    window.title("Login")

    window_width = 790
    window_height = 720
    center_window(window, window_width, window_height)
    window.resizable(False, False)
    window.tk_setPalette('#22092C')

    # frame for login white background
    login_frame = Frame(window, width=500, height=500, bg='white', bd=5)
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # title label and positioning
    titlelabel = Label(login_frame, text="Login", font=('Poppins', 30), bg='white', bd=2, fg='black')
    titlelabel.grid(row=0, column=0, pady=(50, 5), padx=10)

    # Username Label and Entry
    label_username = Label(login_frame, text="Username", font=('Poppins', 15), bg='white', fg='black')
    label_username.grid(row=1, column=0, pady=(5, 5), padx=60, sticky='w')
    entry_username = Entry(login_frame, width=25, bd=5, font=('Poppins', 15))
    entry_username.grid(row=2, column=0, pady=(5, 5), padx=10)

    # Password Label and Entry
    label_password = Label(login_frame, text="Password", font=('Poppins', 15), bg='white', fg='black')
    label_password.grid(row=3, column=0, pady=(5, 5), padx=60, sticky='w')
    entry_password = Entry(login_frame, width=25, bd=5, font=('Poppins', 15), show="*")
    entry_password.grid(row=4, column=0, pady=(5, 5), padx=10)

    # Login Button
    login_button = Button(login_frame, width=20, text="Login", command=login, bg="#4CAF50", font=('Poppins', 15))
    login_button.grid(row=5, columnspan=2, pady=(5, 10))

    # Sign Up label
    label_signup = Label(login_frame, text="Don't have an account?", font=('Poppins', 10), bg='white', fg='black')
    label_signup.grid(row=6, column=0, pady=(5, 10), padx=(110, 115), sticky='w')
    # Sign Up button
    signup_button = Button(login_frame, text="Sign Up", command=open_signup_window, bg="white", bd=0, fg='blue', cursor='hand2', font=('Poppins', 10))
    signup_button.grid(row=6, column=0, pady=(5, 10), padx=(250, 110), sticky='w')

    # Run the Tkinter event loop
    window.mainloop()


def signup():

    def open_index_window():
        window.destroy()
        index()

    def signup_func():
        username = entry_username.get()
        password = entry_password.get()
        cp = entry_cp.get()

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", db="spmc")
            if username == "" or password == "" or cp == "":
                messagebox.showinfo("Error", "Please fill out all fields")
            else:
                if password == cp:
                    if conn.is_connected():
                        pst = conn.cursor()
                        sql_query = 'INSERT INTO user (username, password) VALUES (%s, %s)'
                        pst.execute(sql_query, (username, password))
                        conn.commit()
                        messagebox.showinfo("Success", "Successfully signed up")
                        # Open the login
                        window.destroy()
                        index()
                else:
                    messagebox.showinfo("Error", "Password doesn't match")
        except Error as e:
            print(e)

    # GUI title and size
    window = Tk()
    window.title("Sign Up")
    window_width = 790
    window_height = 720
    center_window(window, window_width, window_height)
    window.resizable(False, False)
    window.tk_setPalette('#22092C')

    signup_frame = Frame(window, width=500, height=500, bg='white', bd=5)
    signup_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # title label and positioning
    titlelabel = Label(signup_frame, text="Signup", font=('Poppins', 30), bg='white', bd=2, fg='black')
    titlelabel.grid(row=0, column=0, pady=(50, 5), padx=10)

    # Username Label and Entry
    label_username = Label(signup_frame, text="Username", font=('Poppins', 15), bg='white', fg='black')
    label_username.grid(row=1, column=0, pady=(5, 5), padx=50, sticky='w')
    entry_username = Entry(signup_frame, width=25, bd=5, font=('Poppins', 15))
    entry_username.grid(row=2, column=0, pady=(5, 5), padx=10)

    # Password Label and Entry
    label_password = Label(signup_frame, text="Password", font=('Poppins', 15), bg='white', fg='black')
    label_password.grid(row=3, column=0, pady=(5, 5), padx=50, sticky='w')
    entry_password = Entry(signup_frame, width=25, bd=5, font=('Poppins', 15), show="*")
    entry_password.grid(row=4, column=0, pady=(5, 5), padx=10)

    # Password Label and Entry
    label_cp = Label(signup_frame, text="Confirm Password", font=('Poppins', 15), bg='white', fg='black')
    label_cp.grid(row=5, column=0, pady=(5, 5), padx=50, sticky='w')
    entry_cp = Entry(signup_frame, width=25, bd=5, font=('Poppins', 15), show="*")
    entry_cp.grid(row=6, column=0, pady=(5, 5), padx=10)

    # button Button
    signup_button = Button(signup_frame, width=20, text="Signup", command=signup_func, bg="#4CAF50", font=('Poppins', 15))
    signup_button.grid(row=7, columnspan=2, pady=(5, 10))

    # login label
    label_signup = Label(signup_frame, text="Already have an account?", font=('Poppins', 10), bg='white', fg='black')
    label_signup.grid(row=8, column=0, pady=(5, 10), padx=(95, 115), sticky='w')
    # login Button
    login_button = Button(signup_frame, text="Login", command=open_index_window, bg="white", bd=0, fg='blue', cursor='hand2', font=('Poppins', 10))
    login_button.grid(row=8, column=0, pady=(5, 10), padx=(250, 110), sticky='w')

    # Run the Tkinter event loop
    window.mainloop()


# Call the index function to start the application
index()
