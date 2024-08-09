import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import pyttsx3
import speech_recognition as sr

class JarvisGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS")
        self.geometry("400x500")  # Adjusted size

        # File paths
        self.sleeping_gif_path = r"D:\BCS_IT\Python Project\JARVIS\img\sleeping.gif"
        self.waking_gif_path = r"D:\BCS_IT\Python Project\JARVIS\img\greeting.gif"
        self.goodbye_gif_path = r"D:\BCS_IT\Python Project\JARVIS\img\byee.gif"

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()

        # Create GUI components
        self.gif_label = tk.Label(self)
        self.gif_label.pack(pady=20)
        self.load_gif(self.sleeping_gif_path)

        # Wake Up, Talk, and Exit buttons
        self.wake_button = ttk.Button(self, text="Wake Up JARVIS", command=self.wake_up_jarvis)
        self.wake_button.pack(pady=10)

        self.talk_button = ttk.Button(self, text="Talk", command=self.start_talking)
        self.talk_button.pack_forget()  # Initially hidden

        self.exit_button = ttk.Button(self, text="Exit", command=self.exit_jarvis)
        self.exit_button.pack(pady=10)

        # Text area to display recognized speech
        self.text_area = tk.Text(self, wrap='word', height=10, state='disabled')
        self.text_area.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    def load_gif(self, gif_path):
        gif = Image.open(gif_path)
        self.frames = [ImageTk.PhotoImage(frame.copy().resize((150, 150))) for frame in ImageSequence.Iterator(gif)]
        self.current_frame = 0
        self.animate_gif()

    def animate_gif(self):
        self.gif_label.config(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.after(100, self.animate_gif)

    def wake_up_jarvis(self):
        # Load and display the waking GIF
        self.load_gif(self.waking_gif_path)
        self.wake_button.config(state=tk.DISABLED)  # Disable wake-up button after it's clicked

        # Speak the greeting message
        self.engine.say("Hi, how can I help you?")
        self.engine.runAndWait()

        # Show the talk button
        self.talk_button.pack(pady=10)

    def start_talking(self):
        # Speak a message
        self.engine.say("I am listening...")
        self.engine.runAndWait()

        # Start listening and recognizing speech
        with sr.Microphone() as source:
            print("Microphone activated.")  # Debugging
            self.recognizer.adjust_for_ambient_noise(source, duration=1)  # Increased duration
            print("Listening...")  # Debugging
            try:
                audio_data = self.recognizer.listen(source, timeout=5)  # Added timeout
                print("Processing...")  # Debugging
                text = self.recognizer.recognize_google(audio_data)
                self.display_recognized_text(text)
            except sr.UnknownValueError:
                self.display_recognized_text("Sorry, I did not catch that.")
            except sr.RequestError as e:
                self.display_recognized_text(f"Could not request results; {e}")
            except Exception as e:
                print(f"An error occurred: {e}")  # General error handling

    def display_recognized_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.config(state='disabled')

    def exit_jarvis(self):
        # Load and display the goodbye GIF, then exit
        self.load_gif(self.goodbye_gif_path)
        self.after(len(self.frames) * 100, self.destroy)  # Close after the goodbye GIF plays

if __name__ == "__main__":
    app = JarvisGUI()
    app.mainloop()
