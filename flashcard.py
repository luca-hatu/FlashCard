import tkinter as tk
from tkinter import messagebox
import json
import time
import random

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("500x600")
        
        self.flashcards = []
        self.current_index = 0
        self.flipped = False
        self.quiz_mode = False
        self.quiz_score = 0
        self.quiz_question_order = []

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(root, textvariable=self.search_var, font=("Helvetica", 16))
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.search_flashcards)
        
        self.sort_button = tk.Button(root, text="Sort Flashcards", command=self.sort_flashcards)
        self.sort_button.pack(pady=5)
        
        self.canvas = tk.Canvas(root, width=400, height=250)
        self.canvas.pack(pady=20)

        self.card = self.canvas.create_rectangle(50, 50, 350, 200, fill="white", outline="black", width=2)

        self.card_text = self.canvas.create_text(200, 125, text="", font=("Helvetica", 24))
        
        self.word_entry = tk.Entry(root, font=("Helvetica", 16))
        self.word_entry.pack(pady=5)
        self.word_entry.insert(0, "Enter word")
        self.word_entry.pack_forget()

        self.meaning_entry = tk.Entry(root, font=("Helvetica", 16))
        self.meaning_entry.pack(pady=5)
        self.meaning_entry.insert(0, "Enter meaning")
        self.meaning_entry.pack_forget()

        self.add_button = tk.Button(root, text="Add Flashcard", command=self.show_input_fields)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Edit Flashcard", command=self.edit_flashcard)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Flashcard", command=self.delete_flashcard)
        self.delete_button.pack(pady=5)

        self.prev_button = tk.Button(root, text="Previous", command=self.prev_card)
        self.prev_button.pack(side="left", padx=20)

        self.next_button = tk.Button(root, text="Next", command=self.next_card)
        self.next_button.pack(side="right", padx=20)

        self.quiz_button = tk.Button(root, text="Start Quiz", command=self.start_quiz)
        self.quiz_button.pack(pady=5)

        self.submit_button = tk.Button(root, text="Submit Answer", command=self.check_answer)
        self.submit_button.pack(pady=5)
        self.submit_button.pack_forget()

        self.answer_entry = tk.Entry(root, font=("Helvetica", 16))
        self.answer_entry.pack(pady=5)
        self.answer_entry.pack_forget()

        self.save_button = tk.Button(root, text="Save Flashcards", command=self.save_flashcards)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(root, text="Load Flashcards", command=self.load_flashcards)
        self.load_button.pack(pady=5)

        self.canvas.bind("<Button-1>", self.flip_card)
        
        self.load_flashcards()

        self.apply_hover_effects()

    def apply_hover_effects(self):
        buttons = [self.add_button, self.edit_button, self.delete_button, self.prev_button, self.next_button, self.save_button, self.load_button, self.sort_button, self.quiz_button, self.submit_button]
        for button in buttons:
            button.bind("<Enter>", lambda e, b=button: b.config(bg="#add8e6"))
            button.bind("<Leave>", lambda e, b=button: b.config(bg="SystemButtonFace"))

    def show_card(self):
        if not self.flashcards:
            self.canvas.itemconfig(self.card_text, text="No Flashcards")
            self.word_entry.delete(0, tk.END)
            self.meaning_entry.delete(0, tk.END)
            return
        
        card = self.flashcards[self.current_index]
        self.canvas.itemconfig(self.card_text, text=card["word"] if not self.flipped else card["meaning"])
        self.word_entry.delete(0, tk.END)
        self.meaning_entry.delete(0, tk.END)
        self.word_entry.insert(0, card["word"])
        self.meaning_entry.insert(0, card["meaning"])

    def flip_card(self, event=None):
        if not self.flashcards or self.quiz_mode:
            return
        
        self.animate_flip()

        self.flipped = not self.flipped
        card = self.flashcards[self.current_index]
        new_text = card["meaning"] if self.flipped else card["word"]
        self.canvas.itemconfig(self.card_text, text=new_text)

        self.animate_flip(reverse=True)

    def animate_flip(self, reverse=False):
        scales = range(10, 0, -1) if not reverse else range(1, 11)
        for scale in scales:
            factor = max(scale / 10, 0.1)
            self.canvas.scale(self.card_text, 200, 125, factor, 1)
            self.root.update()
            time.sleep(0.02)

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
        self.quiz_question_order = random.sample(range(len(self.flashcards)), len(self.flashcards))
        self.current_index = 0

        self.answer_entry.pack(pady=5)
        self.submit_button.pack(pady=5)

        self.quiz_button.config(state="disabled")
        self.add_button.pack_forget()
        self.edit_button.pack_forget()
        self.delete_button.pack_forget()
        self.prev_button.pack_forget()
        self.next_button.pack_forget()

        self.show_quiz_question()

    def show_quiz_question(self):
        if self.current_index < len(self.quiz_question_order):
            card = self.flashcards[self.quiz_question_order[self.current_index]]
            self.canvas.itemconfig(self.card_text, text=card["word"])
        else:
            self.end_quiz()

    def check_answer(self):
        if self.current_index >= len(self.quiz_question_order):
            return

        card = self.flashcards[self.quiz_question_order[self.current_index]]
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = card["meaning"].strip().lower()

        if user_answer == correct_answer:
            self.quiz_score += 1

        self.current_index += 1
        self.answer_entry.delete(0, tk.END)

        self.show_quiz_question()

    def end_quiz(self):
        messagebox.showinfo("Quiz Completed", f"Quiz finished! Your score is {self.quiz_score}/{len(self.flashcards)}.")
        self.quiz_mode = False
        self.quiz_button.config(state="normal")

        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        
        self.add_button.pack(pady=5)
        self.edit_button.pack(pady=5)
        self.delete_button.pack(pady=5)
        self.prev_button.pack(side="left", padx=20)
        self.next_button.pack(side="right", padx=20)

        self.current_index = 0
        self.flipped = False
        self.show_card()

    def search_flashcards(self, event=None):
        query = self.search_var.get().strip().lower()
        if query:
            self.flashcards = [card for card in self.flashcards if query in card["word"].lower()]
        else:
            self.load_flashcards()
        self.current_index = 0
        self.flipped = False
        self.show_card()

    def sort_flashcards(self):
        self.flashcards.sort(key=lambda card: card["word"].lower())
        self.current_index = 0
        self.flipped = False
        self.show_card()

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
