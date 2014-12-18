#-*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import create_engine
import numpy as np

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
        
    def recensement_etalons_vitesse(self, designation_etalon):
        '''fct pour avoir l'ensemble des afficheurs du type : afficheur_type'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = table.select().where(table.c.DESIGNATION == designation_etalon)

        result = self.connection.execute(ins)
        
        identification_etalon = []
        for ele in result:
          identification_etalon.append(ele[1])
          
        return  identification_etalon
        
    def caract_afficheur(self, identification):
        '''fct qui recupere un n° serie , constructeur , type, en fct identification affcheur'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.N_SERIE, table.c.CONSTRUCTEUR, table.c.TYPE, table.c.COMMENTAIRE]).where(table .c.IDENTIFICATION == identification)
        result = self.connection.execute(ins)    
        
        for ele in result:
            n_serie = ele[0]
            constructeur = ele[1]
            type = ele[2]
            commentaire = ele[3]
            
        return n_serie, constructeur, type, commentaire
        
        
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
    
    def recuperation_code_client_affectation(self, identification):
        '''fct qui recupere le code du client et affectation de l'instrument en fct de l'identification afficheur'''
        
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.CODE, table.c.AFFECTATION]).where(table .c.IDENTIFICATION == identification)
        result = self.connection.execute(ins)    
        
        for ele in result:
            code_client = ele[0]
            affectation = ele[1]
            
        table = Table("CLIENTS", self.meta)
        ins = select([table.c.SOCIETE, table.c.ADRESSE, table.c.CODE_POSTAL, table.c.VILLE]).where(table .c.CODE_CLIENT == code_client)
        result = self.connection.execute(ins)      
        
        for ele in result:
            societe = ele[0]
            adresse = ele[1]
            code_postal = ele[2]
            ville = ele[3]
            
        return societe, affectation, adresse, code_postal, ville
    
    
    def sauvegarde_table_afficheur_ctrl_admin(self, afficheur):
        '''fct qui sauvegarde dans la table afficheur controle admin'''
        donnees = {}
        #recuperation id instrument*
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM]).where(table .c.IDENTIFICATION == afficheur["identification_instrument"])
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_instrum = ele[0]
                
        #recuperation id cmr
        cmr = afficheur["operateur"].split()
        table = Table("CORRESPONDANTS", self.meta)
        ins = select([table.c.ID_CMR]).where(and_(table .c.NOM == cmr[0], table.c.PRENOM == cmr[1]))
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_cmr = ele[0]
        
        #insertion dans table afficheur_controle admin
        donnees["DATE_CONTROLE"] = afficheur["date_etalonnage"]
        donnees["IDENTIFICATION"] = id_instrum
        donnees["NOM_PROCEDURE"] = "PDL/PIL/SUR/MET/MO" + afficheur["n_mode_operatoire"]
        donnees["NBR_PT"] = afficheur["nbr_pt_etalonnage"]
        donnees["TECHNICIEN"] = id_cmr
        donnees["ARCHIVAGE"] = False
        
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = table.insert(returning=[table.c.ID_AFFICHEUR_ADMINISTRATIF])
        result = self.connection.execute(ins, donnees)
        id = []
        for ele in result:            
            id = ele 
        
        #construction numero doc
        if afficheur["designation"] == "Sonde alarme température":
            prefix = "SAT"
        elif afficheur["designation"] == "Afficheur de température":
            prefix = "AFT"
        elif afficheur["designation"] == "Afficheur de temps":
            prefix = "AFM"
        elif afficheur["designation"] == "Afficheur de vitesse":
            prefix = "AFV"         
        
        num_doc = prefix + afficheur["num_doc_provisoire"]+"_"+ str(id[0])
        
        table = Table("AFFICHEUR_CONTROLE_ADMINISTRATIF", self.meta)
        ins = table.update().where(table.c.ID_AFFICHEUR_ADMINISTRATIF == id[0]).values(NUM_DOC = num_doc)
        result = self.connection.execute(ins, donnees)
        
        
        n_ce = afficheur["ce_etalon"].split()   #permet de recuperer juste le n°ce etalon sinon n°CE etalon +la date
        
        #gestion insertion bdd table AFFICHEUR_CONTROLE_RESULTAT
            # recuperation id etalon
            #recuperation id instrument*
        table = Table("INSTRUMENTS", self.meta)
        ins = select([table.c.ID_INSTRUM]).where(table .c.IDENTIFICATION == afficheur["etalon"])
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_etalon = ele[0]
            
        list_table_aff_result = []       
        for i in range(0, donnees["NBR_PT"]):
            dict_table_aff_result = {}
            dict_table_aff_result["ID_AFF_CTRL_ADMIN"] = id[0]
            dict_table_aff_result["NBR_PT_CTRL"] = donnees["NBR_PT"]
            dict_table_aff_result["N_PT_CTRL"] = i +1
            dict_table_aff_result["ID_ETALON"] = id_etalon
            dict_table_aff_result["CE_ETALON"] = n_ce[0]
            dict_table_aff_result["RESOLUTION"] =  afficheur["resolution"][i]
            dict_table_aff_result["MOYENNE_ETALON_NC"] =  np.mean(afficheur["valeurs_etalon_nc"][i])
            dict_table_aff_result["MOYENNE_ETALON_C"] = afficheur["moyenne_etalon_corri"][i]
            dict_table_aff_result["MOYENNE_AFFICHEUR"] = afficheur["moyenne_instrum"][i]
            dict_table_aff_result["MOYENNE_CORRECTION"] = afficheur["moyenne_correction"][i]
            dict_table_aff_result["U"] =  afficheur["U"][i]
            dict_table_aff_result["CONFORMITE"] =  afficheur["conformite"] [i]
            dict_table_aff_result["ARCHIVAGE"] = False
            dict_table_aff_result["EMT"] =  afficheur["emt"][i]
            
            list_table_aff_result.append(dict_table_aff_result)

        #insertion table resultat
        table = Table("AFFICHEUR_CONTROLE_RESULTAT", self.meta)
        ins = table.insert()
        result = self.connection.execute(ins, list_table_aff_result)

        #○recherche id polynome
            
        table = Table("POLYNOME_CORRECTION", self.meta)
        ins = select([table.c.ID_POLYNOME]).where(table .c.NUM_CERTIFICAT == n_ce[0])
        result = self.connection.execute(ins)    
        
        for ele in result:
            id_poly = ele[0]
        
        
        
        list_mesures = []
        for i in range(0, donnees["NBR_PT"]):           
            for j in range(0, len(afficheur["valeurs_etalon_nc"][i])):
                dict_table_mesures = {}
                
                dict_table_mesures["ID_AFF_CTRL_ADMIN"] = id[0]
                dict_table_mesures["ID_ETALON"] = id_etalon
                dict_table_mesures["ID_POLYNOME"] = id_poly
                dict_table_mesures["ETALON_NC"] = afficheur["valeurs_etalon_nc"][i][j]
                dict_table_mesures["ETALON_C"] = afficheur["valeurs_etalon_c"][i][j]
                dict_table_mesures["AFFICHEUR"] = afficheur["valeurs_afficheur"][i][j]
                dict_table_mesures["NBR_PTS"] = donnees["NBR_PT"]
                dict_table_mesures["N_PT"] = i + 1
                dict_table_mesures["NBR_MESURE"] = len(afficheur["valeurs_etalon_nc"][i])
                dict_table_mesures["N_MESURE"] = j+1
                list_mesures.append(dict_table_mesures)

        #insertion table resultat
        table = Table("AFFICHEUR_CONTROLE_MESURES", self.meta)
        ins = table.insert()
        result = self.connection.execute(ins, list_mesures)
        
        
        return num_doc
        
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
