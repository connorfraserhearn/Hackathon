import tkinter as tk
from tkinter import Label, Entry, Button
import openai
import random
import requests
import pygame
import threading
from PIL import Image, ImageTk

# Initialize OpenAI and ElevenLabs API keys (replace with your actual keys)
openai.api_key = ""
api_key = ""  # Replace with your ElevenLabs API key

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are a wise and friendly ghost advisor, giving spooky yet thoughtful advice. You can become the ghost of anyone you are requested to be."}
]

# Function to generate speech with ElevenLabs API and play it immediately
def generate_speech(text, voice_id="Dz5ybcCvrahl9DAD0yAG", output_filename="output.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.2,
            "similarity_boost": 0.9
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        # Save the audio content to a file
        with open(output_filename, "wb") as file:
            file.write(response.content)
        print(f"Audio saved as {output_filename}")
        
        # Play the audio file in a separate thread
        threading.Thread(target=play_audio, args=(output_filename,)).start()
    else:
        print("Error:", response.status_code, response.text)

# Function to play audio using pygame
def play_audio(output_filename):
    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load(output_filename)  # Load the mp3 file
    pygame.mixer.music.play()  # Play the audio
    while pygame.mixer.music.get_busy():  # Wait until the sound is finished playing
        pygame.time.Clock().tick(10)  # Add a small delay to prevent high CPU usage
    pygame.mixer.quit()  # Clean up the mixer after playing

# Function to set ghost persona
def set_ghost_persona():
    chosen_ghost = ghost_entry.get().strip()
    persona = f"You are the ghost of {chosen_ghost}, known for wisdom and unique perspectives. Speak thoughtfully and mystically."
    conversation_history.append({"role": "system", "content": persona})
    load_ghost_image(chosen_ghost)

# Function to load ghost image
def load_ghost_image(ghost_name):
    formatted_name = ghost_name.lower().replace(" ", "_")
    try:
        ghost_image_path = f"{formatted_name}.png"
        ghost_image = Image.open(ghost_image_path)
        ghost_image = ghost_image.resize((150, 150), Image.LANCZOS)  # Adjusted image size
        ghost_photo = ImageTk.PhotoImage(ghost_image)
        ghost_image_label.config(image=ghost_photo)
        ghost_image_label.image = ghost_photo  # Keep a reference to prevent garbage collection
    except FileNotFoundError:
        ghost_image_label.config(image="")
        ghost_image_label.config(text="Ghost image not found.")

# Function to handle ghost response
def ghost_response():
    user_input = user_entry.get()
    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        answer = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": answer})
        
        # Display the response text before generating speech
        ghost_response_label.config(text=answer)
        
        # Generate speech with the assistant's response
        generate_speech(text=answer, voice_id="Dz5ybcCvrahl9DAD0yAG", output_filename="output.mp3")

    except Exception as e:
        answer = f"The ghost is silent... (Error: {e})"
        ghost_response_label.config(text=answer)

# Function to flicker background
def flicker_background(sequence_step=0):
    flash_duration = random.randint(100, 300)
    canvas.configure(bg="#666666")
    window.configure(bg="#666666")
    window.after(flash_duration, return_to_dark)

    if sequence_step == 0:
        window.after(8000, lambda: flicker_background(1))
    
    elif sequence_step == 1:
        window.after(8000, lambda: flicker_background(2))

    elif sequence_step == 2:
        window.after(flash_duration + 100, return_to_light)
        window.after(flash_duration + 200, return_to_dark)
        window.after(flash_duration + 300, return_to_light)
        window.after(flash_duration + 400, return_to_dark)
        window.after(8000, lambda: flicker_background(0))

def return_to_dark():
    canvas.configure(bg="black")
    window.configure(bg="black")
    bg_label.lower()  # Send the background image to the back

def return_to_light():
    canvas.configure(bg="#333333")
    window.configure(bg="#333333")
    bg_label.lift()  # Bring the background image to the front

# Function to create ominous mist particles from the sides
def create_mist():
    for _ in range(5):
        side = random.choice([-1, 1])
        x = 0 if side == -1 else canvas.winfo_width()
        dx = random.uniform(-1.0, 1.0) * side
        y = canvas.winfo_height()
        size = random.randint(10, 60)
        
        gray_value = random.randint(0, 80)
        mist_color = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
        
        mist_particle = canvas.create_oval(
            x, y, x + size, y + size,
            fill=mist_color, outline="", tags="mist"
        )
        
        # Schedule the mist particle to disappear after 40 seconds
        window.after(50000, lambda particle=mist_particle: canvas.delete(particle))

        # Move the mist particle
        move_mist(mist_particle, dx)

def move_mist(mist_particle, dx):
    canvas.move(mist_particle, dx, -random.uniform(0.1, 0.13))
    coords = canvas.coords(mist_particle)
    if not coords or (coords[1] < 0):
        canvas.delete(mist_particle)
        return
    window.after(50, lambda: move_mist(mist_particle, dx))

# Update mist periodically to keep the screen filled
def update_mist():
    create_mist()
    window.after(500, update_mist)

# Function to position elements dynamically
def center_elements():
    width = window.winfo_width()
    height = window.winfo_height()

    label.place(x=width / 2 - label.winfo_width() / 2, y=20)
    ghost_entry.place(x=width / 2 - ghost_entry.winfo_width() / 2, y=60)
    set_ghost_button.place(x=width / 2 - set_ghost_button.winfo_width() / 2, y=100)
    user_entry.place(x=width / 2 - user_entry.winfo_width() / 2, y=150)
    ask_button.place(x=width / 2 - ask_button.winfo_width() / 2, y=200)
    ghost_image_label.place(x=width / 2 - 75, y=250)  # Ghost image above response
    ghost_response_label.place(x=width / 2 - ghost_response_label.winfo_width() / 2, y=ghost_image_label.winfo_y() + ghost_image_label.winfo_height() + 10)  # Text below the ghost image

# Function to resize the background image when window is resized
def resize_background(event=None):
    # Resize the background image based on the current window dimensions
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    resized_bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)
    bg_photo_resized = ImageTk.PhotoImage(resized_bg_image)
    
    # Update the image of the background label
    bg_label.config(image=bg_photo_resized)
    bg_label.image = bg_photo_resized  # Keep a reference to prevent garbage collection

    # Re-center other UI elements
    center_elements()

