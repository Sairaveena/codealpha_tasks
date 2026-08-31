import random
import tkinter as tk
from tkinter import messagebox

# Word list
WORDS = [
    "PYTHON",
    "DEVELOPER",
    "INTERNSHIP",
    "PROGRAMMING",
    "SOFTWARE",
    "COMPUTER",
]

# Visual stages for Hangman
HANGMAN_STAGES = [
    """
   +---+
   |   |
       |
       |
       |
       |
=========
""",
    """
   +---+
   |   |
   O   |
       |
       |
       |
=========
""",
    """
   +---+
   |   |
   O   |
   |   |
       |
       |
=========
""",
    """
   +---+
   |   |
   O   |
  /|   |
       |
       |
=========
""",
    """
   +---+
   |   |
   O   |
  /|\\  |
       |
       |
=========
""",
    """
   +---+
   |   |
   O   |
  /|\\  |
  /    |
       |
=========
""",
    """
   +---+
   |   |
   O   |
  /|\\  |
  / \\  |
       |
=========
""",
]


class HangmanGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Hangman Game")
        self.root.geometry("450x550")
        self.root.config(bg="#f0f4f8")

        self.reset_game()

        # Title
        tk.Label(
            root,
            text="🎮 Advanced Hangman Game",
            font=("Helvetica", 16, "bold"),
            bg="#f0f4f8",
            fg="#1e293b",
        ).pack(pady=10)

        # Hangman Art Display
        self.stage_label = tk.Label(
            root,
            text=HANGMAN_STAGES[0],
            font=("Courier", 10),
            justify="left",
            bg="#ffffff",
            relief="solid",
            bd=1,
            padx=10,
            pady=10,
        )
        self.stage_label.pack(pady=10)

        # Hidden Word Display
        self.word_label = tk.Label(
            root,
            text=self.get_display_word(),
            font=("Consolas", 20, "bold"),
            bg="#f0f4f8",
            fg="#2563eb",
        )
        self.word_label.pack(pady=10)

        # Guessed Letters Display
        self.guessed_label = tk.Label(
            root,
            text="Guessed: None",
            font=("Helvetica", 10),
            bg="#f0f4f8",
            fg="#64748b",
        )
        self.guessed_label.pack(pady=5)

        # Lives Display
        self.lives_label = tk.Label(
            root,
            text=f"Lives Remaining: {self.max_attempts - self.attempts}",
            font=("Helvetica", 11, "bold"),
            bg="#f0f4f8",
            fg="#dc2626",
        )
        self.lives_label.pack(pady=5)

        # Input Frame
        input_frame = tk.Frame(root, bg="#f0f4f8")
        input_frame.pack(pady=15)

        self.entry = tk.Entry(
            input_frame, font=("Helvetica", 14), width=5, justify="center"
        )
        self.entry.pack(side="left", padx=5)
        self.entry.bind("<Return>", lambda event: self.make_guess())

        self.guess_btn = tk.Button(
            input_frame,
            text="Guess",
            font=("Helvetica", 11, "bold"),
            bg="#2563eb",
            fg="white",
            command=self.make_guess,
            padx=10,
        )
        self.guess_btn.pack(side="left", padx=5)

    def reset_game(self):
        self.secret_word = random.choice(WORDS)
        self.guessed_letters = set()
        self.attempts = 0
        self.max_attempts = len(HANGMAN_STAGES) - 1

    def get_display_word(self):
        return " ".join(
            [
                letter if letter in self.guessed_letters else "_"
                for letter in self.secret_word
            ]
        )

    def make_guess(self):
        guess = self.entry.get().strip().upper()
        self.entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning(
                "Warning", "Please enter a single valid letter!"
            )
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Info", "You already guessed that letter!")
            return

        self.guessed_letters.add(guess)

        if guess not in self.secret_word:
            self.attempts += 1

        self.update_ui()

    def update_ui(self):
        self.stage_label.config(text=HANGMAN_STAGES[self.attempts])
        self.word_label.config(text=self.get_display_word())
        self.guessed_label.config(
            text=f"Guessed: {', '.join(sorted(self.guessed_letters)) if self.guessed_letters else 'None'}"
        )
        self.lives_label.config(
            text=f"Lives Remaining: {self.max_attempts - self.attempts}"
        )

        # Win condition
        if all(
            letter in self.guessed_letters for letter in self.secret_word
        ):
            messagebox.showinfo(
                "🎉 You Won!",
                f"Congratulations! You guessed '{self.secret_word}'!",
            )
            self.restart_game()

        # Lose condition
        elif self.attempts >= self.max_attempts:
            messagebox.showerror(
                "💥 Game Over",
                f"You ran out of lives! The word was '{self.secret_word}'.",
            )
            self.restart_game()

    def restart_game(self):
        self.reset_game()
        self.update_ui()


if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
