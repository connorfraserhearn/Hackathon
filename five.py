import tkinter as tk
from tkinter import Label, Entry, Button
import openai
import random
from PIL import Image, ImageTk

# Initialize OpenAI API key (replace 'your_api_key' with your actual key)
openai.api_key = "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"  # Add your OpenAI API key here

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are a wise and friendly ghost advisor, giving spooky yet thoughtful advice. You can become the ghost of anyone you are requested to be."}
]

# Function to set ghost persona
def set_ghost_persona():
    chosen_ghost = ghost_entry.get().strip()
    persona = f"You are the ghost of {chosen_ghost}, known for wisdom and unique perspectives. Speak thoughtfully and mystically."
    conversation_history.append({"role": "system", "content": persona})
    load_ghost_image(chosen_ghost)

# Function to load ghost image
def load_ghost_image(ghost_name):
    # Format the ghost name to lowercase and replace spaces with underscores
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
    ghost_response_label.place(x=width / 2 - ghost_response_label.winfo_width() / 2, y=320)  # Adjusted position for the ghost response

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
window.title("Misty Ghostly Advisor")
window.geometry("600x400")
window.configure(bg="black")

# Define the canvas for drawing mist particles
canvas = tk.Canvas(window, width=600, height=400, bg="black", highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

# Load and prepare the background image
bg_image_path = "halloween_background.png"  # Change to your image path
bg_image = Image.open(bg_image_path).convert("RGBA")

# Create a label to hold the background image
bg_label = Label(window)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create spooky label and entries
label = tk.Label(window, text="Ask the ghost a question:", font=("Helvetica", 14), fg="white", bg="black")
label.place(x=300, y=20)

ghost_entry = Entry(window, width=20, font=("Helvetica", 12), bg="#333333", fg="white")
ghost_entry.place(x=300, y=60)

set_ghost_button = Button(window, text="Set Ghost", command=set_ghost_persona, bg="grey", fg="black")
set_ghost_button.place(x=300, y=100)

user_entry = tk.Entry(window, width=40, font=("Helvetica", 12), bg="#333333", fg="white")
user_entry.place(x=300, y=150)

ask_button = tk.Button(window, text="Ask", command=ghost_response, bg="grey", fg="black")
ask_button.place(x=300, y=200)

# Ghost image label
ghost_image_label = Label(window, bg="black")
ghost_image_label.place(x=50, y=250)  # Positioned above the response label

ghost_response_label = tk.Label(window, text="", font=("Helvetica", 12, "italic"), fg="#90EE90", bg="black", wraplength=500)
ghost_response_label.place(x=300, y=320)  # Positioned below the ghost image

# Bind the resize function to the Configure event
window.bind("<Configure>", resize_background)

flicker_background()
create_mist()
update_mist()

window.mainloop()