# Create the main Tkinter window
window = tk.Tk()
window.title("Whispers of STEM Beyond the Grave")
window.geometry("800x600")  # Set the default window size
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack(fill=tk.BOTH, expand=True)

# Load background image
bg_image_path = "halloween_background.png"  # Replace with your actual background image path
bg_image = Image.open(bg_image_path)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(window, image=bg_photo, bd=0)
bg_label.place(relwidth=1, relheight=1)

# Elements of the GUI
label = Label(window, text="Whispers of STEM Beyond the Grave", font=("Helvetica", 24), fg="white", bg="black")
ghost_entry = Entry(window, font=("Helvetica", 16))
set_ghost_button = Button(window, text="Summon your ghost", command=set_ghost_persona, font=("Helvetica", 14))
user_entry = Entry(window, font=("Helvetica", 16))
ask_button = Button(window, text="Talk to your ghost", command=ghost_response, font=("Helvetica", 14))
ghost_response_label = Label(window, text="", font=("Helvetica", 16), fg="white", bg="black")
ghost_response_label.config(wraplength=600)  # Set the wrap length to allow text wrapping
ghost_image_label = Label(window, bg="black")

# Start flickering background and mist creation
flicker_background()
update_mist()

# Center elements and bind the resize event
center_elements()
window.bind("<Configure>", resize_background)

# Start the Tkinter event loop
window.mainloop()
