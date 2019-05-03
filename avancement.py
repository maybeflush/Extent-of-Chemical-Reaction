# coding: utf-8
__author__='maybeflush'
__date__='2019'
#______@ import zone____________________________________________
from chempy import Equilibrium                         #pypi.org/project/chempy/
from chempy import Substance                           #pypi.org/project/chempy/
from decimal import *                                  #docs.python.org/3/library/decimal.html
import itertools                                       #docs.python.org/3.7/library/itertools.html
import numpy as np                                     #www.numpy.org/
import json                                            #https://docs.python.org/3/library/json.html
import os                                              #https://docs.python.org/3/library/os.html
from tkinter import *                                  #https://docs.python.org/3.7/library/tkinter.html
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import matplotlib                                      ##https://matplotlib.org
'''Matplotlib va travailler en ''backend'' de façon à dessiner dans une frame;
Le module graphique est Tkinter et on lui dit d'utiliser TK en mode AGG
(https://en.wikipedia.org/wiki/Anti-Grain_Geometry)'''
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
#https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_canvas_sgskip.html
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#______@ Class zone____________________________________________
#définition de la classe
class Avancement(Tk):
    '''What can i say that u dont know yet :p'''
    # constructeur de la classe
    def __init__(self):
        #comme il s'agit d'un héritage on active le constructeur de la clase parente
        Tk.__init__(self)

        #Initialisation des attributs de la classe
        self.nb_reac=0
        self.nb_prod=0
        self.REAC=[]
        self.PROD=[]
        self.Liste_reac={}
        self.Liste_prod={}
        self.ligne=0
        self.file_name=''


        # Taille de la fenêtre initiale, titre
        self.geometry("482x100")
        self.title('Avancement_v1.2')

        # Ancrage de la  frame à la fenêtre
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        #Création d'un cadre avec un texte "Fichier de données"
        self.frame1=Frame(self,borderwidth=10, relief="groove")
        self.frame1.grid(row=0, column=0, sticky=NSEW)
        self.label1=Label(self.frame1, text="Fichier de données :")
        self.label1.grid(row=1, sticky=W)

        #Création d'une entrée de type texte pour le path_file
        self.path=Entry(self.frame1,relief="raised")
        self.path.grid(row=1, column=1, sticky=E)

        #Création d'un bouton avec appel de la fonction browse
        self.entree=Button(self.frame1, text="Parcourir" ,command=self.browse)
        self.entree.grid(row=1, column=2, sticky=E)

        #Création d'un bouton avec appel de la fonction _delete_window
        self.quitter =  Button(self.frame1, text='QUITTER',bg='green',fg='red',height=3, width=8,command=self._delete_window)
        self.quitter.grid(row=2, column=0, sticky=W)

        #Création d'un bouton avec appel de la fonction empty_alert
        self.launch1 = Button(self.frame1, text='Afficher le Tableau',height=3,fg='red',command=self.empty_alert)
        self.launch1.grid(row=2, column=2, sticky=E)

        #En cas de fermeture de la fenêtre, appel de la fonction _delete_window
        self.protocol("WM_DELETE_WINDOW", self._delete_window)

