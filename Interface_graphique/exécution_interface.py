import tkinter as tk
from interface import FenêtreInterface


def main():
    interface = tk.Tk()
    app = FenêtreInterface(interface)       # Création d'une instance de la classe            
    interface.mainloop()                    #Démarre la boucle principale de tk.Tk()

if __name__=="__main__":
    main()