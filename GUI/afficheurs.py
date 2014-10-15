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

        
        #configuration largeur colonnes tablewidget
        self.tableWidget.setColumnWidth(0,600)
        self.tableWidget.setColumnWidth(1,600)
        
        self.tableWidget_2.setColumnWidth(0,600)
        self.tableWidget_2.setColumnWidth(1,600)
        
        self.tableWidget_3.setColumnWidth(0,600)
        self.tableWidget_3.setColumnWidth(1,600)
    
    @pyqtSlot()
    def on_radioButton_temperature_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.db.recensement_afficheurs("Afficheur de température")
    
    @pyqtSlot()
    def on_radioButton_vitesse_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_radioButton_temps_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