#______@ Methods zone____________________________________________

    def browse(self):
        '''On parcourt les fichiers pour récupèrer le .json'''
        self.file_name=askopenfilename()#Ouvre l'explorateur de fichier
        self.set_text()#appel de la fonction set_text

    def set_text(self):
        '''On vide la zone de texte et on ajoute le chemin du fichier'''
        self.path.delete(0,END)#efface la zone
        self.path.insert(0,self.file_name)#Ajoute le chemin

    def _delete_window(self):
        '''On essaye de détruire la frame puis on quitte l'appli'''
        try:
            self.destroy()#detruit la fenetre
            os._exit(0)#quitte !!
        except:
            print("ENCORE RATE")

    def empty_alert(self):
        '''On vérifie qu'un fichier source existe'''
        if  self.file_name=='':#si le nom est vide
            messagebox.showinfo("Erreur_Fichier", "Veuillez entrer le chemin du fichier source")
        else:#sinon
            self.new()#appel la fonction new

    def new(self):
        '''C'est la méthode pivot !!On génère trois frames:
            * Une contenant le graphique
            * Une Résumant les calculs + équation
            * Une affichant le tableau'''

        #Création d'une seconde fenêtre "self.top" qui dépend de la fenêtre principale
        self.top = Toplevel(master=self)
        self.top.title("TABLEAU D'AVANCEMENT")

        #En cas de fermeture de la fenêtre, appel de la fonction RAZ
        self.top.protocol("WM_DELETE_WINDOW", self.RAZ)

        #Création d'un cadre vierge s'étendant sur 2 colonnes"
        self.top.frame2=Frame(self.top,borderwidth=10, relief="sunken", width=100, height=100)
        self.top.frame2.grid(row=0, columnspan=2, sticky=NSEW)#W => cadre à gauche(west)

        #Création d'un cadre vierge adjascent (row=0) s'étendant sur 4 colonnes"
        self.top.frame3=Frame(self.top, borderwidth=10, relief="sunken", width=100, height=100)
        self.top.frame3.grid(row=0, column=2, columnspan=4, sticky=NSEW)#W => cadre à gauche(west)

        # Ancrage de la  frame à la fenêtre
        self.top.grid_columnconfigure(0,weight=1)#fit la fenetre
        self.top.grid_rowconfigure(0,weight=1)

        #Initialisation de la variable name  &  Affichage du texte
        name="Fichier Source :"+self.file_name
        Label(self.top.frame2,text=name, fg="red").grid(row=1, sticky=W)

        #appel de la fonction calcul
        self.calcul()

        #double appel de la fonction search
        self.Liste_reac=self.search(self.REAC)
        self.Liste_prod=self.search(self.PROD)

        #appel de la fonction melange
        self.Xmax=Decimal(self.melange())

        #appel de la fonction tableau
        self.tableau()

        #appel de la fonction plot
        self.plot()

        #Python fait une pause sur cette fenêtre
        self.top.mainloop()

    def RAZ(self):
        '''Si on revient à la première fenêtre, on détruit 'top' et
         on remet tout à zéro pour un éventuel nouveau tableau'''
        self.top.destroy()
        self.nb_reac=0
        self.nb_prod=0
        self.REAC=[]
        self.PROD=[]
        self.Liste_reac={}
        self.Liste_prod={}
        self.ligne=0



    def calcul(self):
        '''A partir du fichier de données, on prépare nos attributs'''

        #Ouvre le fichier en lecture avec un alias
        with open(self.file_name)as my_file:
            #chargement des données du fichier au format json (dictionnaire)
            data=json.load(my_file)
             #Pour chaque clé & valeurs
            for k,v in data.items():
                #Si la ligne commence par R (comme réactifs)
                if v["Type"] =='R':
                    #Incrèmente le nb de réactifs
                    self.nb_reac+=1
                    #Alimente la liste REAC avec un tuple (Formule, Coefficient,n)
                    self.REAC.append(tuple([v["Formule"],v["Coeff"],v["n"]]))
                #Si la ligne commence par P (comme produits)
                if  v["Type"] =='P':
                    #Incrèmente le nb de produits
                    self.nb_prod+=1
                    #Alimente la liste PROD avec un tuple (Formule, Coefficient,n)
                    self.PROD.append(tuple([v["Formule"],v["Coeff"],v["n"]]))
        #Ferme le fichier
        my_file.close()
        #Formate REAC: coeff entiers et qtté décimales
        self.REAC=[(x,int(y),Decimal(z)) for (x,y,z) in self.REAC]
        #Formate PROD: coeff entiers et qtté décimales
        self.PROD=[(x,int(y),Decimal(z)) for (x,y,z) in self.PROD]
        #Le rapport w/v minium donnera le réactifs limitant
        self.etat_ini={k:round(float(Decimal(w)),15)/round(float(Decimal(v)),15)
        for (k,v,w) in self.REAC}

    def search(self,my_list):
        '''On cherche dans notre base Chem.json si toutes les espèces de my_list sont connues;
        sinon, on ajoute les espèces inconnues.'''
        #Extrait les formules de la liste en argument
        local_list=[x for (x,y,z) in my_list]
        #liste identique mais au format chempy
        temp=[Substance.from_formula(x).unicode_name for x in local_list]
        #Génère un dictionnaire au format chempy{Formule:coeff stoechio}
        #La fonction zip permet d'extraire depuis deux listes
        local_dict={v : y for v ,(x,y,z) in zip(temp, my_list)}

        #Ouvre le fichier en lecture
        with open("chem.json") as my_file:
            #chargement des données du fichier au format json (dictionnaire)
            data=json.load(my_file)
            #Récupère les formules du fichier
            formules=[ v for k,v in data.items()]
        #Ferme le fichier
        my_file.close()
        #Récupère l'intersection avec la liste entrée
        self.connus=list(set(formules).intersection(local_list))
        #Appelle la fonction ajout
        self.ajout(local_list)
        #Renvoie le dictionnaire pour l'équation
        return local_dict

    def ajout(self,my_list):
        '''ajoute des lignes au fichier espèce_chimique.txt'''
        #Ouvre le fichier en lecture
        with open("chem.json") as my_file:
            #chargement des données du fichier au format json (dictionnaire)
            data=json.load(my_file)
            #Parcourt la liste des espèces chimiques
            for elt in my_list:
                #Si l'espèce n'est pas connue
                if not elt in self.connus:
                    #Demande une entrée clavier....
                    nom=input("Entrer le nom de "+elt)
                    #Message d'information pour l'utilisateur
                    print(elt+" ajouté à mon Index")
                    #Initialisation de l'entrée
                    autre={nom:elt}
                    #La fonction update ajoute l'entrée au dictionnaire
                    data.update(autre)
            #Ferme le fichier
            my_file.close()
        #Ouvre le fichier en écriture
        with open("chem.json","w") as my_file:
            #Ecrit dans le fichier
            json.dump(data,my_file)
        #Ferme le fichier
        my_file.close()

    def melange(self):
        '''Calcule Xmax, affiche le(s) réactif(s) limitant(s)'''
        #Génère la liste de tuples (n/coeff,occurence) triée par ordre croissant de n/coeff
        local_list=[(k, len(list(v)))
                for k, v in itertools.groupby(sorted(self.etat_ini.values()))]
        #initialisation
        RL='Réactif(s) limitant(s):'
        #Pour tout les éléments dans la liste contenant les formules (k) si le réactif est limitant
        for elt in [k for k,v in self.etat_ini.items() if v==local_list[0][0]]:
            #Incrémente la chaîne en ajoutant une virgule
            RL+=str(elt)+','
        #Retient tout sauf la dernière virgule
        RL=RL[:-1]
        #Création d'un label avec un texte "Résultats" & incrémentation de la variable ligne
        Label(self.top.frame3,text="Résultats:").grid(row=self.ligne, sticky=W)
        self.ligne+=1
        #Création d'un label avec un texte "RL" en rouge & incrémentation de la variable ligne
        Label(self.top.frame3,text=RL, fg="red").grid(row=self.ligne, sticky=W)
        self.ligne+=1
        #Affectation du nb de réactifs limitant
        txt="Réactif(s) limitant(s): "+str(local_list[0][1])+"."
        #Création d'un label avec le texte 'txt' en rouge & incrémentation de la variable ligne
        Label(self.top.frame3,text=txt).grid(row=self.ligne, sticky=W)
        self.ligne+=1
        #Affectation de Xmax
        txt="Avancement maximal: Xmax="+"{:5.2E}".format(local_list[0][0])+ " mol"
        #Création d'un label avec le texte 'txt' & incrémentation de la variable ligne
        Label(self.top.frame3,text=txt).grid(row=self.ligne, sticky=W)
        self.ligne+=1
        #Création d'un label avec l'équation-bilan & incrémentation de la variable ligne
        Label(self.top.frame3,text=Equilibrium(self.Liste_reac, self.Liste_prod)).grid(row=self.ligne, sticky=W)
        self.ligne+=1
        #retourne Xmax
        return local_list[0][0]

    def tableau (self):
        '''Affiche le tableau dans un cadre'''
        #appel de la fonction bloc1 pour la 1ere ligne
        self.bloc1(1,"Etat du système ","Avancement (mol)")
        #on récupère les formules des réactifs
        data=[k for k in  self.Liste_reac.keys()]
        #appel de la fonction bloc2 pour la 1ere ligne
        self.bloc2(1,2,data,self.REAC)
        #on récupère les noms des produits
        data=[k for k in  self.Liste_prod.keys()]
        #appel de la fonction bloc2 pour la 1ere ligne
        self.bloc2(1,2+len(self.REAC),data,self.PROD)

        #appel de la fonction bloc1 pour la 2e ligne
        self.bloc1(2,"Etat Initial (t=0s)","X_initial = 0")
        #on récupère les n_initiaux des réactifs
        data=["{:5.2E}".format(float(z)) for (x,y,z) in self.REAC]
        #appel de la fonction bloc2 pour la 2e ligne
        self.bloc2(2,2,data,self.REAC)
        #on récupère les n_initiaux des produits
        data=["{:5.2E}".format(float(z)) for (x,y,z) in self.PROD]
        #appel de la fonction bloc2 pour la 2e ligne
        self.bloc2(2,2+len(self.REAC),data,self.PROD)

        #appel de la fonction bloc1 pour la 3e ligne
        self.bloc1(3,"Etat Intermédiaire (t)","X")
        #on récupère l'équation n=f(x) des réactifs
        data=["{:5.2E}".format(float(z))+"-"+str(y)+"X" for (x,y,z) in self.REAC]
        #appel de la fonction bloc2 pour la 3e ligne
        self.bloc2(3,2,data,self.REAC)
        #on récupère l'équation n=f(x) des produits
        data=["{:5.2E}".format(float(z))+"+"+str(y)+"X" for (x,y,z) in self.PROD]
        #appel de la fonction bloc2 pour la 3e ligne
        self.bloc2(3,2+len(self.REAC),data,self.PROD)

        #appel de la fonction bloc1 pour la 4e ligne
        self.bloc1(4,"Etat Final (tmax)", "Xmax="+"{:5.2E}".format(self.Xmax))
        #on récupère les n_finaux des réactifs
        data=["{:5.2E}".format(abs(round(float(z-y*self.Xmax),15))) for (x,y,z) in self.REAC]
        #appel de la fonction bloc2 pour la 4e ligne
        self.bloc2(4,2,data,self.REAC)
        #on récupère les n_finaux des produits
        data=["{:5.2E}".format(abs(round(float(z+y*self.Xmax),15))) for (x,y,z) in self.PROD]
        #appel de la fonction bloc2 pour la 4e ligne
        self.bloc2(4,2+len(self.REAC),data,self.PROD)


    def bloc1(self,ligne,my_chaine1,my_chaine2):
        '''On construit les deux premières colonnes du tableau'''
        #Création d'un cadre à la ligne n°=ligne  & colonne 0
        self.top.new_frame=Frame(self.top,borderwidth=3, relief="raised")
        self.top.new_frame.grid(row=ligne, column=0, sticky=NSEW)#W => cadre à gauche(west)
        #Création d'un label avec un texte "my_chaine1"
        Label(self.top.new_frame,text=my_chaine1).grid(row=ligne, column=0, sticky=W)
        #Ancrage
        self.top.columnconfigure(0, pad=3)
        #Création d'un cadre à la ligne n°=ligne  & colonne 1
        self.top.new_frame=Frame(self.top,borderwidth=3, relief="raised")
        self.top.new_frame.grid(row=ligne, column=1, sticky=NSEW)#W => cadre à gauche(west)
        #Création d'un label avec un texte "my_chaine2"
        Label(self.top.new_frame,text=my_chaine2).grid(row=ligne, column=1, sticky=W)
        #Ancrage
        self.top.columnconfigure(1, pad=3)

    def bloc2(self,ligne,start_col,my_liste1,my_liste2):
        '''On construit toutes les colonnes du tableau pour les réactifs et les produits'''
        #on parcourt my_liste2 (liste des réactfis/produits)
        for loop in range(len(my_liste2)):
            #Création d'un cadre à la ligne n°=ligne  & colonne = colonne courante+colonne de départ
            self.top.new_frame=Frame(self.top,borderwidth=3, relief="raised")
            self.top.new_frame.grid(row=ligne, column=loop+start_col, sticky=NSEW)
            #Création d'un label avec un texte qui dépend du contenu du fichier my_liste1/data
            Label(self.top.new_frame,text=my_liste1[loop]).grid(row=ligne, column=loop+start_col, sticky=NSEW)
            #Ancrage
            self.top.columnconfigure(loop+start_col, pad=3)

    def plot (self):
        '''On créer une figure pour préparer le graphique'''
        #On définit une variable de type Figure
        fig = Figure(figsize=(5,5))
        a = fig.add_subplot(111)#1*1 grid 1st subplot
        #on génère un tableau de 100 points entre 0 et Xmax
        self.x=np.linspace(0,float(self.Xmax),100)
        #On génère les valeurs pour les réactifs via la fonction droite
        y=self.droite(self.Liste_reac, self.REAC,"réactifs")
        #On boucle sur le nb de réactifs
        for loop in range(len(self.REAC)):
            #on dessine avec un label= formule chimique
            a.plot(self.x,y[loop],label=self.molecule[loop])
        #On génère les valeurs pour les produits via la fonction droite
        y=self.droite(self.Liste_prod, self.PROD,"produits")
        #On boucle sur le nb de produits
        for loop in range(len(self.PROD)):
            #on dessine avec un label= formule chimique
            a.plot(self.x,y[loop],label=self.molecule[loop])
        #Titre du graphe/figure
        a.set_title ("n=f(x)", fontsize=11)
        #Nom des axes
        a.set_ylabel("n (mol)", fontsize=8)
        a.set_xlabel("x (mol)", fontsize=8)
        #Valeurs limites
        a.set_xlim(0,float(self.Xmax))
        a.set_ylim(bottom=0)
        #Format scientifiques des axes
        a.ticklabel_format(axis='both', style='Sci', scilimits=(0,0) )
        #Affichage de la légende
        a.legend()
        #On génère un canvas
        canvas = FigureCanvasTkAgg(fig, master=self.top.frame2)
        canvas.get_tk_widget().grid(row=2, sticky=NSEW)
        canvas.draw( )

    def droite(self,my_dict, my_list, chaine) :
        '''Calcul des y pour les réactifs/produits'''
        #'booleen'
        delta=1
        #si réactfis
        if chaine=='réactifs':
            #n va diminuer
            delta=-1
        #on génère une liste avec de valeurs y : n_ini plus ou moin coeff fois x
        my_y=[float(k)+delta*j*self.x for (i,j,k) in my_list]
        #On récupère les formules au format chempy
        self.molecule=[k for (k,v) in my_dict.items()]
        #retourne les y
        return my_y

#__________Core zone____________________________________________
if __name__ =="__main__":# pas exécuté si le script est importé en tant que modu
    app=Avancement()
    app.mainloop()
