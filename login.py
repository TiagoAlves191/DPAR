import tkinter as tk
from tkinter import messagebox
import subprocess
import mysql.connector
from tkinter import PhotoImage

def open_main_page():
    username = username_entry.get()
    password = password_entry.get()

    # Connect to MySQL/MariaDB database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dpar"
    )
    cursor = conn.cursor()

    # Execute a query to fetch the user's data based on the provided username and password
    cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    # Check if the user exists and the password is correct
    if not user:
        messagebox.showerror("Login Failed", "Invalid username or password")
        conn.close()
        return

    # Fetch the corresponding manager's data
    cursor.execute("SELECT * FROM gestores WHERE Nr_Gestor=%s", (user[0],))
    manager = cursor.fetchone()

    # Check if the manager exists and has the permission to login (Estado = 1)
    if not manager or manager[2] != 1:  # Assuming the 'Estado' column is at index 2
        messagebox.showerror("Login Failed", "User does not have permission to access the application. Please contact the Manager if you think this is an error")
        conn.close()
        return

    # Check if the manager is an admin (Admin = 1)
    if manager[4] != 1:  # Assuming the 'Admin' column is at index 3
        # Successful login, open main interface window
        subprocess.Popen(["python", "test.py"])
        root.destroy()  # Close the login window
    else:
        # Successful login as an admin, open "gerir.py" page
        subprocess.Popen(["python", "gerir.py"])
        root.destroy()  # Close the login window

    # Close the database connection
    conn.close()

# Create the login window
root = tk.Tk()
root.title("Login")
root.configure(bg='#f8f9fa')  # Set background color to light gray
root.attributes("-fullscreen", True)  # Start in fullscreen mode

# Function to leave fullscreen mode
def leave_fullscreen(event=None):
    root.attributes("-fullscreen", False)

# Bind the "Escape" key to leave fullscreen mode
root.bind("<Escape>", leave_fullscreen)

# Create the logo image
logo_image = PhotoImage(file="logo.png")  # Replace "logo.png" with your logo file path
logo_label = tk.Label(root, image=logo_image, bg='#f8f9fa')
logo_label.pack(pady=50)

# Center the login window
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width/2) - (window_width/2)
y_coordinate = (screen_height/2) - (window_height/2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

# Create the username label and entry
username_label = tk.Label(root, text="Username:", font=("Arial", 14), bg='#f8f9fa')
username_label.pack(pady=10)
username_entry = tk.Entry(root, font=("Arial", 14))
username_entry.pack(pady=10)

# Create the password label and entry
password_label = tk.Label(root, text="Password:", font=("Arial", 14), bg='#f8f9fa')
password_label.pack(pady=10)
password_entry = tk.Entry(root, show="*", font=("Arial", 14))
password_entry.pack(pady=10)

# Create the login button
login_button = tk.Button(root, text="Login", command=open_main_page, font=("Arial", 14, "bold"), bg='#007BFF', fg='#007BFF', bd=0, padx=10, pady=5)
login_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
