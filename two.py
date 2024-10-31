import customtkinter as ctk
import openai
from PIL import Image, ImageTk

# Set your OpenAI API key here
openai.api_key = "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"

# Set the appearance mode to dark
ctk.set_appearance_mode("dark")

# Create the main window
app = ctk.CTk()
app.title("GHOST GPT")
app.geometry("1000x1000")

# Function to get input text and respond using OpenAI
def get_input_text():
    user_input = text_box.get()  # Get the text from the text box
    response = get_ghost_response(user_input)  # Generate AI response
    response_label.configure(text=response)  # Update response label

# Function to generate a response using OpenAI API
def get_ghost_response(question):
    messages = [
        {"role": "system",
         "content": "You are Alan Turing's ghost. Be scary."},
        {"role": "user", "content": question}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Add a label for user instructions
label = ctk.CTkLabel(app, text="A ghost approaches...", font=("Arial", 40), text_color="red")
label.pack(pady=20)

# Load and display an image
image_path = "Alan_Turing.png"  # Replace with your image path
image = Image.open(image_path)
image = image.resize((500, 500), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = ctk.CTkLabel(app, image=photo, text=" ")
image_label.image = photo  # Keep a reference to avoid garbage collection
image_label.pack(pady=10)

# Create a text box for user input
text_box = ctk.CTkEntry(app, width=300, font=("Arial", 20))
text_box.pack(pady=20)

# Button to submit the input
submit_button = ctk.CTkButton(app, text="Speak", command=get_input_text)
submit_button.pack(pady=10)

# Label to display the AI response
response_label = ctk.CTkLabel(app, text="", font=("Arial", 20), text_color="red", wraplength=600, justify="center")
response_label.pack(pady=10)

# Run the application
app.mainloop()
