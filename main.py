from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile, FileDialog
from pygame import mixer
import os
from google.cloud import texttospeech
from poppler import load_from_file

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'logical-honor-341113-c6ae6a879673.json'
client = texttospeech.TextToSpeechClient()


def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    for voice in voices.voices:
        # Display the voice's name. Example: tpc-vocoded
        print(f"Name: {voice.name}")

        # Display the supported language codes for this voice. Example: "en-US"
        for language_code in voice.language_codes:
            print(f"Supported language: {language_code}")

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Display the SSML Voice Gender
        print(f"SSML Voice Gender: {ssml_gender.name}")

        # Display the natural sample rate hertz for this voice. Example: 24000
        print(
            f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")


text = ""


def get_audio():

    sys_text = texttospeech.SynthesisInput(ssml=text)

    voice = texttospeech.VoiceSelectionParams(
        name='en-US-Standard-E',
        language_code='en-US'
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response1 = client.synthesize_speech(
        input=sys_text,
        voice=voice,
        audio_config=audio_config
    )

    with open('audio.mp3', 'wb') as output:
        output.write(response1.audio_content)


def open_file():
    global text
    # grab the filename of the pdf file
    open_file = filedialog.askopenfilename(
        initialdir="E:\Python projects\PDF-to-audio",
        title="Open PDF file",
        filetypes=(
            ("PDF Files", "*.pdf"),
            ("All Files", "*.*")))
    # check to see if there is a file
    if open_file:
        # Open the PDF file
        pdf_file = load_from_file(open_file)
        print(f'*********{pdf_file}***************')
        # Set the page to read
        page = pdf_file.create_page(1)
        # Extract the text from the pdf file
        text = page.text()

        # Add text to textbox
        text_box.insert(1.0, text)
        return text


mixer.init()


def play_music():
    mixer.music.load("audio.mp3")
    mixer.music.play()


root = Tk()
root.title("PDF to audio")
header = Frame(root, width=800, height=175)
header.grid(columnspan=3, rowspan=3, row=0)

# main content area - image extraction
main_content = Frame(root, width=800, height=250)
main_content.grid(columnspan=3, rowspan=1, row=3)


# Create a textbox
text_box = Text(root, height=30, width=110)
text_box.grid(columnspan=3, rowspan=2, row=2)

# Create a Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# add dropdown menus
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Convert", command=get_audio)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add play button
play_button = Button(root, text="Play", command=play_music)
play_button.grid(row=2, column=3)


root.mainloop()
