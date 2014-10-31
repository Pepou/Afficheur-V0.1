# -*- coding: utf-8 -*-

"""
Module implementing Afficheurs.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow
from PyQt4 import QtGui
from PyQt4 import QtCore
from .Ui_afficheurs import Ui_MainWindow
from Package.AccesBdd import AccesBdd
import decimal
class Afficheurs(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self,login, password,  parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        #gestion onglet :
        self.onglet = [self.tab, self.tab_2, self.tab_3, self.tab_4]
        self.nbr_pt =self.spinBox.value()
        i=0
        for i in range(self.nbr_pt+1): #+1 car s'arrete avant la derniere valeur
            self.onglet[3-i].setEnabled(False)
           
        #bdd
        self.db = AccesBdd(login, password)
        list_cmr = self.db.recensement_cmr()
        list_cmr.sort()
        #insertion combobox
        self.comboBox_cmr.addItems(list_cmr)

        
        #configuration largeur colonnes tablewidget
        self.tableWidget.setColumnWidth(0,300)
        self.tableWidget.setColumnWidth(1,300)
        self.tableWidget.setColumnWidth(2,300)
        
        self.tableWidget_2.setColumnWidth(0,300)
        self.tableWidget_2.setColumnWidth(1,300)
        self.tableWidget_2.setColumnWidth(2,300)
        
        self.tableWidget_3.setColumnWidth(0,300)
        self.tableWidget_3.setColumnWidth(1,300)
        self.tableWidget_3.setColumnWidth(2,300)
        
        #Gestion polynome de l'etalon:
        self.ordre_poly_etalon = 0
        self.coeff_a_poly_etalon = 0
        self.coeff_b_poly_etalon = 0
        self.coeff_c_poly_etalon = 0
        
        
    @pyqtSlot(str)
    def on_comboBox_famille_afficheur_activated(self, p0):
        """
        lors de la selection d'une famille d'afficheurs on va chercher topute
        cette famille dans la base et on tire par rapport au site du cmr
        """
        # TODO: not implemented yet
        nom_cmr = self.comboBox_cmr.currentText().split() #list avec nom et prenom
        
        type_afficheur = str(self.comboBox_famille_afficheur.currentText())
        
        #recherche domaine de mesure pour etalons
        if type_afficheur == "Sonde alarme température" or type_afficheur == "Afficheur de température":
            domaine_mesure = "Température"
            designation_etalon = "Chaîne de mesure de température"            
        elif type_afficheur == "Afficheur de temps":
            domaine_mesure = "Temps-Fréquence"
            designation_etalon = "Chronomètre/minuterie de travail"
        elif type_afficheur == "Afficheur de vitesse":
            domaine_mesure = "Vitesse"
            designation_etalon = "Tachymetre Optique"
        
        
        #tri des afficheurs/etalons
        service_site = self.db.recuperation_site_service_cmr(nom_cmr[0], nom_cmr[1])
        
        if service_site[0]not in ["LMS", "SNA", "ANG", "LRY", "LAV"]:           
            afficheurs_nts = self.db.recensement_afficheurs(type_afficheur, "*", "Nantes")            
            afficheurs_nts_nord = self.db.recensement_afficheurs(type_afficheur, "*", "NTSNO")
            afficheurs = list(set(afficheurs_nts+afficheurs_nts_nord))
        
            etalons_nts = self.db.recensement_etalons(domaine_mesure, "*", "Nantes", designation_etalon)
            etalons_nts_nord = self.db.recensement_etalons(domaine_mesure, "*", "NTSNO", designation_etalon)
            etalons = list(set( etalons_nts + etalons_nts_nord))
        else:
            afficheurs = self.db.recensement_afficheurs(type_afficheur, "*", service_site[0])
            etalons = self.db.recensement_etalons(domaine_mesure, "*", service_site[0], designation_etalon)
        
        afficheurs.sort()
        etalons.sort()
        
        self.comboBox_identification.clear()
        self.comboBox_ident_etalon.clear()
        
        self.comboBox_identification.addItems(afficheurs)
        self.comboBox_ident_etalon.addItems(etalons)        

            
    
    @pyqtSlot(int)
    def on_comboBox_identification_activated(self, index):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
                #Recherche n°serie 
        identification = self.comboBox_identification.currentText()
        
        n_serie = self.db.n_serie_afficheur( identification)
        self.textEdit_n_serie.clear()
        self.textEdit_n_serie.append(n_serie)
    
    @pyqtSlot(int)
    def on_spinBox_valueChanged(self, p0):
        """
        fct qui autorise l'ecriture des onglet en fct du nbr selectionné
        """        
        nbr_pt =self.spinBox.value()
        
        for i in range(nbr_pt+1):
             self.onglet[i].setEnabled(True)
        
        for i in range(nbr_pt+1, 4): #+1 car s'arrete avant la derniere valeur
           self.onglet[i].setEnabled(False)
    
    @pyqtSlot(int)
    def on_comboBox_ident_etalon_activated(self, index):
        """
        Slot documentation goes here.
        """
        
        etalon_select = self.comboBox_ident_etalon.currentText()
        donnee_poly = self.db.recuperation_polynomes_etal(etalon_select)

        mise_en_forme_combobox = []
        for ele in donnee_poly:
            donnee = str(ele[0] +" "+ "du" +" "+ ele[1].strftime("%d/%m/%y"))
            mise_en_forme_combobox.append(donnee)

        self.comboBox_ce_etal.clear()
        self.comboBox_ce_etal.addItems(mise_en_forme_combobox)
    
    @pyqtSlot(int)
    def on_comboBox_ce_etal_activated(self, index):
        """
        fct qui va chercher les donnees du poly selectionne sur le combobox
        """

        ce_select = self.comboBox_ce_etal.currentText().split()
        del ce_select[1]
        del ce_select[1]

        donnee_poly = self.db.recuperation_polynome_etal_num_ce(ce_select[0])
        
        self.ordre_poly_etalon = donnee_poly[0][2]
        self.coeff_a_poly_etalon = donnee_poly[0][3]
        self.coeff_b_poly_etalon = donnee_poly[0][4]
        self.coeff_c_poly_etalon = donnee_poly[0][5]
    
    @pyqtSlot(int, int)
    def on_tableWidget_cellChanged(self, row, column):
        """
        fct qui calcul valeur corrigée de l'etalon si on ecrit dans la colonne etal brute
        """
        # TODO: not implemented yet
        colonne = self.tableWidget.currentColumn()
        ligne = self.tableWidget.currentRow()

        #gestion donnees etalon brute
        try:
            if colonne == 0:
                print("valeur cell {}".format(self.tableWidget.item(ligne, 0).text()))
                valeur_etal_brute = decimal.Decimal(self.tableWidget.item(ligne, 0).text())
                
                print("valeur brute etal {}".format(valeur_etal_brute))
                if self.ordre_poly_etalon == 1:                
                    correction = self.coeff_a_poly_etalon*valeur_etal_brute + self.coeff_b_poly_etalon
                    
                        
                elif self.ordre_poly_etalon == 2:
                    correction = self.coeff_a_poly_etalon*(valeur_etal_brute * valeur_etal_brute)\
                                        + self.coeff_b_poly_etalon * valeur_etal_brute + self.coeff_c_poly_etalon
                
                valeur_etal_corri = valeur_etal_brute + correction                
                
                #on reaffect les lignes et colonnes de reference afin d'eviter une boucle infinie
                self.tableWidget.setCurrentCell (ligne,1)
                self.ecriture_tableau(self.tableWidget, ligne, 1, valeur_etal_corri)
                
            else:
                pass
                
        except decimal.InvalidOperation:
            self.tableWidget.setCurrentCell (ligne,1)
            self.ecriture_tableau(self.tableWidget, ligne, 1, "Erreur de Saisie donnees etalon brute")

            
    def ecriture_tableau(self, nom_tableau_, ligne, colonne, valeur):
        '''fct pour ecrire dans une case du tableau si une erreur fond case rouge'''
        if valeur == "Erreur de Saisie donnees etalon brute":
            item = QtGui.QTableWidgetItem(str(valeur))
            item.setBackground(QtGui.QColor('red'))
            nom_tableau_.setItem(ligne, colonne, item)
            
            self.tableWidget.setCurrentCell (ligne + 1,colonne-1)
        else:
            item = QtGui.QTableWidgetItem(str(valeur))            
            nom_tableau_.setItem(ligne, colonne, item)            
            self.tableWidget.setCurrentCell (ligne + 1,colonne-1)
