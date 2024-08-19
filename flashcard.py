import tkinter as tk

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("400x300")
        
        self.flashcards = [
            {"word": "Python", "meaning": "A high-level programming language."},
            {"word": "Variable", "meaning": "A storage location in programming."},
            {"word": "Function", "meaning": "A block of code that performs a specific task."}
        ]
        self.current_index = 0
        
        self.word_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.word_label.pack(pady=50)
        
        self.meaning_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.meaning_label.pack(pady=20)
        
        self.prev_button = tk.Button(root, text="Previous", command=self.prev_card)
        self.prev_button.pack(side="left", padx=20)
        
        self.next_button = tk.Button(root, text="Next", command=self.next_card)
        self.next_button.pack(side="right", padx=20)
        
        self.show_card()

    def show_card(self):
        card = self.flashcards[self.current_index]
        self.word_label.config(text=card["word"])
        self.meaning_label.config(text=card["meaning"])
        
    def prev_card(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_card()

    def next_card(self):
        if self.current_index < len(self.flashcards) - 1:
            self.current_index += 1
            self.show_card()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
