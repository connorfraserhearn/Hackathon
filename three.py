import customtkinter as ctk
import openai
from PIL import Image, ImageTk
import random

# Set your OpenAI API key
openai.api_key = "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"

# Set the appearance mode to dark
ctk.set_appearance_mode("dark")

# Initialize the conversation history list
conversation_history = []

# Create the main application window
app = ctk.CTk()
app.title("GHOST GPT")
app.geometry("1000x1000")

def set_ghost_persona():
    # Get the user's chosen ghost persona
    chosen_ghost = persona_entry.get()
    persona_message = f"You are the ghost of {chosen_ghost}, known for wisdom and unique perspectives. Speak thoughtfully and mystically."
    
    # Clear previous conversation history and set new persona
    conversation_history.clear()
    conversation_history.append({"role": "system", "content": persona_message})
    
    # Update persona label with chosen ghost name
    persona_label.configure(text=f"You are now speaking with the ghost of {chosen_ghost}.")
    
    # Display the corresponding ghost image if available
    try:
        image_path = f"{chosen_ghost.replace(' ', '_')}.png"  # Assumes each ghost has an image file
        image = Image.open(image_path)
        image = image.resize((500, 500), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        # Update the image label with the new ghost image
        image_label.configure(image=photo, text=" ")
        image_label.image = photo  # Keep a reference to avoid garbage collection
    except FileNotFoundError:
        response_label.configure(text="No image found for this ghost.")

def get_input_text():
    user_input = text_box.get()  # Get text from the text box
    conversation_history.append({"role": "user", "content": user_input})  # Add to conversation history
    
    # Generate response from OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            max_tokens=300,
            temperature=0.7
        )
        answer = response.choices[0].message['content'].strip()
        conversation_history.append({"role": "assistant", "content": answer})  # Append AI response to history
    except Exception as e:
        answer = f"The ghost is silent... (Error: {e})"
    
    # Update response label with the ghost's response
    response_label.configure(text=answer)

# GUI setup
instructions_label = ctk.CTkLabel(app, text="Enter the name of the ghost you want to summon (e.g., 'Alan Turing'):", font=("Arial", 20), text_color="red")
instructions_label.pack(pady=10)

persona_entry = ctk.CTkEntry(app, width=300, font=("Arial", 20))
persona_entry.pack(pady=10)

set_persona_button = ctk.CTkButton(app, text="Summon Ghost", command=set_ghost_persona)
set_persona_button.pack(pady=10)

label = ctk.CTkLabel(app, text="Ask the ghost a question:", font=("Arial", 30), text_color="red")
label.pack(pady=20)

# Load placeholder image initially
placeholder_image = Image.new("RGB", (500, 500), color=(0, 0, 0))  # Black placeholder
photo = ImageTk.PhotoImage(placeholder_image)

image_label = ctk.CTkLabel(app, image=photo, text=" ")
image_label.image = photo  # Keep reference
image_label.pack(pady=10)

text_box = ctk.CTkEntry(app, width=400, font=("Arial", 20))
text_box.pack(pady=20)

submit_button = ctk.CTkButton(app, text="Ask", command=get_input_text)
submit_button.pack(pady=10)

response_label = ctk.CTkLabel(app, text="", font=("Arial", 20), text_color="red", wraplength=600, justify="center")
response_label.pack(pady=10)

persona_label = ctk.CTkLabel(app, text="", font=("Arial", 18), text_color="green")
persona_label.pack(pady=5)

app.mainloop()
