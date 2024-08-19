import tkinter as tk
from tkinter import messagebox
import time

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("500x400")
        
        self.flashcards = []
        self.current_index = 0
        self.flipped = False 
        self.canvas = tk.Canvas(root, width=400, height=250)
        self.canvas.pack(pady=20)
        self.card = self.canvas.create_rectangle(50, 50, 350, 200, fill="white", outline="black", width=2)
        self.card_text = self.canvas.create_text(200, 125, text="", font=("Helvetica", 24))
        
        self.word_entry = tk.Entry(root, font=("Helvetica", 16))
        self.word_entry.pack(pady=5)
        
        self.meaning_entry = tk.Entry(root, font=("Helvetica", 16))
        self.meaning_entry.pack(pady=5)
        
        self.add_button = tk.Button(root, text="Add Flashcard", command=self.add_flashcard)
        self.add_button.pack(pady=5)
        
        self.edit_button = tk.Button(root, text="Edit Flashcard", command=self.edit_flashcard)
        self.edit_button.pack(pady=5)
        
        self.delete_button = tk.Button(root, text="Delete Flashcard", command=self.delete_flashcard)
        self.delete_button.pack(pady=5)
        
        self.canvas.bind("<Button-1>", self.flip_card)

        self.show_card()

    def show_card(self):
        if not self.flashcards:
            self.canvas.itemconfig(self.card_text, text="No Flashcards")
            return
        
        card = self.flashcards[self.current_index]
        self.canvas.itemconfig(self.card_text, text=card["word"] if not self.flipped else card["meaning"])
        
    def flip_card(self, event=None):
        if not self.flashcards:
            return
        
        for scale in range(10, 0, -1):
            factor = max(scale / 10, 0.1) 
            self.canvas.scale(self.card_text, 200, 125, factor, 1)
            self.root.update()
            time.sleep(0.02)

        self.flipped = not self.flipped
        card = self.flashcards[self.current_index]
        new_text = card["meaning"] if self.flipped else card["word"]
        self.canvas.itemconfig(self.card_text, text=new_text)
        
        for scale in range(1, 11):
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
        
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
