#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine


class AccesBdd():
    '''class gerant la bdd'''
    
    def __init__(self, login, password):
        self.namebdd = "Labo_Metro_Test"#"Labo_Metro_Prod"
        self.adressebdd = "localhost" # "10.42.1.74"   #"localhost"            
        self.portbdd = "5432"
        self.login = login
        self.password = password
           
            #création de l'"engine"
        self.engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(self.login, self.password, self.adressebdd, self.portbdd, self.namebdd)) 
        self.meta = MetaData()        
        self.meta.reflect(bind=self.engine)
        self.polynome_correction = Table('POLYNOME_CORRECTION', self.meta)
        self.connection = self.engine.connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session.configure(bind=self.engine)
        
        
    def __del__(self):
        self.connection.close()
        
    def recensement_afficheurs(self, type_afficheur):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        table = Table("INSTRUMENTS", self.meta)
        ins = table.select(table.c.DESIGNATION == type_afficheur)
        result = self.connection.execute(ins)

        caracteristiques_afficheurs = []
        identification_afficheurs = []
        for ele in result:
          caracteristiques_afficheurs.append(ele)
          identification_afficheurs.append(ele[1])
            
        print (ele)
        
            
        return caracteristiques_afficheurs, identification_afficheurs
        
   
    def insert_table_polynome(self,  donnees):
        '''fct qui insert le poly dans la base '''
        
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = table.insert(returning=[table.c.ID_POLYNOME])
        result = self.connection.execute(ins, donnees)

        id = []
        for ele in result:            
            id = ele          
        return id
        
    def insert_polynome_table_etalonnage(self,  donnees):
        '''fct qui insert les donnees de construction du poly dans la base '''

        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = table.insert()
        self.connection.execute(ins, donnees)


    def recuperation_donnees_table_polynome_table_etalonnage(self, id_poly):
        '''fct pour recuperer les donnnees dans la table polynome-table-etal'''
        
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = select([table.c.MOYENNE_ETALON_CORRI, table.c.MOYENNE_INSTRUM, table.c.CORRECTION, table.c.INCERTITUDE]).where(table.c.ID_POLYNOME == id_poly).order_by(table.c.ID_POLY_TABLE_ETAL)
        result = self.connection.execute(ins)
        
        donnees_poly_table_etal = []        
        for ele in result:   
            donnees_poly_table_etal.append(ele) 
        
        return donnees_poly_table_etal
        
    def delete_table_polynome_table_etalonnage(self, id_poly):
        '''efface les lignes de la table polynome_donnees_etal'''
        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
        ins = table.delete(table.c.ID_POLYNOME == id_poly)
        self.connection.execute(ins)
        
