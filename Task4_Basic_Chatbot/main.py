import datetime
import random
import re
import tkinter as tk
from tkinter import ttk


class AdvancedChatbot:

    def __init__(self):
        # Predefined responses based on pattern matching (Intents)
        self.rules = {
            r"\b(hi|hello|hey|greetings|good morning|good evening)\b": [
                "Hello there! How can I assist you today?",
                "Hi! Nice to meet you. What's on your mind?",
                "Hey! How can I help you today?",
            ],
            r"\b(how are you|how's it going|how do you do)\b": [
                "I'm doing great, thank you for asking! How are you?",
                "I'm just a bundle of code, but I'm feeling optimal! How about you?",
            ],
            r"\b(your name|who are you|what are you)\b": [
                "I am AlphaBot, your intelligent virtual assistant!",
                "You can call me AlphaBot. I'm a rule-based AI assistant.",
            ],
            r"\b(time|date|clock|day)\b": [
                self.get_time_date,
            ],
            r"\b(joke|funny|laugh)\b": [
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "There are 10 types of people in the world: those who understand binary, and those who don't. 😄",
                "Why was the computer cold? It left its Windows open! ❄️",
            ],
            r"\b(help|support|what can you do)\b": [
                "I can answer basic questions, tell jokes, give you the current time/date, or just chat with you!",
            ],
            r"\b(bye|goodbye|see you|exit|quit)\b": [
                "Goodbye! Have a wonderful day ahead! 👋",
                "Farewell! Feel free to chat with me anytime. 😊",
            ],
        }

        self.default_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "That's interesting! Tell me more.",
            "I'm still learning! Try asking me about the time, a joke, or just say hello.",
        ]

    def get_time_date(self):
        now = datetime.datetime.now()
        return f"Current date and time is: {now.strftime('%A, %B %d, %Y at %I:%M %p')}"

    def get_response(self, user_input):
        user_input_clean = user_input.lower().strip()

        for pattern, responses in self.rules.items():
            if re.search(pattern, user_input_clean):
                response = random.choice(responses)
                if callable(response):
                    return response()
                return response

        return random.choice(self.default_responses)


class ChatbotGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("AlphaBot - Advanced AI Assistant")
        self.root.geometry("450x550")
        self.root.minsize(400, 450)  # Ensures window can't get too small
        self.root.configure(bg="#0f172a")

        self.bot = AdvancedChatbot()

        self.create_widgets()

    def create_widgets(self):
        # 1. Header (Top)
        header = tk.Label(
            self.root,
            text="🤖 AlphaBot Virtual Assistant",
            font=("Arial", 14, "bold"),
            bg="#1e293b",
            fg="#f8fafc",
            pady=10,
        )
        header.pack(side="top", fill="x")

        # 2. Input Frame (Bottom) - Packed BEFORE text area to guarantee visibility!
        input_frame = tk.Frame(self.root, bg="#1e293b", pady=10, padx=10)
        input_frame.pack(side="bottom", fill="x")

        self.entry_box = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="solid",
            bd=1,
        )
        self.entry_box.pack(
            side="left", fill="x", expand=True, padx=(0, 10), ipady=5
        )
        self.entry_box.bind("<Return>", lambda event: self.send_message())
        self.entry_box.focus()

        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=("Arial", 10, "bold"),
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            activeforeground="white",
            relief="flat",
            command=self.send_message,
            padx=15,
            pady=3,
            cursor="hand2",
        )
        send_btn.pack(side="right")

        # 3. Chat display area (Middle) - Fills remaining space
        self.chat_display = tk.Text(
            self.root,
            bg="#0f172a",
            fg="#f8fafc",
            font=("Arial", 10),
            wrap="word",
            state="disabled",
            padx=10,
            pady=10,
        )
        self.chat_display.pack(
            side="top", fill="both", expand=True, padx=10, pady=10
        )

        # Configure message tag colors
        self.chat_display.tag_config(
            "user", foreground="#38bdf8", font=("Arial", 10, "bold")
        )
        self.chat_display.tag_config(
            "bot", foreground="#4ade80", font=("Arial", 10, "bold")
        )

        # Initial Welcome Message
        self.append_message(
            "AlphaBot",
            "Hello! I am AlphaBot. How can I assist you today?",
            "bot",
        )

    def append_message(self, sender, message, tag):
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"{sender}: ", tag)
        self.chat_display.insert("end", f"{message}\n\n")
        self.chat_display.config(state="disabled")
        self.chat_display.yview("end")

    def send_message(self):
        user_text = self.entry_box.get().strip()
        if not user_text:
            return

        self.entry_box.delete(0, tk.END)
        self.append_message("You", user_text, "user")

        bot_response = self.bot.get_response(user_text)
        self.root.after(
            300,
            lambda: self.append_message("AlphaBot", bot_response, "bot"),
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
