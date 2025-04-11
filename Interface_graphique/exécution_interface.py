import tkinter as tk
from interface import FenêtreInterface


'''
Ceci est le seul et unique fichier que l'utilisateur a besoin d'exécuter pour lancer l'interface graphique de l'application.
'''

'''
Description : Ce fichier exécute l'interface graphique de l'application en important la classe FenêtreInterface du fichier interface.py et crée une instance de cette classe.
Ensuite, on démarre la boucle principale de tkinter pour afficher l'interface en continu.

'''
def main():
    interface = tk.Tk()
    app = FenêtreInterface(interface)       # Création d'une instance de la classe            
    interface.mainloop()                    #Démarre la boucle principale de tk.Tk()

if __name__=="__main__":
    main()