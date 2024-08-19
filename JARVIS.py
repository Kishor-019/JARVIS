from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import time
import pyttsx3
import speech_recognition as sr

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
head = Label(root, text="Hi!! I am JARVIS", font=('calibri', 16, 'bold'))
head.pack(pady=10)

# Paths to the GIFs
main_gif_path = r"D:\BCS_IT\Python Project\JARVIS\self\img\sleeping.gif"
greeting_gif_path = r"D:\BCS_IT\Python Project\JARVIS\self\img\greeting.gif"
byee_gif_path = r"D:\BCS_IT\Python Project\JARVIS\self\img\byee.gif"

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

# Functions to handle button actions
def play_greeting_gif():
    global greeting_frames
    # Stop the current animation
    image_label.configure(image=None)  # Clear the current image
    # Display the greeting GIF
    greeting_frames = load_gif_frames(greeting_gif_path)
    if greeting_frames:
        # Display the first frame and start playing the GIF
        play_gif(greeting_frames, loop=False)
        # Remove the Wake Up button
        wake_up_button.pack_forget()
        # Show the Talk button
        talk_button.pack(side=LEFT, padx=10)
        # Speak the greeting message
        speak('Hi! how can I help you')
    else:
        print("Failed to load greeting GIF frames.")

def exit_program():
    frames = load_gif_frames(byee_gif_path)
    play_gif(frames, loop=False, on_complete=root.quit)

def start_sleeping_gif():
    global sleeping_frames
    sleeping_frames = load_gif_frames(main_gif_path)
    play_gif(sleeping_frames, loop=True)

# Create a label widget to hold the GIF animation
image_label = Label(root)
image_label.pack(pady=10)

# Create buttons
button_frame = Frame(root)
button_frame.pack(pady=10)

wake_up_button = Button(button_frame, text="Wake Up", command=play_greeting_gif, font=('calibri', 12, 'bold'), bg='#4CAF50', fg='white')
wake_up_button.pack(side=LEFT, padx=10)

exit_button = Button(button_frame, text="Exit", command=exit_program, font=('calibri', 12, 'bold'), bg='#f44336', fg='white')
exit_button.pack(side=RIGHT, padx=10)

talk_button = Button(button_frame, text="Talk", command=lambda: talk(), font=('calibri', 12, 'bold'), bg='#2196F3', fg='white')
talk_button.pack_forget()  # Initially hidden

# Create a label for the clock with a white background, black text, and a border
clock_label = Label(root, font=('calibri', 18, 'bold'), background='white', foreground='black', padx=10, pady=10,
                    borderwidth=2, relief='solid')
clock_label.pack(side=TOP, anchor=NW, padx=10, pady=(10, 0))

# Function to update the clock every second
def update_clock():
    current_time = time.strftime('%I:%M:%S %p')  # Time in 12-hour format with AM/PM
    current_date = time.strftime('%A, %B %d, %Y')  # Day, Month Day, Year
    clock_label.config(text=f"{current_time}\n{current_date}")
    root.after(1000, update_clock)  # Update the clock every 1000 milliseconds (1 second)

# Start the clock
update_clock()

# Global variables to manage animation state
animation_running = False
talk_animation_running = False

# Start by playing the sleeping GIF and set it to loop
start_sleeping_gif()

# Create a label for the "Listening..." message, initially hidden
talk_label = Label(root, font=('calibri', 14), background='white', foreground='black')
talk_label.pack(side=TOP, pady=5)

# Create a text box for displaying detected speech with border and padding
speech_text_box = Text(root, font=('calibri', 14), background='white', foreground='black', height=6, width=60, wrap=WORD,
                       borderwidth=2, relief='solid')
speech_text_box.pack(side=BOTTOM, pady=10, padx=10)

# Function to animate the ellipses
def talk():
    global talk_animation_running
    # Show "Listening..." message immediately
    talk_label.config(text="Listening..")
    # Speak the listening message
    speak('I am listening')
    # Update the text box with animated ellipses
    talk_animation_running = True
    animate_ellipses()
    # Start listening for speech
    listen_for_speech()

def animate_ellipses():
    if not talk_animation_running:
        return
    current_text = talk_label.cget("text")  # Get current text
    if current_text.endswith(".."):
        talk_label.config(text="Listening...")  # Reset text
    else:
        talk_label.config(text=current_text + ".")
    root.after(500, animate_ellipses)

# Function to listen for speech and display the result in the text box
def listen_for_speech():
    global talk_animation_running
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
        talk_animation_running = False  # Stop ellipses animation
        talk_label.config(text="")  # Hide the "Listening..." text

# Event loop to make the window interactive
root.mainloop()
