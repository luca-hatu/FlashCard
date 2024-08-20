import pygame
import tkinter as tk
from tkinter import messagebox, Menu, Frame
import json
import random
import time
import os

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("800x600")

        self.flashcards = []
        self.current_index = 0
        self.flipped = False
        self.quiz_mode = False
        self.quiz_score = 0
        self.quiz_question_order = []
        self.quiz_mistakes = []
        self.time_left = 10

        pygame.init()
        self.frame = Frame(root, width=400, height=250)
        self.frame.pack(pady=20)
        self.frame.place(x=200, y=150)
        os.environ['SDL_WINDOWID'] = str(self.frame.winfo_id())
        self.screen = pygame.display.set_mode((400, 250), pygame.NOFRAME)
        pygame.display.init()
        self.font = pygame.font.SysFont('Helvetica', 40)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.card_color = self.white

        self.create_menu()

        self.word_entry = tk.Entry(root, font=("Helvetica", 16))
        self.meaning_entry = tk.Entry(root, font=("Helvetica", 16))

        self.add_button = tk.Button(root, text="Add Flashcard", command=self.show_input_fields)
        self.add_button.pack(pady=5)
        
        self.quiz_button = tk.Button(root, text="Start Quiz", command=self.start_quiz)
        self.quiz_button.pack(pady=5)

        self.submit_button = tk.Button(root, text="Submit Answer", command=self.check_answer)
        self.submit_button.pack(pady=5)
        self.submit_button.pack_forget()

        self.answer_entry = tk.Entry(root, font=("Helvetica", 16))
        self.answer_entry.pack(pady=5)
        self.answer_entry.pack_forget()

        self.timer_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.timer_label.pack(pady=5)
        self.timer_label.pack_forget()

        self.timer_input_label = tk.Label(root, text="Set Timer (seconds):", font=("Helvetica", 14))
        self.timer_input_label.pack(pady=5)

        self.timer_input = tk.Entry(root, font=("Helvetica", 16))
        self.timer_input.pack(pady=5)
        self.timer_input.insert(0, "10")

        self.root.bind("<Button-1>", self.flip_card)

        self.load_flashcards()

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        flashcard_menu = Menu(menubar, tearoff=0)
        flashcard_menu.add_command(label="Add Flashcard", command=self.show_input_fields)
        flashcard_menu.add_command(label="Edit Flashcard", command=self.edit_flashcard)
        flashcard_menu.add_command(label="Delete Flashcard", command=self.delete_flashcard)
        flashcard_menu.add_separator()
        flashcard_menu.add_command(label="Load Flashcards", command=self.load_flashcards)
        flashcard_menu.add_command(label="Save Flashcards", command=self.save_flashcards)
        menubar.add_cascade(label="Flashcards", menu=flashcard_menu)

        nav_menu = Menu(menubar, tearoff=0)
        nav_menu.add_command(label="Next", command=self.next_card)
        nav_menu.add_command(label="Previous", command=self.prev_card)
        menubar.add_cascade(label="Navigate", menu=nav_menu)

        quiz_menu = Menu(menubar, tearoff=0)
        quiz_menu.add_command(label="Start Quiz", command=self.start_quiz)
        menubar.add_cascade(label="Quiz", menu=quiz_menu)

        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Set Timer", command=self.set_timer)
        menubar.add_cascade(label="Settings", menu=settings_menu)

    def flip_card(self, event=None):
        if not self.flashcards or self.quiz_mode:
            return
        
        self.flipped = not self.flipped
        card = self.flashcards[self.current_index]
        new_text = card["meaning"] if self.flipped else card["word"]

        self.animate_flip(new_text)

    def animate_flip(self, text):
        for scale in range(10, -11, -1):
            self.screen.fill(self.black)
            card_rect = pygame.Rect(50, 50, 300 * abs(scale) // 10, 200)
            card_rect.center = (200, 125)
            pygame.draw.rect(self.screen, self.card_color, card_rect)
            if scale <= 0:
                rendered_text = self.font.render(text, True, self.black)
            else:
                rendered_text = self.font.render("", True, self.black)
            text_rect = rendered_text.get_rect(center=card_rect.center)
            self.screen.blit(rendered_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(50)
        
        for scale in range(-10, 11):
            self.screen.fill(self.black)
            card_rect = pygame.Rect(50, 50, 300 * abs(scale) // 10, 200)
            card_rect.center = (200, 125)
            pygame.draw.rect(self.screen, self.card_color, card_rect)
            if scale >= 0:
                rendered_text = self.font.render(text, True, self.black)
            else:
                rendered_text = self.font.render("", True, self.black)
            text_rect = rendered_text.get_rect(center=card_rect.center)
            self.screen.blit(rendered_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(50)

    def show_card(self):
        if not self.flashcards:
            return
        card = self.flashcards[self.current_index]
        text = card["meaning"] if self.flipped else card["word"]

        self.screen.fill(self.black)
        pygame.draw.rect(self.screen, self.card_color, [50, 50, 300, 200])
        rendered_text = self.font.render(text, True, self.black)
        self.screen.blit(rendered_text, (75, 100))
        pygame.display.flip()

    def show_input_fields(self):
        self.word_entry.pack(pady=5)
        self.meaning_entry.pack(pady=5)
        self.add_button.config(text="Save Flashcard", command=self.add_flashcard)

    def add_flashcard(self):
        word = self.word_entry.get()
        meaning = self.meaning_entry.get()
        
        if word and meaning:
            self.flashcards.append({"word": word, "meaning": meaning})
            self.word_entry.delete(0, tk.END)
            self.meaning_entry.delete(0, tk.END)
            self.word_entry.pack_forget()
            self.meaning_entry.pack_forget()
            self.add_button.config(text="Add Flashcard", command=self.show_input_fields)
            messagebox.showinfo("Success", "Flashcard added!")
            if len(self.flashcards) == 1:
                self.show_card()
        else:
            messagebox.showwarning("Input Error", "Please enter both word and meaning.")
        
    def edit_flashcard(self):
        word = self.word_entry.get()
        meaning = self.meaning_entry.get()
        
        if word and meaning and self.flashcards:
            self.flashcards[self.current_index] = {"word": word, "meaning": meaning}
            self.show_card()
            messagebox.showinfo("Success", "Flashcard updated!")
        else:
            messagebox.showwarning("Input Error", "Please enter both word and meaning, or select a flashcard to edit.")
        
    def delete_flashcard(self):
        if self.flashcards:
            del self.flashcards[self.current_index]
            if self.current_index > 0:
                self.current_index -= 1
            self.flipped = False
            self.show_card()
            messagebox.showinfo("Success", "Flashcard deleted!")
        else:
            messagebox.showwarning("Delete Error", "No flashcard to delete.")
        
    def prev_card(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.flipped = False
            self.show_card()

    def next_card(self):
        if self.current_index < len(self.flashcards) - 1:
            self.current_index += 1
            self.flipped = False
            self.show_card()

    def start_quiz(self):
        if not self.flashcards:
            messagebox.showwarning("Quiz Error", "No flashcards available for the quiz.")
            return

        self.quiz_mode = True
        self.quiz_score = 0
        self.quiz_question_order = list(range(len(self.flashcards)))
        random.shuffle(self.quiz_question_order)
        self.quiz_mistakes = []
        self.current_index = 0

        self.add_button.pack_forget()
        self.quiz_button.pack_forget()

        self.answer_entry.pack(pady=5)
        self.submit_button.pack(pady=5)
        self.timer_label.pack(pady=5)

        self.time_left = int(self.timer_input.get().strip() or 10)
        self.update_timer()

        self.show_quiz_question()

    def show_quiz_question(self):
        if self.current_index >= len(self.quiz_question_order):
            return

        card = self.flashcards[self.quiz_question_order[self.current_index]]
        self.screen.fill(self.black)
        pygame.draw.rect(self.screen, self.card_color, [50, 50, 300, 200])
        rendered_text = self.font.render(card["word"], True, self.black)
        self.screen.blit(rendered_text, (75, 100))
        pygame.display.flip()

    def check_answer(self):
        if self.current_index >= len(self.quiz_question_order):
            return

        card = self.flashcards[self.quiz_question_order[self.current_index]]
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = card["meaning"].strip().lower()

        if user_answer == correct_answer:
            self.quiz_score += 1
        else:
            self.quiz_mistakes.append(card)

        self.current_index += 1
        self.time_left = int(self.timer_input.get().strip() or 10)
        self.answer_entry.delete(0, tk.END)

        if self.current_index < len(self.quiz_question_order):
            self.show_quiz_question()
        else:
            self.end_quiz()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.root.after(1000, self.update_timer)
        else:
            self.check_answer()

    def end_quiz(self):
        messagebox.showinfo("Quiz Finished", f"Your score: {self.quiz_score}/{len(self.flashcards)}")
        if self.quiz_mistakes:
            mistakes_summary = "\n".join([f"{card['word']} - {card['meaning']}" for card in self.quiz_mistakes])
            messagebox.showinfo("Mistakes", f"You missed the following flashcards:\n\n{mistakes_summary}")

        self.quiz_mode = False
        self.quiz_button.pack(pady=5)

        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        self.timer_label.pack_forget()

        self.add_button.pack(pady=5)
        self.current_index = 0
        self.flipped = False
        self.show_card()

    def set_timer(self):
        time = self.timer_input.get()
        try:
            self.time_left = int(time)
            messagebox.showinfo("Timer Set", f"Timer set to {time} seconds.")
        except ValueError:
            messagebox.showerror("Timer Error", "Please enter a valid number.")

    def save_flashcards(self):
        try:
            with open("flashcards.json", "w") as file:
                json.dump(self.flashcards, file, indent=4)
            messagebox.showinfo("Success", "Flashcards saved to flashcards.json")
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving flashcards: {e}")

    def load_flashcards(self):
        try:
            with open("flashcards.json", "r") as file:
                self.flashcards = json.load(file)
            self.current_index = 0
            self.flipped = False
            self.show_card()
        except FileNotFoundError:
            self.flashcards = []
            self.current_index = 0
            self.flipped = False
            self.show_card()
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred while loading flashcards: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
