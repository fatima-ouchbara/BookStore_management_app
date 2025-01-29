# colors #DBC4AD #AE6A31 #8B6A4E #512D16 #1D0E07

from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from tkinter.ttk import Treeview
import projet_onsql as nosql
import tkinter as tk

root = Tk()
root.title("FSTELivres")
root.geometry("1250x700+100+40")
root.iconbitmap("icon.ico")
root.config(bg="#8B6A4E")


def utilisateurauth():
    cneu = cne.get()
    motpasse = motpu.get()
    utilisateur = nosql.utilisateur(cneu)
    if utilisateur:
        if motpasse == utilisateur["motPasse"]:
            f4.destroy()
            # Cadre contenant la barre de défilement
            frame = ttk.Frame(root)
            frame.pack(fill="both", expand=True)

            def on_vertical_scroll(*args):
                canvas.yview(*args)

            # Barre de défilement verticale
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=on_vertical_scroll)

            # Zone de dessin (Canvas) à l'intérieur du cadre
            canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)

            # Configuration de la barre de défilement
            scrollbar.pack(side="right", fill="y")

            # Contenu du cadre
            content_frame = ttk.Frame(canvas)
            canvas.create_window((0, 0), window=content_frame, anchor="nw")

            # Création de la frame pour la recherche
            search_frame = ttk.Frame(frame)
            search_frame.pack(side="top", fill="x")

            # Ajout d'un Entry pour la recherche
            nom = StringVar()
            search_entry = ttk.Entry(search_frame, width=40, background="#DBC4AD", textvariable=nom)
            search_entry.pack(padx=10, pady=15)

            def livrerecherche():
                nomrecu, etatrecu = nosql.recherchenom(nom.get())
                for widget in content_frame.winfo_children():
                    widget.destroy()
                if nomrecu:
                    label = Label(content_frame, text=nomrecu + "\n " + etatrecu,
                                  font="arial 13 bold", bg="#DBC4AD", width=39)
                    label.grid(row=0, column=0, padx=40, pady=10)
            # Ajout d'un bouton de recherche
            search_button = ttk.Button(search_frame, text="Rechercher", command=livrerecherche)
            search_button.pack(pady=5)

            # Ajoutez des livres à content_frame
            documents = nosql.toutrecuperer()

            for i, document in enumerate(documents):
                row = i // 2
                column = i % 2
                titrel = document.get("titre", "")
                etatl = document.get("etat", "")
                label = Label(content_frame, text=titrel + "\n " + etatl,
                              font="arial 13 bold", bg="#DBC4AD", width=39)
                label.grid(row=row, column=column, padx=40, pady=10)

            # Configurer la zone de défilement du canevas
            content_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        else:
            messagebox.showwarning("Avertissement", "Mot de passe incorrecte.")
    else:
        messagebox.showwarning("Avertissement", "Utilisateur non reconnue.")


def utilisteur():
    global f4, cne, motpu
    f.destroy()
    f4 = Frame(root, bd=3, bg="#8B6A4E", relief=GROOVE)
    f4.pack(fill=BOTH, expand=True)

    obj = Frame(f4, bd=2, width=200, bg="#8B6A4E", height=420, relief=GROOVE)
    obj.place(x=230, y=80)

    lblauthf = Label(obj, text="Authentification:", width=30, height=2, bg="#8B6A4E", fg="#DBC4AD",
                     font=('Monotype Corsiva', 20, 'bold'))
    lblauthf.pack(side=TOP)
    # image
    imgauth = Image.open("user.png")
    nsize = (400, 400)
    resized_imgauth = imgauth.resize(nsize)
    img = ImageTk.PhotoImage(resized_imgauth)
    lblauth = Label(obj, bg="#8B6A4E", image=img)
    lblauth.image = img
    lblauth.pack(side=RIGHT)

    lblauthf = Label(obj, text="Identifiant:", width=20, height=3, bg="#8B6A4E", font="arial 13 bold")
    lblauthf.pack()

    cne = StringVar()
    Entry(obj, textvariable=cne, width=30, bd=2, font="arial 12 bold", bg="#DBC4AD").pack(padx=30)

    lblAuthf = Label(obj, text="Mot de passe:", width=20, height=3, bg="#8B6A4E", font="arial 13 bold")
    lblAuthf.pack()
    motpu = StringVar()
    Entry(obj, textvariable=motpu, width=30, bd=2, font="arial 12 bold", bg="#DBC4AD", show='*').pack(padx=30)
    Button(obj, text="Connexion", width=16, height=2, font="arial 12 bold", bg="#DBC4AD",
           command=utilisateurauth).place(x=90, y=320)


