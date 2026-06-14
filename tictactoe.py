import tkinter as tk
from tkinter import ttk
import random

class Morpion:
    def __init__(self, root):
        self.root = root
        self.root.title("Morpion vs Ordinateur")
        self.root.geometry("380x520")
        self.root.resizable(False, False)
        
        # Force un fond de fenêtre clair
        self.root.configure(bg="#f0f0f0")
        
        # Variables du jeu
        self.joueur = "X"
        self.ia = "O"
        self.plateau = [""] * 9
        self.partie_active = True
        self.attente_ia = False
        
        self.difficulte_var = tk.StringVar(value="Moyen")
        
        # Configuration du style ttk
        self.style = ttk.Style()
        # Le thème 'alt' ou 'classic' respecte beaucoup mieux les couleurs sous Linux 
        # que le thème par défaut du système
        try:
            self.style.theme_use('alt')
        except tk.TclError:
            pass
            
        self.style.configure("Status.TLabel", font=("Helvetica", 14, "bold"), background="#f0f0f0")
        self.style.configure("Title.TLabel", font=("Helvetica", 18, "bold"), background="#f0f0f0")
        self.style.configure("Control.TButton", font=("Helvetica", 12))
        
        # Couleurs garanties (fonctionnent avec les Labels)
        self.couleur_x = "#1976D2"       # Bleu
        self.couleur_o = "#D32F2F"       # Rouge
        self.couleur_win_bg = "#FF9800"  # Orange vif pour la victoire
        self.couleur_win_fg = "#FFFFFF"  # Texte blanc pour la victoire
        self.couleur_bg_normal = "#FFFFFF"
        self.couleur_text_normal = "#333333"
        
        self.construire_interface()
        
    def construire_interface(self):
        # Titre
        titre = ttk.Label(self.root, text="Morpion", style="Title.TLabel")
        titre.pack(pady=(15, 5))
        
        # Sélecteur de difficulté
        cadre_diff = ttk.Frame(self.root)
        cadre_diff.pack(pady=5)
        ttk.Label(cadre_diff, text="Difficulté :").pack(side=tk.LEFT, padx=(0, 10))
        self.combo_difficulte = ttk.Combobox(
            cadre_diff, textvariable=self.difficulte_var, 
            values=["Facile", "Moyen", "Difficile"], state="readonly", width=10
        )
        self.combo_difficulte.pack(side=tk.LEFT)
        self.combo_difficulte.bind("<<ComboboxSelected>>", lambda e: self.reinitialiser_jeu())
        
        # Label de statut
        self.statut_var = tk.StringVar(value="C'est à votre tour (X)")
        self.label_statut = ttk.Label(self.root, textvariable=self.statut_var, style="Status.TLabel")
        self.label_statut.pack(pady=5)
        
        # Cadre pour la grille de jeu
        self.cadre_grille = tk.Frame(self.root, bg="#f0f0f0")
        self.cadre_grille.pack(pady=10)
        
        # ASTUCE LINUX : Utilisation de tk.Label au lieu de tk.Button.
        # Les Labels ne sont pas affectés par les thèmes GTK qui forcent le gris.
        self.boutons = []
        for i in range(9):
            ligne = i // 3
            colonne = i % 3
            lbl = tk.Label(
                self.cadre_grille, 
                text="", 
                font=("Helvetica", 32, "bold"),
                width=3,
                height=2,
                relief="groove",      # Donne un aspect de case en creux
                bd=3,                 # Épaisseur de la bordure
                bg=self.couleur_bg_normal,
                fg=self.couleur_text_normal,
                cursor="hand2"        # Curseur en forme de main au survol
            )
            lbl.grid(row=ligne, column=colonne, padx=5, pady=5)
            # On simule le clic d'un bouton en liant le clic gauche de la souris (<Button-1>)
            lbl.bind("<Button-1>", lambda event, idx=i: self.clic_bouton(idx))
            self.boutons.append(lbl)
            
        # Bouton pour recommencer
        self.bouton_rejouer = ttk.Button(self.root, text="Nouvelle Partie", style="Control.TButton", command=self.reinitialiser_jeu)
        self.bouton_rejouer.pack(pady=15)

    def clic_bouton(self, index):
        if self.plateau[index] == "" and self.partie_active and not self.attente_ia:
            self.plateau[index] = self.joueur
            self.boutons[index].config(text=self.joueur, fg=self.couleur_x)
            
            combinaison_gagnante = self.verifier_victoire(self.plateau, self.joueur)
            if combinaison_gagnante:
                self.surligner_victoire(combinaison_gagnante)
                self.statut_var.set("🎉 Vous avez gagné !")
                self.partie_active = False
                self.desactiver_grille()
            elif "" not in self.plateau:
                self.statut_var.set("🤝 Match nul !")
                self.partie_active = False
            else:
                self.attente_ia = True
                self.statut_var.set("L'ordinateur réfléchit...")
                self.desactiver_grille()
                self.root.after(400, self.tour_ia)

    def tour_ia(self):
        if not self.partie_active:
            return
            
        difficulte = self.difficulte_var.get()
        coup = -1
        
        if difficulte == "Facile":
            coup = self.get_coup_aleatoire()
        elif difficulte == "Moyen":
            coup = self.get_coup_moyen()
        else: # Difficile (Minimax)
            coup = self.get_coup_minimax()
            
        if coup != -1:
            self.plateau[coup] = self.ia
            self.boutons[coup].config(text=self.ia, fg=self.couleur_o)
            
            combinaison_gagnante = self.verifier_victoire(self.plateau, self.ia)
            if combinaison_gagnante:
                self.surligner_victoire(combinaison_gagnante)
                self.statut_var.set("💻 L'ordinateur a gagné !")
                self.partie_active = False
            elif "" not in self.plateau:
                self.statut_var.set("🤝 Match nul !")
                self.partie_active = False
            else:
                self.statut_var.set("C'est à votre tour (X)")
                
        self.attente_ia = False
        if self.partie_active:
            self.activer_grille()

    def surligner_victoire(self, combinaison):
        for index in combinaison:
            self.boutons[index].config(
                bg=self.couleur_win_bg, 
                fg=self.couleur_win_fg, 
                relief="flat" # Change le relief pour bien montrer que c'est sélectionné
            )

    def get_coup_aleatoire(self):
        cases_vides = [i for i, val in enumerate(self.plateau) if val == ""]
        return random.choice(cases_vides)

    def get_coup_moyen(self):
        # 1. Gagner si possible
        for i in range(9):
            if self.plateau[i] == "":
                self.plateau[i] = self.ia
                if self.verifier_victoire(self.plateau, self.ia):
                    self.plateau[i] = ""
                    return i
                self.plateau[i] = ""
                
        # 2. Bloquer le joueur
        for i in range(9):
            if self.plateau[i] == "":
                self.plateau[i] = self.joueur
                if self.verifier_victoire(self.plateau, self.joueur):
                    self.plateau[i] = ""
                    return i
                self.plateau[i] = ""
                
        # 3. Prendre le centre
        if self.plateau[4] == "":
            return 4
            
        # 4. Aléatoire
        return self.get_coup_aleatoire()

    def get_coup_minimax(self):
        meilleur_score = -float('inf')
        meilleur_coup = -1
        
        for i in range(9):
            if self.plateau[i] == "":
                self.plateau[i] = self.ia
                score = self.minimax(self.plateau, 0, False)
                self.plateau[i] = "" 
                
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coup = i
        return meilleur_coup

    def minimax(self, board, profondeur, est_maximisant):
        if self.verifier_victoire(board, self.ia):
            return 10 - profondeur
        if self.verifier_victoire(board, self.joueur):
            return profondeur - 10
        if "" not in board:
            return 0
            
        if est_maximisant:
            meilleur_score = -float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = self.ia
                    score = self.minimax(board, profondeur + 1, False)
                    board[i] = ""
                    meilleur_score = max(score, meilleur_score)
            return meilleur_score
        else:
            meilleur_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = self.joueur
                    score = self.minimax(board, profondeur + 1, True)
                    board[i] = ""
                    meilleur_score = min(score, meilleur_score)
            return meilleur_score

    def verifier_victoire(self, board, joueur):
        combinaisons = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in combinaisons:
            if board[a] == board[b] == board[c] == joueur:
                return (a, b, c)
        return None

    def desactiver_grille(self):
        # Pour un Label, on change le curseur pour indiquer qu'on ne peut plus cliquer
        for lbl in self.boutons:
            lbl.config(cursor="")

    def activer_grille(self):
        for i, lbl in enumerate(self.boutons):
            if self.plateau[i] == "":
                lbl.config(cursor="hand2")

    def reinitialiser_jeu(self):
        self.plateau = [""] * 9
        self.partie_active = True
        self.attente_ia = False
        self.statut_var.set("C'est à votre tour (X)")
        for lbl in self.boutons:
            lbl.config(
                text="", 
                fg=self.couleur_text_normal, 
                bg=self.couleur_bg_normal, 
                relief="groove",
                cursor="hand2"
            )

if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.update_idletasks()
    largeur, hauteur = 380, 520
    x = (fenetre.winfo_screenwidth() // 2) - (largeur // 2)
    y = (fenetre.winfo_screenheight() // 2) - (hauteur // 2)
    fenetre.geometry(f'{largeur}x{hauteur}+{x}+{y}')
    
    jeu = Morpion(fenetre)
    fenetre.mainloop()