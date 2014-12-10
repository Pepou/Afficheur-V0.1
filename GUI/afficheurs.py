# -*- coding: utf-8 -*-

"""
Module implementing Afficheurs.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QMessageBox
from .Ui_afficheurs import Ui_MainWindow
from Package.AccesBdd import AccesBdd
from Package.RapportAfficheur import RapportAfficheur
import decimal
import numpy as np

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
        
        #gestion EMT
        self.EMT_temperature = ["±0.13", "±0.3", "±0.5", "±0.8", "±1", "±2", "±3", "±4"]
        self.EMT_vitesse = ["±1%", "±3%", "±20%"]
        self.EMT_temps = ["±1% + 4s","±1% + 18s", "±1% + 1min" ]
        
        
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
            self.comboBox_EMT.addItems(self.EMT_temperature)
            self.comboBox_EMT_2.addItems(self.EMT_temperature)
            self.comboBox_EMT_3.addItems(self.EMT_temperature)

        elif type_afficheur == "Afficheur de temps":
            domaine_mesure = "Temps-Fréquence"
            designation_etalon = "Chronomètre/minuterie de travail"
            self.comboBox_EMT.addItems(self.EMT_temps)
            self.comboBox_EMT_2.addItems(self.EMT_temps)
            self.comboBox_EMT_3.addItems(self.EMT_temps)
            
            
        elif type_afficheur == "Afficheur de vitesse":
            domaine_mesure = "Vitesse"
            designation_etalon = "Tachymetre Optique"
            self.comboBox_EMT.addItems(self.EMT_vitesse)
            self.comboBox_EMT_2.addItems(self.EMT_vitesse)
            self.comboBox_EMT_3.addItems(self.EMT_vitesse)
            
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
        
        
        if type_afficheur == "Afficheur de vitesse":
            etalons = self.db.recensement_etalons_vitesse(designation_etalon)
        
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
        
        caract_afficheur = self.db.caract_afficheur(identification)
        n_serie = caract_afficheur[0]
        constructeur = caract_afficheur[1]
        type = caract_afficheur[2]
        renseignement_complementaire = caract_afficheur[3]
        
        self.textEdit_n_serie.clear()
        self.textEdit_n_serie.append(n_serie)
        
        self.lineEdit_constructeur.clear()
        self.lineEdit_constructeur.setText (constructeur)
        
        self.lineEdit_type.clear()
        self.lineEdit_type.setText(type)
        
        self.textEdit_renseignement_complementaire.clear()
        self.textEdit_renseignement_complementaire.append(renseignement_complementaire)
    
    @pyqtSlot(int)
    def on_spinBox_valueChanged(self, p0):
        """
        fct qui autorise l'ecriture des onglet en fct du nbr selectionné
        """        
        self.nbr_pt =self.spinBox.value()
        
        for i in range(self.nbr_pt+1):
             self.onglet[i].setEnabled(True)
        
        for i in range(self.nbr_pt+1, 4): #+1 car s'arrete avant la derniere valeur
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
        #gestion donnees etalon brute
        try:
            colonne = self.tableWidget.currentColumn()
            ligne = self.tableWidget.currentRow()
          
            if colonne == 0:                
                valeur_etal_brute = decimal.Decimal(self.tableWidget.item(ligne, 0).text())
                
                if self.ordre_poly_etalon == 1:                
                    correction = self.coeff_a_poly_etalon*valeur_etal_brute + self.coeff_b_poly_etalon
                                            
                elif self.ordre_poly_etalon == 2:
                    correction = self.coeff_a_poly_etalon*(valeur_etal_brute * valeur_etal_brute)\
                                        + self.coeff_b_poly_etalon * valeur_etal_brute + self.coeff_c_poly_etalon
                
                valeur_etal_corri = valeur_etal_brute + correction                
          
                #on reaffect les lignes et colonnes de reference afin d'eviter une boucle infinie
                self.ecriture_tableau(self.tableWidget, ligne, 1, valeur_etal_corri, 'white')
                
                self.calculs(self.tableWidget, self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_afficheur, 
                            self.lineEdit_correction, self.lineEdit_ecartype, self.lineEdit_incertitude, 
                            self.doubleSpinBox_resolution)
                            
                self.conformite(self.comboBox_EMT, self.lineEdit_correction, self.lineEdit_incertitude, self.lineEdit_conformite, self.doubleSpinBox_resolution)
                
            elif colonne == 2:                
                string_valeur_afficheur = self.tableWidget.item(ligne, 2).text()
                self.ecriture_tableau(self.tableWidget, ligne, 2, string_valeur_afficheur, 'white')
                
                decimal.Decimal(self.tableWidget.item(ligne, 2).text()) # permet de detecter erreur de saisie tru except
                
                self.calculs(self.tableWidget, self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_afficheur, 
                            self.lineEdit_correction, self.lineEdit_ecartype, self.lineEdit_incertitude, 
                            self.doubleSpinBox_resolution)
                            
                self.conformite(self.comboBox_EMT, self.lineEdit_correction, self.lineEdit_incertitude, self.lineEdit_conformite, self.doubleSpinBox_resolution)            
            
            else:
                pass                        

            
        except decimal.InvalidOperation:            
            if colonne == 0:                
                self.ecriture_tableau(self.tableWidget, ligne, 1, "Erreur de Saisie donnees etalon brute", 'red')            
            elif colonne == 2:
                self.ecriture_tableau(self.tableWidget, ligne, colonne, string_valeur_afficheur, 'red')

            self.calculs(self.tableWidget, self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_afficheur, 
                            self.lineEdit_correction, self.lineEdit_ecartype, self.lineEdit_incertitude, 
                            self.doubleSpinBox_resolution) 
                
    
    
    @pyqtSlot(int, int)
    def on_tableWidget_2_cellChanged(self, row, column):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
                
        #gestion donnees etalon brute
        try:
            colonne = self.tableWidget_2.currentColumn()
            ligne = self.tableWidget_2.currentRow()
          
            if colonne == 0:                
                valeur_etal_brute = decimal.Decimal(self.tableWidget_2.item(ligne, 0).text())
                
                if self.ordre_poly_etalon == 1:                
                    correction = self.coeff_a_poly_etalon*valeur_etal_brute + self.coeff_b_poly_etalon
                    
                        
                elif self.ordre_poly_etalon == 2:
                    correction = self.coeff_a_poly_etalon*(valeur_etal_brute * valeur_etal_brute)\
                                        + self.coeff_b_poly_etalon * valeur_etal_brute + self.coeff_c_poly_etalon
                
                valeur_etal_corri = valeur_etal_brute + correction                
          
                #on reaffect les lignes et colonnes de reference afin d'eviter une boucle infinie
                self.ecriture_tableau(self.tableWidget_2, ligne, 1, valeur_etal_corri, 'white')
                
                self.calculs(self.tableWidget_2, self.lineEdit_moyenne_etalon_2, self.lineEdit_moyenne_afficheur_2, 
                        self.lineEdit_correction_2, self.lineEdit_ecartype_2, self.lineEdit_incertitude_2, 
                        self.doubleSpinBox_resolution_2)
                        
                self.conformite(self.comboBox_EMT_2, self.lineEdit_correction_2, self.lineEdit_incertitude_2, self.lineEdit_conformite_2, self.doubleSpinBox_resolution_2)
                        
                
                
            elif colonne == 2:                
                string_valeur_afficheur = self.tableWidget_2.item(ligne, 2).text()
                self.ecriture_tableau(self.tableWidget_2, ligne, 2, string_valeur_afficheur, 'white')
                
                decimal.Decimal(self.tableWidget_2.item(ligne, 2).text()) # permet de detecter erreur de saisie tru except
                
                self.calculs(self.tableWidget_2, self.lineEdit_moyenne_etalon_2, self.lineEdit_moyenne_afficheur_2, 
                        self.lineEdit_correction_2, self.lineEdit_ecartype_2, self.lineEdit_incertitude_2, 
                        self.doubleSpinBox_resolution_2)
                     
                self.conformite(self.comboBox_EMT_2, self.lineEdit_correction_2, self.lineEdit_incertitude_2, self.lineEdit_conformite_2, self.doubleSpinBox_resolution_2)
                        
                
            else:
                pass                        

            
        except decimal.InvalidOperation:            
            if colonne == 0:                
                self.ecriture_tableau(self.tableWidget_2, ligne, 1, "Erreur de Saisie donnees etalon brute", 'red')            
            elif colonne == 2:
                self.ecriture_tableau(self.tableWidget_2, ligne, colonne, string_valeur_afficheur, 'red')

            self.calculs(self.tableWidget_2, self.lineEdit_moyenne_etalon_2, self.lineEdit_moyenne_afficheur_2, 
                        self.lineEdit_correction_2, self.lineEdit_ecartype_2, self.lineEdit_incertitude_2, 
                        self.doubleSpinBox_resolution_2)   
    
    @pyqtSlot(int, int)
    def on_tableWidget_3_cellChanged(self, row, column):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
            #gestion donnees etalon brute
            
        try:
            colonne = self.tableWidget_3.currentColumn()
            ligne = self.tableWidget_3.currentRow()
          
            if colonne == 0:                
                valeur_etal_brute = decimal.Decimal(self.tableWidget_3.item(ligne, 0).text())
                
                if self.ordre_poly_etalon == 1:                
                    correction = self.coeff_a_poly_etalon*valeur_etal_brute + self.coeff_b_poly_etalon
                    
                        
                elif self.ordre_poly_etalon == 2:
                    correction = self.coeff_a_poly_etalon*(valeur_etal_brute * valeur_etal_brute)\
                                        + self.coeff_b_poly_etalon * valeur_etal_brute + self.coeff_c_poly_etalon
                
                valeur_etal_corri = valeur_etal_brute + correction                
          
                #on reaffect les lignes et colonnes de reference afin d'eviter une boucle infinie
                self.ecriture_tableau(self.tableWidget_3, ligne, 1, valeur_etal_corri, 'white')
                
                self.calculs(self.tableWidget_3, self.lineEdit_moyenne_etalon_3, self.lineEdit_moyenne_afficheur_3, 
                        self.lineEdit_correction_3, self.lineEdit_ecartype_3, self.lineEdit_incertitude_3, 
                        self.doubleSpinBox_resolution_3)
                        
                self.conformite(self.comboBox_EMT_3, self.lineEdit_correction_3, self.lineEdit_incertitude_3, self.lineEdit_conformite_3, self.doubleSpinBox_resolution_3)

                
            elif colonne == 2:                
                string_valeur_afficheur = self.tableWidget_3.item(ligne, 2).text()
                self.ecriture_tableau(self.tableWidget_3, ligne, 2, string_valeur_afficheur, 'white')
                
                decimal.Decimal(self.tableWidget_3.item(ligne, 2).text()) # permet de detecter erreur de saisie tru except
                
                self.calculs(self.tableWidget_3, self.lineEdit_moyenne_etalon_3, self.lineEdit_moyenne_afficheur_3, 
                        self.lineEdit_correction_3, self.lineEdit_ecartype_3, self.lineEdit_incertitude_3, 
                        self.doubleSpinBox_resolution_3)
         
                self.conformite(self.comboBox_EMT_3, self.lineEdit_correction_3, self.lineEdit_incertitude_3, self.lineEdit_conformite_3, self.doubleSpinBox_resolution_3)
            
            else:
                pass                        

            
        except decimal.InvalidOperation:            
            if colonne == 0:                
                self.ecriture_tableau(self.tableWidget_3, ligne, 1, "Erreur de Saisie donnees etalon brute", 'red')            
            elif colonne == 2:
                self.ecriture_tableau(self.tableWidget_3, ligne, colonne, string_valeur_afficheur, 'red')

            self.calculs(self.tableWidget_3, self.lineEdit_moyenne_etalon_3, self.lineEdit_moyenne_afficheur_3, 
                        self.lineEdit_correction_3, self.lineEdit_ecartype_3, self.lineEdit_incertitude_3, 
                        self.doubleSpinBox_resolution_3)
    

    
    
    
    def ecriture_tableau(self, nom_tableau_, ligne, colonne, valeur, color):
        '''fct pour ecrire dans une case du tableau si une erreur fond case rouge'''
        
        nom_tableau_.setCurrentCell (1,1)
        item = QtGui.QTableWidgetItem(str(valeur))
        item.setBackground(QtGui.QColor(color))
        nom_tableau_.setItem(ligne, colonne, item)
        
        
    def calculs(self, nom_tableau, nom_lineedit_moyenne_etalon, nom_lineedit_moyenne_afficheur, 
                nom_lineedit_correction, nom_lineedit_ecartype, nom_lineedit_incertitude, nom_doublespinbox):
        '''fct pour calculer moyenne etalon,moyenne afficheurs ,....'''       
        try:
            #calcul automatique moyenne etalon corrigé
            valeurs_etalon_corriges = []
            valeurs_afficheur = []
            
            for i in range (0, 6):
                if nom_tableau.item(i, 1) is not None:
                    valeurs_etalon_corriges.append(decimal.Decimal(nom_tableau.item(i, 1).text()))
                else:
                    pass
            moyenne_etal_corri = np.mean(valeurs_etalon_corriges)
            nom_lineedit_moyenne_etalon.setText(str(moyenne_etal_corri))
                
            # calcul moyenne afficheur:
            
            for i in range(0, 6):
                if nom_tableau.item(i, 2) is not None:
                    valeurs_afficheur.append(decimal.Decimal(nom_tableau.item(i, 2).text()))
                else:
                    pass
            
            moyenne_afficheur = np.mean(valeurs_afficheur)
            nom_lineedit_moyenne_afficheur.setText(str(moyenne_afficheur))
    
            #Corrections , moyenne des corrections,ecart type_afficheur:
            
            corrections =[]
            for i in range(0, 6):
                if nom_tableau.item(i, 1) is not None and nom_tableau.item(i, 2) is not None:
                    corrections.append(decimal.Decimal(nom_tableau.item(i, 1).text())- decimal.Decimal(nom_tableau.item(i, 2).text()))
                else:
                    pass
            moyenne_corrections = np.mean(corrections)
            ecartype_corrections = np.std(corrections , ddof=1)
            nom_lineedit_correction.setText(str(moyenne_corrections))
            nom_lineedit_ecartype.setText(str(ecartype_corrections))
            
            #Incertitudes:
                #SAT#
                ####################################################################################################c
            if self.comboBox_famille_afficheur.currentText() == "Sonde alarme température":
                    #etalon
                    ############################################
                        #uetalonnage
                identification_etalon = self.comboBox_ident_etalon.currentText()
                numero_ce = self.comboBox_ce_etal.currentText().split()
                
                U_etalonnage_etalon = self.db.incertitude_etalonnage_temperature(identification_etalon, numero_ce[0])
                
                max_u_etalonnage = float(np.amax(U_etalonnage_etalon)/2)
                
                        #umodelisation                
                table_etal_tlue_correction = self.db.recuperation_corrections_etalonnage_temp(identification_etalon, numero_ce[0])
                tlue_etalonnage = [x[0] for x in table_etal_tlue_correction ]
                correction_etalonnage = [decimal.Decimal(x[1]) for x in table_etal_tlue_correction ]
 
                if self.ordre_poly_etalon == 1:
                    correction_modelisee = [decimal.Decimal(x * self.coeff_a_poly_etalon + self.coeff_b_poly_etalon) for x in tlue_etalonnage]
                else:                    
                    correction_modelisee = [decimal.Decimal(x * x* self.coeff_a_poly_etalon + x * self.coeff_b_poly_etalon +self.coeff_c_poly_etalon) for x in tlue_etalonnage]

                residu = []
                for i in range(0, len(correction_etalonnage)):
                    valeur_residu = correction_etalonnage[i]-correction_modelisee[i]
                    residu.append(valeur_residu)
                max_residu_absolu = np.amax([np.abs(x) for x in residu])
                                
                u_modelisation = np.array(max_residu_absolu, dtype=np.float)/np.sqrt(3)
                
                        #uresolution
                resolution_etalon = float(self.db.recuperation_resolution_etalon(identification_etalon))                
                u_resolution_etalon = resolution_etalon/(2*np.sqrt(3))
                
                        #uderive (pour linstant 0.15)
                u_derive = 0.15/np.sqrt(3)
                                
                    #sat
                    #####################################################################################
                        #uresolution

                resolution = nom_doublespinbox.value()#float(self.db.recuperation_resolution_etalon(ident_sat))
                
                u_resolution = resolution/(2*np.sqrt(3))
                
                        #ufidelite
                u_fidelite = float(ecartype_corrections)
                
                    #milieu de comparaison
                    ##################################################################################
                        #stabilite
                u_stab =np.std(np.array(valeurs_etalon_corriges, dtype=np.float))
                
                U_final = 2*np.sqrt(np.power(max_u_etalonnage, 2)+ np.power(u_modelisation, 2)+
                    np.power(u_resolution_etalon, 2) + np.power(u_derive, 2) + np.power(u_resolution, 2)+
                    np.power(u_fidelite, 2) + np.power(u_stab, 2))
                
                nom_lineedit_incertitude.setText(str(U_final))        
                
        except decimal.InvalidOperation:
            
            affichage = "Erreur dans les saisies effectuées"
            nom_lineedit_moyenne_etalon.setText(affichage)
    
    def conformite(self, nom_comboBox_EMT, nom_lineEdit_correction, nom_lineedit_incertitude, nom_lineEdit_conformite, nom_doublespinbox_resolution):
        '''fct qui gere la declaration de conformite'''
        
        resolution = str(nom_doublespinbox_resolution.value())
        U = nom_lineedit_incertitude.text()
        U_arrondie = decimal.Decimal(U).quantize(decimal.Decimal(resolution), rounding=decimal.ROUND_UP)
    
        if self.comboBox_famille_afficheur.currentText() == "Sonde alarme température" or self.comboBox_famille_afficheur.currentText() == "Afficheur de température":
            nom_brute_emt = nom_comboBox_EMT.currentText()
            if nom_brute_emt[:1] == "±":
                emt = float(nom_brute_emt[1:])

            moyenne_corrections = float(nom_lineEdit_correction.text())
            U = float(nom_lineedit_incertitude.text())
            valeur =np.abs(moyenne_corrections) + U

            if np.abs(moyenne_corrections) + U <=emt:
                nom_lineEdit_conformite.setText("Conforme")
            else:
                nom_lineEdit_conformite.setText("Non Conforme")
                
        elif self.comboBox_famille_afficheur.currentText() == "Afficheur de vitesse":
            print("coucou")
    
    @pyqtSlot()
    def on_actionEnregistrement_triggered(self):
        """
        fct qui enregistre les resultats dans la bdd et genere le rapport
        """
        resolution_afficheur_list = [self.doubleSpinBox_resolution.value(), self.doubleSpinBox_resolution_2.value(), self.doubleSpinBox_resolution_3.value()]
        moyenne_etalon_list = [self.lineEdit_moyenne_etalon.text(), self.lineEdit_moyenne_etalon_2.text(), self.lineEdit_moyenne_etalon_3.text()]
        moyenne_afficheur_list = [self.lineEdit_moyenne_afficheur.text(), self.lineEdit_moyenne_afficheur_2.text(), self.lineEdit_moyenne_afficheur_3.text()]
        moyenne_corrections_list = [self.lineEdit_moyenne_etalon.text(), self.lineEdit_moyenne_etalon_2.text(), self.lineEdit_moyenne_etalon_3.text()]
        ecartype_corrections_list = [self.lineEdit_ecartype.text(), self.lineEdit_ecartype_2.text(), self.lineEdit_ecartype_3.text()]
        U_list = [self.lineEdit_incertitude.text(), self.lineEdit_incertitude_2.text(), self.lineEdit_incertitude_3.text()]
        conformite_list = [self.lineEdit_conformite.text(), self.lineEdit_conformite_2.text(), self.lineEdit_conformite_3.text()]
        emt_list = [self.comboBox_EMT.currentText(), self.comboBox_EMT_2.currentText(), self.comboBox_EMT_3.currentText()]
        afficheur = {}
        client = self.db.recuperation_code_client_affectation(self.comboBox_identification.currentText())
#        afficheur["n_certificat"] = 
        
        afficheur["societe"] = client[0]
        afficheur["affectation"] = client[1]
        afficheur["adresse"] = client[2]
        afficheur["code_postal"] = client[3]
        afficheur["ville"] = client[4]
        
        afficheur["identification_instrument"] = self.comboBox_identification.currentText()
        afficheur["n_serie"] = self.textEdit_n_serie.toPlainText ()
        afficheur["constructeur"] = self.lineEdit_constructeur.text()
        afficheur["designation"] = self.comboBox_famille_afficheur.currentText()
        afficheur["type"] = self.lineEdit_type.text()
        afficheur["resolution"] = resolution_afficheur_list 
        afficheur["date_etalonnage"] = self.dateEdit.date().toString('dd/MM/yyyy')
        afficheur["operateur"] = self.comboBox_cmr.currentText()
        
        if self.comboBox_famille_afficheur.currentText() == "Sonde alarme température":
            afficheur["n_mode_operatoire"] = "/006"
        else:
            afficheur["n_mode_operatoire"] = "/002"

        afficheur["etalon"] = self.comboBox_ident_etalon.currentText()
        afficheur["ce_etalon"] = self.comboBox_ce_etal.currentText()
        afficheur["operateur"] = self.comboBox_cmr.currentText()
        afficheur["renseignement_complementaire"] = self.textEdit_renseignement_complementaire.toPlainText()
        print(self.textEdit_renseignement_complementaire.toPlainText())
        
        afficheur["commentaire"] = self.textEdit_commentaire.toPlainText()
        
        afficheur["moyenne_etalon_corri"] = moyenne_etalon_list
        afficheur["moyenne_instrum"] = moyenne_afficheur_list
        afficheur["moyenne_correction"] = moyenne_corrections_list
        afficheur["U"] = U_list
        
        afficheur["conformite"] = conformite_list
        afficheur["emt"] = emt_list
        afficheur["n_certificat"] = "DTC"
        afficheur["nbr_pt_etalonnage"] = self.spinBox.value()
        cvr = RapportAfficheur()
        cvr.mise_en_forme_ce(afficheur)
        
        
        
        
    @pyqtSlot(str)
    def on_comboBox_EMT_3_activated(self, p0):
        """
        si changement EMT on recalcul tout
        """
        self.calculs(self.tableWidget_3, self.lineEdit_moyenne_etalon_3, self.lineEdit_moyenne_afficheur_3, 
                        self.lineEdit_correction_3, self.lineEdit_ecartype_3, self.lineEdit_incertitude_3, 
                        self.doubleSpinBox_resolution_3)
                        
        self.conformite(self.comboBox_EMT_3, self.lineEdit_correction_3, self.lineEdit_incertitude_3, self.lineEdit_conformite_3, self.doubleSpinBox_resolution_3)

    
    @pyqtSlot(str)
    def on_comboBox_EMT_2_activated(self, p0):
        """
        si changement EMT on recalcul tout
        """
        self.calculs(self.tableWidget_2, self.lineEdit_moyenne_etalon_2, self.lineEdit_moyenne_afficheur_2, 
                        self.lineEdit_correction_2, self.lineEdit_ecartype_2, self.lineEdit_incertitude_2, 
                        self.doubleSpinBox_resolution_2)
                        
        self.conformite(self.comboBox_EMT_2, self.lineEdit_correction_2, self.lineEdit_incertitude_2, self.lineEdit_conformite_2, self.doubleSpinBox_resolution_2)
   
    @pyqtSlot(str)
    def on_comboBox_EMT_activated(self, p0):
        """
        si changement EMT on recalcul tout
        """
        # TODO: not implemented yet
        self.calculs(self.tableWidget, self.lineEdit_moyenne_etalon, self.lineEdit_moyenne_afficheur, 
                            self.lineEdit_correction, self.lineEdit_ecartype, self.lineEdit_incertitude, 
                            self.doubleSpinBox_resolution)
                            
        self.conformite(self.comboBox_EMT, self.lineEdit_correction, self.lineEdit_incertitude, self.lineEdit_conformite, self.doubleSpinBox_resolution)
    
