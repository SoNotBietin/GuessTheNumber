import tkinter as tk
import random
import pickle
from tkinter import messagebox

class GuessTheNumberGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guess the Number")
        self.geometry("400x600")
        self.random_number = None
        self.attempts = 0
        self.max_attempts = 10
        self.difficulty_level = "Medium"
        self.best_scores = {"Easy": float('inf'), "Medium": float('inf'), "Hard": float('inf')}
        self.little_more_threshold = 5
        self.win_streak = 0
        self.lose_streak = 0
        self.countdown_seconds = 20
        self.time_limit_mode = False
        self.previous_guesses = []
        self.custom_max_attempts = 10  # For Free Play mode
        self.load_data()  # Load saved game data
        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        self.label = tk.Label(self, text=f"Guess the number (between 1 and 1000):")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.difficulty_frame = tk.Frame(self)
        self.difficulty_frame.pack(pady=5)

        self.difficulty_label = tk.Label(self.difficulty_frame, text="Difficulty Level:")
        self.difficulty_label.pack(side=tk.LEFT)

        self.easy_button = tk.Button(self.difficulty_frame, text="Easy", command=lambda: self.set_difficulty("Easy"))
        self.easy_button.pack(side=tk.LEFT, padx=5)

        self.medium_button = tk.Button(self.difficulty_frame, text="Medium", command=lambda: self.set_difficulty("Medium"))
        self.medium_button.pack(side=tk.LEFT, padx=5)

        self.hard_button = tk.Button(self.difficulty_frame, text="Hard", command=lambda: self.set_difficulty("Hard"))
        self.hard_button.pack(side=tk.LEFT, padx=5)

        self.free_play_button = tk.Button(self.difficulty_frame, text="Free Play", command=self.set_free_play_mode)
        self.free_play_button.pack(side=tk.LEFT, padx=5)

        self.check_button = tk.Button(self, text="Check", command=self.check_guess)
        self.check_button.pack(pady=10)
        self.check_button.config(state=tk.DISABLED)

        self.hint_button = tk.Button(self, text="Hint", command=self.give_hint)
        self.hint_button.pack(pady=5)
        self.hint_button.config(state=tk.DISABLED)

        self.expose_answer_button = tk.Button(self, text="Expose Answer", command=self.expose_answer)
        self.expose_answer_button.pack(pady=5)
        self.expose_answer_button.config(state=tk.DISABLED)

        self.result_label = tk.Label(self, text="", fg="green", font=("Helvetica", 12, "bold"))
        self.result_label.pack(pady=5)

        self.play_again_button = tk.Button(self, text="Play Again", command=self.confirm_new_game)
        self.play_again_button.pack(pady=10)
        self.play_again_button.pack_forget()

        self.new_game_button = tk.Button(self, text="New Game", command=self.confirm_new_game)
        self.new_game_button.pack(pady=10)

        self.quit_button = tk.Button(self, text="Quit", command=self.confirm_quit_game)
        self.quit_button.pack(pady=5)

        self.attempts_label = tk.Label(self, text="", font=("Helvetica", 10))
        self.attempts_label.pack()

        self.best_scores_label = tk.Label(self, text="")
        self.best_scores_label.pack()

        self.win_streak_label = tk.Label(self, text="")
        self.win_streak_label.pack()

        self.lose_streak_label = tk.Label(self, text="")
        self.lose_streak_label.pack()

        self.range_label = tk.Label(self, text="")
        self.range_label.pack()

        self.timer_label = tk.Label(self, text="", font=("Helvetica", 12, "bold"))
        self.timer_label.pack()

        self.previous_guesses_label = tk.Label(self, text="Previous Guesses:")
        self.previous_guesses_label.pack(pady=5)
        self.previous_guesses_text = tk.Text(self, height=5, wrap=tk.WORD)
        self.previous_guesses_text.pack()

        self.achievements_label = tk.Label(self, text="Achievements:", font=("Helvetica", 12, "bold"))
        self.achievements_label.pack(pady=10)

        self.achievement_1 = tk.Label(self, text="", fg="blue")
        self.achievement_1.pack()
        self.achievement_2 = tk.Label(self, text="", fg="green")
        self.achievement_2.pack()
        self.achievement_3 = tk.Label(self, text="", fg="purple")
        self.achievement_3.pack()

    def load_data(self):
        try:
            with open("game_data.pkl", "rb") as file:
                data = pickle.load(file)
                self.best_scores = data.get("best_scores", self.best_scores)
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {"best_scores": self.best_scores}
        with open("game_data.pkl", "wb") as file:
            pickle.dump(data, file)

    def generate_random_number(self):
        if self.difficulty_level == "Easy":
            return random.randint(1, 50)
        elif self.difficulty_level == "Hard":
            return random.randint(1, 1000)
        else:
            return random.randint(51, 500)

    def set_difficulty(self, difficulty):
        self.difficulty_level = difficulty
        self.time_limit_mode = False
        self.start_new_game()

    def set_free_play_mode(self):
        self.difficulty_level = "Free Play"
        self.max_attempts = self.custom_max_attempts
        self.time_limit_mode = False
        self.start_new_game()

    def start_new_game(self):
        self.random_number = self.generate_random_number()
        self.attempts = 0
        self.result_label.config(text="")
        self.check_button.config(state=tk.NORMAL)
        self.hint_button.config(state=tk.NORMAL)
        self.expose_answer_button.config(state=tk.NORMAL)
        self.play_again_button.pack_forget()
        self.new_game_button.pack_forget()
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.update_attempts_label()
        self.win_streak = 0
        self.lose_streak = 0
        self.update_win_streak_label()
        self.update_lose_streak_label()

        self.previous_guesses.clear()
        self.previous_guesses_text.delete(1.0, tk.END)

        self.timer_label.config(text="")
        self.countdown_seconds = 20

        self.set_number_range_label()

        if self.difficulty_level != "Free Play":
            self.set_time_limit_mode()

        self.achievement_1.config(text="")
        self.achievement_2.config(text="")
        self.achievement_3.config(text="")

    def set_time_limit_mode(self):
        self.time_limit_mode = True
        self.start_timer()

    def update_attempts_label(self):
        attempts_left = self.max_attempts - self.attempts
        self.attempts_label.config(text=f"Attempts left: {attempts_left}")

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1

            if 1 <= guess <= 1000:
                self.previous_guesses.append(guess)
                self.previous_guesses_text.insert(tk.END, f"{guess}\n")

                if guess < self.random_number:
                    self.result_label.config(text="Too low! Try again.", fg="red")
                elif guess > self.random_number:
                    self.result_label.config(text="Too high! Try again.", fg="red")
                else:
                    self.result_label.config(text=f"Congratulations! You guessed the number {self.random_number} "
                                                  f"correctly in {self.attempts} attempts!", fg="green")
                    self.check_button.config(state=tk.DISABLED)
                    self.hint_button.config(state=tk.DISABLED)
                    self.expose_answer_button.config(state=tk.DISABLED)
                    self.play_again_button.pack(pady=10)
                    self.new_game_button.pack(pady=10)

                    self.update_best_scores()
                    self.update_win_streak()
                    self.time_limit_mode = False

                if self.attempts >= self.max_attempts:
                    self.result_label.config(text=f"Game Over! The number was {self.random_number}.", fg="red")
                    self.check_button.config(state=tk.DISABLED)
                    self.hint_button.config(state=tk.DISABLED)
                    self.expose_answer_button.config(state=tk.DISABLED)
                    self.play_again_button.pack(pady=10)
                    self.new_game_button.pack(pady=10)
                    self.time_limit_mode = False

                self.update_attempts_label()
                self.little_more_feedback()
                self.check_speed_achievement()
            else:
                self.result_label.config(fg="red", text=f"Please enter a number between 1 and 1000 for {self.difficulty_level} level.")
        except ValueError:
            self.result_label.config(fg="red", text="Invalid input. Please enter a valid number.")

    def give_hint(self):
        if self.random_number % 2 == 0:
            hint = "The number is even."
        else:
            hint = "The number is odd."
        self.result_label.config(fg="blue", text=hint)

    def expose_answer(self):
        self.result_label.config(fg="purple", text=f"The answer is {self.random_number}. You're a CHICKEN BRO!")
        self.expose_answer_button.config(state=tk.DISABLED)

    def update_best_scores(self):
        if self.difficulty_level != "Free Play" and self.attempts < self.best_scores[self.difficulty_level]:
            self.best_scores[self.difficulty_level] = self.attempts
            self.best_scores_label.config(text=f"Best Scores:\n"
                                               f"Easy: {self.best_scores['Easy']} attempts\n"
                                               f"Medium: {self.best_scores['Medium']} attempts\n"
                                               f"Hard: {self.best_scores['Hard']} attempts")

        self.save_data()  # Save game data after updating best scores

    def little_more_feedback(self):
        if abs(self.random_number - int(self.entry.get())) <= self.little_more_threshold:
            self.result_label.config(fg="orange", text="A little more...")

    def check_speed_achievement(self):
        if self.attempts == 1:
            self.result_label.config(fg="gold", text="Yes, FIRST ANSWER!")

    def update_win_streak(self):
        self.win_streak += 1
        self.update_win_streak_label()
        if self.win_streak >= 3:
            self.result_label.config(fg="green", text="Nice! You've got a win streak of 3!")

    def update_win_streak_label(self):
        self.win_streak_label.config(text=f"Win Streak: {self.win_streak}")

    def update_lose_streak(self):
        self.lose_streak += 1
        self.update_lose_streak_label()

    def update_lose_streak_label(self):
        self.lose_streak_label.config(text=f"Lose Streak: {self.lose_streak}")

    def set_number_range_label(self):
        if self.difficulty_level == "Easy":
            self.range_label.config(text="The number is between 1 and 50.")
        elif self.difficulty_level == "Hard":
            self.range_label.config(text="The number is between 1 and 1000.")
        else:
            self.range_label.config(text="The number is between 51 and 500.")

        if self.time_limit_mode:
            self.start_timer()

    def start_timer(self):
        self.countdown_seconds = 20
        self.update_timer_label()

    def update_timer_label(self):
        if self.time_limit_mode:
            self.timer_label.config(text=f"Time left: {self.countdown_seconds} seconds")

            if self.countdown_seconds > 0:
                self.countdown_seconds -= 1
                self.after(1000, self.update_timer_label)
            else:
                self.result_label.config(text="Time's up! Try again.", fg="red")
                self.check_button.config(state=tk.DISABLED)
                self.hint_button.config(state=tk.DISABLED)
                self.expose_answer_button.config(state=tk.DISABLED)
                self.play_again_button.pack(pady=10)
                self.new_game_button.pack(pady=10)
                self.time_limit_mode = False

    def quit_game(self):
        self.destroy()

    def confirm_new_game(self):
        confirm = messagebox.askyesno("New Game", "Are you sure you want to start a new game?")
        if confirm:
            self.start_new_game()

    def confirm_quit_game(self):
        confirm = messagebox.askyesno("Quit", "Are you sure you want to quit the game?")
        if confirm:
            self.quit_game()

if __name__ == "__main__":
    messagebox.showinfo("Thanks!","Enjoy playing this buggy game.")
    app = GuessTheNumberGame()
    app.mainloop()
