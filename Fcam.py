import os
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image, ImageTk
from twilio.rest import Client
from datetime import datetime
import mysql.connector

# Load YOLO model
modelo = YOLO('yolov8n.pt')

# Load class names from "coco.names"
with open("coco.names", "r") as my_file:
    class_list = my_file.read().strip().split("\n")

# Minimum distance for crowd detection
min_distance = 100  # You can adjust this value

# Twilio account credentials
account_sid = 'AC2ebfa0c76307c276e9e5136be4eeacbe'
auth_token = '799cae47a3357c07f67604a6a1addad7'

# Create a directory to save the screenshots
if not os.path.exists("agglomeration_screenshots"):
    os.makedirs("agglomeration_screenshots")

# Function to send SMS
def enviar_sms(numero_destino, localizacao, timestamp):
    client = Client(account_sid, auth_token)

    mensagem = f"Aglomeração detectada em {localizacao} às {timestamp}."
    message = client.messages.create(
        body=mensagem,
        from_='+14128992912',  # Your Twilio number
        to=numero_destino  # Destination number
    )

    print("SMS enviado com sucesso!")

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to toggle fullscreen mode
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Function to process video and display crowd alerts
def process_video():
    ret, frame = cap.read()
    if not ret:
        return

    # Detect objects using YOLO
    results = modelo(frame)

    # Initialize a list to store middle points
    middle_points = []

    persons_detected = 0  # Initialize count of persons detected

    for detection in results[0]:
        for box in detection.boxes:
            class_id = detection.names[box.cls[0].item()]
            xyxy = box.xyxy[0].tolist()
            xyxy = [round(x) for x in xyxy]
            conf = round(box.conf[0].item(), 2)

            if class_id == 'person':
                persons_detected += 1  # Increment count of persons detected

                x, y, w, h = xyxy  # Bounding box coordinates
                cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)  # Draw bounding box
                middle_x = int((x + w)/ 2)
                middle_y = int((y + h) / 2)

                cv2.circle(frame, (middle_x, middle_y), 10, (255, 0,0), 1)
                middle_points.append((middle_x, middle_y))

    # Check for crowd
    agglomeration_detected = False
    for i in range(len(middle_points)):
        for j in range(i + 1, len(middle_points)):
            dist = calculate_distance(middle_points[i], middle_points[j])
            if dist <= min_distance:
                cv2.line(frame, middle_points[i], middle_points[j], (0,0,255), 1) 
                print("Existe aglomeração: Distância minima Violada")
                agglomeration_detected = True
                break

    # If agglomeration is detected, save the current frame
    if agglomeration_detected:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join("agglomeration_screenshots/live", f"agglomeration_{timestamp}.png")
        cv2.imwrite(screenshot_path, frame)
        print(f"Agglomeration screenshot saved at: {screenshot_path}")

        # Fetch contact number from the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dpar"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT Contacto FROM gestores")
        gestor_contacto = cursor.fetchone()[0]
        conn.close()

        if persons_detected >= 2:  # Check if 2 or more persons detected
            enviar_sms(gestor_contacto, "Câmera Frontal", timestamp)

    # Display the count of persons detected on the screen
    cv2.putText(frame, f"Persons detected: {persons_detected}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Resize frame to match window size
    resized_frame = cv2.resize(frame, (root.winfo_width(), root.winfo_height()))

    # Display the frame with detections
    img = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
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

# Open the camera
cap = cv2.VideoCapture(0)

# Create a panel for displaying OpenCV image
panel = tk.Label(root)
panel.pack(fill=tk.BOTH, expand=True)

# Start the main Tkinter loop
root.after(1, process_video)  # Call process_video after 1 millisecond
root.mainloop()
