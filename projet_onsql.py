import tkinter as tk
from pymongo import MongoClient

# Connexion à la base de données
client = MongoClient('mongodb://localhost:27017/')
db = client['livres_project']
collection = db['livres']
collectionu = db['utilisateur']


def ajouter_livre(livre):
    # livre = {'titre': self.entry_titre.get(), 'auteur': self.entry_auteur.get(), 'annee': int(self.entry_annee.get())}
    collection.insert_one(livre)
    # clear_entries()


def supprimer_livre(isbn):
    # titre = self.entry_titre.get()
    collection.delete_one({'isbn': isbn})
    # self.clear_entries()


def mettre_a_jour_livre(isbn, nouveau_livre):
    # titre = self.entry_titre.get()
    livre = collection.find_one({'isbn': isbn})
    if livre:
        # nouveau_titre = self.entry_titre.get()
        # nouvel_auteur = self.entry_auteur.get()
        # nouvelle_annee = int(self.entry_annee.get())

        collection.update_one(
            {'_id': livre['_id']},
            {'$set': {'isbn': nouveau_livre['isbn'], 'titre': nouveau_livre['titre'], 'auteur': nouveau_livre['auteur'],
                      'type': nouveau_livre['type'], 'etat': nouveau_livre['etat']}}
        )
        # self.clear_entries()


def recuperation(isbn):
    livre = collection.find_one({'isbn': isbn})
    return livre


def recherchenom(nom):
    livre = collection.find_one({'titre': nom})
    return livre['titre'], livre['etat']


def toutrecuperer():
    ma_collection = collection.find()
    return ma_collection


def utilisateur(cne):
    utiliateur = collectionu.find_one({'cne': cne})
    return utiliateur



def clear_entries(self):
    self.entry_titre.delete(0, tk.END)
    self.entry_auteur.delete(0, tk.END)
    self.entry_annee.delete(0, tk.END)
