import tkinter as tk
from interface import FenêtreInterface


def main():
    root = tk.Tk()
    app = FenêtreInterface(root)
    root.mainloop()

if __name__=="__main__":
    main()