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
        
        
#        for 
        
    def __del__(self):
        self.connection.close()
        
    def recensement_afficheurs(self, type_afficheur, service, site):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = table.select().where(and_(table.c.DESIGNATION == type_afficheur, table.c.SITE == site))#, table.c.AFFECTATION == service))

        result = self.connection.execute(ins)
        
        identification_afficheurs = []
        for ele in result:
          identification_afficheurs.append(ele[1])
          
        return  identification_afficheurs
        
    def recensement_etalons(self, type_afficheur, service, site, designation_etalon):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = table.select().where(and_(table.c.DOMAINE_MESURE == type_afficheur, table.c.SITE == site, table.c.DESIGNATION == designation_etalon))#, table.c.AFFECTATION == service))

        result = self.connection.execute(ins)
        
        identification_etalon = []
        for ele in result:
          identification_etalon.append(ele[1])
          
        return  identification_etalon
        
    def n_serie_afficheur(self, identification):
        '''fct qui recupere un n° serie en fct identification affcheur'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.N_SERIE]).where(table .c.IDENTIFICATION == identification)
        result = self.connection.execute(ins)    
        
        for ele in result:
            n_serie = ele[0]
        return n_serie
        
        
    def recensement_cmr(self):
        '''fct pour rapatrier le nom+prenom cmr dela table CORRESPONDANTS'''
        table = Table("CORRESPONDANTS", self.meta)
        ins = table.select().order_by(table.c.ID_CMR)
        result = self.connection.execute(ins)
        
        cmr = []
        for ele in result:
            cmr.append(ele[1] + " "+ele[2])

        return cmr
    def recuperation_site_service_cmr(self, nom, prenom):
        '''fct pour recupere le site et le service du cmr'''
        
        table = Table("CORRESPONDANTS", self.meta)
        ins = select([table.c.SITE, table.c.SERVICE]).where(and_(table.c.NOM == nom, table.c.PRENOM == prenom))

        result = self.connection.execute(ins)
         
        for ele in result:
            service_site = ele
        return service_site
        
#    def insert_table_polynome(self,  donnees):
#        '''fct qui insert le poly dans la base '''
#        
#        table = Table("POLYNOME_CORRECTION", self.meta)
#        ins = table.insert(returning=[table.c.ID_POLYNOME])
#        result = self.connection.execute(ins, donnees)
#
#        id = []
#        for ele in result:            
#            id = ele          
#        return id
        
#    def insert_polynome_table_etalonnage(self,  donnees):
#        '''fct qui insert les donnees de construction du poly dans la base '''
#
#        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
#        ins = table.insert()
#        self.connection.execute(ins, donnees)
#
#
#    def recuperation_donnees_table_polynome_table_etalonnage(self, id_poly):
#        '''fct pour recuperer les donnnees dans la table polynome-table-etal'''
#        
#        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
#        ins = select([table.c.MOYENNE_ETALON_CORRI, table.c.MOYENNE_INSTRUM, table.c.CORRECTION, table.c.INCERTITUDE]).where(table.c.ID_POLYNOME == id_poly).order_by(table.c.ID_POLY_TABLE_ETAL)
#        result = self.connection.execute(ins)
#        
#        donnees_poly_table_etal = []        
#        for ele in result:   
#            donnees_poly_table_etal.append(ele) 
#        
#        return donnees_poly_table_etal
#        
#    def delete_table_polynome_table_etalonnage(self, id_poly):
#        '''efface les lignes de la table polynome_donnees_etal'''
#        table = Table("POLYNOME_TABLE_ETALONNAGE", self.meta)
#        ins = table.delete(table.c.ID_POLYNOME == id_poly)
#        self.connection.execute(ins)
        
    def recuperation_polynomes_etal(self, identification):
        '''fct qui va recuperer dans la table polynome corrections
        les differents poly ainsi que leurs caracteristiques'''
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.NUM_CERTIFICAT, table.c.DATE_ETAL, table.c.ORDRE_POLY,\
                        table.c.COEFF_A, table.c.COEFF_B, table.c.COEFF_C, table.c.ARCHIVAGE])\
                        .where(table.c.IDENTIFICATION == identification).order_by(table.c.NUM_CERTIFICAT)
        result = self.connection.execute(ins)
        
        donnees_poly_table_etal = []        
        for ele in result:   
            donnees_poly_table_etal.append(ele) 
        
        return donnees_poly_table_etal
        
    def recuperation_polynome_etal_num_ce(self, num_ce):
        '''fct qui va recuperer dans la table polynome corrections
        les differents poly ainsi que leurs caracteristiques'''
        
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.NUM_CERTIFICAT, table.c.DATE_ETAL, table.c.ORDRE_POLY,\
                        table.c.COEFF_A, table.c.COEFF_B, table.c.COEFF_C, table.c.ARCHIVAGE])\
                        .where(table.c.NUM_CERTIFICAT == num_ce).order_by(table.c.NUM_CERTIFICAT)
        result = self.connection.execute(ins)
        
        donnees_poly_table_etal = []        
        for ele in result:   
            donnees_poly_table_etal.append(ele) 
        
        return donnees_poly_table_etal
        
    def incertitude_etalonnage_temperature(self, identification_etalon, numero_ce):
        '''fct permettant de recupere l'incertitude max d'etalonnage'''
        
        table = Table("ETALONNAGE_RESULTAT", self.meta)
        ins = select([table.c.U]).where(and_(table.c.CODE_INSTRUM == identification_etalon, table.c.NUM_ETAL == numero_ce))
        result = self.connection.execute(ins)
        
        U_etalonnage_etalon =[]
        for ele in result:
            U_etalonnage_etalon.append(ele)
                       
        return U_etalonnage_etalon
        
    def recuperation_corrections_etalonnage_temp(self, identification_etalon, numero_ce):
        '''fct permettant de recuêrer les donnees d'etalonnage (correction...) 
        afin de calculer une incertitude de modelisation'''
        
        table = Table("ETALONNAGE_RESULTAT", self.meta)
        ins = select([table.c.MOYENNE_INSTRUM, table.c.MOYENNE_CORRECTION]).where(and_(table.c.CODE_INSTRUM == identification_etalon, table.c.NUM_ETAL == numero_ce))
        result = self.connection.execute(ins)
        
        table_etal_tlue_correction = []
        for ele in result:
            table_etal_tlue_correction.append(ele)
        
        return table_etal_tlue_correction
        
    def recuperation_resolution_etalon(self, identification_etalon):
        '''fct pour aller cherche la resolution table instrument'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.RESOLUTION]).where(table.c.IDENTIFICATION == identification_etalon)
        result = self.connection.execute(ins)
        
        
        for ele in result:
            resolution = ele[0]
        
        return resolution
