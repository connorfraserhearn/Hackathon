import tkinter as tk
from tkinter import Label
import openai
import random
from PIL import Image, ImageTk

# Initialize OpenAI API key (replace 'your_api_key' with your actual key)
openai.api_key = "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"  # Add your OpenAI API key here

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are a wise and friendly ghost advisor, giving spooky yet thoughtful advice. You can become the ghost of anyone you are requested to be."}
]

def set_ghost_persona():
    chosen_ghost = ghost_entry.get()
    persona = f"You are the ghost of {chosen_ghost}, known for wisdom and unique perspectives. Speak thoughtfully and mystically."
    conversation_history.append({"role": "system", "content": persona})

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

def flicker_background(sequence_step=0):
    flash_duration = random.randint(100, 300)

    if sequence_step == 0:  # Single flash
        bg_label.place_forget()  # Hide the background
        window.after(flash_duration, return_to_dark)
        window.after(8000, lambda: flicker_background(1))  # Wait 8 seconds to move to the next step
    
    elif sequence_step == 1:  # Double flash
        bg_label.place_forget()  # Hide the background
        window.after(flash_duration, return_to_dark)
        window.after(flash_duration + 100, return_to_light)
        window.after(flash_duration + 200, return_to_dark)
        window.after(flash_duration + 300, return_to_light)
        window.after(flash_duration + 400, return_to_dark)
        window.after(8000, lambda: flicker_background(0))  # Wait 8 seconds to move back to the single flash

def return_to_dark():
    canvas.configure(bg="black")
    window.configure(bg="black")
    bg_label.lower()  # Send the background image to the back

def return_to_light():
    canvas.configure(bg="#333333")
    window.configure(bg="#333333")
    bg_label.lift()  # Bring the background image to the front

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
    
    label.place(x=width / 2 - label.winfo_width() / 2, y=50)
    user_entry.place(x=width / 2 - user_entry.winfo_width() / 2, y=100)
    ask_button.place(x=width / 2 - ask_button.winfo_width() / 2, y=150)
    ghost_response_label.place(x=width / 2 - ghost_response_label.winfo_width() / 2, y=250)

# Function to resize the background image when the window is resized
def resize_background(event=None):
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    resized_bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)
    bg_photo_resized = ImageTk.PhotoImage(resized_bg_image)
    
    bg_label.config(image=bg_photo_resized)
    bg_label.image = bg_photo_resized  # Keep a reference to prevent garbage collection

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
image_path = "halloween_background.png"  # Change to your image path

try:
    bg_image = Image.open(image_path).convert("RGBA")
    print("Background image loaded successfully.")
except Exception as e:
    print(f"Error loading background image: {e}")  # Debugging output

# Create a label to hold the background image
bg_label = Label(window)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create spooky label and entry
label = tk.Label(window, text="Ask the ghost a question:", font=("Helvetica", 14), fg="white", bg="black")
label.place(x=300, y=50)

user_entry = tk.Entry(window, width=40, font=("Helvetica", 12), bg="#333333", fg="white")
user_entry.place(x=300, y=100)

ask_button = tk.Button(window, text="Ask", command=ghost_response, bg="grey", fg="black")
ask_button.place(x=300, y=150)

ghost_response_label = tk.Label(window, text="", font=("Helvetica", 12, "italic"), fg="#90EE90", bg="black", wraplength=500)
ghost_response_label.place(x=300, y=250)

# Bind the resize function to the Configure event
window.bind("<Configure>", resize_background)

# Start the flickering and mist effects
flicker_background()
create_mist()
update_mist()

window.mainloop()
