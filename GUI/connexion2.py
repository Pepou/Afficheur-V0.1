# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QMessageBox
from GUI.afficheurs import Afficheurs
from GUI.Ui_connexion2 import Ui_MainWindow


class Connexion(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_buttonBox_2_accepted(self):
        """
        Connexion à la base
        """
        # acces à la BDD
#        try:
        login = self.login.text()
        password = self.password.text()

        self.close()
        self.afficheurs = Afficheurs(login, password)
        self.afficheurs.showMaximized()
        self.close()            
        
        return login, password
#        except:
#            QMessageBox.information(self, 
#                ("Erreur connexion "), 
#                ("Erreur sur le login et/ou mot de passe")) 
#            self.show()
#        

    
    @pyqtSlot()
    def on_buttonBox_2_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.close()
