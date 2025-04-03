import tkinter as tk
from interface import FenêtreInterface

'''
Ce fichier exécute l'interface graphique de l'application.
Il importe la classe FenêtreInterface du fichier interface.py et crée une instance de cette classe.
Il démarre ensuite la boucle principale de tkinter pour afficher l'interface en continu.

'''
def main():
    interface = tk.Tk()
    app = FenêtreInterface(interface)       # Création d'une instance de la classe            
    interface.mainloop()                    #Démarre la boucle principale de tk.Tk()

if __name__=="__main__":
    main()