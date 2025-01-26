import tkinter as tk
import BouletDeCanon as BC


root = tk.Tk()
root.title("Capitaine Morgan")

def on_click():
    BC.equProjectile(45,9.81,15,3)

lbl= tk.Label(root, text='Test1')
lbl.grid(row=0,column=0)

bouton=tk.Button(root, text='FEU!', command=on_click)
bouton.grid()

root.mainloop()