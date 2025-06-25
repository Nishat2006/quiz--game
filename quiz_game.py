import tkinter as tk
from tkinter import messagebox
import json
import random

# Animation helper
import threading
import time

class QuizGame:
    def __init__(self, master):
        self.master = master
        self.master.title('Quiz Game with Leaderboard')
        self.master.geometry('500x400')
        self.master.configure(bg='#22223b')
        self.score = 0
        self.current_q = 0
        self.questions = self.load_questions()
        random.shuffle(self.questions)
        self.selected = tk.StringVar()
        self.create_widgets()
        self.show_question(animated=False)

    def load_questions(self):
        with open('questions.json', 'r') as f:
            return json.load(f)

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text='Quiz Game', font=('Arial', 24, 'bold'), fg='#f2e9e4', bg='#22223b')
        self.title_label.pack(pady=20)
        self.question_label = tk.Label(self.master, text='', font=('Arial', 16), fg='#c9ada7', bg='#22223b', wraplength=400, justify='center')
        self.question_label.pack(pady=10)
        self.option_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(self.master, text='', variable=self.selected, value='', font=('Arial', 14), fg='#4a4e69', bg='#f2e9e4', indicatoron=0, width=30, pady=8, bd=0, relief='ridge', selectcolor='#9a8c98', activebackground='#c9ada7')
            btn.pack(pady=5)
            self.option_buttons.append(btn)
        self.next_btn = tk.Button(self.master, text='Next', command=self.next_question, font=('Arial', 14, 'bold'), bg='#4a4e69', fg='#f2e9e4', activebackground='#9a8c98', activeforeground='#22223b')
        self.next_btn.pack(pady=20)
        self.score_label = tk.Label(self.master, text='Score: 0', font=('Arial', 12), fg='#f2e9e4', bg='#22223b')
        self.score_label.pack()
        # Placeholder for leaderboard button
        self.leaderboard_btn = tk.Button(self.master, text='View Leaderboard', font=('Arial', 12), bg='#c9ada7', fg='#22223b', command=self.show_leaderboard)
        self.leaderboard_btn.pack(pady=5)

    def animate_question(self, new_text, options):
        # Fade out
        for alpha in range(100, -1, -10):
            self.question_label.configure(fg=f'#c9ada7{alpha:02x}')
            self.master.update()
            time.sleep(0.01)
        self.question_label.config(text=new_text)
        for i, btn in enumerate(self.option_buttons):
            btn.config(text=options[i], value=options[i])
            self.selected.set('')
        # Fade in
        for alpha in range(0, 101, 10):
            self.question_label.configure(fg=f'#c9ada7{alpha:02x}')
            self.master.update()
            time.sleep(0.01)

    def show_question(self, animated=True):
        q = self.questions[self.current_q]
        if animated:
            threading.Thread(target=self.animate_question, args=(q['question'], q['options'])).start()
        else:
            self.question_label.config(text=q['question'], fg='#c9ada7')
            for i, btn in enumerate(self.option_buttons):
                btn.config(text=q['options'][i], value=q['options'][i])
            self.selected.set('')

    def next_question(self):
        q = self.questions[self.current_q]
        if self.selected.get() == '':
            messagebox.showwarning('No selection', 'Please select an answer!')
            return
        if self.selected.get() == q['answer']:
            self.score += 1
            self.score_label.config(text=f'Score: {self.score}')
        self.current_q += 1
        if self.current_q < len(self.questions):
            self.show_question(animated=True)
        else:
            self.end_quiz()

    def end_quiz(self):
        messagebox.showinfo('Quiz Finished', f'Your score: {self.score}')
        # TODO: Save score to leaderboard
        # Placeholder for leaderboard logic
        self.master.destroy()

    def show_leaderboard(self):
        # TODO: Implement leaderboard window
        messagebox.showinfo('Leaderboard', 'Leaderboard feature coming soon!')

if __name__ == '__main__':
    root = tk.Tk()
    app = QuizGame(root)
    root.mainloop() 