def recherche():
    livre_isbn = isbn.get()
    if livre_isbn != "":
        livre = nosql.recuperation(livre_isbn)
        titre.set(livre['titre'])
        auteur.set(livre['auteur'])
        typel.set(livre['type'])
        etat.set(livre['etat'])
    else:
        messagebox.showwarning("Avertissement", "ISBN vide,veuillez le remplir.")


def miseajour():
    livre_isbn = isbn.get()
    n_livre = {'isbn': livre_isbn, 'titre': titre.get(), 'auteur': auteur.get(), 'type': typel.get(),
               'etat': etat.get()}
    if livre_isbn != "":
        nosql.mettre_a_jour_livre(livre_isbn, n_livre)
        messagebox.showinfo("Information", "Le livre est mis a jours.")

    else:
        messagebox.showwarning("Avertissement", "ISBN vide,veuillez le remplir.")


def suppression():
    livre_isbn = isbn.get()
    if livre_isbn != "":
        nosql.supprimer_livre(livre_isbn)
        messagebox.showinfo("Information", "Le livre est bien supprimer.")
    else:
        messagebox.showwarning("Avertissement", "ISBN vide,veuillez le remplir.")


def ajout():
    i = isbn.get()
    t = titre.get()
    a = auteur.get()
    ty = typel.get()
    e = etat.get()
    if i != "" and t != "" and a != "" and ty != "" and e != "":
        livre = {'isbn': i, 'titre': t, 'auteur': a, 'type': ty, 'etat': e}
        nosql.ajouter_livre(livre)
        messagebox.showinfo("Information", "Le livre est enregistré avec succes.")
    else:
        messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs.")


def requets():
    global f3, isbn, titre, auteur, typel, etat
    f2.destroy()
    f3 = Frame(root, bd=3, bg="#8B6A4E", relief=GROOVE)
    f3.pack(fill=BOTH, expand=True)
    lblb = Frame(f3, bd=2, width=1000, bg="#8B6A4E", height=620, relief=GROOVE)
    lblb.place(x=100, y=30)

    # les boutons
    rbutton = Button(lblb, text="Recherche", width=16, height=2, font=('Monotype Corsiva', 15, 'bold'), bg="#DBC4AD",
                     command=recherche)
    rbutton.place(x=700, y=130)

    mbutton = Button(lblb, text="Mise a jour", width=16, height=2, font=('Monotype Corsiva', 15, 'bold'), bg="#DBC4AD",
                     command=miseajour)
    mbutton.place(x=700, y=220)

    sbutton = Button(lblb, text="Supprimer", width=16, height=2, font=('Monotype Corsiva', 15, 'bold'), bg="#DBC4AD",
                     command=suppression)
    sbutton.place(x=700, y=310)

    abutton = Button(lblb, text="Ajouter", width=16, height=2, font=('Monotype Corsiva', 15, 'bold'), bg="#DBC4AD",
                     command=ajout)
    abutton.place(x=700, y=400)

    # les champs de base de données
    Label(lblb, text="ISBN:", width=10, height=2, bg="#8B6A4E",
          font=('Monotype Corsiva', 13, 'bold')).place(x=100, y=100)
    isbn = StringVar()
    Entry(lblb, textvariable=isbn, width=30, bd=2, font="arial 15", bg="#DBC4AD").place(x=230, y=100)

    Label(lblb, text="Titre de livre:", width=10, height=2, bg="#8B6A4E",
          font=('Monotype Corsiva', 13, 'bold')).place(x=100, y=200)
    titre = StringVar()
    Entry(lblb, textvariable=titre, width=30, bd=2, font="arial 15", bg="#DBC4AD").place(x=230, y=200)

    Label(lblb, text="Auteur:", width=10, height=2, bg="#8B6A4E",
          font=('Monotype Corsiva', 13, 'bold')).place(x=100, y=300)
    auteur = StringVar()
    Entry(lblb, textvariable=auteur, width=30, bd=2, font="arial 15", bg="#DBC4AD").place(x=230, y=300)

    Label(lblb, text="Type de livre:", width=10, height=2, bg="#8B6A4E",
          font=('Monotype Corsiva', 13, 'bold')).place(x=100, y=400)
    typel = StringVar()
    Entry(lblb, textvariable=typel, width=30, bd=2, font="arial 15", bg="#DBC4AD").place(x=230, y=400)

    Label(lblb, text="Etat:", width=10, height=2, bg="#8B6A4E",
          font=('Monotype Corsiva', 13, 'bold')).place(x=100, y=500)
    etat = StringVar()
    Entry(lblb, textvariable=etat, width=30, bd=2, font="arial 15", bg="#DBC4AD").place(x=230, y=500)


