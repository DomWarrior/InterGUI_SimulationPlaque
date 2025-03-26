import tkinter as tk
from interface import SimulationInterface

def main():
    root = tk.Tk()
    app = SimulationInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()