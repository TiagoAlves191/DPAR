import tkinter as tk
from tkinter import ttk
import subprocess

def open_camera():
    loading_label.config(text="Opening Camera...")
    loading_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the loading frame
    loading_bar.start(10)  # Start the progress bar animation
    root.after(13000, hide_loading_screen)
    # Open the camera script
    subprocess.Popen(["python", "Fcam.py"])

def open_video():
    loading_label.config(text="Opening Video...")
    loading_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the loading frame
    loading_bar.start(10)  # Start the progress bar animation
    root.after(13000, hide_loading_screen)
    # Open the video script
    subprocess.Popen(["python", "ccg.py"])

def hide_loading_screen():
    loading_frame.place_forget()  # Hide the loading frame
    loading_bar.stop()  # Stop the progress bar animation

def leave_fullscreen(event):
    root.attributes('-fullscreen', False)

#def toggle_fullscreen(event=None):
    #root.attributes("-fullscreen", not root.attributes("-fullscreen"))


# Create the main window
root = tk.Tk()
root.title("DPAR")
root.attributes("-fullscreen", False)
root.configure(bg='#f8f9fa')  # Set background color to light gray
win_width, win_height = 1500, 1300
root.geometry(f'{win_width}x{win_height}')

# Bind the "Escape" key to leave full-screen mode
root.bind('<Escape>', leave_fullscreen)
# Create the logo image
logo_image = tk.PhotoImage(file="logo.png")  # Replace "logo.png" with your logo file path
smaller_logo = logo_image.subsample(3, 3)  # Make the logo even smaller
logo_label = tk.Label(root, image=smaller_logo, bg='#f8f9fa')  # Set background color to light gray
logo_label.pack(pady=20)  # Add some padding between logo and buttons

# Create a frame for buttons
button_frame = tk.Frame(root, bg='#f8f9fa')
button_frame.pack(pady=20)

# Create the buttons
camera_button = tk.Button(button_frame, text="Live", command=open_camera, font=("Arial", 16, "bold"), width=15, bg='#007BFF', fg='#007BFF', bd=0, padx=10, pady=5)
camera_button.grid(row=0, column=0, padx=20)

video_button = tk.Button(button_frame, text="Video", command=open_video, font=("Arial", 16, "bold"), width=15, bg='#FF5722', fg='#007BFF', bd=0, padx=10, pady=5)
video_button.grid(row=0, column=1, padx=20)

# Create the loading screen inside the main window
loading_frame = tk.Frame(root, bg='white', width=300, height=200)

loading_label = tk.Label(loading_frame, text="", font=("Arial", 20), bg='#f8f9fa')
loading_label.pack(pady=20)

loading_bar = ttk.Progressbar(loading_frame, mode='indeterminate', length=200)
loading_bar.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
