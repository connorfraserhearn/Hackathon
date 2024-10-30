import openai
# from gtts import gTTS
# from moviepy.editor import TextClip, ImageClip, AudioFileClip, CompositeVideoClip

# Initialize OpenAI API key
openai.api_key = "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"

# Function to get the ghost response
def get_ghost_response(question):
    messages = [
        {"role": "system",
         "content": "You are a ghost. Be scary."},
        {"role": "user", "content": question}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()


# def text_to_speech(text, filename="ghost_response.mp3"):
#     tts = gTTS(text=text, lang='en')
#     tts.save(filename)
#     print(f"Audio saved to {filename}")
#     return filename

# # Function to create video with text and audio
# def create_video(response_text, audio_file):
#     # Create an image background (could be a ghostly background image)
#     background = ImageClip("ghostly_background.jpg").set_duration(10)  # Use any image you'd like

#     # Add text overlay
#     text_clip = TextClip(response_text, fontsize=24, color='white', font="Arial").set_duration(10).set_position(
#         "center")

#     # Add audio
#     audio_clip = AudioFileClip(audio_file)

#     # Combine background, text, and audio
#     video = CompositeVideoClip([background, text_clip])
#     video = video.set_audio(audio_clip)

#     # Export final video
#     video.write_videofile("ghostly_response_video.mp4", fps=24)


def main():
    question = input("What would you like to ask the ghost? ")
    response_text = get_ghost_response(question)
    print(response_text)

    # # Generate audio for the response
    # audio_file = text_to_speech(response_text)

    # # Create video with the response text and audio
    # create_video(response_text, audio_file)
    # print("Video created: ghostly_response_video.mp4")


if __name__ == "__main__":
    main()