def gestion():
    global f2
    if login.get() == "Admin" and motp.get() == "Admin123":
        f1.destroy()
        # requets.f3.destroy()
        f2 = Frame(root, bd=3, bg="#8B6A4E", relief=GROOVE)
        f2.pack(fill=BOTH, expand=True)
        mon_menu = Menu(root, bg="#8B6A4E")
        root.config(menu=mon_menu)

        file_menu = Menu(mon_menu, tearoff=0)
        mon_menu.add_cascade(label="GESTION", menu=file_menu)
        file_menu.add_command(label="Affichage", command=gestion)
        file_menu.add_command(label="Gestion de Base de donnée", command=requets)
        file_menu.add_command(label="Quitter", command=root.destroy)
        colonnes = ["ISBN", "Titre de livre", "Auteur", "Type", "Etat"]
        # Création d'un Treeview
        tree = Treeview(f2, columns=colonnes, show="headings")

        # Ajout des colonnes
        for col in colonnes:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        documents = nosql.toutrecuperer()
        for document in documents:
            data_row = [
                document.get("isbn", ""),
                document.get("titre", ""),
                document.get("auteur", ""),
                document.get("type", ""),
                document.get("etat", "")
            ]
            tree.insert("", "end", values=data_row)

        tree.grid(row=0, column=0, sticky="nsew")

        # Redimensionnement automatique des colonnes et lignes
        f2.columnconfigure(0, weight=1)
        f2.rowconfigure(0, weight=1)
    else:
        messagebox.showwarning("Avertissement", "Identifiant ou Mot de passe incorrecte")


def admin():
    global f1, login, motp
    f.destroy()
    f1 = Frame(root, bd=3, bg="#8B6A4E", relief=GROOVE)
    f1.pack(fill=BOTH, expand=True)

    obj = Frame(f1, bd=2, width=200, bg="#8B6A4E", height=420, relief=GROOVE)
    obj.place(x=200, y=60)

    lblAuthf = Label(obj, text="Authentification:", width=30, height=2, bg="#8B6A4E", fg="#DBC4AD",
                     font=('Monotype Corsiva', 20, 'bold'))
    lblAuthf.pack(side=TOP)
    # image
    imgAuth = PhotoImage(file="b.png")
    lblAuth = Label(obj, bg="#8B6A4E", image=imgAuth)
    lblAuth.image = imgAuth
    lblAuth.pack(side=RIGHT)

    lblAuthf = Label(obj, text="Identifiant:", width=20, height=3, bg="#8B6A4E", font="arial 13 bold")
    lblAuthf.pack()

    login = StringVar()
    Entry(obj, textvariable=login, width=30, bd=2, font="arial 12 bold", bg="#DBC4AD").pack(padx=30)

    lblAuthf = Label(obj, text="Mot de passe:", width=20, height=3, bg="#8B6A4E", font="arial 13 bold")
    lblAuthf.pack()
    motp = StringVar()
    Entry(obj, textvariable=motp, width=30, bd=2, font="arial 12 bold", bg="#DBC4AD", show='*').pack(padx=30)
    Button(obj, text="Connexion", width=16, height=2, font="arial 12 bold", bg="#DBC4AD",
           command=gestion).place(x=90, y=300)


f = Frame(root, bd=3, bg="#8B6A4E", relief=GROOVE)
f.pack(fill=BOTH, expand=True)
# Label(f, text="Réaliser par: SASSIOUI Souhayla & OUCHBARA Fatima Zohra", width=10, height=3, bg="#8B6A4E",
# anchor='e').pack(side=TOP,
# fill=X)
original_image = Image.open("bg1.png")
size = (900, 500)
resized_image = original_image.resize(size)
img1 = ImageTk.PhotoImage(resized_image)
lbl1 = Label(f, bg="white", image=img1)
lbl1.pack(pady=50)

Button(f, text="Utilisateur", width=19, height=2, font="arial 12 bold", bg="#DBC4AD", command=utilisteur).place(x=300,
                                                                                                                y=620)
Button(f, text="Adminstrateur", width=19, height=2, font="arial 12 bold", bg="#DBC4AD", command=admin).place(x=800,
                                                                                                             y=620)
root.mainloop()
