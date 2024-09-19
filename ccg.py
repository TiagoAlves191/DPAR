import os
import tkinter as tk
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime

# Load YOLO model
modelo = YOLO('yolov8n.pt')

# Open the video
cap = cv2.VideoCapture("videoteste.mp4")

# Create a directory to save the screenshots
screenshot_dir = "agglomeration_screenshots/video"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# Function to toggle fullscreen mode
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Load class names from "coco.names"
with open("coco.names", "r") as my_file:
    class_list = my_file.read().strip().split("\n")

# Minimum distance for crowd detection
min_distance = 100  # You can adjust this value

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to insert detection information into the database
def insert_detection_info(timestamp, persons_detected, agglomeration):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dpar"
        )
        cursor = conn.cursor()
        
        # Insert data into the "detecoes" table
        cursor.execute("INSERT INTO detecoes (Tipo, Data, Hora, Nmr_pessoas, Aglomeracao) VALUES (%s, %s, %s, %s, %s)",
                       ("Video", timestamp.date(), timestamp.time(), persons_detected, 1 if agglomeration else 0))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error while inserting detection info:", e)

# Variables to keep track of the last insertion time
last_insert_time = None

# Function to process video and display crowd alerts
def process_video():
    global last_insert_time
    ret, frame = cap.read()
    if not ret:
        return

    # Detect objects using YOLO
    results = modelo(frame, verbose=False)

    # Initialize a list to store middle points
    middle_points = []
    persons_detected = 0  # Initialize count of persons detected
    
    for detection in results[0]:
        for box in detection.boxes:
            class_id = detection.names[box.cls[0].item()]
            xyxy = box.xyxy[0].tolist()
            xyxy = [round(x) for x in xyxy]
            conf = round(box.conf[0].item(), 2)

            if class_id == 'person' and conf >= 0.4:
                x, y, w, h = xyxy  # Bounding box coordinates
                cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)  # Draw bounding box
                middle_x = int((x + w) / 2)
                middle_y = int((y + h) / 2)

                cv2.circle(frame, (middle_x, middle_y), 10, (255, 0, 0), 1)
                middle_points.append((middle_x, middle_y))
                persons_detected += 1  # Increment count of persons detected

    # Check for crowd
    agglomeration_detected = False
    for i in range(len(middle_points)):
        for j in range(i + 1, len(middle_points)):
            dist = calculate_distance(middle_points[i], middle_points[j])
            if dist <= min_distance:
                cv2.line(frame, middle_points[i], middle_points[j], (0, 0, 255), 1) 
                print("Existe aglomeração: Distância mínima violada")
                agglomeration_detected = True
                break

    # Get current timestamp
    timestamp = datetime.now()

    # Insert detection information into the database every 10 seconds
    if last_insert_time is None or (timestamp - last_insert_time).seconds >= 10:
        insert_detection_info(timestamp, persons_detected, agglomeration_detected)
        last_insert_time = timestamp

    # If agglomeration is detected, save the current frame
    if agglomeration_detected:
        folder_path = os.path.join(screenshot_dir, timestamp.strftime('%Y'), timestamp.strftime('%m'), timestamp.strftime('%d'), timestamp.strftime('%H'))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        screenshot_path = os.path.join(folder_path, f"{timestamp.strftime('%M%S')}.png")
        cv2.imwrite(screenshot_path, frame)
        print(f"Agglomeration screenshot saved at: {screenshot_path}")

    # Display the count of persons detected on the screen
    cv2.putText(frame, f"Persons detected: {persons_detected}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with detections
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)
    panel.img = img
    panel.config(image=img)
    root.after(1, process_video)  # Call process_video after 1 millisecond

# Create the main Tkinter window
root = tk.Tk()
root.title("DPAR")
root.attributes("-fullscreen", True)  # Open window in full screen mode
root.bind("<Escape>", toggle_fullscreen)  # Bind Escape key to toggle fullscreen mode
root.bind("<F11>", toggle_fullscreen)  # Bind F11 key to toggle fullscreen mode

# Configure the action of the main window close button
def close_application():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_application)

# Create a panel for displaying OpenCV image
panel = tk.Label(root)
panel.pack(fill=tk.BOTH, expand=True)

# Start the main Tkinter loop
root.after(1, process_video)  # Call process_video after 1 millisecond
root.mainloop()
