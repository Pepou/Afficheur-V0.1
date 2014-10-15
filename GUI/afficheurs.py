# -*- coding: utf-8 -*-

"""
Module implementing Afficheurs.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow

from .Ui_afficheurs import Ui_MainWindow
from Package.AccesBdd import AccesBdd

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
        
        self.db = AccesBdd(login, password)
        list_cmr = self.db.recensement_cmr()
        #insertion combobox
        self.comboBox_cmr.addItems(list_cmr)

        
        #configuration largeur colonnes tablewidget
        self.tableWidget.setColumnWidth(0,600)
        self.tableWidget.setColumnWidth(1,600)
        
        self.tableWidget_2.setColumnWidth(0,600)
        self.tableWidget_2.setColumnWidth(1,600)
        
        self.tableWidget_3.setColumnWidth(0,600)
        self.tableWidget_3.setColumnWidth(1,600)

    
    @pyqtSlot(str)
    def on_comboBox_famille_afficheur_activated(self, p0):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        nom_cmr = self.comboBox_cmr.currentText().split() #list avec nom et prenom
        print(nom_cmr)
        type_afficheur = self.comboBox_famille_afficheur.currentText()
        service_site = self.db.recuperation_site_service_cmr(nom_cmr[0], nom_cmr[1])
        print(service_site)
        afficheurs = self.db.recensement_afficheurs(type_afficheur, "HLA", "ANG")
        print(afficheurs)
