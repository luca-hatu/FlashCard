import tkinter as tk
from tkinter import messagebox
import json
import time

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("500x600")
        
        self.flashcards = []
        self.current_index = 0
        self.flipped = False
        
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

        self.meaning_entry = tk.Entry(root, font=("Helvetica", 16))
        self.meaning_entry.pack(pady=5)
        self.meaning_entry.insert(0, "Enter meaning")

        self.add_button = tk.Button(root, text="Add Flashcard", command=self.add_flashcard)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Edit Flashcard", command=self.edit_flashcard)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Flashcard", command=self.delete_flashcard)
        self.delete_button.pack(pady=5)

        self.prev_button = tk.Button(root, text="Previous", command=self.prev_card)
        self.prev_button.pack(side="left", padx=20)

        self.next_button = tk.Button(root, text="Next", command=self.next_card)
        self.next_button.pack(side="right", padx=20)

        self.save_button = tk.Button(root, text="Save Flashcards", command=self.save_flashcards)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(root, text="Load Flashcards", command=self.load_flashcards)
        self.load_button.pack(pady=5)

        self.canvas.bind("<Button-1>", self.flip_card)
        
        self.load_flashcards()

        self.apply_hover_effects()

    def apply_hover_effects(self):
        buttons = [self.add_button, self.edit_button, self.delete_button, self.prev_button, self.next_button, self.save_button, self.load_button, self.sort_button]
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
        if not self.flashcards:
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

    def add_flashcard(self):
        word = self.word_entry.get()
        meaning = self.meaning_entry.get()
        
        if word and meaning:
            self.flashcards.append({"word": word, "meaning": meaning})
            self.word_entry.delete(0, tk.END)
            self.meaning_entry.delete(0, tk.END)
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
