from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import pyttsx3
import speech_recognition as sr
import threading
import time

# Initialize the TTS engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Create a base for the GUI
root = Tk()

# Set the window size and limits
root.geometry("600x800")
root.minsize(300, 400)

# Add a label with some text
head = Label(root, text="Hi! I am JARVIS", font=('calibri', 16, 'bold'))
head.pack(pady=10)

# Paths to the GIFs
greeting_gif_path = r"D:\BCS_IT\Python Project\JARVIS\Final\img\greeting.gif"
byee_gif_path = r"D:\BCS_IT\Python Project\JARVIS\Final\img\byee.gif"

# Function to load GIF frames
def load_gif_frames(gif_path):
    image = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(image)]
    return frames

# Function to play a GIF
def play_gif(frames, loop=False, on_complete=None):
    def update_frame(index):
        frame = frames[index % len(frames)]
        image_label.configure(image=frame)
        if loop:
            root.after(100, update_frame, (index + 1) % len(frames))
        else:
            if index + 1 < len(frames):
                root.after(100, update_frame, index + 1)
            else:
                if on_complete:
                    on_complete()

    update_frame(0)

# Function to handle the Talk button action
def start_talk():
    global greeting_frames
    # Play the greeting GIF
    play_gif(greeting_frames, loop=False)
    # Speak "I am listening"
    speak("I am listening")
    # Start a new thread to handle speech recognition
    threading.Thread(target=listen_for_speech).start()

# Function to play the Bye GIF and exit the program
def exit_program():
    global byee_frames
    # Play the Bye GIF
    play_gif(byee_frames, loop=False, on_complete=root.quit)

# Create a label widget to hold the GIF image
image_label = Label(root)
image_label.pack(pady=10)

# Load and display the first frame of the greeting GIF
greeting_frames = load_gif_frames(greeting_gif_path)
image_label.configure(image=greeting_frames[0])

# Load the Bye GIF frames
byee_frames = load_gif_frames(byee_gif_path)

# Create buttons
button_frame = Frame(root)
button_frame.pack(pady=10)

talk_button = Button(button_frame, text="Talk", command=start_talk, font=('calibri', 12, 'bold'), bg='#2196F3', fg='white')
talk_button.pack(side=LEFT, padx=10)

exit_button = Button(button_frame, text="Exit", command=exit_program, font=('calibri', 12, 'bold'), bg='#f44336', fg='white')
exit_button.pack(side=RIGHT, padx=10)

# Create a text box for displaying detected speech
speech_text_box = Text(root, font=('calibri', 14), background='white', foreground='black', height=6, width=60, wrap=WORD,
                       borderwidth=2, relief='solid')
speech_text_box.pack(side=BOTTOM, pady=10, padx=10)

# Function to listen for speech and display the result in the text box
def listen_for_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            speech_text = recognizer.recognize_google(audio)
            print(f"Detected Speech: {speech_text}")
            # Update the speech text box
            speech_text_box.delete("1.0", "end")  # Clear previous text
            speech_text_box.insert("1.0", speech_text)  # Insert new text
        except sr.UnknownValueError:
            speech_text_box.delete("1.0", "end")
            speech_text_box.insert("1.0", "Sorry, I did not understand that.")
        except sr.RequestError as e:
            speech_text_box.delete("1.0", "end")
            speech_text_box.insert("1.0", f"Sorry, there was an error: {e}")

# Function to update the digital clock with date and time
def update_clock():
    current_time = time.strftime('%H:%M:%S')
    current_date = time.strftime('%Y-%m-%d')
    clock_canvas.delete("all")  # Clear the canvas
    clock_canvas.create_oval(5, 5, 145, 145, fill='#FFA07A', outline="black", width=4)  # Draw filled clock circle
    clock_canvas.create_text(75, 50, text=current_date, font=('calibri', 10, 'bold'))
    clock_canvas.create_text(75, 90, text=current_time, font=('calibri', 16, 'bold'))
    root.after(1000, update_clock)

# Create a canvas for the clock
clock_canvas = Canvas(root, width=150, height=150)
clock_canvas.place(relx=1.0, y=10, anchor='ne')

# Start updating the clock
update_clock()

# Event loop to make the window interactive
root.mainloop()
