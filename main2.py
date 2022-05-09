from matplotlib.pyplot import title
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_js
from pywebio import start_server, config, platform

from cutecharts.charts import Bar
from cutecharts.faker import Faker

import plotly.express as px

import pandas as pd

from pymongo import MongoClient
import math
import flask

import time
from datetime import date,timedelta,datetime
import datetime

from dateutil.relativedelta import relativedelta

from time import strptime
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import time

from urllib.request import urlopen
import json

from dateutil.relativedelta import relativedelta

import numpy as np
import numpy_financial
from numpy_financial import pmt, ppmt, ipmt
import plotly.graph_objects as go

from dateutil.relativedelta import *
from dateutil.rrule import *
from dateutil.rrule import rrule, YEARLY

from tkinter import *
from tkcalendar import Calendar

from fpdf import FPDF, HTMLMixin
from dateutil import relativedelta

import numpy_financial as npf

import requests
from bs4 import BeautifulSoup

from math import *


def imposition1(rv, qf, taux, coef):
    """ Imposition simple
     :param rv: revenu
     :param qf: quotient familial
     :param taux: taux
     :param coef: coefficient
     :return: l’imposition simple
    """
    return (rv * taux - coef)


CELIBATAIRE = "Celibataire"
CONCUBINAGE = "Concubinage"
MARIE = "Marié"
NEUF = 'n'
ANCIEN = "a"


# def saisirStatutFamilial():
#     """ Calcul du quotient familial
#      :param npers: nombre de personnes a charge
#      :param vinitiale: valeur initiale (1 ou 2)
#      :param incr1pers: increment pour 1 personne (1 ou 0.5)
#      :return: le quotient familial
#     """
#     statut = "."
#     rep = input("Etes vous Marié ou Pacsé (o/n)")[0]
#     if rep == "n" or rep == "N":
#         statut = CELIBATAIRE
#     else:
#         rep = input("Vivez-vous en concubinage (o/n)?")[0]
#         statut = (CONCUBINAGE if rep == "o" or rep=="O" else CELIBATAIRE)
#     return statut

class MyFPDF(FPDF, HTMLMixin):
    pass


def QFcalcul(npers, vinitiale, incr1pers): 
    rs = vinitiale 
    if npers >= 1:
        rs += incr1pers 
    if npers >= 2:
        rs += 0.5 + (npers - 2) 
    return rs

def quotientFamilial(statut, npers): 
    """ Quotient familial
    :param statut: statut familial parmi une des constantes
    :param npers: nombre de personnes à charge >= 0
    :return: le quotient familial
    """
    rs = 0.0
    if statut == CELIBATAIRE:
        rs = QFcalcul(npers, 1.0, 1.0)
    elif statut == CONCUBINAGE:
        rs = QFcalcul(npers, 1.0, 0.5) 
    elif statut == MARIE:
        rs = QFcalcul(npers, 2.0, 0.5) 
    return rs

def afficherFicheImpots(rv, statut, npers,TMI,impots):
    """  Affichage d’une fiche d’impot
     :param rv: revenu
     :param statut: statut familial
     :param npers: nombre de personnes à charge
    """
    #print("==> Nombre de personnes a charge : ", npers, sep="") # quotient familial
    qf = quotientFamilial(statut, npers)
    put_text("REVENUS ET COMPOSITION DU FOYER").style('color: dark; font-size: 20px; font-weight:bold;')
    put_table([
            ["Nombre de parts","Revenu imposable","Votre impot sur le revenu","TMI"],
            [float("{:.2f}".format(qf)),float("{:.2f}".format(rv)),float("{:.2f}".format(impots)),float("{:.2f}".format(TMI))]
        ])

def saisirStatutFamilial():
    """ Calcul du quotient familial
     :param npers: nombre de personnes a charge
     :param vinitiale: valeur initiale (1 ou 2)
     :param incr1pers: increment pour 1 personne (1 ou 0.5)
     :return: le quotient familial
    """
    statut = "."
    rep = input("Etes vous marié (o/n)")[0]
    if rep == "o" or rep == "O":
        statut = MARIE
    else:
        rep = input("Vivez-vous en concubinage (o/n)?")[0]
        statut = (CONCUBINAGE if rep == "o" or rep=="O" else CELIBATAIRE)
    return statut

def test_impotFinal():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    revenu = float(input("Quel est le revenu net annuel du foyer : "))
    revenu2 = 0.9*revenu
    if revenu2 > 126520:
        revenuAvantAbbatement = revenu - 12652
    else :
        revenuAvantAbbatement = 0.9*revenu
    statut = saisirStatutFamilial()
    npers = int(input("Nombre de personnes a charge? "))
    ##########CONCUBINAGE
    if statut == CONCUBINAGE:
        if quotientFamilial(statut, npers) ==1:
            if revenuAvantAbbatement < 10225:
                impots = 0
                TMI = 0
            if 10225 < revenuAvantAbbatement <= 26070:
                impots = (revenuAvantAbbatement*0.11)-1124.75
                TMI = 11
            if 26070 < revenuAvantAbbatement <= 74545:
                impots = (revenuAvantAbbatement*0.3)-6078.05
                TMI = 30
            if 74545 < revenuAvantAbbatement <= 160336:
                impots = (revenuAvantAbbatement*0.41)-14278
                TMI = 41
            if revenuAvantAbbatement > 160336:
                impots = (revenuAvantAbbatement*0.45)-20691.44
                TMI = 45
            
        if quotientFamilial(statut, npers) ==1.5:
            if revenuAvantAbbatement < 15338:
                impots = 0
                TMI = 0
            if 15338 < revenuAvantAbbatement <= 31491:
                impots = (revenuAvantAbbatement*0.11)-1687.13
                TMI = 11
            if 31492 < revenuAvantAbbatement <= 74545:
                impots = (revenuAvantAbbatement*0.3)-7670.05
                TMI = 30
            if 74545 < revenuAvantAbbatement <= 160336:
                impots = (revenuAvantAbbatement*0.41)-15870
                TMI = 41
            if revenuAvantAbbatement > 160336:
                impots = (revenuAvantAbbatement*0.45)-22283.44
                TMI = 45
            
        if quotientFamilial(statut, npers) ==2:
            if revenuAvantAbbatement < 20450:
                impots = 0
                TMI = 0
            if 20450 < revenuAvantAbbatement <= 36908:
                impots = (revenuAvantAbbatement*0.11)-2249.5
                TMI = 11
            if 36909 < revenuAvantAbbatement <= 74545:
                impots = (revenuAvantAbbatement*0.3)-9262.05
                TMI = 30
            if 74545 < revenuAvantAbbatement <= 160336:
                impots = (revenuAvantAbbatement*0.41)-17462
                TMI = 41
            if revenuAvantAbbatement > 160336:
                impots = (revenuAvantAbbatement*0.45)-23875.44
                TMI = 45
            
        if quotientFamilial(statut, npers) ==3:
            if revenuAvantAbbatement < 30675:
                impots = 0
                TMI = 0
            if 30675 < revenuAvantAbbatement <= 47748:
                impots = (revenuAvantAbbatement*0.11)-3374.25
                TMI = 11
            if 47749 < revenuAvantAbbatement <= 74545:
                impots = (revenuAvantAbbatement*0.3)-12446.05
                TMI = 30
            if 74545 < revenuAvantAbbatement <= 160336:
                impots = (revenuAvantAbbatement*0.41)-20646
                TMI = 41
            if revenuAvantAbbatement > 160336:
                impots = (revenuAvantAbbatement*0.45)-27059.44
                TMI = 45
            
        if quotientFamilial(statut, npers) ==4:
            if revenuAvantAbbatement < 40900:
                impots = 0
                TMI = 0
            if 40900 < revenuAvantAbbatement <= 58585:
                impots = (revenuAvantAbbatement*0.11)-4499
                TMI = 11
            if 58586 < revenuAvantAbbatement <= 74545:
                impots = (revenuAvantAbbatement*0.3)-15630.05
                TMI = 30
            if 74545 < revenuAvantAbbatement <= 160336:
                impots = (revenuAvantAbbatement*0.41)-23830
                TMI = 41
            if revenuAvantAbbatement > 160336:
                impots = (revenuAvantAbbatement*0.45)-30243.44
                TMI = 45
    ###########CELIBATAIRE
    if statut == CELIBATAIRE:
        if quotientFamilial(statut, npers) ==1:
            if revenuAvantAbbatement < 10225:
                impots = 0
                TMI = 0
            if 10225 < revenuAvantAbbatement <= 26070:
                impots = (revenuAvantAbbatement*0.11)-1124.75
                TMI = 11
            if 26070 < revenuAvantAbbatement <= 74545:
                impots = (revenuAvantAbbatement*0.3)-6078.05
                TMI = 30
            if 74545 < revenuAvantAbbatement <= 160336:
                impots = (revenuAvantAbbatement*0.41)-14278
                TMI = 41
            if revenuAvantAbbatement > 160336:
                impots = (revenuAvantAbbatement*0.45)-20691.44
                TMI = 45
            
        if quotientFamilial(statut, npers) ==1.5:
            if revenuAvantAbbatement < 15338:
                impots = 0
                TMI = 0
            if 15338 < revenuAvantAbbatement <= 31491:
                impots = (revenuAvantAbbatement*0.11)-1687.13
                TMI = 11
            if 31492 < revenuAvantAbbatement <= 74545:
                impots = (revenuAvantAbbatement*0.3)-7670.05
                TMI = 30
            if 74545 < revenuAvantAbbatement <= 160336:
                impots = (revenuAvantAbbatement*0.41)-15870
                TMI = 41
            if revenuAvantAbbatement > 160336:
                impots = (revenuAvantAbbatement*0.45)-22283.44
                TMI = 45
            
        if quotientFamilial(statut, npers) ==2:
            if revenuAvantAbbatement < 20450:
                impots = 0
                TMI = 0
            if 20450 < revenuAvantAbbatement <= 36908:
                impots = (revenuAvantAbbatement*0.11)-2249.5
                TMI = 11
            if 36909 < revenuAvantAbbatement <= 74545:
                impots = (revenuAvantAbbatement*0.3)-9262.05
                TMI = 30
            if 74545 < revenuAvantAbbatement <= 160336:
                impots = (revenuAvantAbbatement*0.41)-17462
                TMI = 41
            if revenuAvantAbbatement > 160336:
                impots = (revenuAvantAbbatement*0.45)-23875.44
                TMI = 45
            
        if quotientFamilial(statut, npers) ==3:
            if revenuAvantAbbatement < 30675:
                impots = 0
                TMI = 0
            if 30675 < revenuAvantAbbatement <= 47748:
                impots = (revenuAvantAbbatement*0.11)-3374.25
                TMI = 11
            if 47749 < revenuAvantAbbatement <= 74545:
                impots = (revenuAvantAbbatement*0.3)-12446.05
                TMI = 30
            if 74545 < revenuAvantAbbatement <= 160336:
                impots = (revenuAvantAbbatement*0.41)-20646
                TMI = 41
            if revenuAvantAbbatement > 160336:
                impots = (revenuAvantAbbatement*0.45)-27059.44
                TMI = 45
            
        if quotientFamilial(statut, npers) ==4:
            if revenuAvantAbbatement < 40900:
                impots = 0
                TMI = 0
            if 40900 < revenuAvantAbbatement <= 58585:
                impots = (revenuAvantAbbatement*0.11)-4499
                TMI = 11
            if 58586 < revenuAvantAbbatement <= 74545:
                impots = (revenuAvantAbbatement*0.3)-15630.05
                TMI = 30
            if 74545 < revenuAvantAbbatement <= 160336:
                impots = (revenuAvantAbbatement*0.41)-23830
                TMI = 41
            if revenuAvantAbbatement > 160336:
                impots = (revenuAvantAbbatement*0.45)-30243.44
                TMI = 45
            
    ############MARIE
    if statut == MARIE:
        if quotientFamilial(statut, npers) ==2:
            if revenuAvantAbbatement < 20450:
                impots = 0
                TMI = 0
            if 20450 < revenuAvantAbbatement <= 52140:
                impots = (revenuAvantAbbatement*0.11)-2249.50
                TMI = 11
            if 52140 < revenuAvantAbbatement <= 149090:
                impots = (revenuAvantAbbatement*0.3)-12156.1
                TMI = 30
            if 149090 < revenuAvantAbbatement <= 320672:
                impots = (revenuAvantAbbatement*0.41)-28556
                TMI = 41
            if revenuAvantAbbatement > 320672:
                impots = (revenuAvantAbbatement*0.45)-41382.88
                TMI = 45
            
        if quotientFamilial(statut, npers) ==2.5:
            if revenuAvantAbbatement < 25563:
                impots = 0
                TMI = 0
            if 25563 < revenuAvantAbbatement <= 57561:
                impots = (revenuAvantAbbatement*0.11)-2811.88
                TMI = 11
            if 57562 < revenuAvantAbbatement <= 149090:
                impots = (revenuAvantAbbatement*0.3)-13748.10
                TMI = 30
            if 149090 < revenuAvantAbbatement <= 320672:
                impots = (revenuAvantAbbatement*0.41)-30148
                TMI = 41
            if revenuAvantAbbatement > 320672:
                impots = (revenuAvantAbbatement*0.45)-42974.88
                TMI = 45
            
        if quotientFamilial(statut, npers) ==3:
            if revenuAvantAbbatement < 30675:
                impots = 0
                TMI = 0
            if 30675 < revenuAvantAbbatement <= 62978:
                impots = (revenuAvantAbbatement*0.11)-3374.25
                TMI = 11
            if 62979 < revenuAvantAbbatement <= 149090:
                impots = (revenuAvantAbbatement*0.3)-15340.1
                TMI = 30
            if 149090 < revenuAvantAbbatement <= 320672:
                impots = (revenuAvantAbbatement*0.41)-31740
                TMI = 41
            if revenuAvantAbbatement > 320672:
                impots = (revenuAvantAbbatement*0.45)-44566.88
                TMI = 45
            
        if quotientFamilial(statut, npers) ==4:
            if revenuAvantAbbatement < 40900:
                impots = 0
                TMI = 0
            if 40900 < revenuAvantAbbatement <= 73818:
                impots = (revenuAvantAbbatement*0.11)-4499
                TMI = 11
            if 73819 < revenuAvantAbbatement <= 149090:
                impots = (revenuAvantAbbatement*0.3)-18524.10
                TMI = 30
            if 149090 < revenuAvantAbbatement <= 320672:
                impots = (revenuAvantAbbatement*0.41)-34924
                TMI = 41
            if revenuAvantAbbatement > 320672:
                impots = (revenuAvantAbbatement*0.45)-47750.88
                TMI = 45
            
        if quotientFamilial(statut, npers) ==5:
            if revenuAvantAbbatement < 51125:
                impots = 0
                TMI = 0
            if 51125 < revenuAvantAbbatement <= 84655:
                impots = (revenuAvantAbbatement*0.11)-5623.75
                TMI = 11
            if 84656 < revenuAvantAbbatement <= 149090:
                impots = (revenuAvantAbbatement*0.3)-21708.1
                TMI = 30
            if 149090 < revenuAvantAbbatement <= 320672:
                impots = (revenuAvantAbbatement*0.41)-38108
                TMI = 41
            if revenuAvantAbbatement > 320672:
                impots = (revenuAvantAbbatement*0.45)-50934.88
                TMI = 45
            
        if quotientFamilial(statut, npers) ==6:
            if revenuAvantAbbatement < 61350:
                impots = 0
                TMI = 0
            if 61350 < revenuAvantAbbatement <= 94495:
                impots = (revenuAvantAbbatement*0.11)-6748.5
                TMI = 11
            if 94496 < revenuAvantAbbatement <= 149090:
                impots = (revenuAvantAbbatement*0.3)-24892.1
                TMI = 30
            if 149090 < revenuAvantAbbatement <= 320672:
                impots = (revenuAvantAbbatement*0.41)-40292
                TMI = 41
            if revenuAvantAbbatement > 320672:
                impots = (revenuAvantAbbatement*0.45)-54118.88
                TMI = 45

    afficherFicheImpots(revenuAvantAbbatement, statut, npers,TMI,impots)


def CalculerMensualité():
    #put_buttons([
    #    dict(label=i, value=i, color=i)
    #    for i in ['Retour']
    #], onclick=lambda b: run_js('window.location.reload()'), outline=True,color="dark")
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")  
    C = float(input("Capital emprunté en euros : "))
    T = str(input("Taux annuel du crédit en % : "))
    T = T.replace(",",".")
    T = float(T)
    N2 = int(input("Durée en années : "))
    N = N2*12
    ASSU = str(input("Taux d'assurance en % :"))
    ASSU = ASSU.replace(",",".")
    ASSU = float(ASSU)
    t = (T / 12) 
    q = 1 + t / 100 # calcul du coefficient multiplicateur associé à une hausse de t%
    M = (q**N * (C) * (1 - q) / (1 - q**N)) + C*((ASSU/100)/12)
    #print("Votre mensualité sera de {0:.2f} euros".format(M))
    I = N * M - C # calcul des intérêts versés
    #put_text(f"Votre mensulaité sera de {M} euros")
    #put_text(f"Le montant total des intérêts versés sera de {I} euros")
    T2 = T*1/100
    rng = pd.date_range("01-01-2021", periods=N, freq='MS')
    rng.name = "Date"
    df = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
    df.reset_index(inplace=True)
    df.index += 1
    df.index.name = "Periode (Mois)"

    df["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, C)+ C*((ASSU/100)/12)
    df["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12,df.index,N, C)
    df["Intérêts"] = -1 * numpy_financial.ipmt(T2/12,df.index, N, C) 
    df = df.round(2)

    df["Capital restant dû"] = 0
    df.loc[1, "Capital restant dû"] = C - df.loc[1, "Capital Amorti"]

    for period in range(2, len(df)+1):
        previous_balance = df.loc[period-1, "Capital restant dû"]
        principal_paid = df.loc[period, "Capital Amorti"]
        
        if previous_balance == 0:
            df.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] == 0
            continue
        elif principal_paid <= previous_balance:
            df.loc[period, "Capital restant dû"] = previous_balance - principal_paid
    
    df["Date"] = pd.to_datetime(df["Date"],format='%d-%m-%Y')

    put_text("TABLEAU D'AMORTISSEMENT").style('color: dark; font-size: 20px; font-weight:bold;')
    put_collapse('Voir le tableau', [put_html(df.to_html(border = 0))])


    #put_table([
    #    ["Mensualité","Montant total des Intérêts Versés"],
    #    [float("{:.2f}".format(M)),float("{:.2f}".format(I))]
    #])


    

def CapaciteEmprunt():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    M = float(input("Capacité de remboursement mensuelle en euros : "))
    T = str(input("Taux annuel du crédit en % : "))
    T = T.replace(",",".")
    T = float(T)
    N2 = int(input("Durée en années : "))
    N = N2*12
    t = T / 12
    q = 1 + t / 100
    C = M * (1 - q**N) / (q**N * (1 - q))
    #put_text("Votre capacité d'emprunt s'élève à {0:.2f} euros".format(C))
    I = N * M - C
    #put_text("Le montant total des intérêts versés sera de {0:.2f} euros".format(I))
    put_table([
        ["Capacité d'emprunt","Montant total des Intérêts Versés"],
        [float("{:.2f}".format(C)),float("{:.2f}".format(I))]
    ])
    
    

def InvestirNeuf():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    prix2 = float(input("Prix du bien dans le neuf :"))
    prix = float(input("Prix du bien dans l'ancien : "))
    fraisNotaire1 = (7.5*1/100)*prix
    fraisNotaireNeuf = (2.5*1/100)*prix2
    prix3 = prix2 + fraisNotaireNeuf
    #put_text("Votre prix de revient sera de {0:.2f} euros".format(prix3))
    put_table([
        ["Prix de revient"],
        [float("{:.2f}".format(prix3))]
    ])

def InvestirAncien():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    prix2 = float(input("Indiquez le prix de votre appartement dans le neuf :"))
    prix = float(input("Indiquez le prix de votre appartement dans l'ancien : "))
    fraisNotaire1 = (7.5*1/100)*prix
    fraisNotaireNeuf = (2.5*1/100)*prix2
    fraisAgence1 = (4*1/100)*prix
    prix3 = prix2 + fraisNotaireNeuf
    travaux1 = float(input("Indiquez le prix des travaux de rénovation pour votre bien dans l'ancien : "))
    #travauxCopro = float(input("Travaux sur la copropriété sur 10 ans : "))
    impotsNonEconomise = 0.02*(prix2+(fraisNotaireNeuf))*12
    prixTotalAncien = prix + (fraisNotaire1 + fraisAgence1 + travaux1)
    prixAvecImpots = prixTotalAncien + impotsNonEconomise
    prixTotalNeuf = prix3 - impotsNonEconomise
    put_markdown("# ANCIEN")
    put_table([
        ["Prix réel de mon appartement dans l'ancien","Impôt non économisé","Prix réel du bien après impôt"],
        [float("{:.2f}".format(prixTotalAncien)),float("{:.2f}".format(impotsNonEconomise)),float("{:.2f}".format(prixAvecImpots))]
    ])
    put_markdown("# NEUF")
    put_table([
        ["Prix réel de mon appartement dans le neuf","Impôt économisé","Prix réel du bien après impôt"],
        [float("{:.2f}".format(prix3)),float("{:.2f}".format(impotsNonEconomise)),float("{:.2f}".format(prixTotalNeuf))]
    ])

def ChosirZone():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    zoneB1 = ['Toulouse', 'Nantes', 'Strasbourg', 'Bordeaux', 'Rennes', 'Reims', 'Le Havre', 'Grenoble', 'Dijon', 'Nîmes', 'Clermont-Ferrand', 'Limoges', 'Tours', 'Amiens', 'Metz', 'Perpignan', 'Orléans', 'Rouen', 'Mulhouse', 'Caen', 'Nancy', 'Roubaix', 'Tourcoing', 'Avignon', 'La Rochelle', "Villeneuve-d'Ascq", 'Vénissieux', 'Chambéry', 'Pessac', 'Beauvais', 'Arles', 'Annecy', 'Saint-Malo', 'Bayonne', 'Valenciennes', 'Sète', 'Saint-Herblain', 'Bastia', 'Salon-de-Provence', 'Vaulx-en-Velin', 'Douai', 'Talence', 'Caluire-et-Cuire', 'Wattrelos', 'Compiègne', 'Chartres', 'Rezé', 'Anglet', 'Bron', 'Draguignan', "Saint-Martin-d'Hères", 'Joué-lès-Tours', 'Échirolles', 'Villefranche-sur-Saône', 'Colomiers', 'Thonon-les-Bains', 'Lens', 'Creil', 'Schiltigheim', 'Meyzieu', 'Vandoeuvre-lès-Nancy', 'Rillieux-la-Pape', 'Orange', 'Carpentras', "Villenave-d'Ornon", 'Sotteville-lès-Rouen', 'Aix-les-Bains', 'Saint-Médard-en-Jalles', 'Saint-Étienne-du-Rouvray', 'Illkirch-Graffenstaden', 'Bourgoin-Jallieu', 'Biarritz', 'Béthune', 'Tournefeuille', 'Décines-Charpieu', 'Saint-Sébastien-sur-Loire', 'Armentières', 'Cavaillon', 'Lunel', 'Oullins', 'Bègles', 'Orvault', 'La Teste-de-Buch', 'Le Grand-Quevilly', 'Muret', 'Étampes', 'Agde', 'Gradignan', 'Le Bouscat', 'Frontignan', 'Montigny-lès-Metz', 'Blagnac', 'Cenon', 'Le Petit-Quevilly', 'Vertou', 'Sainte-Foy-lès-Lyon', 'Hérouville-Saint-Clair', 'Bois-Guillaume-Bihorel', 'Mons-en-Baroeul', 'Fleury-les-Aubrais', 'Saint-Genis-Laval', 'Lormont', 'Annecy-le-Vieux', 'Halluin', 'Croix', 'Eysines', 'Gujan-Mestras', 'Tassin-la-Demi-Lune', 'Voiron', 'Olivet', 'Saint-Jean-de-Braye', 'Mont-Saint-Aignan', 'Givors', 'Albertville', 'Pertuis', 'Couëron', 'Nogent-sur-Oise', 'Seynod', 'Bouguenais', 'Carquefou', 'Sorgues', 'Villefontaine', 'Meylan', 'Écully', 'Hem', 'Chamalières', 'Ronchin', 'La Chapelle-sur-Erdre', 'Cluses', 'Bischheim', 'Faches-Thumesnil', 'Cran-Gevrier', 'Saint-Fons', 'Elbeuf', 'Bruz', 'Saint-Jean-de-la-Ruelle', 'Lingolsheim', 'Cestas', 'Montereau-Fault-Yonne', 'La Baule-Escoublac', 'Saint-Cyr-sur-Loire', 'Lucé', 'Montivilliers', 'Brignoles', 'Senlis', 'Guérande', 'Plaisance-du-Touch', 'Hendaye', 'Saint-Égrève', 'Sallanches', 'Cugnaux', 'Cesson-Sévigné', 'Saint-Pierre-des-Corps', 'Bruges', 'Saran', 'Canteleu', 'Coulommiers', 'Laxou', 'Saint-Maximin-la-Sainte-Baume', 'Saint-Avertin', 'Villers-lès-Nancy', 'Bailleul', 'Pornic', 'Crépy-en-Valois', 'Olonne-sur-Mer', 'Haubourdin', "Les Sables-d'Olonne", 'Balma', 'Chenôve', "Château-d'Olonne", 'Saint-Gilles', 'Mouvaux', 'Ambarès-et-Lagrave', 'Lys-lez-Lannoy', 'Wattignies', 'Saint-Jean-de-Luz', 'Amboise', 'Canet-en-Roussillon', 'Roncq', 'Woippy', 'Nemours', 'Sainte-Luce-sur-Loire', 'Biscarrosse', 'Montataire', 'Villeneuve-lès-Avignon', 'Comines', 'Provins', 'Ramonville-Saint-Agne', 'Genas', 'Seclin', 'Pont-Sainte-Maxence', 'Seyssinet-Pariset', 'Tarnos', 'Mions', 'Méricourt', 'La Motte-Servolex', 'Gisors', 'Fonsorbes', 'Ostwald', 'Saint-Martin-de-Crau', 'Brignais', 'Ifs', 'Sassenage', 'Saint-Orens-de-Gameville', 'Maromme', 'Oissel', 'Castanet-Tolosan', 'Talant', 'Monteux', 'Obernai', 'Le Pont-de-Claix', 'Arcachon', 'Mèze', 'Hoenheim', 'Saint-Rémy-de-Provence', 'Chambray-lès-Tours', 'Vedène', 'La Roche-sur-Foron', 'Saint-Jacques-de-la-Lande', 'Dinard', 'Villers-Cotterêts', 'Montlouis-sur-Loire', 'Pacé', 'Vidauban', 'Fondettes', 'Pernes-les-Fontaines', 'Corbas', 'Pornichet', 'Mainvilliers', 'Déville-lès-Rouen', 'Saint-Jean', 'Betton', 'Chevigny-Saint-Sauveur', 'Neuville-en-Ferrain', 'Chantepie', 'La Riche', 'Tinqueux', 'Quetigny', 'Dourdan', 'Argelès-sur-Mer', 'Voreppe', 'Marquette-lez-Lille', 'Marly', 'Brumath', 'Pierre-Bénite', 'Craponne', 'Grand-Couronne', 'Bondues', 'Caudebec-lès-Elbeuf', 'La Chapelle-Saint-Mesmin', 'Biganos', 'Eybens', 'Chassieu', 'Pélissanne', 'Saint-Max', 'Wambrechies', 'Maxéville', 'Mondeville', 'Fosses', 'Portet-sur-Garonne', 'Le Luc', 'Le Haillan', 'Louvres', 'Ouistreham', 'Darnétal', 'Léognan', 'Lambesc', 'Le Muy', 'Fontaine-lès-Dijon', 'Leers', 'Feyzin', 'Longvic', 'La Ferté-sous-Jouarre', 'Petit-Couronne', 'Lorgues', 'Le Taillan-Médoc', 'Castelginest', 'Urrugne', "Gonfreville-l'Orcher", 'Miribel', 'Aytré', 'Saint-Laurent-de-la-Salanque', 'Saint-Grégoire', 'Dardilly', 'Villeneuve-Tolosane', 'Léguevin', 'Marguerittes', 'Port-Saint-Louis-du-Rhône', 'Crolles', 'Aigues-Mortes', 'Évian-les-Bains', 'Chécy', 'Le Thor', 'La Ravoire', 'Meythet', 'Lançon-Provence', 'Pibrac', 'Les Angles', 'Saint-Pierre-lès-Elbeuf', "La Chapelle-d'Armentières", 'Irigny', 'Le Grau-du-Roi', 'Basse-Goulaine', 'Capbreton', 'Frouzins', 'Honfleur', 'Vern-sur-Seiche', 'Harfleur', 'Saint-Loubès', 'Linselles', 'Ballan-Miré', 'Nangis', 'Pérenchies', 'Margny-lès-Compiègne', 'Saint-Aubin-lès-Elbeuf', 'Chaponost', 'Elne', 'Vif', 'Aucamville', 'Ingré', 'Entraigues-sur-la-Sorgue', 'Parempuyre', 'Noisy-le-Roi', 'Charvieu-Chavagneux', 'Thouaré-sur-Loire', 'Le Rheu', 'Seysses', 'Boucau', 'Saint-Vincent-de-Tyrosse', 'Vizille', 'Gleizé', 'Morières-lès-Avignon', 'Moirans', 'Borgo', 'Houplines', 'Sainte-Adresse', 'Éguilles', 'Les Sorinières', 'Le Mesnil-Esnard', 'Souffelweyersheim', 'Scionzier', 'Rochefort-du-Gard', 'Nieppe', 'Thorigné-Fouillard', 'Ballancourt-sur-Essonne', 'Trignac', 'Saint-Gilles-Croix-de-Vie', 'Chartres-de-Bretagne', 'Biguglia', 'Mordelles', 'Lagord', 'Launaguet', 'Gaillon', 'La Fare-les-Oliviers', 'Villard-Bonnot', 'Saint-Denis-en-Val', 'Neuville-sur-Saône', 'Artigues-près-Bordeaux', 'Martignas-sur-Jalle', 'Montluel', 'Liancourt', 'Geispolsheim', 'Donges', 'Poisy', 'Montoir-de-Bretagne', 'Sautron', 'Quesnoy-sur-Deûle', 'Luisant', 'Notre-Dame-de-Bondeville', "Saint-Jean-d'Illac", 'Ciboure', 'Seyssins', 'Bassens', 'Bassens', 'Carbon-Blanc', 'Balaruc-les-Bains', 'La Salvetat-Saint-Gilles', 'Le Teich', 'Les Arcs', 'Sérignan', 'Saint-Ismier', 'Huningue', 'Trévoux', 'Saint-Bonnet-de-Mure', 'Le Perray-en-Yvelines', 'Domène', 'Aussonne', 'Itteville', 'La Mulatière', 'La Tronche', 'Champagne-sur-Seine', 'Noyal-Châtillon-sur-Seiche', 'Eckbolsheim', 'La Verpillière', "Saint-Didier-au-Mont-d'Or", 'Bonsecours', 'Pignan', 'Varces-Allières-et-Risset', 'Bétheny', 'Ustaritz', 'Othis', 'Saint-Aubin-de-Médoc', 'Audenge', 'Publier', 'Bidart', 'Les Essarts-le-Roi', 'Lesquin', 'Marignier', 'Anse', 'Fontaines-sur-Saône', 'Baillargues', 'Tignieu-Jameyzieu', 'Acigné', 'Villers-Saint-Paul', 'Bouillargues', 'Gières', 'Escalquens', 'Franqueville-Saint-Pierre', 'Thônes', 'Veigné', 'Marsillargues', 'Jassans-Riottier', 'Bouaye', 'Rives', 'Châtelaillon-Plage', 'Cormontreuil', 'Cognin', 'La Montagne', 'Saint-Pierre-en-Faucigny', 'Malaunay', 'Montauroux', 'Manduel', 'La Wantzenau', 'Mazan', 'Saint-Quentin-Fallavier', 'Le Pian-Médoc', 'Cournonterral', 'Maule', 'Castries', 'Sarrians', 'Cornebarrieu', 'Saint-Alban-Leysse', 'Milhaud', 'Octeville-sur-Mer', 'Lèves', 'Thyez', 'Gigean', 'Nieul-sur-Mer', 'Jonage', 'Longueau', 'Pierrefeu-du-Var', 'Pont-Saint-Martin', 'Marennes', 'Santes', 'Brindas', 'Saint-Pierre-lès-Nemours', "Saint-Cyr-au-Mont-d'Or", 'Trans-en-Provence', 'Calvi', 'Mornant', 'Rosny-sur-Seine', 'Haute-Goulaine', "Saint-Martin-d'Uriage", 'Eaunes', 'Puilboreau', 'Vendenheim', 'Saint-Cannat', 'Lardy', 'Furiani', 'Marly-la-Ville', 'Épernon', 'Fegersheim', 'Colombelles', 'Cléon', 'Chasse-sur-Rhône', 'Saint-Martin-le-Vinoux', 'Courthézon', "Saint-Georges-d'Orques", 'Saint-Jory', 'Beauzelle', 'Izon', 'Lentilly', 'Dompierre-sur-Mer', 'Vias', "Saint-Symphorien-d'Ozon", 'Le Puy-Sainte-Réparade', 'Saint-Nom-la-Bretèche', 'Challes-les-Eaux', 'Luynes', 'Fayence', 'Saint-Laurent-de-Mure', 'Bléré', 'Mouy', 'Saint-Jean-de-Boiseau', 'Aubignan', 'Marsannay-la-Côte', 'Cadaujac', 'Saint-Pryvé-Saint-Mesmin', "Champagne-au-Mont-d'Or", 'Marnaz']
    zoneA = ['Marseille', 'Lyon', 'Nice', 'Montpellier', 'Lille', 'Toulon', 'Villeurbanne', 'Aix-en-Provence', 'Argenteuil', 'Créteil', 'Vitry-sur-Seine', 'Aulnay-sous-Bois', 'Champigny-sur-Marne', 'Antibes', 'Cannes', 'Ajaccio', 'Drancy', 'Noisy-le-Grand', 'La Seyne-sur-Mer', 'Cergy', 'Sarcelles', 'Hyères', 'Épinay-sur-Seine', 'Meaux', 'Bondy', 'Fréjus', 'Grasse', 'Le Blanc-Mesnil', 'Sartrouville', 'Sevran', 'Martigues', 'Bobigny', 'Cagnes-sur-Mer', 'Aubagne', 'Corbeil-Essonnes', 'Alfortville', 'Istres', 'Le Cannet', 'Mantes-la-Jolie', 'Livry-Gargan', 'Gennevilliers', 'Choisy-le-Roi', 'Rosny-sous-Bois', 'Melun', 'Marcq-en-Baroeul', 'Noisy-le-Sec', 'Garges-lès-Gonesse', 'Gagny', 'La Courneuve', 'Poissy', 'Savigny-sur-Orge', 'Pontault-Combault', 'Conflans-Sainte-Honorine', 'Stains', 'Six-Fours-les-Plages', 'Tremblay-en-France', 'Marignane', 'Neuilly-sur-Marne', 'La Ciotat', 'Montigny-le-Bretonneux', 'Annemasse', 'Villeneuve-Saint-Georges', 'Houilles', 'Viry-Châtillon', 'Plaisir', 'Pontoise', 'Palaiseau', 'Les Mureaux', 'Athis-Mons', 'Saint-Laurent-du-Var', 'Clichy-sous-Bois', 'Trappes', 'Thiais', 'Menton', 'Savigny-le-Temple', 'Yerres', 'Draveil', 'Lambersart', 'Guyancourt', 'Bezons', 'Vigneux-sur-Seine', 'Pierrefitte-sur-Seine', 'Villiers-le-Bel', 'Vallauris', 'Ermont', 'Villiers-sur-Marne', 'Sannois', 'Ris-Orangis', 'Herblay', 'Élancourt', 'Gonesse', 'Rambouillet', 'Taverny', 'Montfermeil', 'Sucy-en-Brie', 'Brunoy', 'Villeneuve-la-Garenne', 'Romainville', 'Miramas', 'Bussy-Saint-Georges', 'Les Ulis', 'Brétigny-sur-Orge', 'Champs-sur-Marne', 'Villeparisis', 'Eaubonne', "Saint-Ouen-l'Aumône", 'Cormeilles-en-Parisis', 'Montgeron', 'Roissy-en-Brie', 'La Madeleine', 'Les Pavillons-sous-Bois', 'Mandelieu-la-Napoule', 'Combs-la-Ville', 'Deuil-la-Barre', 'Longjumeau', 'La Celle-Saint-Cloud', 'Orly', 'Loos', 'Gif-sur-Yvette', 'Montmorency', 'Morsang-sur-Orge', 'La Valette-du-Var', 'Le Mée-sur-Seine', 'Limeil-Brévannes', 'Dammarie-les-Lys', 'Gardanne', 'Lagny-sur-Marne', 'Saint-Michel-sur-Orge', 'Allauch', 'Ozoir-la-Ferrière', 'Wasquehal', 'Mantes-la-Ville', 'Les Pennes-Mirabeau', 'Montigny-lès-Cormeilles', 'Vence', 'Maurepas', 'Le Plessis-Trévise', 'Chilly-Mazarin', 'Mitry-Mory', 'Mougins', 'Villeneuve-le-Roi', 'Chevilly-Larue', "Saint-Cyr-l'École", 'Chennevières-sur-Marne', 'Les Clayes-sous-Bois', 'Soisy-sous-Montmorency', 'Port-de-Bouc', 'Moissy-Cramayel', 'La Crau', 'Éragny', 'Mauguio', 'Osny', 'Jouy-le-Moutier', 'Bonneuil-sur-Marne', 'Boissy-Saint-Léger', 'Limay', 'Vauréal', 'Brie-Comte-Robert', 'Castelnau-le-Lez', 'Orsay', 'Sanary-sur-Mer', 'Lattes', 'Verrières-le-Buisson', 'Noisiel', 'Verneuil-sur-Seine', 'Fos-sur-Mer', 'Carrières-sur-Seine', 'Carrières-sous-Poissy', 'Montesson', 'Fontainebleau', 'Domont', 'Villeneuve-Loubet', 'Juvisy-sur-Orge', 'Le Bourget', 'Saint-Leu-la-Forêt', 'Saint-Brice-sous-Forêt', 'Lognes', 'Avon', 'Montmagny', 'Bouc-Bel-Air', "Bois-d'Arcy", "Berre-l'Étang", 'Arnouville', 'Courcouronnes', 'Méru', 'Beausoleil', 'Mennecy', 'Sainte-Maxime', 'Valbonne', 'Ollioules', 'Fontenay-le-Fleury', 'Saint-Fargeau-Ponthierry', 'Vaires-sur-Marne', 'Villetaneuse', 'Roquebrune-Cap-Martin', 'Roquebrune-sur-Argens', 'Châteauneuf-les-Martigues', 'Saint-Julien-en-Genevois', 'Épinay-sous-Sénart', 'Andrésy', 'Valenton', 'Auriol', 'Voisins-le-Bretonneux', 'Aubergenville', 'Vernouillet', 'Saint-Cyr-sur-Mer', 'Rognac', 'Triel-sur-Seine', 'Saint-André-lez-Lille', 'Solliès-Pont', 'Le Pradet', 'La Queue-en-Brie', 'Carros', 'Gaillard', 'Claye-Souilly', 'Cogolin', 'Chantilly', 'Porto-Vecchio', 'Septèmes-les-Vallons', 'Plan-de-Cuques', 'Vaux-le-Pénil', 'Persan', 'Dugny', 'Arpajon', 'Gex', 'Mouans-Sartoux', 'Épinay-sur-Orge', 'Cuers', 'Trets', 'La Trinité', 'Villepreux', 'Carqueiranne', 'La Londe-les-Maures', 'Ormesson-sur-Marne', 'Biot', 'Villebon-sur-Yvette', 'Bures-sur-Yvette', 'Villecresnes', 'Gouvieux', 'Chanteloup-les-Vignes', 'Chambly', 'Fuveau', 'Lamorlaye', 'Saint-Germain-lès-Arpajon', 'Villeneuve-lès-Maguelone', 'Méry-sur-Oise', 'Ézanville', 'Beaumont-sur-Oise', 'Saint-Genis-Pouilly', 'Bondoufle', 'Cesson', 'Magny-les-Hameaux', 'Crosne', 'Thorigny-sur-Marne', 'Le Beausset', 'Saint-Gély-du-Fesc', 'Gignac-la-Nerthe', 'Fleury-Mérogis', 'Cabriès', 'Meulan-en-Yvelines', 'Montévrain', 'Saint-Jean-de-Védas', 'Beauchamp', 'Groslay', 'Velaux', 'La Farlède', 'Saint-Pierre-du-Perray', 'Roquevaire', 'Pérols', 'Ferney-Voltaire', 'Divonne-les-Bains', 'Bougival', 'La Grande-Motte', 'Venelles', 'Jouy-en-Josas', 'Dammartin-en-Goële', 'Le Crès', 'Tournan-en-Brie', 'Quincy-sous-Sénart', 'Ville-la-Grand', 'Pierrelaye', 'Marcoussis', 'Gretz-Armainvilliers', 'Peymeinade', 'Saint-Rémy-lès-Chevreuse', 'Serris', 'Saint-Chamas', 'Sausset-les-Pins', 'Le Plessis-Bouchard', 'La Colle-sur-Loup', 'Cassis', 'Juvignac', 'Bandol', 'Bormes-les-Mimosas', 'Lésigny', 'Vétraz-Monthoux', 'Écouen', 'Lisses', 'Louveciennes', 'Saint-Germain-lès-Corbeil', 'Émerainville', 'Montlhéry', 'Paray-Vieille-Poste', 'Reignier-Ésery', 'La Ville-du-Bois', 'Contes', 'Pégomas', 'Vert-Saint-Denis', 'Soisy-sur-Seine', 'Cavalaire-sur-Mer', 'Villemoisson-sur-Orge', 'Prévessin-Moëns', 'La Gaude', 'Auvers-sur-Oise', 'Bailly-Romainvilliers', 'Bessancourt', 'Carnoux-en-Provence', 'Gargenville', 'Vaujours', 'Puget-sur-Argens', 'Le Mesnil-Saint-Denis', 'Saint-Victoret', 'Courdimanche', 'Grabels', 'Magny-le-Hongre', 'Limours', 'Linas', 'Longpont-sur-Orge', 'Épône', 'Gournay-sur-Marne', 'Le Mesnil-le-Roi', 'Roquefort-les-Pins', 'Carry-le-Rouet', 'La Penne-sur-Huveaune', 'Fabrègues', 'Saint-Thibault-des-Vignes', 'Courtry', 'Boussy-Saint-Antoine', 'Gémenos', 'Wissous', 'Palavas-les-Flots', 'Ambilly', 'La Bouilladisse', 'Magnanville', 'La Verrière', 'Chambourcy', 'Bouffémont', 'Esbly', 'Chevreuse', 'Nandy', 'Vendargues', 'Cranves-Sales', 'Saint-Mandrier-sur-Mer', 'Rungis', 'Saint-Mitre-les-Remparts', 'Parmain', 'Thoiry', 'Nanteuil-lès-Meaux', 'Simiane-Collongue', "La Cadière-d'Azur", 'Villefranche-sur-Mer', 'Le Lavandou', 'Menucourt', 'Buc', 'Peypin', 'Clapiers', 'Jouars-Pontchartrain', 'Solliès-Toucas', 'Meyreuil', 'Égly', 'Ensuès-la-Redonne', 'Saint-André-de-la-Roche', 'Jacou', 'Villennes-sur-Seine', 'Ablon-sur-Seine', 'Saintry-sur-Seine', 'La Roquette-sur-Siagne', 'Saint-Clément-de-Rivière', 'Quincy-Voisins', 'Roquefort-la-Bédoule', 'Saulx-les-Chartreux', 'Villabé', 'Saint-Zacharie', 'Le Port-Marly', 'Trilport', "Cap-d'Ail", 'Vaux-sur-Seine', 'Mériel', 'Le Coudray-Montceaux', 'Tourrette-Levens', 'Coubron', 'Levens', 'Champagne-sur-Oise', 'Noiseau', 'Prades-le-Lez', 'La Frette-sur-Seine', 'Teyran', 'Issou', 'Mimet', 'Saint-Tropez', 'Coignières', 'Le Rove', 'Mandres-les-Roses', 'Crégy-lès-Meaux', 'Maurecourt', 'Brou-sur-Chantereine', 'Fourqueux', 'Crécy-la-Chapelle', 'Drap', 'Cessy', 'Ceyreste', 'Villenoy', 'Grimaud', 'Le Plessis-Pâté', 'Cruseilles', 'Gréasque', 'Le Thillay', 'Leuville-sur-Orge', 'La Norville', 'Tourrettes-sur-Loup', 'Gattières', 'Le Rouret', 'Coye-la-Forêt', 'Villiers-sur-Orge', 'Collonges-sous-Salève', 'Ornex', 'Juziers', 'Forges-les-Bains', 'Ballainvilliers', 'Beaulieu-sur-Mer', 'Santeny', 'Le Revest-les-Eaux', 'Veigy-Foncenex', 'Boissise-le-Roi', 'Mareil-Marly', 'La Croix-Valmer', 'Sospel', 'Bornel', 'Saint-Germain-sur-Morin', 'Mézières-sur-Seine', 'Saint-Paul-de-Vence', 'Pomponne', 'Montferrier-sur-Lez', 'Saclay', 'Orry-la-Ville', 'Valleiry', 'Bruyères-le-Châtel', 'Montry', 'Colomars', 'Saint-Cergues', 'Fillinges', 'Saint-Savournin', 'Châteauneuf-Grasse', 'Le Tignet', 'Étiolles', 'La Turbie', 'Dampmart', 'Peynier', 'Collégien', 'Porcheville', 'Neauphle-le-Château', 'Auribeau-sur-Siagne', 'La Destrousse', 'Bonne', 'Tigery', 'Bonifacio', 'La Chapelle-en-Serval', 'Le Bar-sur-Loup', 'Margency', 'Gassin', 'Roissy-en-France', 'Frépillon', 'Villiers-Saint-Frédéric', 'Lavérune', 'Pers-Jussy', 'Montlignon', 'Breuillet', "Les Adrets-de-l'Estérel", 'Vulaines-sur-Seine', 'Coupvray', 'Saint-Martin-du-Var', 'Gometz-le-Châtel', 'Champlan', 'Héricy', 'Èze', 'Solliès-Ville', 'Longperrier', 'Belgentier', 'Buchelay', 'Chanteloup-en-Brie', 'Flins-sur-Seine', 'Bernes-sur-Oise', 'Varennes-Jarcy', 'Samoreau', 'Monnetier-Mornex', 'Le Tholonet', 'Archamps', 'Le Mesnil-en-Thelle', 'Péron']
    zoneAbis = ['Paris', 'Chatou', 'Croissy-sur-Seine', 'Le Chesnay', 'Le Pecq', 'Le Vésinet', 'Maisons-Laffitte', 'Marly-le-Roi', 'Rocquencourt', 'Saint-Germain-en-Laye', 'Vélizy-Villacoublay', 'Versailles', 'Viroflay', 'Antony', 'Asnières-sur-Seine', 'Bagneux', 'Bois-Colombes', 'Boulogne-Billancourt', 'Bourg-la-Reine', 'Châtenay-Malabry', 'Châtillon', 'Chaville', 'Clamart', 'Clichy', 'Colombes', 'Courbevoie', 'Fontenay-aux-Roses', 'Garches', 'Issy-les-Moulineaux', 'La Garenne-Colombes', 'Le Plessis-Robinson', 'Levallois-Perret', 'Malakoff', 'Marnes-la-Coquette', 'Meudon', 'Montrouge', 'Nanterre', 'Neuilly-sur-Seine', 'Puteaux', 'Rueil-Malmaison', 'Saint-Cloud', 'Sceaux', 'Sèvres', 'Suresnes', 'Vanves', 'Vaucresson', "Ville-d'Avray", 'Aubervilliers', 'Bagnolet', 'Le Pré-Saint-Gervais', 'Le Raincy', 'Les Lilas', 'Montreuil', 'Neuilly-Plaisance', 'Pantin', 'Saint-Denis', 'Saint-Ouen', 'Villemomble', 'Arcueil', 'Bry-sur-Marne', 'Cachan', 'Charenton-le-Pont', 'Fontenay-sous-Bois', 'Gentilly', 'Ivry-sur-Seine', 'Joinville-le-Pont', "L'Haÿ-les-Roses", 'Le Kremlin-Bicêtre', 'Le Perreux-sur-Marne', 'Maisons-Alfort', 'Nogent-sur-Marne', 'Saint-Mandé', 'Saint-Maur-des-Fossés', 'Saint-Maurice', 'Villejuif', 'Vincennes', 'Enghien-les-Bains']
    zoneB1 = sorted(zoneB1)
    zoneAbis = sorted(zoneAbis)
    zoneA = sorted(zoneA)
    list_total = zoneB1+zoneAbis+zoneA
    list_total = sorted(list_total)
    choix = select("Selectionnez la ville de votre investissement Pinel :", list_total)
    list_dict = {"A" : zoneA,"A bis":zoneAbis,"B1":zoneB1}
    for key, value in list_dict.items():
        if choix in value:
    #choixZone = radio("Selectionner la zone Pinel", options=['zone A bis', 'zone A', "zone B1"])
    #if (choixZone == "zone A bis") :
            if key == "A bis":
                surfaceHabitable = float(input("Votre surface habitable :"))
                surfaceTerasse = float(input("Votre surface exterieur (balcons, terasse), hors jardin : "))
                prixAbis = 17.55
                surfaceTerasse2 = surfaceTerasse/2
                if(surfaceTerasse2 < 9):
                    surfaceTotale = surfaceHabitable + surfaceTerasse2
                    coeff = (19/surfaceTotale) + 0.7
                    Loyermax = prixAbis*coeff*surfaceTotale
                    #put_text("Le plafond de loyer sera de {0:.2f} euros".format(Loyermax))
                    put_table([
                    ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone"],
                    [float("{:.2f}".format(Loyermax)),surfaceTotale, key]
                ])
                    #put_button("Retour",onclick = lambda: run_js('window.location.reload()'))
                if (surfaceTerasse2 > 9):
                    surfaceTerasse3 = 4.5
                    surfaceTotale = surfaceHabitable + surfaceTerasse3
                    coeff = (19/surfaceTotale) + 0.7
                    Loyermax2 = prixAbis*coeff*surfaceTotale
                    put_table([
                    ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone"],
                    [float("{:.2f}".format(Loyermax2)),surfaceTotale, key]
                ])
                    #put_button("Retour",onclick = lambda: run_js('window.location.reload()'))
                    #put_text("Le plafond de loyer sera de {0:.2f} euros".format(Loyermax2))
            #elif (choixZone == "zone A") :
            if key == "A":
                surfaceHabitable = float(input("Votre surface habitable :"))
                surfaceTerasse = float(input("Votre surface exterieur (balcons, terasse), hors jardin : "))
                prixA = 13.04
                surfaceTerasse2 = surfaceTerasse/2
                if(surfaceTerasse2 < 9):
                    surfaceTotale = surfaceHabitable + surfaceTerasse2
                    coeff = (19/surfaceTotale) + 0.7
                    Loyermax = prixA*coeff*surfaceTotale
                    #put_text("Le plafond de loyer sera de {0:.2f} euros".format(Loyermax))
                    put_table([
                    ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone"],
                    [float("{:.2f}".format(Loyermax)),surfaceTotale,key]
                ])
                    #put_button("Retour",onclick = lambda: run_js('window.location.reload()'))
                if (surfaceTerasse2 > 9):
                    surfaceTerasse3 = 4.5
                    surfaceTotale = surfaceHabitable + surfaceTerasse3
                    coeff = (19/surfaceTotale) + 0.7
                    Loyermax2 = prixA*coeff*surfaceTotale
                    put_table([
                    ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone"],
                    [float("{:.2f}".format(Loyermax2)),surfaceTotale,key]
                ])
                # put_button("Retour",onclick = lambda: run_js('window.location.reload()'))
                    #put_text("Le plafond de loyer sera de {0:.2f} euros".format(Loyermax2))
            #elif (choixZone == "zone B1") :
            if key == "B1":
                surfaceHabitable = float(input("Votre surface habitable :"))
                surfaceTerasse = float(input("Votre surface exterieur (balcons, terasse), hors jardin : "))    
                prixB1 = 10.51
                surfaceTerasse2 = surfaceTerasse/2
                if(surfaceTerasse2 < 9):
                    surfaceTotale = surfaceHabitable + surfaceTerasse2
                    coeff = (19/surfaceTotale) + 0.7
                    Loyermax = prixB1*coeff*surfaceTotale
                    #put_text("Le plafond de loyer sera de {0:.2f} euros".format(Loyermax))
                    put_table([
                    ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone"],
                    [float("{:.2f}".format(Loyermax)),surfaceTotale,key]
                ])
                # put_button("Retour",onclick = lambda: run_js('window.location.reload()'))
                if (surfaceTerasse2 > 9):
                    surfaceTerasse3 = 4.5
                    surfaceTotale = surfaceHabitable + surfaceTerasse3
                    coeff = (19/surfaceTotale) + 0.7
                    Loyermax2 = prixB1*coeff*surfaceTotale
                    put_table([
                    ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone"],
                    [float("{:.2f}".format(Loyermax2)),surfaceTotale,key]
                ])

def RentabiliteInvestissement():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    loyer = float(input("Votre loyer :"))
    prixDuBien = float(input("Le prix de votre bien : "))
    renta = ((loyer*12)/prixDuBien)*100
    if(renta <3):
        put_table([
                ["Rentabilité sur investissement"],
                ["{:.2f}%".format(renta),style(put_text('Mauvaise rentabilité'), 'color:red')],
            ])
    else:
        put_table([
                ["Rentabilité sur investissement"],
                ["{:.2f}%".format(renta),style(put_text('Bonne rentabilité'), 'color:green')],
            ])

def RentaEconomieImpot():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    loyer = float(input("Votre loyer Pinel :"))
    prixDuBien = float(input("Le prix de votre appartement Pinel : "))
    economie = 0.02*prixDuBien
    renta = (((loyer+(economie/12))*12)/prixDuBien)*100
    put_table([
            ["Rentabilité avec économie d'impôt"],
            ["{:.2f}%".format(renta)]
        ])

def ChargesLoyer():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    loyer = float(input("Votre loyer : "))
    assurance = float(input("Pourcentage d'assurance sur votre loyer :"))
    fraisDeGestion = float(input("Pourcentage des frais de gestions sur votre loyer :"))
    chargecopro = float(input("Pourcentage des charges de copropriété sur votre loyer :"))
    taxeFonciere = loyer/12
    autre = float(input("Pourcentage des autres charges déductibles sur votre loyer :"))
    toutcharges = loyer*(assurance/100) + loyer*(fraisDeGestion/100) + loyer*(chargecopro/100) + taxeFonciere + loyer*(autre/100)
    put_table([
            ["Montant de vos charges"],
            [float("{:.2f}".format(toutcharges))]
        ])

def TauxEndettement():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    revenu = float(input("Quel est le revenu net du foyer annuel avant impôts ?"))
    revenu = revenu/12
    loyerCredit = float(input("Percevez vous des loyers par mois, si oui de combien : "))
    autreRevenus = float(input("Percevez-vous des pensions par mois, si oui de quel montant :"))
    autreRevenus2 = float(input("Percevez-vous d'autres revenus par mois, si oui de quel montant :"))
    Sommetotale = float(input("Indiquez la somme totale de vos pensions et de vos crédit immobiliers en cours par mois : "))
    #pensionOui = float(input("Versez vous une pension par mois, si oui de combien :"))
    #pensionOui = float(input("Percevez vous une pension par mois, si oui de combien :"))
    #revenuTotal = revenu + pensionOui - pensionNon
    #revenuFoncier = float(input("Percevez vous des revenus foncier, si oui quel est le montant par mois : "))
    loyerCredit = 0.7*loyerCredit
    recettes = revenu + loyerCredit + autreRevenus + autreRevenus2
    depenses = Sommetotale

    taux = (depenses/recettes)*100
    #taux = (loyerCredit*12)/((revenu*12)+((autreRevenus*12)*70/100))*100
    if(taux <33):
        put_table([
                ["Votre taux d'endettement"],
                ["{:.2f}%".format(taux)]
            ])
    else:
        put_table([
                ["Votre taux d'endettement"],
                ["{:.2f}%".format(taux)]
            ])

def IFI():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    residencePrincipale = float(input("Quel est le prix de votre résidence principale ?"))
    residenceP70 = 0.7 * residencePrincipale
    autreBiens = float(input("Valeur de vos autres biens :"))
    capitalRestantDu = float(input("Quel est le capital restant dû à date de vos crédits immobilier en cours : "))
    patrimoine = residenceP70 + autreBiens - capitalRestantDu

    if patrimoine < 800000:
        tax = 0
    elif patrimoine < 1300000:
        tax = 0.005*(patrimoine - 800000)
    elif patrimoine < 2570000:
        tax = 0.005*(1300000 - 800000) + 0.007*(patrimoine - 1300000) 
    elif patrimoine < 5000000:
        tax = 0.005*(1300000 - 800000) + 0.007*(2570000 - 1300000) + 0.01*(patrimoine - 2570000)
    elif patrimoine< 10000000:
        tax = 0.005*(1300000 - 800000) + 0.007*(2570000 - 1300000) + 0.01*(5000000 - 2570000) + 0.0125*(patrimoine - 5000000)
    elif patrimoine > 10000000:
        tax = 0.005*(1300000 - 800000) + 0.007*(2570000 - 1300000) + 0.01*(5000000 - 2570000) + 0.0125*(10000000 - 5000000) + 0.015*(patrimoine - 10000000) 
    put_table([
                ["Total de votre IFI à payer"],
                [float("{:.2f}".format(tax))]
            ])

def EconomieImpotPinel():
    put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    prixDuBien1 = float(input("Quel est le prix de votre appartement Pinel : "))
    fraisnotaire = (2.5/100)*prixDuBien1
    prixDuBien = prixDuBien1 + fraisnotaire

    if prixDuBien > 300000:
        economie = 6000
    else :
        #economie = (2/100)*prixDuBien
        surfaceHabitable = float(input("Votre surface habitable :"))
        surfaceTerasse = float(input("Votre surface exterieur (balcons, terasse), hors jardin : "))
        surfaceTerasse2 = surfaceTerasse/2

        if(surfaceTerasse2 < 9):
            surfaceTotale = surfaceHabitable + surfaceTerasse2
        else :
            surfaceTerasse3 = 4.5
            surfaceTotale = surfaceHabitable + surfaceTerasse3

        if (prixDuBien/surfaceTotale) > 5500:
            a = surfaceTotale*5500
            economie = a*(2/100)
        else:
            economie = (2/100)*prixDuBien
    put_table([
            ["Votre Economie d'impôt"],
            [float("{:.2f}".format(economie))]
        ])
    radio("Voulez-vous que l'on vous propose des biens ?", options=["Oui","Non"])

def generate_pdf(data,file_name):
	pdf = MyFPDF()
	pdf.add_page()
	pdf.set_font('Arial', 'B', 18)
	pdf.cell(190, 15, 'Professional Info', ln=1, align='C')
	#pdf.image('papillon.png', 85, 30, 40)
	pdf.line(10, 80, 200, 80)
	pdf.cell(60, 60, '', ln=2)
	pdf.write_html(data)
	pdf.output(f'{file_name}.pdf', 'F')



###########CREDIT IMMOBILIER
def main():
  
    set_env(output_max_width='300%',title = "PAPILLON PATRIMOINE")
    put_image(open("papillon2.png", 'rb').read())
    #choixSim = select("Que voulez vous faire ?", ["Faire une simulation","Modules"])
    #put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    
    choix = select("Que voulez vous faire ?", ["1 - Calculer mes mensualités","2 - Calculer ma capacité d'emprunt","3 - Investir dans le neuf",
    "4 - Comparateur Investissement Neuf ou Ancien","5 - Calculer un loyer Pinel","6 - Calcul de la rentabilité de l'investissement","7 - Calcul de la rentabilité Pinel avec économie d'impôt",
    "8 - Calcul des charges sur le loyer", "9 - Calcul du Taux d'endettement","10 - Calculez votre IFI", "11 - Calculez votre impôt",
    "12 - Calculer Economie Impôt Pinel","13 - Simulateur Pinel",
    "14 - Simulateur Malraux","15 - Simulateur meublé à l'amortissement", "16 - Simulateur Monument historique","17 - Comparateur d'epargne",
    "18 - Calcul des prix des villes au mètre carré","19 - Simulateur SCPI Pinel", "20 - Simulateur SCPI Malraux","21 - Simulateur d'epargne",
    "22 - Meilleur dispositif selon vos informations", "23 - Comparateur de rentabilité entre le neuf et l'ancien", "24 - Simulateur d'impôts sur la plus-value immobilière",
    "25 - Étude Patrimoiniale","26 - Simulateur de calcul de Prêt à taux zéro", "27 - Calcul assurance de prêt immobilier"])
    #put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
    #choix = checkbox("Que voulez vous faire ?", options=["1 - Calculer mes mensualités","2 - Calculer ma capacité d'emprunt"])
    #if(choixSim == "Modules"):
    if (choix == "1 - Calculer mes mensualités") :
        CalculerMensualité()
    elif (choix == "2 - Calculer ma capacité d'emprunt") :
        CapaciteEmprunt()


#############COMPARATIF NEUF ET ANCIEN
#put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")

    if (choix == "3 - Investir dans le neuf") :
        InvestirNeuf()
    elif (choix == "4 - Comparateur Investissement Neuf ou Ancien") :
        InvestirAncien()
##################

    ######### COMPARATIF ZONE
#if(choixSim == "Modules"):
    if (choix == "5 - Calculer un loyer Pinel"):
        ChosirZone()
################

############# RENTABILITE INVESTISSEMENT
#if(choixSim == "Modules"):
    if (choix == "6 - Calcul de la rentabilité de l'investissement"):
        RentabiliteInvestissement()
###############

#############CALCUL DE LA RENTABILITE AVEC ECONOMIE D'IMPOTS
#if(choixSim == "Modules"):
    if (choix == "7 - Calcul de la rentabilité Pinel avec économie d'impôt"):
        RentaEconomieImpot()
#################

################CALCUL DES CHARGES
#if(choixSim == "Modules"):
    if (choix == "8 - Calcul des charges sur le loyer"):
        ChargesLoyer()
#################

################CALCUL DU TAUX D'ENDETTEMENT
#if(choixSim == "Modules"):
    if (choix == "9 - Calcul du Taux d'endettement"):
        TauxEndettement()
###############

#############CALCUL DE L'IFI
#if(choixSim == "Modules"):
    if (choix == "10 - Calculez votre IFI"):
        IFI()
################

##################CALCULEZ VOTRE IMPOT
#if(choixSim == "Modules"):
    if (choix == "11 - Calculez votre impôt") :
        #put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        test_impotFinal()
#####################


################SIMULATION
#if(choixSim == "Modules"):
    if (choix == "12 - Calculer Economie Impôt Pinel") :
        EconomieImpotPinel()

#################
    if (choix == "13 - Simulateur Pinel"):  
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        put_markdown('# SIMULATION PINEL')
        pd.options.display.float_format = "{:,.2f}".format 
    #revenu = float(input("Revenu global imposable (en euros)? ")) 
        #statut = saisirStatutFamilial()
        #revenuAvantAbattement = (0.9/100)*revenu
        #npers = int(input("Nombre de personnes a charge? "))
        #afficherFicheImpots2(revenu, statut, npers)
        #######PRIX DU BIEN ET LOYER
        #nbrePart = saisirStatutFamilial()
        
        ############
        
        revenu = float(input("Quel est le revenu net annuel du foyer : "))
        revenu2 = 0.9*revenu
        if revenu2 > 126520:
            revenuAvantAbbatement = revenu - 12652
        else :
            revenuAvantAbbatement = 0.9*revenu
        statut = saisirStatutFamilial()
        npers = int(input("Nombre de personnes a charge? "))
        if statut == CONCUBINAGE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
        ###########CELIBATAIRE
        if statut == CELIBATAIRE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
                
        ############MARIE
        
        if statut == MARIE:
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 52140:
                    impots = (revenuAvantAbbatement*0.11)-2249.50
                    TMI = 11
                if 52140 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-12156.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-28556
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-41382.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2.5:
                if revenuAvantAbbatement < 25563:
                    impots = 0
                    TMI = 0
                if 25563 < revenuAvantAbbatement <= 57561:
                    impots = (revenuAvantAbbatement*0.11)-2811.88
                    TMI = 11
                if 57562 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-13748.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-30148
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-42974.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 62978:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 62979 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-15340.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-31740
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-44566.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 73818:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 73819 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-18524.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-34924
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-47750.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==5:
                if revenuAvantAbbatement < 51125:
                    impots = 0
                    TMI = 0
                if 51125 < revenuAvantAbbatement <= 84655:
                    impots = (revenuAvantAbbatement*0.11)-5623.75
                    TMI = 11
                if 84656 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-21708.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-38108
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-50934.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==6:
                if revenuAvantAbbatement < 61350:
                    impots = 0
                    TMI = 0
                if 61350 < revenuAvantAbbatement <= 94495:
                    impots = (revenuAvantAbbatement*0.11)-6748.5
                    TMI = 11
                if 94496 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-24892.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-40292
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-54118.88
                    TMI = 45
            
                
        afficherFicheImpots(revenuAvantAbbatement, statut, npers,TMI,impots)
        #############
        prixDuBien = float(input("Montant du bien : "))
        Apport = float(input("Votre apport :"))
        fraisNotaire = (2.5/100)*prixDuBien
        prixDuBien2 = prixDuBien + fraisNotaire
        garantieBancaire = (1.5/100)*prixDuBien
        prixTotalBien = prixDuBien2 + garantieBancaire - Apport
        ######SURFACE
        zoneB1 = ['Toulouse', 'Nantes', 'Strasbourg', 'Bordeaux', 'Rennes', 'Reims', 'Le Havre', 'Grenoble', 'Dijon', 'Nîmes', 'Clermont-Ferrand', 'Limoges', 'Tours', 'Amiens', 'Metz', 'Perpignan', 'Orléans', 'Rouen', 'Mulhouse', 'Caen', 'Nancy', 'Roubaix', 'Tourcoing', 'Avignon', 'La Rochelle', "Villeneuve-d'Ascq", 'Vénissieux', 'Chambéry', 'Pessac', 'Beauvais', 'Arles', 'Annecy', 'Saint-Malo', 'Bayonne', 'Valenciennes', 'Sète', 'Saint-Herblain', 'Bastia', 'Salon-de-Provence', 'Vaulx-en-Velin', 'Douai', 'Talence', 'Caluire-et-Cuire', 'Wattrelos', 'Compiègne', 'Chartres', 'Rezé', 'Anglet', 'Bron', 'Draguignan', "Saint-Martin-d'Hères", 'Joué-lès-Tours', 'Échirolles', 'Villefranche-sur-Saône', 'Colomiers', 'Thonon-les-Bains', 'Lens', 'Creil', 'Schiltigheim', 'Meyzieu', 'Vandoeuvre-lès-Nancy', 'Rillieux-la-Pape', 'Orange', 'Carpentras', "Villenave-d'Ornon", 'Sotteville-lès-Rouen', 'Aix-les-Bains', 'Saint-Médard-en-Jalles', 'Saint-Étienne-du-Rouvray', 'Illkirch-Graffenstaden', 'Bourgoin-Jallieu', 'Biarritz', 'Béthune', 'Tournefeuille', 'Décines-Charpieu', 'Saint-Sébastien-sur-Loire', 'Armentières', 'Cavaillon', 'Lunel', 'Oullins', 'Bègles', 'Orvault', 'La Teste-de-Buch', 'Le Grand-Quevilly', 'Muret', 'Étampes', 'Agde', 'Gradignan', 'Le Bouscat', 'Frontignan', 'Montigny-lès-Metz', 'Blagnac', 'Cenon', 'Le Petit-Quevilly', 'Vertou', 'Sainte-Foy-lès-Lyon', 'Hérouville-Saint-Clair', 'Bois-Guillaume-Bihorel', 'Mons-en-Baroeul', 'Fleury-les-Aubrais', 'Saint-Genis-Laval', 'Lormont', 'Annecy-le-Vieux', 'Halluin', 'Croix', 'Eysines', 'Gujan-Mestras', 'Tassin-la-Demi-Lune', 'Voiron', 'Olivet', 'Saint-Jean-de-Braye', 'Mont-Saint-Aignan', 'Givors', 'Albertville', 'Pertuis', 'Couëron', 'Nogent-sur-Oise', 'Seynod', 'Bouguenais', 'Carquefou', 'Sorgues', 'Villefontaine', 'Meylan', 'Écully', 'Hem', 'Chamalières', 'Ronchin', 'La Chapelle-sur-Erdre', 'Cluses', 'Bischheim', 'Faches-Thumesnil', 'Cran-Gevrier', 'Saint-Fons', 'Elbeuf', 'Bruz', 'Saint-Jean-de-la-Ruelle', 'Lingolsheim', 'Cestas', 'Montereau-Fault-Yonne', 'La Baule-Escoublac', 'Saint-Cyr-sur-Loire', 'Lucé', 'Montivilliers', 'Brignoles', 'Senlis', 'Guérande', 'Plaisance-du-Touch', 'Hendaye', 'Saint-Égrève', 'Sallanches', 'Cugnaux', 'Cesson-Sévigné', 'Saint-Pierre-des-Corps', 'Bruges', 'Saran', 'Canteleu', 'Coulommiers', 'Laxou', 'Saint-Maximin-la-Sainte-Baume', 'Saint-Avertin', 'Villers-lès-Nancy', 'Bailleul', 'Pornic', 'Crépy-en-Valois', 'Olonne-sur-Mer', 'Haubourdin', "Les Sables-d'Olonne", 'Balma', 'Chenôve', "Château-d'Olonne", 'Saint-Gilles', 'Mouvaux', 'Ambarès-et-Lagrave', 'Lys-lez-Lannoy', 'Wattignies', 'Saint-Jean-de-Luz', 'Amboise', 'Canet-en-Roussillon', 'Roncq', 'Woippy', 'Nemours', 'Sainte-Luce-sur-Loire', 'Biscarrosse', 'Montataire', 'Villeneuve-lès-Avignon', 'Comines', 'Provins', 'Ramonville-Saint-Agne', 'Genas', 'Seclin', 'Pont-Sainte-Maxence', 'Seyssinet-Pariset', 'Tarnos', 'Mions', 'Méricourt', 'La Motte-Servolex', 'Gisors', 'Fonsorbes', 'Ostwald', 'Saint-Martin-de-Crau', 'Brignais', 'Ifs', 'Sassenage', 'Saint-Orens-de-Gameville', 'Maromme', 'Oissel', 'Castanet-Tolosan', 'Talant', 'Monteux', 'Obernai', 'Le Pont-de-Claix', 'Arcachon', 'Mèze', 'Hoenheim', 'Saint-Rémy-de-Provence', 'Chambray-lès-Tours', 'Vedène', 'La Roche-sur-Foron', 'Saint-Jacques-de-la-Lande', 'Dinard', 'Villers-Cotterêts', 'Montlouis-sur-Loire', 'Pacé', 'Vidauban', 'Fondettes', 'Pernes-les-Fontaines', 'Corbas', 'Pornichet', 'Mainvilliers', 'Déville-lès-Rouen', 'Saint-Jean', 'Betton', 'Chevigny-Saint-Sauveur', 'Neuville-en-Ferrain', 'Chantepie', 'La Riche', 'Tinqueux', 'Quetigny', 'Dourdan', 'Argelès-sur-Mer', 'Voreppe', 'Marquette-lez-Lille', 'Marly', 'Brumath', 'Pierre-Bénite', 'Craponne', 'Grand-Couronne', 'Bondues', 'Caudebec-lès-Elbeuf', 'La Chapelle-Saint-Mesmin', 'Biganos', 'Eybens', 'Chassieu', 'Pélissanne', 'Saint-Max', 'Wambrechies', 'Maxéville', 'Mondeville', 'Fosses', 'Portet-sur-Garonne', 'Le Luc', 'Le Haillan', 'Louvres', 'Ouistreham', 'Darnétal', 'Léognan', 'Lambesc', 'Le Muy', 'Fontaine-lès-Dijon', 'Leers', 'Feyzin', 'Longvic', 'La Ferté-sous-Jouarre', 'Petit-Couronne', 'Lorgues', 'Le Taillan-Médoc', 'Castelginest', 'Urrugne', "Gonfreville-l'Orcher", 'Miribel', 'Aytré', 'Saint-Laurent-de-la-Salanque', 'Saint-Grégoire', 'Dardilly', 'Villeneuve-Tolosane', 'Léguevin', 'Marguerittes', 'Port-Saint-Louis-du-Rhône', 'Crolles', 'Aigues-Mortes', 'Évian-les-Bains', 'Chécy', 'Le Thor', 'La Ravoire', 'Meythet', 'Lançon-Provence', 'Pibrac', 'Les Angles', 'Saint-Pierre-lès-Elbeuf', "La Chapelle-d'Armentières", 'Irigny', 'Le Grau-du-Roi', 'Basse-Goulaine', 'Capbreton', 'Frouzins', 'Honfleur', 'Vern-sur-Seiche', 'Harfleur', 'Saint-Loubès', 'Linselles', 'Ballan-Miré', 'Nangis', 'Pérenchies', 'Margny-lès-Compiègne', 'Saint-Aubin-lès-Elbeuf', 'Chaponost', 'Elne', 'Vif', 'Aucamville', 'Ingré', 'Entraigues-sur-la-Sorgue', 'Parempuyre', 'Noisy-le-Roi', 'Charvieu-Chavagneux', 'Thouaré-sur-Loire', 'Le Rheu', 'Seysses', 'Boucau', 'Saint-Vincent-de-Tyrosse', 'Vizille', 'Gleizé', 'Morières-lès-Avignon', 'Moirans', 'Borgo', 'Houplines', 'Sainte-Adresse', 'Éguilles', 'Les Sorinières', 'Le Mesnil-Esnard', 'Souffelweyersheim', 'Scionzier', 'Rochefort-du-Gard', 'Nieppe', 'Thorigné-Fouillard', 'Ballancourt-sur-Essonne', 'Trignac', 'Saint-Gilles-Croix-de-Vie', 'Chartres-de-Bretagne', 'Biguglia', 'Mordelles', 'Lagord', 'Launaguet', 'Gaillon', 'La Fare-les-Oliviers', 'Villard-Bonnot', 'Saint-Denis-en-Val', 'Neuville-sur-Saône', 'Artigues-près-Bordeaux', 'Martignas-sur-Jalle', 'Montluel', 'Liancourt', 'Geispolsheim', 'Donges', 'Poisy', 'Montoir-de-Bretagne', 'Sautron', 'Quesnoy-sur-Deûle', 'Luisant', 'Notre-Dame-de-Bondeville', "Saint-Jean-d'Illac", 'Ciboure', 'Seyssins', 'Bassens', 'Bassens', 'Carbon-Blanc', 'Balaruc-les-Bains', 'La Salvetat-Saint-Gilles', 'Le Teich', 'Les Arcs', 'Sérignan', 'Saint-Ismier', 'Huningue', 'Trévoux', 'Saint-Bonnet-de-Mure', 'Le Perray-en-Yvelines', 'Domène', 'Aussonne', 'Itteville', 'La Mulatière', 'La Tronche', 'Champagne-sur-Seine', 'Noyal-Châtillon-sur-Seiche', 'Eckbolsheim', 'La Verpillière', "Saint-Didier-au-Mont-d'Or", 'Bonsecours', 'Pignan', 'Varces-Allières-et-Risset', 'Bétheny', 'Ustaritz', 'Othis', 'Saint-Aubin-de-Médoc', 'Audenge', 'Publier', 'Bidart', 'Les Essarts-le-Roi', 'Lesquin', 'Marignier', 'Anse', 'Fontaines-sur-Saône', 'Baillargues', 'Tignieu-Jameyzieu', 'Acigné', 'Villers-Saint-Paul', 'Bouillargues', 'Gières', 'Escalquens', 'Franqueville-Saint-Pierre', 'Thônes', 'Veigné', 'Marsillargues', 'Jassans-Riottier', 'Bouaye', 'Rives', 'Châtelaillon-Plage', 'Cormontreuil', 'Cognin', 'La Montagne', 'Saint-Pierre-en-Faucigny', 'Malaunay', 'Montauroux', 'Manduel', 'La Wantzenau', 'Mazan', 'Saint-Quentin-Fallavier', 'Le Pian-Médoc', 'Cournonterral', 'Maule', 'Castries', 'Sarrians', 'Cornebarrieu', 'Saint-Alban-Leysse', 'Milhaud', 'Octeville-sur-Mer', 'Lèves', 'Thyez', 'Gigean', 'Nieul-sur-Mer', 'Jonage', 'Longueau', 'Pierrefeu-du-Var', 'Pont-Saint-Martin', 'Marennes', 'Santes', 'Brindas', 'Saint-Pierre-lès-Nemours', "Saint-Cyr-au-Mont-d'Or", 'Trans-en-Provence', 'Calvi', 'Mornant', 'Rosny-sur-Seine', 'Haute-Goulaine', "Saint-Martin-d'Uriage", 'Eaunes', 'Puilboreau', 'Vendenheim', 'Saint-Cannat', 'Lardy', 'Furiani', 'Marly-la-Ville', 'Épernon', 'Fegersheim', 'Colombelles', 'Cléon', 'Chasse-sur-Rhône', 'Saint-Martin-le-Vinoux', 'Courthézon', "Saint-Georges-d'Orques", 'Saint-Jory', 'Beauzelle', 'Izon', 'Lentilly', 'Dompierre-sur-Mer', 'Vias', "Saint-Symphorien-d'Ozon", 'Le Puy-Sainte-Réparade', 'Saint-Nom-la-Bretèche', 'Challes-les-Eaux', 'Luynes', 'Fayence', 'Saint-Laurent-de-Mure', 'Bléré', 'Mouy', 'Saint-Jean-de-Boiseau', 'Aubignan', 'Marsannay-la-Côte', 'Cadaujac', 'Saint-Pryvé-Saint-Mesmin', "Champagne-au-Mont-d'Or", 'Marnaz']
        zoneA = ['Marseille', 'Lyon', 'Nice', 'Montpellier', 'Lille', 'Toulon', 'Villeurbanne', 'Aix-en-Provence', 'Argenteuil', 'Créteil', 'Vitry-sur-Seine', 'Aulnay-sous-Bois', 'Champigny-sur-Marne', 'Antibes', 'Cannes', 'Ajaccio', 'Drancy', 'Noisy-le-Grand', 'La Seyne-sur-Mer', 'Cergy', 'Sarcelles', 'Hyères', 'Épinay-sur-Seine', 'Meaux', 'Bondy', 'Fréjus', 'Grasse', 'Le Blanc-Mesnil', 'Sartrouville', 'Sevran', 'Martigues', 'Bobigny', 'Cagnes-sur-Mer', 'Aubagne', 'Corbeil-Essonnes', 'Alfortville', 'Istres', 'Le Cannet', 'Mantes-la-Jolie', 'Livry-Gargan', 'Gennevilliers', 'Choisy-le-Roi', 'Rosny-sous-Bois', 'Melun', 'Marcq-en-Baroeul', 'Noisy-le-Sec', 'Garges-lès-Gonesse', 'Gagny', 'La Courneuve', 'Poissy', 'Savigny-sur-Orge', 'Pontault-Combault', 'Conflans-Sainte-Honorine', 'Stains', 'Six-Fours-les-Plages', 'Tremblay-en-France', 'Marignane', 'Neuilly-sur-Marne', 'La Ciotat', 'Montigny-le-Bretonneux', 'Annemasse', 'Villeneuve-Saint-Georges', 'Houilles', 'Viry-Châtillon', 'Plaisir', 'Pontoise', 'Palaiseau', 'Les Mureaux', 'Athis-Mons', 'Saint-Laurent-du-Var', 'Clichy-sous-Bois', 'Trappes', 'Thiais', 'Menton', 'Savigny-le-Temple', 'Yerres', 'Draveil', 'Lambersart', 'Guyancourt', 'Bezons', 'Vigneux-sur-Seine', 'Pierrefitte-sur-Seine', 'Villiers-le-Bel', 'Vallauris', 'Ermont', 'Villiers-sur-Marne', 'Sannois', 'Ris-Orangis', 'Herblay', 'Élancourt', 'Gonesse', 'Rambouillet', 'Taverny', 'Montfermeil', 'Sucy-en-Brie', 'Brunoy', 'Villeneuve-la-Garenne', 'Romainville', 'Miramas', 'Bussy-Saint-Georges', 'Les Ulis', 'Brétigny-sur-Orge', 'Champs-sur-Marne', 'Villeparisis', 'Eaubonne', "Saint-Ouen-l'Aumône", 'Cormeilles-en-Parisis', 'Montgeron', 'Roissy-en-Brie', 'La Madeleine', 'Les Pavillons-sous-Bois', 'Mandelieu-la-Napoule', 'Combs-la-Ville', 'Deuil-la-Barre', 'Longjumeau', 'La Celle-Saint-Cloud', 'Orly', 'Loos', 'Gif-sur-Yvette', 'Montmorency', 'Morsang-sur-Orge', 'La Valette-du-Var', 'Le Mée-sur-Seine', 'Limeil-Brévannes', 'Dammarie-les-Lys', 'Gardanne', 'Lagny-sur-Marne', 'Saint-Michel-sur-Orge', 'Allauch', 'Ozoir-la-Ferrière', 'Wasquehal', 'Mantes-la-Ville', 'Les Pennes-Mirabeau', 'Montigny-lès-Cormeilles', 'Vence', 'Maurepas', 'Le Plessis-Trévise', 'Chilly-Mazarin', 'Mitry-Mory', 'Mougins', 'Villeneuve-le-Roi', 'Chevilly-Larue', "Saint-Cyr-l'École", 'Chennevières-sur-Marne', 'Les Clayes-sous-Bois', 'Soisy-sous-Montmorency', 'Port-de-Bouc', 'Moissy-Cramayel', 'La Crau', 'Éragny', 'Mauguio', 'Osny', 'Jouy-le-Moutier', 'Bonneuil-sur-Marne', 'Boissy-Saint-Léger', 'Limay', 'Vauréal', 'Brie-Comte-Robert', 'Castelnau-le-Lez', 'Orsay', 'Sanary-sur-Mer', 'Lattes', 'Verrières-le-Buisson', 'Noisiel', 'Verneuil-sur-Seine', 'Fos-sur-Mer', 'Carrières-sur-Seine', 'Carrières-sous-Poissy', 'Montesson', 'Fontainebleau', 'Domont', 'Villeneuve-Loubet', 'Juvisy-sur-Orge', 'Le Bourget', 'Saint-Leu-la-Forêt', 'Saint-Brice-sous-Forêt', 'Lognes', 'Avon', 'Montmagny', 'Bouc-Bel-Air', "Bois-d'Arcy", "Berre-l'Étang", 'Arnouville', 'Courcouronnes', 'Méru', 'Beausoleil', 'Mennecy', 'Sainte-Maxime', 'Valbonne', 'Ollioules', 'Fontenay-le-Fleury', 'Saint-Fargeau-Ponthierry', 'Vaires-sur-Marne', 'Villetaneuse', 'Roquebrune-Cap-Martin', 'Roquebrune-sur-Argens', 'Châteauneuf-les-Martigues', 'Saint-Julien-en-Genevois', 'Épinay-sous-Sénart', 'Andrésy', 'Valenton', 'Auriol', 'Voisins-le-Bretonneux', 'Aubergenville', 'Vernouillet', 'Saint-Cyr-sur-Mer', 'Rognac', 'Triel-sur-Seine', 'Saint-André-lez-Lille', 'Solliès-Pont', 'Le Pradet', 'La Queue-en-Brie', 'Carros', 'Gaillard', 'Claye-Souilly', 'Cogolin', 'Chantilly', 'Porto-Vecchio', 'Septèmes-les-Vallons', 'Plan-de-Cuques', 'Vaux-le-Pénil', 'Persan', 'Dugny', 'Arpajon', 'Gex', 'Mouans-Sartoux', 'Épinay-sur-Orge', 'Cuers', 'Trets', 'La Trinité', 'Villepreux', 'Carqueiranne', 'La Londe-les-Maures', 'Ormesson-sur-Marne', 'Biot', 'Villebon-sur-Yvette', 'Bures-sur-Yvette', 'Villecresnes', 'Gouvieux', 'Chanteloup-les-Vignes', 'Chambly', 'Fuveau', 'Lamorlaye', 'Saint-Germain-lès-Arpajon', 'Villeneuve-lès-Maguelone', 'Méry-sur-Oise', 'Ézanville', 'Beaumont-sur-Oise', 'Saint-Genis-Pouilly', 'Bondoufle', 'Cesson', 'Magny-les-Hameaux', 'Crosne', 'Thorigny-sur-Marne', 'Le Beausset', 'Saint-Gély-du-Fesc', 'Gignac-la-Nerthe', 'Fleury-Mérogis', 'Cabriès', 'Meulan-en-Yvelines', 'Montévrain', 'Saint-Jean-de-Védas', 'Beauchamp', 'Groslay', 'Velaux', 'La Farlède', 'Saint-Pierre-du-Perray', 'Roquevaire', 'Pérols', 'Ferney-Voltaire', 'Divonne-les-Bains', 'Bougival', 'La Grande-Motte', 'Venelles', 'Jouy-en-Josas', 'Dammartin-en-Goële', 'Le Crès', 'Tournan-en-Brie', 'Quincy-sous-Sénart', 'Ville-la-Grand', 'Pierrelaye', 'Marcoussis', 'Gretz-Armainvilliers', 'Peymeinade', 'Saint-Rémy-lès-Chevreuse', 'Serris', 'Saint-Chamas', 'Sausset-les-Pins', 'Le Plessis-Bouchard', 'La Colle-sur-Loup', 'Cassis', 'Juvignac', 'Bandol', 'Bormes-les-Mimosas', 'Lésigny', 'Vétraz-Monthoux', 'Écouen', 'Lisses', 'Louveciennes', 'Saint-Germain-lès-Corbeil', 'Émerainville', 'Montlhéry', 'Paray-Vieille-Poste', 'Reignier-Ésery', 'La Ville-du-Bois', 'Contes', 'Pégomas', 'Vert-Saint-Denis', 'Soisy-sur-Seine', 'Cavalaire-sur-Mer', 'Villemoisson-sur-Orge', 'Prévessin-Moëns', 'La Gaude', 'Auvers-sur-Oise', 'Bailly-Romainvilliers', 'Bessancourt', 'Carnoux-en-Provence', 'Gargenville', 'Vaujours', 'Puget-sur-Argens', 'Le Mesnil-Saint-Denis', 'Saint-Victoret', 'Courdimanche', 'Grabels', 'Magny-le-Hongre', 'Limours', 'Linas', 'Longpont-sur-Orge', 'Épône', 'Gournay-sur-Marne', 'Le Mesnil-le-Roi', 'Roquefort-les-Pins', 'Carry-le-Rouet', 'La Penne-sur-Huveaune', 'Fabrègues', 'Saint-Thibault-des-Vignes', 'Courtry', 'Boussy-Saint-Antoine', 'Gémenos', 'Wissous', 'Palavas-les-Flots', 'Ambilly', 'La Bouilladisse', 'Magnanville', 'La Verrière', 'Chambourcy', 'Bouffémont', 'Esbly', 'Chevreuse', 'Nandy', 'Vendargues', 'Cranves-Sales', 'Saint-Mandrier-sur-Mer', 'Rungis', 'Saint-Mitre-les-Remparts', 'Parmain', 'Thoiry', 'Nanteuil-lès-Meaux', 'Simiane-Collongue', "La Cadière-d'Azur", 'Villefranche-sur-Mer', 'Le Lavandou', 'Menucourt', 'Buc', 'Peypin', 'Clapiers', 'Jouars-Pontchartrain', 'Solliès-Toucas', 'Meyreuil', 'Égly', 'Ensuès-la-Redonne', 'Saint-André-de-la-Roche', 'Jacou', 'Villennes-sur-Seine', 'Ablon-sur-Seine', 'Saintry-sur-Seine', 'La Roquette-sur-Siagne', 'Saint-Clément-de-Rivière', 'Quincy-Voisins', 'Roquefort-la-Bédoule', 'Saulx-les-Chartreux', 'Villabé', 'Saint-Zacharie', 'Le Port-Marly', 'Trilport', "Cap-d'Ail", 'Vaux-sur-Seine', 'Mériel', 'Le Coudray-Montceaux', 'Tourrette-Levens', 'Coubron', 'Levens', 'Champagne-sur-Oise', 'Noiseau', 'Prades-le-Lez', 'La Frette-sur-Seine', 'Teyran', 'Issou', 'Mimet', 'Saint-Tropez', 'Coignières', 'Le Rove', 'Mandres-les-Roses', 'Crégy-lès-Meaux', 'Maurecourt', 'Brou-sur-Chantereine', 'Fourqueux', 'Crécy-la-Chapelle', 'Drap', 'Cessy', 'Ceyreste', 'Villenoy', 'Grimaud', 'Le Plessis-Pâté', 'Cruseilles', 'Gréasque', 'Le Thillay', 'Leuville-sur-Orge', 'La Norville', 'Tourrettes-sur-Loup', 'Gattières', 'Le Rouret', 'Coye-la-Forêt', 'Villiers-sur-Orge', 'Collonges-sous-Salève', 'Ornex', 'Juziers', 'Forges-les-Bains', 'Ballainvilliers', 'Beaulieu-sur-Mer', 'Santeny', 'Le Revest-les-Eaux', 'Veigy-Foncenex', 'Boissise-le-Roi', 'Mareil-Marly', 'La Croix-Valmer', 'Sospel', 'Bornel', 'Saint-Germain-sur-Morin', 'Mézières-sur-Seine', 'Saint-Paul-de-Vence', 'Pomponne', 'Montferrier-sur-Lez', 'Saclay', 'Orry-la-Ville', 'Valleiry', 'Bruyères-le-Châtel', 'Montry', 'Colomars', 'Saint-Cergues', 'Fillinges', 'Saint-Savournin', 'Châteauneuf-Grasse', 'Le Tignet', 'Étiolles', 'La Turbie', 'Dampmart', 'Peynier', 'Collégien', 'Porcheville', 'Neauphle-le-Château', 'Auribeau-sur-Siagne', 'La Destrousse', 'Bonne', 'Tigery', 'Bonifacio', 'La Chapelle-en-Serval', 'Le Bar-sur-Loup', 'Margency', 'Gassin', 'Roissy-en-France', 'Frépillon', 'Villiers-Saint-Frédéric', 'Lavérune', 'Pers-Jussy', 'Montlignon', 'Breuillet', "Les Adrets-de-l'Estérel", 'Vulaines-sur-Seine', 'Coupvray', 'Saint-Martin-du-Var', 'Gometz-le-Châtel', 'Champlan', 'Héricy', 'Èze', 'Solliès-Ville', 'Longperrier', 'Belgentier', 'Buchelay', 'Chanteloup-en-Brie', 'Flins-sur-Seine', 'Bernes-sur-Oise', 'Varennes-Jarcy', 'Samoreau', 'Monnetier-Mornex', 'Le Tholonet', 'Archamps', 'Le Mesnil-en-Thelle', 'Péron']
        zoneAbis = ['Paris', 'Chatou', 'Croissy-sur-Seine', 'Le Chesnay', 'Le Pecq', 'Le Vésinet', 'Maisons-Laffitte', 'Marly-le-Roi', 'Rocquencourt', 'Saint-Germain-en-Laye', 'Vélizy-Villacoublay', 'Versailles', 'Viroflay', 'Antony', 'Asnières-sur-Seine', 'Bagneux', 'Bois-Colombes', 'Boulogne-Billancourt', 'Bourg-la-Reine', 'Châtenay-Malabry', 'Châtillon', 'Chaville', 'Clamart', 'Clichy', 'Colombes', 'Courbevoie', 'Fontenay-aux-Roses', 'Garches', 'Issy-les-Moulineaux', 'La Garenne-Colombes', 'Le Plessis-Robinson', 'Levallois-Perret', 'Malakoff', 'Marnes-la-Coquette', 'Meudon', 'Montrouge', 'Nanterre', 'Neuilly-sur-Seine', 'Puteaux', 'Rueil-Malmaison', 'Saint-Cloud', 'Sceaux', 'Sèvres', 'Suresnes', 'Vanves', 'Vaucresson', "Ville-d'Avray", 'Aubervilliers', 'Bagnolet', 'Le Pré-Saint-Gervais', 'Le Raincy', 'Les Lilas', 'Montreuil', 'Neuilly-Plaisance', 'Pantin', 'Saint-Denis', 'Saint-Ouen', 'Villemomble', 'Arcueil', 'Bry-sur-Marne', 'Cachan', 'Charenton-le-Pont', 'Fontenay-sous-Bois', 'Gentilly', 'Ivry-sur-Seine', 'Joinville-le-Pont', "L'Haÿ-les-Roses", 'Le Kremlin-Bicêtre', 'Le Perreux-sur-Marne', 'Maisons-Alfort', 'Nogent-sur-Marne', 'Saint-Mandé', 'Saint-Maur-des-Fossés', 'Saint-Maurice', 'Villejuif', 'Vincennes', 'Enghien-les-Bains']
        zoneB1 = sorted(zoneB1)
        zoneAbis = sorted(zoneAbis)
        zoneA = sorted(zoneA)
        list_total = zoneB1+zoneAbis+zoneA
        list_total = sorted(list_total)
        choix = select("Selectionnez la ville Pinel :", list_total)
        list_dict = {"A" : zoneA,"A bis":zoneAbis,"B1":zoneB1}
        for key, value in list_dict.items():
            if choix in value:
                if key == "A bis":
                    surfaceHabitable = float(input("Votre surface habitable :"))
                    surfaceTerasse = float(input("Votre surface exterieur (balcons, terasse), hors jardin : "))
                    prixAbis = 17.55
                    surfaceTerasse2 = surfaceTerasse/2
                    if(surfaceTerasse2 < 9):
                        surfaceTotale = surfaceHabitable + surfaceTerasse2
                        coeff = (19/surfaceTotale) + 0.7
                        Loyermax = prixAbis*coeff*surfaceTotale
                    if (surfaceTerasse2 > 9):
                        surfaceTerasse3 = 4.5
                        surfaceTotale = surfaceHabitable + surfaceTerasse3
                        coeff = (19/surfaceTotale) + 0.7
                        Loyermax = prixAbis*coeff*surfaceTotale
                if key == "A":
                    surfaceHabitable = float(input("Votre surface habitable :"))
                    surfaceTerasse = float(input("Votre surface exterieur (balcons, terasse), hors jardin : "))
                    prixA = 13.04
                    surfaceTerasse2 = surfaceTerasse/2
                    if(surfaceTerasse2 < 9):
                        surfaceTotale = surfaceHabitable + surfaceTerasse2
                        coeff = (19/surfaceTotale) + 0.7
                        Loyermax = prixA*coeff*surfaceTotale
                    if (surfaceTerasse2 > 9):
                        surfaceTerasse3 = 4.5
                        surfaceTotale = surfaceHabitable + surfaceTerasse3
                        coeff = (19/surfaceTotale) + 0.7
                        Loyermax = prixA*coeff*surfaceTotale
                if key == "B1":
                    surfaceHabitable = float(input("Votre surface habitable :"))
                    surfaceTerasse = float(input("Votre surface exterieur (balcons, terasse), hors jardin : "))    
                    prixB1 = 10.51
                    surfaceTerasse2 = surfaceTerasse/2
                    if(surfaceTerasse2 < 9):
                        surfaceTotale = surfaceHabitable + surfaceTerasse2
                        coeff = (19/surfaceTotale) + 0.7
                        Loyermax = prixB1*coeff*surfaceTotale
                    if (surfaceTerasse2 > 9):
                        surfaceTerasse3 = 4.5
                        surfaceTotale = surfaceHabitable + surfaceTerasse3
                        coeff = (19/surfaceTotale) + 0.7
                        Loyermax = prixB1*coeff*surfaceTotale
            
                put_text("TOTAL À FINANCER").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
                put_table([
                        ["Prix du bien","Frais de notaire","Garantie bancaire","Apport","Prix Total","Surface pondérée","Zone Pinel","Plafond de loyer en euros (hors charges)"],
                        ["{:,.2f}".format(prixDuBien),"{:,.2f}".format(fraisNotaire),"{:,.2f}".format(garantieBancaire),
                        "{:,.2f}".format(Apport),"{:,.2f}".format(prixTotalBien),
                        "{:,.2f}".format(surfaceTotale),key,"{:,.2f}".format(Loyermax)
                        ]
                    ])

        T = str(input("Taux annuel du crédit en % : "))
        T = T.replace(",",".")
        T = float(T)
        N2 = int(input("Durée en années du crédit : "))
        N = N2*12
        AssuDeces = str(input("Taux d'assurance Décès et Invalidité en % :"))
        AssuDeces = AssuDeces.replace(",",".")
        AssuDeces = float(AssuDeces)
        
        liste = []
        liste_loyer = [Loyermax]
        for year in range(1, int((N+12)/12)):
            Loyermax = Loyermax*1.01
            liste.append(Loyermax)
        liste_loyer.extend(liste)
        
        put_text("ÉVOLUTION ANNUEL DU LOYER SUR LES 10 PROCHAINES ANNÉES").style('color: dark; font-size: 20px; font-weight:bold;')
        put_table([
                ["Année 1","Année 2","Année 3","Année 4","Année 5","Année 6","Année 7","Année 8","Année 9","Année 10",
                ],
                [float("{:.2f}".format(liste_loyer[0])),float("{:.2f}".format(liste_loyer[1])),float("{:.2f}".format(liste_loyer[2])),float("{:.2f}".format(liste_loyer[3])),float("{:.2f}".format(liste_loyer[4])),
                float("{:.2f}".format(liste_loyer[5])),float("{:.2f}".format(liste_loyer[6])),float("{:.2f}".format(liste_loyer[7])),float("{:.2f}".format(liste_loyer[8])),float("{:.2f}".format(liste_loyer[9]))]
            ])

        pourcentageRevente = (10*1/100)*prixDuBien
        t = (T / 12) 
        q = 1 + t / 100 # calcul du coefficient multiplicateur associé à une hausse de t%
        M = (q**N * (prixTotalBien) * (1 - q) / (1 - q**N)) + prixTotalBien*((AssuDeces/100)/12)
        I = N * M - prixTotalBien # calcul des intérêts versés
        garantie = (1.5/100)*prixTotalBien
        prixRevente = prixDuBien + prixDuBien*(pourcentageRevente/100)
        
        durée = 108
        DateAcquisition = input("Date d'acquisition du bien (dd-mm-yyyy)")
        DateAcquisition = DateAcquisition.replace("/","-")
        DateLivraison = input("Date de livraison (dd-mm-yyyy)")
        DateLivraison = DateLivraison.replace("/","-")
        date_time_obj = datetime.datetime.strptime(DateLivraison, '%d-%m-%Y')
        if date_time_obj.month == 1:
            date_time_obj = date_time_obj + relativedelta.relativedelta(months=1)
        FinFinancement = date_time_obj + relativedelta.relativedelta(months=N)
        FinDispositifPinel = date_time_obj + relativedelta.relativedelta(months=durée)
        date2 = "31-12-{}".format(date_time_obj.year)
        date3 = datetime.datetime.strptime(date2, '%d-%m-%Y')
        nbreMois = date3.month - date_time_obj.month + 1
        
        put_text("MOMENTS CLÉS").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_table([
                ["Date d'acquisition","Date de livraison","Fin du dispositif Pinel","Fin du financement"],
                [DateAcquisition,DateLivraison,FinDispositifPinel.strftime('%d-%m-%Y'),FinFinancement.strftime('%d-%m-%Y')]
            ])

        
        liste_charges = []
        liste_chargecopro = []
        list_assuranceloyerimpaye = []
        list_fraisdegestion = []
        list_taxefonciere = []
        list_loyerpercus = []
        list_reductionimpots = []
        list_fiscalitefonciere = []
        list_effortepargne = []
        list_interetsemprunts = []
        list_mensualite = []
        list_EffortEpargnePlus = []
        list_EffortEpargneMoins = []

        fraisDeGestion = str(input("Pourcentage des frais de gestions sur votre loyer :"))
        fraisDeGestion = fraisDeGestion.replace(",",".")
        fraisDeGestion = float(fraisDeGestion)
        fraisDeGestion2 = (fraisDeGestion/100)*Loyermax
        assurance = str(input("Pourcentage d'assurance de loyer impayé sur votre loyer :"))
        assurance = assurance.replace(",",".")
        assurance = float(assurance)
        dureeduPinel = int(input("Durée de votre Pinel (Années) :"))

        liste_prixdubien = []
        listeprixdubieninitial = [prixDuBien]
        for year in range(1, int((N+12)/12)):
            prixDuBien = prixDuBien*1.01
            liste_prixdubien.append(prixDuBien)
        listeprixdubieninitial.extend(liste_prixdubien)

        my_new_list = [i * 12 for i in liste_loyer]

        list_taxefonciere = []
        list_assuloyerimpaye = []
        list_chargescopro = []
        list_fraisdegestion = []
        list_mensualite = []
        list_economieImpot = []
        list_total = []

        for j in my_new_list:
            fraisDeGestion2 = (fraisDeGestion/100)*j
            assuranceLoyerImpaye = (assurance/100)*j
            chargecopro = (4/100)*j
            taxeFonciere = (j/12)
            economieImpot = ((2/100)*prixDuBien2)/12
            total = fraisDeGestion2 + assuranceLoyerImpaye + chargecopro + taxeFonciere
            list_taxefonciere.append(taxeFonciere)
            list_assuloyerimpaye.append(assuranceLoyerImpaye)
            list_chargescopro.append(chargecopro)
            list_fraisdegestion.append(fraisDeGestion2)
            list_economieImpot.append(economieImpot*12)
            list_total.append(total)
    
        for x in listeprixdubieninitial:
            M = (q**N * (prixTotalBien) * (1 - q) / (1 - q**N)) + prixTotalBien*((AssuDeces/100)/12)
            list_mensualite.append(M*12)
             

        T2 = T*1/100
        rng = pd.date_range(date_time_obj, periods=N, freq='MS')
        rng.name = "Date"
        df = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
        df.reset_index(inplace=True)
        df.index += 1
        df.index.name = "Periode (Mois)"

        df["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, prixTotalBien)+ prixTotalBien*((AssuDeces/100)/12)
        df["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12,df.index,N, prixTotalBien)
        df["Intérêts"] = -1 * numpy_financial.ipmt(T2/12,df.index, N, prixTotalBien) 
        df = df.round(2)

        df["Capital restant dû"] = 0
        df.loc[1, "Capital restant dû"] = prixTotalBien - df.loc[1, "Capital Amorti"]

        for period in range(2, len(df)+1):
            previous_balance = df.loc[period-1, "Capital restant dû"]
            principal_paid = df.loc[period, "Capital Amorti"]
            
            if previous_balance == 0:
                df.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] == 0
                continue
            elif principal_paid <= previous_balance:
                df.loc[period, "Capital restant dû"] = previous_balance - principal_paid
        
        df["Date"] = pd.to_datetime(df["Date"],format='%d-%m-%Y')
        df.set_index("Date")
        df = df.resample('AS', on='Date').sum()
        #put_html(df.to_html(border = 0))


        df5 = pd.DataFrame({
            "Loyer perçus" : my_new_list,
            "Économie d'impôts":list_economieImpot,
            "Frais de gestion" : list_fraisdegestion,
            "Taxe foncière" : list_taxefonciere,
            "Assurance loyer impayé": list_assuloyerimpaye,
            "Charge de copropriété" : list_chargescopro,
            "Total Charges Locatives" : list_total,
            "Mensualité" : list_mensualite,
            
        })
        

        df5['Taxe foncière'][0:2] = df5['Taxe foncière'][0:2].apply(lambda x: x*(30/100))
        df5.index += 1
        #df5.index.names = ['Periode']
        #df5 = df5.reset_index()

        df5["Économie d'impôts"][1:10] = int((2/100)*prixDuBien2)
        df5["Économie d'impôts"].iloc[0] = 0
        df5["Économie d'impôts"][10:13] = int((1/100)*prixDuBien2)
        df5["Économie d'impôts"][13:] = 0
        df5["Total Charges Locatives"] = df5["Frais de gestion"] + df5["Taxe foncière"] + df5["Assurance loyer impayé"] + df5["Charge de copropriété"]
        df5["Loyer perçus"].iloc[0] = ((df5["Loyer perçus"].iloc[0])/12)*nbreMois
        df5["Frais de gestion"].iloc[0] = ((df5["Frais de gestion"].iloc[0])/12)*nbreMois
        df5["Taxe foncière"].iloc[0] = ((df5["Taxe foncière"].iloc[0])/12)*nbreMois
        df5["Assurance loyer impayé"].iloc[0] = ((df5["Assurance loyer impayé"].iloc[0])/12)*nbreMois
        df5["Charge de copropriété"].iloc[0] = ((df5["Charge de copropriété"].iloc[0])/12)*nbreMois
        df5["Total Charges Locatives"].iloc[0] = ((df5["Total Charges Locatives"].iloc[0])/12)*nbreMois
        df5["Mensualité"].iloc[0] = ((df5["Mensualité"].iloc[0])/12)*nbreMois
        #df5.index += 1 
        df5["Loyer perçus"].iloc[-1] = ((df5["Loyer perçus"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Frais de gestion"].iloc[-1] = ((df5["Frais de gestion"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Taxe foncière"].iloc[-1] = ((df5["Taxe foncière"].iloc[-1])/12)*(12-nbreMois)
        df5["Assurance loyer impayé"].iloc[-1] = ((df5["Assurance loyer impayé"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Charge de copropriété"].iloc[-1] = ((df5["Charge de copropriété"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Total Charges Locatives"].iloc[-1] = ((df5["Total Charges Locatives"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Mensualité"].iloc[-1] = ((df5["Mensualité"].iloc[-1])/12)*(12-nbreMois+1)

        T2 = T*1/100
        
        #df4 = df.set_index(df.index //((N+1)/(N/12))).sum(level = 0)

        #df4.index +=1
        df5["Interêts d'emprunt"] = df["Intérêts"].values
        #df5["Interêts d'emprunt"].iloc[0] = ((df5["Interêts d'emprunt"].iloc[0])/12)*nbreMois
        toutcharges = df5['Taxe foncière'] + df5['Charge de copropriété'] + df5['Assurance loyer impayé'] + df5['Frais de gestion']
        Charges = df5['Total Charges Locatives'] + df5["Interêts d'emprunt"] 

        fiscaliteFonciereMoins = Charges 
        fiscaliteFoncierePlus = df5['Loyer perçus']

        EffortEpargnePlus = df5['Loyer perçus'] + (df5["Économie d'impôts"])
        FiscaliteFonciere = fiscaliteFoncierePlus - fiscaliteFonciereMoins
        fiscaliteFonciere2 = FiscaliteFonciere*((TMI+17.2)/100)
        df5["Fiscalité Foncière"] = fiscaliteFonciere2
        EffortEpargneMoins = df5["Mensualité"] + df5['Total Charges Locatives'] + df5["Fiscalité Foncière"]
        EffortEpargneFinal = EffortEpargnePlus-EffortEpargneMoins
        df5["Recettes"] = EffortEpargnePlus
        df5["Depense"] = EffortEpargneMoins
        df5["Effort d'epargne"] = EffortEpargneFinal
    
        Absolu_effortepargne = abs(EffortEpargneFinal)
            

        pd.options.display.float_format = "{:,.2f}".format 
        #df5 = df5.drop(columns = "Periode" ,axis = 1)
        #df5.index.names = ['Periode (en années)']
        nbreMois = (N+12)/12
        nbreMois = int(nbreMois)
        liste_annne = []
        for i in range(0,nbreMois):
            a = date_time_obj.year + i
            liste_annne.append(a)
        df5["Periode (en années)"] = liste_annne
        df5 = df5.set_index("Periode (en années)")
        #df5 = df5.drop(columns = "index" ,axis = 1)

        df3 = pd.DataFrame({"Financement":['Locataire', "Économie d'impôts", 'Investisseur'], 'Montant':[float("{:.2f}".format(sum(my_new_list[0:dureeduPinel]))), 
        float("{:.0f}".format(sum(df5["Économie d'impôts"][0:dureeduPinel]))),float("{:.2f}".format(sum(Absolu_effortepargne[0:dureeduPinel])))]})
        fig3 = px.pie(df3, values='Montant', names = "Financement", title='Financement de votre opération au terme')
        
        Sum_EffortEpargneMoins = sum(df5["Depense"])
        Sum_EffortEpargnePlus = sum(df5["Recettes"])
        Sum_EffortEpargne = sum(df5["Effort d'epargne"])

        df = pd.DataFrame({"Effort d'épargne":['Entrée', 'Sortie',"Effort d'epargne"], 'Montant':[float("{:.2f}".format(Sum_EffortEpargnePlus)), float("{:.2f}".format(Sum_EffortEpargneMoins)),
        float("{:.2f}".format(Sum_EffortEpargne))]})
        fig = px.bar(df, x="Effort d'épargne", y='Montant',color = "Effort d'épargne", title = "Gain et Perte en trésorerie")
        put_text("CALCUL DE L'EFFORT D'EPARGNE").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_collapse('Voir le tableau', [put_html(df5.to_html(border = 0))])
        
        
        if(dureeduPinel == 9):
            put_text("RECETTES ET DEPENSES MENSUELLES EN MOYENNE PAR MOIS SUR 9 ANS DE PINEL").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
            put_table([
            ['Recettes', put_table([['Loyer perçus', 'Reduction impôts'], 
            ["{:,.0f}".format(math.trunc(sum(df5['Loyer perçus'][0:9])/(dureeduPinel)/12)), "{:,.0f}".format(math.trunc(sum(df5["Économie d'impôts"][0:9])/(dureeduPinel)/12))]]), 
            "Charges" , put_table([['Remboursement du prêt', 'Charges','Fiscalité foncière'], 
            ["{:,.0f}".format(math.trunc(sum(df5["Mensualité"][0:9])/(dureeduPinel)/12)), "{:,.0f}".format(math.trunc(sum(df5['Total Charges Locatives'][0:9])/(dureeduPinel)/12)),
            "{:,.0f}".format(math.trunc(sum(df5["Fiscalité Foncière"][0:9])/(dureeduPinel)/12))]])]
            ])
            put_table([
                    ["Recettes mensuelles", "Dépenses mensuelles"],
                    ["{:,.0f}".format(math.trunc(sum(df5["Recettes"][0:9])/(dureeduPinel)/12)),"{:,.0f}".format(math.trunc(sum(df5["Depense"][0:9])/(dureeduPinel)/12))],
                ])
    
            put_table([
                    ["Votre effort d'epargne"],
                    ["{:,.0f}".format(math.trunc(sum(df5["Effort d'epargne"][0:9])/(dureeduPinel)/12))],
                ])
        elif(dureeduPinel == 12):
            put_text("RECETTES ET DEPENSES MENSUELLES EN MOYENNE PAR MOIS SUR 12 ANS DE PINEL").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
            put_table([
            ['Recettes', put_table([['Loyer perçus', 'Reduction impôts'], 
            ["{:,.0f}".format(math.trunc(sum(df5['Loyer perçus'][0:12])/dureeduPinel)/12), "{:,.0f}".format(math.trunc(sum(df5["Économie d'impôts"][0:12])/dureeduPinel)/12)]]), 
            "Charges" , put_table([['Remboursement du prêt', 'Charges','Fiscalité foncière'], 
            ["{:,.0f}".format(math.trunc(sum(df5["Mensualité"][0:12])/dureeduPinel)/12), "{:,.0f}".format(math.trunc(sum(df5['Total Charges Locatives'][0:12])/dureeduPinel)/12),"{:,.0f}".format(math.trunc(sum(list_fiscalitefonciere[0:12])/dureeduPinel)/12)]])]
            ])
            put_table([
                    ["Recettes mensuelles", "Dépenses mensuelles"],
                    ["{:,.0f}".format(math.trunc(sum(df5["Recettes"][0:12])/dureeduPinel)/12),"{:,.0f}".format(math.trunc(sum(df5["Depense"][0:12])/dureeduPinel)/12)],
                ])
    
            put_table([
                    ["Votre effort d'epargne"],
                    ["{:,.0f}".format(math.trunc(sum(df5["Effort d'epargne"][0:12])/dureeduPinel)/12)],
                ])
        elif(dureeduPinel !=9 or dureeduPinel !=12):
            put_text("RECETTES ET DEPENSES MENSUELLES EN MOYENNE PAR MOIS").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
            put_table([
            ['Recettes', put_table([['Loyer perçus', 'Reduction impôts'], 
            ["{:,.0f}".format(math.trunc(sum(df5['Loyer perçus'])/dureeduPinel)/12), "{:,.0f}".format(math.trunc(sum(df5["Économie d'impôts"])/dureeduPinel)/12)]]), 
            "Charges" , put_table([['Remboursement du prêt', 'Charges','Fiscalité foncière'], 
            ["{:,.0f}".format(math.trunc(sum(df5["Mensualité"])/dureeduPinel)/12), "{:,.0f}".format(math.trunc(sum(df5['Total Charges Locatives'])/dureeduPinel)/12),"{:,.0f}".format(sum(list_fiscalitefonciere)/dureeduPinel)/12]])]
            ])
            put_table([
                    ["Recettes mensuelles", "Dépenses mensuelles"],
                    ["{:,.0f}".format(math.trunc(sum(df5["Recettes"])/dureeduPinel)/12),"{:,.2f}".format(math.trunc(sum(df5["Depense"])/dureeduPinel)/12)],
                ])
    
            put_table([
                    ["Votre effort d'epargne"],
                    ["{:,.0f}".format(math.trunc(sum(df5["Effort d'epargne"])/dureeduPinel)/12)],
                ])

        put_text("RENTABILITÉ LOCATIVE DE L'INVESTISSEMENT").style('color: dark; font-size: 20px; font-weight:bold;')
        renta = ((Loyermax*12)/prixDuBien)*100
        if(renta <3):
            put_table([
                ["Rentabilité sur investissement"],
                ["{:.2f}%".format(renta),style(put_text('Mauvaise rentabilité'), 'color:red')],
            ])
        else:
            put_table([
                ["Rentabilité sur investissement"],
                ["{:.2f}%".format(renta),style(put_text('Bonne rentabilité'), 'color:green')],
            ])
        
        
        html = fig3.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)

        put_text("PREVISIONNEL DU PRIX DE VOTRE BIEN").style('color: dark; font-size: 20px; font-weight:bold;')
        prixPireCas = listeprixdubieninitial[0]
        prixMoyenCas = listeprixdubieninitial[0] + 0.05*listeprixdubieninitial[0]
        prixMeilleurCas = listeprixdubieninitial[0] + 0.1*listeprixdubieninitial[0]
        put_table([
                ["PIRE DES CAS","CAS MOYEN","MEILLEUR CAS"],
                ["{:,.0f}".format(math.trunc(prixPireCas)),"{:,.0f}".format(math.trunc(prixMoyenCas)),"{:,.0f}".format(math.trunc(prixMeilleurCas))],
                ["0%","5%","10%"],
            ])

        put_text("ÉVOLUTION DU PRIX DU BIEN SUR LES 10 PREMIÈRES ANNÉES").style('color: dark; font-size: 20px; font-weight:bold;')
        put_table([
                ["Année 1","Année 2","Année 3","Année 4","Année 5","Année 6","Année 7","Année 8","Année 9","Année 10",
                ],
                ["{:,.0f}".format(math.trunc(listeprixdubieninitial[0])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[1])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[2])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[3])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[4])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[5])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[6])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[7])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[8])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[9]))]
            ])

        T2 = T*1/100
        rng = pd.date_range(date_time_obj, periods=N, freq='MS')
        rng.name = "Date"
        df8 = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
        df8.reset_index(inplace=True)
        df8.index += 1
        df8.index.name = "Periode (Mois)"

        df8["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, prixTotalBien)+ prixTotalBien*((AssuDeces/100)/12)
        df8["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12,df8.index,N, prixTotalBien)
        df8["Intérêts"] = -1 * numpy_financial.ipmt(T2/12,df8.index, N, prixTotalBien) 
        df8 = df8.round(2)

        df8["Capital restant dû"] = 0
        df8.loc[1, "Capital restant dû"] = prixTotalBien - df8.loc[1, "Capital Amorti"]

        for period in range(2, len(df8)+1):
            previous_balance = df8.loc[period-1, "Capital restant dû"]
            principal_paid = df8.loc[period, "Capital Amorti"]
            
            if previous_balance == 0:
                df8.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] == 0
                continue
            elif principal_paid <= previous_balance:
                df8.loc[period, "Capital restant dû"] = previous_balance - principal_paid
        
        df8["Date"] = pd.to_datetime(df8["Date"],format='%d-%m-%Y')
        
        T2 = T*1/100
        liste_date = []
        x = list(rrule(freq=YEARLY, count=(N+12)/12, dtstart=df8.iloc[0]["Date"]))
        for ld in x:
            liste_date.append(ld)
        df_somme = pd.DataFrame(
            {
        'Prix du bien' : listeprixdubieninitial,
        "Date" :liste_date, 
            })
        

        products_dict = dict(zip(df8.Date,df8["Capital restant dû"]))
        df_somme["Capital restant dû"] = df_somme["Date"].map(products_dict)
        df_somme.index += 1
        df_somme.index.name = "Periode (Année)"
        df_somme["Somme disponible en cas de revente"] = df_somme["Prix du bien"] - df_somme["Capital restant dû"] 
        df_somme = df_somme.drop(columns="Date", axis = 1)
        df_somme["Periode (en années)"] = liste_annne
        df_somme = df_somme.set_index("Periode (en années)")
        df_somme["Capital restant dû"].iloc[-1] = 0
        df_somme["Somme disponible en cas de revente"] = df_somme["Prix du bien"] - df_somme["Capital restant dû"] 
        
        put_text("SOMME DISPONIBLE EN CAS DE REVENTE").style('color: dark; font-size: 20px; font-weight:bold;')
        put_collapse('Voir le tableau', [put_html(df_somme.to_html(border = 0))])
        put_text("TABLEAU D'AMORTISSEMENT").style('color: dark; font-size: 20px; font-weight:bold;')
        put_collapse('Voir le tableau', [put_html(df8.to_html(border = 0))])
        
        

        # put_markdown("___")
        # if choice == 'Generate':
        #     file_name = input('Name of pdf file?')
        #     generate_pdf(df, file_name)
        #     put_markdown("**PDF file generated**")
        # else:
        #     put_markdown("PDF not generated")
            


    if (choix == "14 - Simulateur Malraux"):  
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        put_markdown('# SIMULATION MALRAUX')
        pd.options.display.float_format = "{:,.2f}".format 
        
        ############
        revenu = float(input("Quel est le revenu net annuel du foyer : "))
        revenu2 = 0.9*revenu
        if revenu2 > 126520:
            revenuAvantAbbatement = revenu - 12652
        else :
            revenuAvantAbbatement = 0.9*revenu
        statut = saisirStatutFamilial()
        npers = int(input("Nombre de personnes a charge? "))
        if statut == CONCUBINAGE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
        ###########CELIBATAIRE
        if statut == CELIBATAIRE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
                
        ############MARIE
        
        if statut == MARIE:
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 52140:
                    impots = (revenuAvantAbbatement*0.11)-2249.50
                    TMI = 11
                if 52140 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-12156.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-28556
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-41382.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2.5:
                if revenuAvantAbbatement < 25563:
                    impots = 0
                    TMI = 0
                if 25563 < revenuAvantAbbatement <= 57561:
                    impots = (revenuAvantAbbatement*0.11)-2811.88
                    TMI = 11
                if 57562 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-13748.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-30148
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-42974.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 62978:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 62979 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-15340.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-31740
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-44566.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 73818:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 73819 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-18524.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-34924
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-47750.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==5:
                if revenuAvantAbbatement < 51125:
                    impots = 0
                    TMI = 0
                if 51125 < revenuAvantAbbatement <= 84655:
                    impots = (revenuAvantAbbatement*0.11)-5623.75
                    TMI = 11
                if 84656 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-21708.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-38108
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-50934.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==6:
                if revenuAvantAbbatement < 61350:
                    impots = 0
                    TMI = 0
                if 61350 < revenuAvantAbbatement <= 94495:
                    impots = (revenuAvantAbbatement*0.11)-6748.5
                    TMI = 11
                if 94496 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-24892.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-40292
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-54118.88
                    TMI = 45
     
        afficherFicheImpots(revenuAvantAbbatement, statut, npers,TMI,impots)

        prixDuBien = float(input("Montant du foncier : "))
        travaux = float(input("Le prix de vos travaux : "))
        Apport = float(input("Votre apport : "))
        fraisNotaire = (7.5/100)*prixDuBien
        prixDuBien2 = prixDuBien + fraisNotaire + travaux
        garantieBancaire = (1.5/100)*(prixDuBien+travaux)
        prixTotalBien = prixDuBien2 + garantieBancaire - Apport
        prixFoncierTravaux = prixDuBien + travaux
        
        Loyermax = float(input("Votre loyer :"))

        put_text("TOTAL À FINANCER").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_table([
                ["Prix du foncier","Travaux","Frais de notaire","Garantie bancaire","Apport","Prix Total","Votre loyer"],
                ["{:,.2f}".format(prixDuBien),"{:,.2f}".format(travaux),"{:,.2f}".format(fraisNotaire),"{:,.2f}".format(garantieBancaire),
                "{:,.2f}".format(Apport),"{:,.2f}".format(prixTotalBien),"{:,.2f}".format(Loyermax)
                ]
            ])
        
            
        T = str(input("Taux annuel du crédit en % : "))
        T = T.replace(",",".")
        T = float(T)
        N2 = int(input("Durée en années du crédit :"))
        N = N2*12
        AssuDeces = str(input("Taux d'assurance Décès et Invalidité en % :"))
        AssuDeces = AssuDeces.replace(",",".")
        AssuDeces = float(AssuDeces)

        liste = []
        liste_loyer = [Loyermax]
        for year in range(1, int((N+12)/12)):
            Loyermax = Loyermax*1.01
            liste.append(Loyermax)
        liste_loyer.extend(liste)

        put_text("ÉVOLUTION ANNUEL DU LOYER SUR LES 10 PROCHAINES ANNÉES").style('color: dark; font-size: 20px; font-weight:bold;')
        put_table([
                ["Année 1","Année 2","Année 3","Année 4","Année 5","Année 6","Année 7","Année 8","Année 9"
                ],
                [float("{:.2f}".format(liste_loyer[0])),float("{:.2f}".format(liste_loyer[1])),float("{:.2f}".format(liste_loyer[2])),float("{:.2f}".format(liste_loyer[3])),float("{:.2f}".format(liste_loyer[4])),
                float("{:.2f}".format(liste_loyer[5])),float("{:.2f}".format(liste_loyer[6])),float("{:.2f}".format(liste_loyer[7])),float("{:.2f}".format(liste_loyer[8]))]
            ])

        
        pourcentageRevente = (10*1/100)*prixDuBien
        t = (T / 12) 
        q = 1 + t / 100 # calcul du coefficient multiplicateur associé à une hausse de t%
        M = (q**N * (prixTotalBien) * (1 - q) / (1 - q**N)) + prixTotalBien*((AssuDeces/100)/12)
        #print("Votre mensualité sera de {0:.2f} euros".format(M))
        I = N * M - prixTotalBien # calcul des intérêts versés
        garantie = (1.5/100)*prixTotalBien
        #put_text(f"Votre mensulaité sera de {M} euros")
        #put_text(f"Le montant total des intérêts versés sera de {I} euros")
        prixRevente = prixDuBien + prixDuBien*(pourcentageRevente/100)

        durée = 108
        #Année = N/12
        DateAcquisition = input("Date d'acquisition du bien (dd-mm-yyyy)")
        DateAcquisition = DateAcquisition.replace("/","-")
        DateLivraison = input("Date de livraison (dd-mm-yyyy)")
        DateLivraison = DateLivraison.replace("/","-")
        date_time_obj = datetime.datetime.strptime(DateLivraison, '%d-%m-%Y')
        if date_time_obj.month == 1:
            date_time_obj = date_time_obj + relativedelta.relativedelta(months=1)
        FinFinancement = date_time_obj + relativedelta.relativedelta(months=N)
        FinDispositifMalraux = date_time_obj + relativedelta.relativedelta(months=durée)
        date2 = "31-12-{}".format(date_time_obj.year)
        date3 = datetime.datetime.strptime(date2, '%d-%m-%Y')
        nbreMois = date3.month - date_time_obj.month + 1


        put_text("MOMENTS CLÉS").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_table([
                ["Date d'acquisition","Date de livraison","Fin du dispositif Malraux","Fin du financement"],
                [DateAcquisition,DateLivraison,FinDispositifMalraux.strftime('%d-%m-%Y'),FinFinancement.strftime('%d-%m-%Y')]
            ])

        liste_charges = []
        liste_chargecopro = []
        list_assuranceloyerimpaye = []
        list_fraisdegestion = []
        list_taxefonciere = []
        list_loyerpercus = []
        list_reductionimpots = []
        list_fiscalitefonciere = []
        list_effortepargne = []
        list_interetsemprunts = []
        list_mensualite = []
        list_EffortEpargnePlus = []
        list_EffortEpargneMoins = []

        fraisDeGestion = str(input("Pourcentage des frais de gestions sur votre loyer :"))
        fraisDeGestion = fraisDeGestion.replace(",",".")
        fraisDeGestion = float(fraisDeGestion)
        fraisDeGestion2 = (fraisDeGestion/100)*Loyermax
        assurance = str(input("Pourcentage d'assurance de loyer impayé sur votre loyer :"))
        assurance = assurance.replace(",",".")
        assurance = float(assurance)
        dureeMalraux = 9

        liste_prixdubien = []
        listeprixdubieninitial = [prixFoncierTravaux]
        for year in range(1, int((N+12)/12)):
            prixFoncierTravaux = prixFoncierTravaux*1.01
            liste_prixdubien.append(prixFoncierTravaux)
        listeprixdubieninitial.extend(liste_prixdubien)

        my_new_list = [i * 12 for i in liste_loyer]


        list_taxefonciere = []
        list_assuloyerimpaye = []
        list_chargescopro = []
        list_fraisdegestion = []
        list_mensualite = []
        list_economieImpot = []
        list_total = []

        for j in my_new_list:
            fraisDeGestion2 = (fraisDeGestion/100)*j
            assuranceLoyerImpaye = (assurance/100)*j
            chargecopro = (4/100)*j
            taxeFonciere = (j/12)
            economieImpot = ((30/100)*travaux)/4
            total = fraisDeGestion2 + assuranceLoyerImpaye + chargecopro + taxeFonciere
            list_taxefonciere.append(taxeFonciere)
            list_assuloyerimpaye.append(assuranceLoyerImpaye)
            list_chargescopro.append(chargecopro)
            list_fraisdegestion.append(fraisDeGestion2)
            list_economieImpot.append(economieImpot)
            list_total.append(total)

        for x in listeprixdubieninitial:
            M = (q**N * (prixTotalBien) * (1 - q) / (1 - q**N)) + prixTotalBien*((AssuDeces/100)/12)
            list_mensualite.append(M*12)
        
        T2 = T*1/100
        rng = pd.date_range(date_time_obj, periods=N, freq='MS')
        rng.name = "Date"
        df = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
        df.reset_index(inplace=True)
        df.index += 1
        df.index.name = "Periode (Mois)"

        df["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, prixTotalBien)+ prixTotalBien*((AssuDeces/100)/12)
        df["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12,df.index,N, prixTotalBien)
        df["Intérêts"] = -1 * numpy_financial.ipmt(T2/12,df.index, N, prixTotalBien) 
        df = df.round(2)

        df["Capital restant dû"] = 0
        df.loc[1, "Capital restant dû"] = prixTotalBien - df.loc[1, "Capital Amorti"]

        for period in range(2, len(df)+1):
            previous_balance = df.loc[period-1, "Capital restant dû"]
            principal_paid = df.loc[period, "Capital Amorti"]
            
            if previous_balance == 0:
                df.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] == 0
                continue
            elif principal_paid <= previous_balance:
                df.loc[period, "Capital restant dû"] = previous_balance - principal_paid
        
        df["Date"] = pd.to_datetime(df["Date"],format='%d-%m-%Y')
        df.set_index("Date")
        df = df.resample('AS', on='Date').sum()

        df5 = pd.DataFrame({
            "Loyer perçus" : my_new_list,
            "Économie d'impôts":list_economieImpot,
            "Frais de gestion" : list_fraisdegestion,
            "Taxe foncière" : list_taxefonciere,
            "Assurance loyer impayé": list_assuloyerimpaye,
            "Charge de copropriété" : list_chargescopro,
            "Total Charges Locatives" : list_total,
            "Mensualité" : list_mensualite,
            
        })
        
        df5.index += 1 
        #df5.index.names = ['Periode']
        #df5 = df5.reset_index()

        
        #df5["Économie d'impôts"][0:4] = df5["Économie d'impôts"][0:4].apply(lambda x: x*((30/100)*travaux)/4)
        df5["Économie d'impôts"][4:] = 0
        df5["Total Charges Locatives"] = df5["Frais de gestion"] + df5["Taxe foncière"] + df5["Assurance loyer impayé"] + df5["Charge de copropriété"]
        df5["Loyer perçus"].iloc[0] = ((df5["Loyer perçus"].iloc[0])/12)*nbreMois
        df5["Frais de gestion"].iloc[0] = ((df5["Frais de gestion"].iloc[0])/12)*nbreMois
        df5["Taxe foncière"].iloc[0] = ((df5["Taxe foncière"].iloc[0])/12)*nbreMois
        df5["Assurance loyer impayé"].iloc[0] = ((df5["Assurance loyer impayé"].iloc[0])/12)*nbreMois
        df5["Charge de copropriété"].iloc[0] = ((df5["Charge de copropriété"].iloc[0])/12)*nbreMois
        df5["Total Charges Locatives"].iloc[0] = ((df5["Total Charges Locatives"].iloc[0])/12)*nbreMois
        df5["Mensualité"].iloc[0] = ((df5["Mensualité"].iloc[0])/12)*nbreMois
        df5["Total Charges Locatives"] = df5["Frais de gestion"] + df5["Taxe foncière"] + df5["Assurance loyer impayé"] + df5["Charge de copropriété"]
        #df5.index += 1 
        df5["Loyer perçus"].iloc[-1] = ((df5["Loyer perçus"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Frais de gestion"].iloc[-1] = ((df5["Frais de gestion"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Taxe foncière"].iloc[-1] = ((df5["Taxe foncière"].iloc[-1])/12)*(12-nbreMois)
        df5["Assurance loyer impayé"].iloc[-1] = ((df5["Assurance loyer impayé"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Charge de copropriété"].iloc[-1] = ((df5["Charge de copropriété"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Total Charges Locatives"].iloc[-1] = ((df5["Total Charges Locatives"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Mensualité"].iloc[-1] = ((df5["Mensualité"].iloc[-1])/12)*(12-nbreMois+1)

        T2 = T*1/100
        #df4 = df.set_index(df.index //((N+1)/(N/12))).sum(level = 0)
        #df4.index +=1
        df5["Interêts d'emprunt"] = df["Intérêts"].values
        #df5["Interêts d'emprunt"].iloc[0] = ((df5["Interêts d'emprunt"].iloc[0])/12)*nbreMois
        toutcharges = df5['Taxe foncière'] + df5['Charge de copropriété'] + df5['Assurance loyer impayé'] + df5['Frais de gestion']
        Charges = df5['Total Charges Locatives'] + df5["Interêts d'emprunt"] 

        fiscaliteFonciereMoins = Charges 
        fiscaliteFoncierePlus = df5['Loyer perçus']

        EffortEpargnePlus = df5['Loyer perçus'] + (df5["Économie d'impôts"])
        FiscaliteFonciere = fiscaliteFoncierePlus - fiscaliteFonciereMoins
        fiscaliteFonciere2 = FiscaliteFonciere*((TMI+17.2)/100)
        df5["Fiscalité Foncière"] = fiscaliteFonciere2
        EffortEpargneMoins = df5["Mensualité"] + df5['Total Charges Locatives'] + df5["Fiscalité Foncière"]
        EffortEpargneFinal = EffortEpargnePlus-EffortEpargneMoins
        df5["Recettes"] = EffortEpargnePlus
        df5["Depense"] = EffortEpargneMoins
        df5["Effort d'epargne"] = EffortEpargneFinal
        
        Absolu_effortepargne = abs(EffortEpargneFinal)
            

        pd.options.display.float_format = "{:,.2f}".format 
        nbreMois = (N+12)/12
        nbreMois = int(nbreMois)
        liste_annne = []
        for i in range(0,nbreMois):
            a = date_time_obj.year + i
            liste_annne.append(a)
        df5["Periode (en années)"] = liste_annne
        df5 = df5.set_index("Periode (en années)")

        df3 = pd.DataFrame({"Financement":['Locataire', "Économie d'impôts", 'Investisseur'], 'Montant':[float("{:.2f}".format(sum(my_new_list[0:dureeMalraux]))), 
        float("{:.0f}".format(sum(df5["Économie d'impôts"][0:dureeMalraux]))),float("{:.2f}".format(sum(Absolu_effortepargne[0:dureeMalraux])))]})
        fig3 = px.pie(df3, values='Montant', names = "Financement", title='Financement de votre opération au terme')
        
        Sum_EffortEpargneMoins = sum(df5["Depense"])
        Sum_EffortEpargnePlus = sum(df5["Recettes"])
        Sum_EffortEpargne = sum(df5["Effort d'epargne"])

        df = pd.DataFrame({"Effort d'épargne":['Entrée', 'Sortie',"Effort d'epargne"], 'Montant':[float("{:.2f}".format(Sum_EffortEpargnePlus)), float("{:.2f}".format(Sum_EffortEpargneMoins)),
        float("{:.2f}".format(Sum_EffortEpargne))]})
        fig = px.bar(df, x="Effort d'épargne", y='Montant',color = "Effort d'épargne", title = "Gain et Perte en trésorerie")
        put_text("CALCUL DE L'EFFORT D'EPARGNE").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_collapse('Voir le tableau', [put_html(df5.to_html(border = 0))])
        
        
    
        put_text("RECETTES ET DEPENSES MENSUELLES EN MOYENNE PAR MOIS SUR 9 ANS DE MALRAUX").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_table([
        ['Recettes', put_table([['Loyer perçus', 'Reduction impôts'], 
        ["{:,.0f}".format(math.trunc(sum(df5['Loyer perçus'][0:9])/(dureeMalraux)/12)), "{:,.0f}".format(math.trunc(sum(df5["Économie d'impôts"][0:9])/(dureeMalraux)/12))]]), 
        "Charges" , put_table([['Remboursement du prêt', 'Charges','Fiscalité foncière'], 
        ["{:,.0f}".format(math.trunc(sum(df5["Mensualité"][0:9])/(dureeMalraux)/12)), "{:,.0f}".format(math.trunc(sum(df5['Total Charges Locatives'][0:9])/(dureeMalraux)/12)),
        "{:,.0f}".format(math.trunc(sum(df5["Fiscalité Foncière"][0:9])/(dureeMalraux)/12))]])]
        ])
        put_table([
                ["Recettes mensuelles", "Dépenses mensuelles"],
                ["{:,.0f}".format(math.trunc(sum(df5["Recettes"][0:9])/(dureeMalraux)/12)),"{:,.0f}".format(math.trunc(sum(df5["Depense"][0:9])/(dureeMalraux)/12))],
            ])

        put_table([
                ["Votre effort d'epargne"],
                ["{:,.0f}".format(math.trunc(sum(df5["Effort d'epargne"][0:9])/(dureeMalraux)/12))],
            ])
    
        put_text("RENTABILITÉ LOCATIVE DE L'INVESTISSEMENT").style('color: dark; font-size: 20px; font-weight:bold;')
        renta = ((Loyermax*12)/prixDuBien)*100
        if(renta <3):
            put_table([
                ["Rentabilité sur investissement"],
                ["{:.2f}%".format(renta),style(put_text('Mauvaise rentabilité'), 'color:red')],
            ])
        else:
            put_table([
                ["Rentabilité sur investissement"],
                ["{:.2f}%".format(renta),style(put_text('Bonne rentabilité'), 'color:green')],
            ])
        
        
        html = fig3.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)

        put_text("PREVISIONNEL DU PRIX DE VOTRE BIEN").style('color: dark; font-size: 20px; font-weight:bold;')
        prixPireCas = listeprixdubieninitial[0]
        prixMoyenCas = listeprixdubieninitial[0] + 0.05*listeprixdubieninitial[0]
        prixMeilleurCas = listeprixdubieninitial[0] + 0.1*listeprixdubieninitial[0]
        put_table([
                ["PIRE DES CAS","CAS MOYEN","MEILLEUR CAS"],
                ["{:,.0f}".format(math.trunc(prixPireCas)),"{:,.0f}".format(math.trunc(prixMoyenCas)),"{:,.0f}".format(math.trunc(prixMeilleurCas))],
                ["0%","5%","10%"],
            ])

        put_text("ÉVOLUTION DU PRIX DU BIEN SUR LES 10 PREMIÈRES ANNÉES").style('color: dark; font-size: 20px; font-weight:bold;')
        put_table([
                ["Année 1","Année 2","Année 3","Année 4","Année 5","Année 6","Année 7","Année 8","Année 9","Année 10",
                ],
                ["{:,.0f}".format(math.trunc(listeprixdubieninitial[0])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[1])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[2])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[3])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[4])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[5])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[6])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[7])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[8])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[9]))]
            ])

        T2 = T*1/100
        rng = pd.date_range(date_time_obj, periods=N, freq='MS')
        rng.name = "Date"
        df8 = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
        df8.reset_index(inplace=True)
        df8.index += 1
        df8.index.name = "Periode (Mois)"

        df8["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, prixTotalBien)+ prixTotalBien*((AssuDeces/100)/12)
        df8["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12,df8.index,N, prixTotalBien)
        df8["Intérêts"] = -1 * numpy_financial.ipmt(T2/12,df8.index, N, prixTotalBien) 
        df8 = df8.round(2)

        df8["Capital restant dû"] = 0
        df8.loc[1, "Capital restant dû"] = prixTotalBien - df8.loc[1, "Capital Amorti"]

        for period in range(2, len(df8)+1):
            previous_balance = df8.loc[period-1, "Capital restant dû"]
            principal_paid = df8.loc[period, "Capital Amorti"]
            
            if previous_balance == 0:
                df8.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] == 0
                continue
            elif principal_paid <= previous_balance:
                df8.loc[period, "Capital restant dû"] = previous_balance - principal_paid
        
        df8["Date"] = pd.to_datetime(df8["Date"],format='%d-%m-%Y')
        
        T2 = T*1/100
        liste_date = []
        x = list(rrule(freq=YEARLY, count=(N+12)/12, dtstart=df8.iloc[0]["Date"]))
        for ld in x:
            liste_date.append(ld)
        df_somme = pd.DataFrame(
            {
        'Prix du bien' : listeprixdubieninitial,
        "Date" :liste_date, 
            })
        

        products_dict = dict(zip(df8.Date,df8["Capital restant dû"]))
        df_somme["Capital restant dû"] = df_somme["Date"].map(products_dict)
        df_somme.index += 1
        df_somme.index.name = "Periode (Année)"
        df_somme["Somme disponible en cas de revente"] = df_somme["Prix du bien"] - df_somme["Capital restant dû"] 
        df_somme = df_somme.drop(columns="Date", axis = 1)
        df_somme["Periode (en années)"] = liste_annne
        df_somme = df_somme.set_index("Periode (en années)")
        df_somme["Capital restant dû"].iloc[-1] = 0
        df_somme["Somme disponible en cas de revente"] = df_somme["Prix du bien"] - df_somme["Capital restant dû"] 

        
        put_text("SOMME DISPONIBLE EN CAS DE REVENTE").style('color: dark; font-size: 20px; font-weight:bold;')
        put_collapse('Voir le tableau', [put_html(df_somme.to_html(border = 0))])
        put_text("TABLEAU D'AMORTISSEMENT").style('color: dark; font-size: 20px; font-weight:bold;')
        put_collapse('Voir le tableau', [put_html(df8.to_html(border = 0))])

    if (choix == "15 - Simulateur meublé à l'amortissement"):  
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")  
        put_markdown("# SIMULATION MEUBLÉ À L'AMORTISSEMENT")
        #revenu = float(input("Revenu global imposable (en euros)? ")) 
        #statut = saisirStatutFamilial()
        #revenuAvantAbattement = (0.9/100)*revenu
        #npers = int(input("Nombre de personnes a charge? "))
        #afficherFicheImpots2(revenu, statut, npers)
        #######PRIX DU BIEN ET LOYER
        #nbrePart = saisirStatutFamilial()
        
        ############
        
        revenu = float(input("Quel est le revenu net annuel du foyer : "))
        revenu2 = 0.9*revenu
        if revenu2 > 126520:
            revenuAvantAbbatement = revenu - 12652
        else :
            revenuAvantAbbatement = 0.9*revenu
        statut = saisirStatutFamilial()
        npers = int(input("Nombre de personnes a charge? "))
        if statut == CONCUBINAGE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
        ###########CELIBATAIRE
        if statut == CELIBATAIRE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
                
        ############MARIE
        
        if statut == MARIE:
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 52140:
                    impots = (revenuAvantAbbatement*0.11)-2249.50
                    TMI = 11
                if 52140 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-12156.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-28556
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-41382.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2.5:
                if revenuAvantAbbatement < 25563:
                    impots = 0
                    TMI = 0
                if 25563 < revenuAvantAbbatement <= 57561:
                    impots = (revenuAvantAbbatement*0.11)-2811.88
                    TMI = 11
                if 57562 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-13748.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-30148
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-42974.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 62978:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 62979 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-15340.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-31740
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-44566.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 73818:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 73819 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-18524.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-34924
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-47750.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==5:
                if revenuAvantAbbatement < 51125:
                    impots = 0
                    TMI = 0
                if 51125 < revenuAvantAbbatement <= 84655:
                    impots = (revenuAvantAbbatement*0.11)-5623.75
                    TMI = 11
                if 84656 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-21708.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-38108
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-50934.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==6:
                if revenuAvantAbbatement < 61350:
                    impots = 0
                    TMI = 0
                if 61350 < revenuAvantAbbatement <= 94495:
                    impots = (revenuAvantAbbatement*0.11)-6748.5
                    TMI = 11
                if 94496 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-24892.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-40292
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-54118.88
                    TMI = 45
       
        afficherFicheImpots(revenuAvantAbbatement, statut, npers,TMI,impots)



        #############
        
        prixDuBien = float(input("Montant du bien : "))
        statut2 = '.'
        neufOuAncien = input("Votre appartement est dans un immeuble neuf ou ancien (n/a) :")[0]
        Apport = float(input("Votre apport :"))
        if neufOuAncien == "N" or neufOuAncien == "n":
            statut2 = NEUF
        else:
            statut2 = ANCIEN
        if (statut2 == NEUF):
            fraisNotaire = (2.5/100)*prixDuBien
        if (statut2 == ANCIEN):
            fraisNotaire = (7.5/100)*prixDuBien
        prixDuBien2 = prixDuBien + fraisNotaire
        garantieBancaire = (1.5/100)*prixDuBien
        prixTotalBien = prixDuBien2 + garantieBancaire - Apport
        prixBati = (85/100)*prixDuBien
        prixFoncier = (15/100)*prixDuBien
        ######SURFACE
        Loyermax = str(input("Entrez la valeur de votre loyer :"))
        Loyermax = Loyermax.replace(",",".")
        Loyermax = float(Loyermax)
        fraisDeGestion = str(input("Pourcentage des frais de gestions sur votre loyer :"))
        fraisDeGestion = fraisDeGestion.replace(",",".")
        fraisDeGestion = float(fraisDeGestion)
        fraisDeGestion2 = (fraisDeGestion/100)*Loyermax
        assurance = str(input("Pourcentage d'assurance de loyer impayé sur votre loyer :"))
        assurance = assurance.replace(",",".")
        assurance = float(assurance)
        assuranceLoyerImpaye = (assurance/100)*Loyermax
        chargecopro = (4/100)*Loyermax
        taxeFonciere = Loyermax/12
        toutcharges = taxeFonciere + chargecopro + assuranceLoyerImpaye + fraisDeGestion2
        #test_impotFinal()
        put_text("TOTAL À FINANCER").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_table([
                ["Prix du bâti","Prix du Foncier","Frais de notaire","Garantie bancaire","Apport","Prix Total","Votre loyer"],
                [float("{:.2f}".format(prixBati)),float("{:.2f}".format(prixFoncier)),float("{:.2f}".format(fraisNotaire)),
                float("{:.2f}".format(garantieBancaire)),float("{:.2f}".format(Apport)),float("{:.2f}".format(prixTotalBien)),float("{:.2f}".format(Loyermax))
                ]
            ])

        T = str(input("Taux annuel du crédit en % : "))
        T = T.replace(",",".")
        T = float(T)
        N2 = int(input("Durée en années du crédit :"))
        N = N2*12
        AssuDeces = str(input("Taux d'assurance Décès et Invalidité en % :"))
        AssuDeces = AssuDeces.replace(",",".")
        AssuDeces = float(AssuDeces)

        liste = []
        liste_loyer = [Loyermax]
        for year in range(1, int((N+12)/12)):
            Loyermax = Loyermax*1.01
            liste.append(Loyermax)
        liste_loyer.extend(liste)

        put_text("ÉVOLUTION ANNUEL DU LOYER SUR LES 10 PROCHAINES ANNÉES").style('color: dark; font-size: 20px; font-weight:bold;')
        put_table([
                ["Année 1","Année 2","Année 3","Année 4","Année 5","Année 6","Année 7","Année 8","Année 9","Année 10"
                ],
                [float("{:.2f}".format(liste_loyer[0])),float("{:.2f}".format(liste_loyer[1])),float("{:.2f}".format(liste_loyer[2])),float("{:.2f}".format(liste_loyer[3])),float("{:.2f}".format(liste_loyer[4])),
                float("{:.2f}".format(liste_loyer[5])),float("{:.2f}".format(liste_loyer[6])),float("{:.2f}".format(liste_loyer[7])),float("{:.2f}".format(liste_loyer[8])),float("{:.2f}".format(liste_loyer[9]))]
            ])

        
        pourcentageRevente = (10*1/100)*prixDuBien
        t = (T / 12) 
        q = 1 + t / 100 # calcul du coefficient multiplicateur associé à une hausse de t%
        M = (q**N * (prixTotalBien) * (1 - q) / (1 - q**N)) + prixTotalBien*((AssuDeces/100)/12)
        #print("Votre mensualité sera de {0:.2f} euros".format(M))
        I = N * M - prixTotalBien # calcul des intérêts versés
        garantie = (1.5/100)*prixTotalBien
        #put_text(f"Votre mensulaité sera de {M} euros")
        #put_text(f"Le montant total des intérêts versés sera de {I} euros")
        prixRevente = prixDuBien + prixDuBien*(pourcentageRevente/100)

        DateAcquisition = input("Date d'acquisition du bien (dd-mm-yyyy)")
        DateAcquisition = DateAcquisition.replace("/","-")
        DateLivraison = input("Date de livraison (dd-mm-yyyy)")
        DateLivraison = DateLivraison.replace("/","-")
        date_time_obj = datetime.datetime.strptime(DateLivraison, '%d-%m-%Y')
        if date_time_obj.month == 1:
            date_time_obj = date_time_obj + relativedelta.relativedelta(months=1)
        FinFinancement = date_time_obj + relativedelta.relativedelta(months=N)
        date2 = "31-12-{}".format(date_time_obj.year)
        date3 = datetime.datetime.strptime(date2, '%d-%m-%Y')
        nbreMois = date3.month - date_time_obj.month + 1


        put_text("MOMENTS CLÉS").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_table([
                ["Date d'acquisition","Date de livraison","Fin du financement"],
                [DateAcquisition,DateLivraison,FinFinancement.strftime('%d-%m-%Y')]
            ])

        liste_prixdubien = []
        listeprixdubieninitial = [prixDuBien]
        for year in range(1, int((N+12)/12)):
            prixDuBien = prixDuBien*1.01
            liste_prixdubien.append(prixDuBien)
        listeprixdubieninitial.extend(liste_prixdubien)

        my_new_list = [i * 12 for i in liste_loyer]

        list_taxefonciere = []
        list_assuloyerimpaye = []
        list_chargescopro = []
        list_fraisdegestion = []
        list_mensualite = []
        list_total = []

        for j in my_new_list:
            fraisDeGestion2 = (fraisDeGestion/100)*j
            assuranceLoyerImpaye = (assurance/100)*j
            chargecopro = (4/100)*j
            taxeFonciere = (j/12)
            total = fraisDeGestion2 + assuranceLoyerImpaye + chargecopro + taxeFonciere
            list_taxefonciere.append(taxeFonciere)
            list_assuloyerimpaye.append(assuranceLoyerImpaye)
            list_chargescopro.append(chargecopro)
            list_fraisdegestion.append(fraisDeGestion2)
            list_total.append(total)
        for x in listeprixdubieninitial:
            M = (q**N * (prixTotalBien) * (1 - q) / (1 - q**N)) + prixTotalBien*((AssuDeces/100)/12)
            list_mensualite.append(M*12)

        T2 = T*1/100
        rng = pd.date_range(date_time_obj, periods=N, freq='MS')
        rng.name = "Date"
        df = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
        df.reset_index(inplace=True)
        df.index += 1
        df.index.name = "Periode (Mois)"

        df["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, prixTotalBien)+ prixTotalBien*((AssuDeces/100)/12)
        df["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12,df.index,N, prixTotalBien)
        df["Intérêts"] = -1 * numpy_financial.ipmt(T2/12,df.index, N, prixTotalBien) 
        df = df.round(2)

        df["Capital restant dû"] = 0
        df.loc[1, "Capital restant dû"] = prixTotalBien - df.loc[1, "Capital Amorti"]

        for period in range(2, len(df)+1):
            previous_balance = df.loc[period-1, "Capital restant dû"]
            principal_paid = df.loc[period, "Capital Amorti"]
            
            if previous_balance == 0:
                df.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] == 0
                continue
            elif principal_paid <= previous_balance:
                df.loc[period, "Capital restant dû"] = previous_balance - principal_paid
        
        df["Date"] = pd.to_datetime(df["Date"],format='%d-%m-%Y')
        df.set_index("Date")
        df = df.resample('AS', on='Date').sum()

        df5 = pd.DataFrame({
        "Loyer perçus" : my_new_list,
        "Frais de gestion" : list_fraisdegestion,
        "Taxe foncière" : list_taxefonciere,
        "Assurance loyer impayé": list_assuloyerimpaye,
        "Charge de copropriété" : list_chargescopro,
        "Total Charges Locatives" : list_total,
        "Mensualité" : list_mensualite,
        
        })
        df5.index += 1 
        #df5.index.names = ['Periode']
        #df5 = df5.reset_index()

        df5["Total Charges Locatives"] = df5["Frais de gestion"] + df5["Taxe foncière"] + df5["Assurance loyer impayé"] + df5["Charge de copropriété"]
        df5["Loyer perçus"].iloc[0] = ((df5["Loyer perçus"].iloc[0])/12)*nbreMois
        df5["Frais de gestion"].iloc[0] = ((df5["Frais de gestion"].iloc[0])/12)*nbreMois
        df5["Taxe foncière"].iloc[0] = ((df5["Taxe foncière"].iloc[0])/12)*nbreMois
        df5["Assurance loyer impayé"].iloc[0] = ((df5["Assurance loyer impayé"].iloc[0])/12)*nbreMois
        df5["Charge de copropriété"].iloc[0] = ((df5["Charge de copropriété"].iloc[0])/12)*nbreMois
        df5["Total Charges Locatives"].iloc[0] = ((df5["Total Charges Locatives"].iloc[0])/12)*nbreMois
        df5["Mensualité"].iloc[0] = ((df5["Mensualité"].iloc[0])/12)*nbreMois
        #df5.index += 1 
        df5["Loyer perçus"].iloc[-1] = ((df5["Loyer perçus"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Frais de gestion"].iloc[-1] = ((df5["Frais de gestion"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Taxe foncière"].iloc[-1] = ((df5["Taxe foncière"].iloc[-1])/12)*(12-nbreMois)
        df5["Assurance loyer impayé"].iloc[-1] = ((df5["Assurance loyer impayé"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Charge de copropriété"].iloc[-1] = ((df5["Charge de copropriété"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Total Charges Locatives"].iloc[-1] = ((df5["Total Charges Locatives"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Mensualité"].iloc[-1] = ((df5["Mensualité"].iloc[-1])/12)*(12-nbreMois+1)

        T2 = T*1/100
        #df4 = df.set_index(df.index //((N+1)/(N/12))).sum(level = 0)
        #df4.index +=1
        df5["Interêts d'emprunt"] = df["Intérêts"].values
        #df5["Interêts d'emprunt"].iloc[0] = ((df5["Interêts d'emprunt"].iloc[0])/12)*nbreMois
        toutcharges = df5['Taxe foncière'] + df5['Charge de copropriété'] + df5['Assurance loyer impayé'] + df5['Frais de gestion']
        Charges = df5['Total Charges Locatives'] + df5["Interêts d'emprunt"] 
        chargesBati = (prixBati/N)*12
        fiscaliteFonciereMoins = Charges + chargesBati
        fiscaliteFoncierePlus = df5['Loyer perçus']


        EffortEpargnePlus = df5['Loyer perçus'] 
        df5["Fiscalité Foncière1"] = fiscaliteFoncierePlus - fiscaliteFonciereMoins
        df5['Fiscalité Foncière'] = df5["Fiscalité Foncière1"].cumsum() 
        #df5['Fiscalité Foncière'] = df5["Fiscalité Foncière1"].shift() + df5["Fiscalité Foncière1"]
        df5['Fiscalité Foncière'].iloc[0] = df5["Fiscalité Foncière1"].iloc[0]
        df5["Fiscalité Foncière"] = df5["Fiscalité Foncière"]*((TMI+17.2)/100)
        df5["Fiscalité Foncière"][df5["Fiscalité Foncière"].values < 0] = 0
        #fiscaliteFonciere2 = df5["Fiscalité Foncière"]*((TMI+17.2)/100)
        #df5["Fiscalité Foncière"] = fiscaliteFonciere2

        chargesBati = prixBati/25
        #df5["diff"] = fiscaliteFoncierePlus - fiscaliteFonciereMoins
        
        #fiscalite = fiscaliteFoncierePlus + fiscaliteFonciereMoins + abs(df5["diff"]).shift()
        #df5 = df5.fillna(0)
        #df5["Fiscalité Foncière"] = fiscalite*((TMI+17.2)/100)
        #df5["Fiscalité Foncière"][0] = fiscaliteFonciere2
        

        EffortEpargneMoins = df5["Mensualité"] + df5['Total Charges Locatives'] + df5["Fiscalité Foncière"]

        EffortEpargneFinal = EffortEpargnePlus-EffortEpargneMoins
        df5["Recettes"] = EffortEpargnePlus
        df5["Depense"] = EffortEpargneMoins
        df5["Effort d'epargne"] = EffortEpargneFinal

        Absolu_effortepargne = abs(EffortEpargneFinal)
        df5 = df5.drop(columns = "Fiscalité Foncière1", axis = 1)
            

        pd.options.display.float_format = "{:,.2f}".format 
        nbreMois = (N+12)/12
        nbreMois = int(nbreMois)
        liste_annne = []
        for i in range(0,nbreMois):
            a = date_time_obj.year + i
            liste_annne.append(a)
        df5["Periode (en années)"] = liste_annne
        df5 = df5.set_index("Periode (en années)")

        df3 = pd.DataFrame({"Financement":['Locataire', 'Investisseur'], 'Montant':[float("{:.2f}".format(sum(my_new_list[0:N])))
        ,float("{:.2f}".format(sum(Absolu_effortepargne[0:N])))]})
        fig3 = px.pie(df3, values='Montant', names = "Financement", title='Financement de votre opération au terme')

        Sum_EffortEpargneMoins = sum(df5["Depense"])
        Sum_EffortEpargnePlus = sum(df5["Recettes"])
        Sum_EffortEpargne = sum(df5["Effort d'epargne"])

        df = pd.DataFrame({"Effort d'épargne":['Entrée', 'Sortie',"Effort d'epargne"], 'Montant':[float("{:.2f}".format(Sum_EffortEpargnePlus)), float("{:.2f}".format(Sum_EffortEpargneMoins)),
        float("{:.2f}".format(Sum_EffortEpargne))]})
        fig = px.bar(df, x="Effort d'épargne", y='Montant',color = "Effort d'épargne", title = "Gain et Perte en trésorerie")
        put_text("CALCUL DE L'EFFORT D'EPARGNE").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_collapse('Voir le tableau', [put_html(df5.to_html(border = 0))])

        put_text("RECETTES ET DEPENSES MENSUELLES EN MOYENNE SUR LA DURÉE DE L'OPÉRATION").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_table([
        ['Recettes', put_table([['Loyer perçus'], 
        ["{:,.0f}".format(math.trunc(sum(df5['Loyer perçus'])/(N)))]]), 
        "Charges" , put_table([['Remboursement du prêt', 'Charges','Fiscalité foncière'], 
        ["{:,.0f}".format(math.trunc(sum(df5["Mensualité"])/(N))), "{:,.0f}".format(math.trunc(sum(df5['Total Charges Locatives'])/(N))),
        "{:,.0f}".format(math.trunc(sum(df5["Fiscalité Foncière"])/(N)))]])]
        ])
        put_table([
                ["Recettes mensuelles", "Dépenses mensuelles"],
                ["{:,.0f}".format(math.trunc(sum(df5["Recettes"])/(N))),"{:,.0f}".format(math.trunc(sum(df5["Depense"])/(N)))],
            ])

        put_table([
                ["Votre effort d'epargne"],
                ["{:,.0f}".format(math.trunc(sum(df5["Effort d'epargne"])/(N)))],
            ])

        put_text("RENTABILITÉ LOCATIVE DE L'INVESTISSEMENT").style('color: dark; font-size: 20px; font-weight:bold;')
        renta = ((Loyermax*12)/prixDuBien)*100
        if(renta <3):
            put_table([
                ["Rentabilité sur investissement"],
                ["{:.2f}%".format(renta),style(put_text('Mauvaise rentabilité'), 'color:red')],
            ])
        else:
            put_table([
                ["Rentabilité sur investissement"],
                ["{:.2f}%".format(renta),style(put_text('Bonne rentabilité'), 'color:green')],
            ])


        html = fig3.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)

        put_text("PREVISIONNEL DU PRIX DE VOTRE BIEN").style('color: dark; font-size: 20px; font-weight:bold;')
        prixPireCas = listeprixdubieninitial[0]
        prixMoyenCas = listeprixdubieninitial[0] + 0.05*listeprixdubieninitial[0]
        prixMeilleurCas = listeprixdubieninitial[0] + 0.1*listeprixdubieninitial[0]
        put_table([
                ["PIRE DES CAS","CAS MOYEN","MEILLEUR CAS"],
                ["{:,.0f}".format(math.trunc(prixPireCas)),"{:,.0f}".format(math.trunc(prixMoyenCas)),"{:,.0f}".format(math.trunc(prixMeilleurCas))],
                ["0%","5%","10%"],
            ])

        put_text("ÉVOLUTION DU PRIX DU BIEN SUR LES 10 PREMIÈRES ANNÉES").style('color: dark; font-size: 20px; font-weight:bold;')
        put_table([
                ["Année 1","Année 2","Année 3","Année 4","Année 5","Année 6","Année 7","Année 8","Année 9","Année 10",
                ],
                ["{:,.0f}".format(math.trunc(listeprixdubieninitial[0])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[1])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[2])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[3])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[4])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[5])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[6])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[7])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[8])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[9]))]
            ])

        T2 = T*1/100
        rng = pd.date_range(date_time_obj, periods=N, freq='MS')
        rng.name = "Date"
        df8 = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
        df8.reset_index(inplace=True)
        df8.index += 1
        df8.index.name = "Periode (Mois)"

        df8["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, prixTotalBien)+ prixTotalBien*((AssuDeces/100)/12)
        df8["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12,df8.index,N, prixTotalBien)
        df8["Intérêts"] = -1 * numpy_financial.ipmt(T2/12,df8.index, N, prixTotalBien) 
        df8 = df8.round(2)

        df8["Capital restant dû"] = 0
        df8.loc[1, "Capital restant dû"] = prixTotalBien - df8.loc[1, "Capital Amorti"]

        for period in range(2, len(df8)+1):
            previous_balance = df8.loc[period-1, "Capital restant dû"]
            principal_paid = df8.loc[period, "Capital Amorti"]
            
            if previous_balance == 0:
                df8.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] == 0
                continue
            elif principal_paid <= previous_balance:
                df8.loc[period, "Capital restant dû"] = previous_balance - principal_paid

        df8["Date"] = pd.to_datetime(df8["Date"],format='%d-%m-%Y')

        T2 = T*1/100
        liste_date = []
        x = list(rrule(freq=YEARLY, count=(N+12)/12, dtstart=df8.iloc[0]["Date"]))
        for ld in x:
            liste_date.append(ld)
        df_somme = pd.DataFrame(
            {
        'Prix du bien' : listeprixdubieninitial,
        "Date" :liste_date, 
            })


        products_dict = dict(zip(df8.Date,df8["Capital restant dû"]))
        df_somme["Capital restant dû"] = df_somme["Date"].map(products_dict)
        df_somme.index += 1
        df_somme.index.name = "Periode (Année)"
        df_somme["Somme disponible en cas de revente"] = df_somme["Prix du bien"] - df_somme["Capital restant dû"] 
        df_somme = df_somme.drop(columns="Date", axis = 1)
        df_somme["Periode (en années)"] = liste_annne
        df_somme = df_somme.set_index("Periode (en années)")
        df_somme["Capital restant dû"].iloc[-1] = 0
        df_somme["Somme disponible en cas de revente"] = df_somme["Prix du bien"] - df_somme["Capital restant dû"]

        put_text("SOMME DISPONIBLE EN CAS DE REVENTE").style('color: dark; font-size: 20px; font-weight:bold;')
        put_collapse('Voir le tableau', [put_html(df_somme.to_html(border = 0))])
        put_text("TABLEAU D'AMORTISSEMENT").style('color: dark; font-size: 20px; font-weight:bold;')
        put_collapse('Voir le tableau', [put_html(df8.to_html(border = 0))])



    if (choix == "16 - Simulateur Monument historique"):
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark") 
        put_markdown('# SIMULATION MONUMENT HISTORIQUE') 
        revenu = float(input("Quel est le revenu net annuel du foyer : "))
        revenu2 = 0.9*revenu
        if revenu2 > 126520:
            revenuAvantAbbatement = revenu - 12652
        else :
            revenuAvantAbbatement = 0.9*revenu
        statut = saisirStatutFamilial()
        npers = int(input("Nombre de personnes a charge? "))
        if statut == CONCUBINAGE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
        ###########CELIBATAIRE
        if statut == CELIBATAIRE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
                
        ############MARIE
        
        if statut == MARIE:
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 52140:
                    impots = (revenuAvantAbbatement*0.11)-2249.50
                    TMI = 11
                if 52140 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-12156.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-28556
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-41382.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2.5:
                if revenuAvantAbbatement < 25563:
                    impots = 0
                    TMI = 0
                if 25563 < revenuAvantAbbatement <= 57561:
                    impots = (revenuAvantAbbatement*0.11)-2811.88
                    TMI = 11
                if 57562 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-13748.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-30148
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-42974.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 62978:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 62979 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-15340.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-31740
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-44566.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 73818:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 73819 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-18524.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-34924
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-47750.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==5:
                if revenuAvantAbbatement < 51125:
                    impots = 0
                    TMI = 0
                if 51125 < revenuAvantAbbatement <= 84655:
                    impots = (revenuAvantAbbatement*0.11)-5623.75
                    TMI = 11
                if 84656 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-21708.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-38108
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-50934.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==6:
                if revenuAvantAbbatement < 61350:
                    impots = 0
                    TMI = 0
                if 61350 < revenuAvantAbbatement <= 94495:
                    impots = (revenuAvantAbbatement*0.11)-6748.5
                    TMI = 11
                if 94496 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-24892.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-40292
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-54118.88
                    TMI = 45
                
        afficherFicheImpots(revenuAvantAbbatement, statut, npers,TMI,impots)


        prixDuBien = float(input("Montant du foncier : "))
        travaux = float(input("Le prix de vos travaux : "))
        Apport = float(input("Votre apport : "))
        fraisNotaire = (7.5/100)*prixDuBien
        prixDuBien2 = prixDuBien + fraisNotaire + travaux
        garantieBancaire = (1.5/100)*(prixDuBien+travaux)
        prixTotalBien = prixDuBien2 + garantieBancaire - Apport
        prixFoncierTravaux = prixDuBien + travaux
        
        Loyermax = float(input("Votre loyer :"))

        put_text("TOTAL À FINANCER").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_table([
                ["Prix du foncier","Travaux","Frais de notaire","Garantie bancaire","Apport","Prix Total","Votre loyer"],
                ["{:,.2f}".format(prixDuBien),"{:,.2f}".format(travaux),"{:,.2f}".format(fraisNotaire),"{:,.2f}".format(garantieBancaire),
                "{:,.2f}".format(Apport),"{:,.2f}".format(prixTotalBien),"{:,.2f}".format(Loyermax)
                ]
            ])
        
            
        T = str(input("Taux annuel du crédit en % : "))
        T = T.replace(",",".")
        T = float(T)
        N2 = int(input("Durée en années du crédit :"))
        N = N2*12
        AssuDeces = str(input("Taux d'assurance Décès et Invalidité en % :"))
        AssuDeces = AssuDeces.replace(",",".")
        AssuDeces = float(AssuDeces)

        liste = []
        liste_loyer = [Loyermax]
        for year in range(1, int((N+12)/12)):
            Loyermax = Loyermax*1.01
            liste.append(Loyermax)
        liste_loyer.extend(liste)

        put_text("ÉVOLUTION ANNUEL DU LOYER SUR LES 10 PROCHAINES ANNÉES").style('color: dark; font-size: 20px; font-weight:bold;')
        put_table([
                ["Année 1","Année 2","Année 3","Année 4","Année 5","Année 6","Année 7","Année 8","Année 9"
                ],
                [float("{:.2f}".format(liste_loyer[0])),float("{:.2f}".format(liste_loyer[1])),float("{:.2f}".format(liste_loyer[2])),float("{:.2f}".format(liste_loyer[3])),float("{:.2f}".format(liste_loyer[4])),
                float("{:.2f}".format(liste_loyer[5])),float("{:.2f}".format(liste_loyer[6])),float("{:.2f}".format(liste_loyer[7])),float("{:.2f}".format(liste_loyer[8]))]
            ])
        pourcentageRevente = (10*1/100)*prixDuBien
        t = (T / 12) 
        q = 1 + t / 100 # calcul du coefficient multiplicateur associé à une hausse de t%
        M = (q**N * (prixTotalBien) * (1 - q) / (1 - q**N)) + prixTotalBien*((AssuDeces/100)/12)
        #print("Votre mensualité sera de {0:.2f} euros".format(M))
        I = N * M - prixTotalBien # calcul des intérêts versés
        garantie = (1.5/100)*prixTotalBien
        #put_text(f"Votre mensulaité sera de {M} euros")
        #put_text(f"Le montant total des intérêts versés sera de {I} euros")
        prixRevente = prixDuBien + prixDuBien*(pourcentageRevente/100)

        #durée = 108
        #Année = N/12
        durée = 180
        DateAcquisition = input("Date d'acquisition du bien (dd-mm-yyyy)")
        DateAcquisition = DateAcquisition.replace("/","-")
        DateLivraison = input("Date de livraison (dd-mm-yyyy)")
        DateLivraison = DateLivraison.replace("/","-")
        date_time_obj = datetime.datetime.strptime(DateLivraison, '%d-%m-%Y')
        if date_time_obj.month == 1:
            date_time_obj = date_time_obj + relativedelta.relativedelta(months=1)
        FinFinancement = date_time_obj + relativedelta.relativedelta(months=N)
        FinDispositifMonument = date_time_obj + relativedelta.relativedelta(months=durée)
        date2 = "31-12-{}".format(date_time_obj.year)
        date3 = datetime.datetime.strptime(date2, '%d-%m-%Y')
        nbreMois = date3.month - date_time_obj.month + 1


        put_text("MOMENTS CLÉS").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_table([
                ["Date d'acquisition","Date de livraison","Fin du dispositif Monument Historique","Fin du financement"],
                [DateAcquisition,DateLivraison,FinDispositifMonument.strftime('%d-%m-%Y'),FinFinancement.strftime('%d-%m-%Y')]
            ])

        liste_charges = []
        liste_chargecopro = []
        list_assuranceloyerimpaye = []
        list_fraisdegestion = []
        list_taxefonciere = []
        list_loyerpercus = []
        list_reductionimpots = []
        list_fiscalitefonciere = []
        list_effortepargne = []
        list_interetsemprunts = []
        list_mensualite = []
        list_EffortEpargnePlus = []
        list_EffortEpargneMoins = []

        fraisDeGestion = str(input("Pourcentage des frais de gestions sur votre loyer :"))
        fraisDeGestion = fraisDeGestion.replace(",",".")
        fraisDeGestion = float(fraisDeGestion)
        fraisDeGestion2 = (fraisDeGestion/100)*Loyermax
        assurance = str(input("Pourcentage d'assurance de loyer impayé sur votre loyer :"))
        assurance = assurance.replace(",",".")
        assurance = float(assurance)
        dureeMalraux = 9

        liste_prixdubien = []
        listeprixdubieninitial = [prixFoncierTravaux]
        for year in range(1, int((N+12)/12)):
            prixFoncierTravaux = prixFoncierTravaux*1.01
            liste_prixdubien.append(prixFoncierTravaux)
        listeprixdubieninitial.extend(liste_prixdubien)

        my_new_list = [i * 12 for i in liste_loyer]


        list_taxefonciere = []
        list_assuloyerimpaye = []
        list_chargescopro = []
        list_fraisdegestion = []
        list_mensualite = []
        list_economieImpot = []
        list_total = []

        for j in my_new_list:
            fraisDeGestion2 = (fraisDeGestion/100)*j
            assuranceLoyerImpaye = (assurance/100)*j
            chargecopro = (4/100)*j
            taxeFonciere = (j/12)
            economieTravaux = (travaux/3)*(TMI/100)
            total = fraisDeGestion2 + assuranceLoyerImpaye + chargecopro + taxeFonciere
            list_taxefonciere.append(taxeFonciere)
            list_assuloyerimpaye.append(assuranceLoyerImpaye)
            list_chargescopro.append(chargecopro)
            list_fraisdegestion.append(fraisDeGestion2)
            list_economieImpot.append(economieTravaux)
            list_total.append(total)

        for x in listeprixdubieninitial:
            M = (q**N * (prixTotalBien) * (1 - q) / (1 - q**N)) + prixTotalBien*((AssuDeces/100)/12)
            list_mensualite.append(M*12)

        T2 = T*1/100
        rng = pd.date_range(date_time_obj, periods=N, freq='MS')
        rng.name = "Date"
        df = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
        df.reset_index(inplace=True)
        df.index += 1
        df.index.name = "Periode (Mois)"

        df["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, prixTotalBien)+ prixTotalBien*((AssuDeces/100)/12)
        df["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12,df.index,N, prixTotalBien)
        df["Intérêts"] = -1 * numpy_financial.ipmt(T2/12,df.index, N, prixTotalBien) 
        df = df.round(2)

        df["Capital restant dû"] = 0
        df.loc[1, "Capital restant dû"] = prixTotalBien - df.loc[1, "Capital Amorti"]

        for period in range(2, len(df)+1):
            previous_balance = df.loc[period-1, "Capital restant dû"]
            principal_paid = df.loc[period, "Capital Amorti"]
            
            if previous_balance == 0:
                df.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] == 0
                continue
            elif principal_paid <= previous_balance:
                df.loc[period, "Capital restant dû"] = previous_balance - principal_paid
        
        df["Date"] = pd.to_datetime(df["Date"],format='%d-%m-%Y')
        df.set_index("Date")
        df = df.resample('AS', on='Date').sum()
        
        df5 = pd.DataFrame({
        "Loyer perçus" : my_new_list,
        "Économie d'impôts":list_economieImpot,
        "Frais de gestion" : list_fraisdegestion,
        "Taxe foncière" : list_taxefonciere,
        "Assurance loyer impayé": list_assuloyerimpaye,
        "Charge de copropriété" : list_chargescopro,
        "Total Charges Locatives" : list_total,
        "Mensualité" : list_mensualite,
        
        })
        
        df5.index += 1 
        #df5.index.names = ['Periode']
        #df5 = df5.reset_index()

        df5["Économie d'impôts"][3:] = 0
        df5["Total Charges Locatives"] = df5["Frais de gestion"] + df5["Taxe foncière"] + df5["Assurance loyer impayé"] + df5["Charge de copropriété"]
        df5["Loyer perçus"].iloc[0] = ((df5["Loyer perçus"].iloc[0])/12)*nbreMois
        df5["Frais de gestion"].iloc[0] = ((df5["Frais de gestion"].iloc[0])/12)*nbreMois
        df5["Taxe foncière"].iloc[0] = ((df5["Taxe foncière"].iloc[0])/12)*nbreMois
        df5["Assurance loyer impayé"].iloc[0] = ((df5["Assurance loyer impayé"].iloc[0])/12)*nbreMois
        df5["Charge de copropriété"].iloc[0] = ((df5["Charge de copropriété"].iloc[0])/12)*nbreMois
        df5["Total Charges Locatives"].iloc[0] = ((df5["Total Charges Locatives"].iloc[0])/12)*nbreMois
        df5["Mensualité"].iloc[0] = ((df5["Mensualité"].iloc[0])/12)*nbreMois
        #df5.index += 1 
        df5["Loyer perçus"].iloc[-1] = ((df5["Loyer perçus"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Frais de gestion"].iloc[-1] = ((df5["Frais de gestion"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Taxe foncière"].iloc[-1] = ((df5["Taxe foncière"].iloc[-1])/12)*(12-nbreMois)
        df5["Assurance loyer impayé"].iloc[-1] = ((df5["Assurance loyer impayé"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Charge de copropriété"].iloc[-1] = ((df5["Charge de copropriété"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Total Charges Locatives"].iloc[-1] = ((df5["Total Charges Locatives"].iloc[-1])/12)*(12-nbreMois+1)
        df5["Mensualité"].iloc[-1] = ((df5["Mensualité"].iloc[-1])/12)*(12-nbreMois+1)

        T2 = T*1/100
        df5["Interêts d'emprunt"] = df["Intérêts"].values
        toutcharges = df5['Taxe foncière'] + df5['Charge de copropriété'] + df5['Assurance loyer impayé'] + df5['Frais de gestion']
        Charges = df5['Total Charges Locatives'] + df5["Interêts d'emprunt"] 

        prixBati = (85/100)*prixFoncierTravaux
        fiscaliteFonciereMoins = Charges 
        fiscaliteFoncierePlus = df5['Loyer perçus']
        chargesBati = (prixBati/N)*12
        fiscaliteFonciereMoins2 = Charges + chargesBati

        EffortEpargnePlus = df5['Loyer perçus'] + (df5["Économie d'impôts"])
        df5["Fiscalité Foncière1"] = fiscaliteFoncierePlus - fiscaliteFonciereMoins
        df5["Fiscalité Foncière2"] = fiscaliteFoncierePlus - fiscaliteFonciereMoins2
        fiscaliteFonciere2 = df5["Fiscalité Foncière1"]*((TMI+17.2)/100)
        df5["Fiscalité Foncière"] = 0
        df5["Fiscalité Foncière"].loc[0:7] = df5["Fiscalité Foncière1"]*((TMI+17.2)/100)
        df5["Fiscalité Foncière"].loc[7:] = df5["Fiscalité Foncière2"].shift() + df5["Fiscalité Foncière2"]
        #df5["Fiscalité Foncière"] = df5["Fiscalité Foncière"]*((TMI+17.2)/100)
        df5["Fiscalité Foncière"][df5["Fiscalité Foncière"].values < 0] = 0

        EffortEpargneMoins = df5["Mensualité"] + df5['Total Charges Locatives'] + df5["Fiscalité Foncière"]
        EffortEpargneFinal = EffortEpargnePlus-EffortEpargneMoins
        df5["Recettes"] = EffortEpargnePlus
        df5["Depense"] = EffortEpargneMoins
        df5["Effort d'epargne"] = EffortEpargneFinal
        
        Absolu_effortepargne = abs(EffortEpargneFinal)

        df5 = df5.drop(columns = "Fiscalité Foncière1", axis = 1)
        df5 = df5.drop(columns = "Fiscalité Foncière2", axis = 1)
            
        dureeMonument = 15
        pd.options.display.float_format = "{:,.2f}".format 
        nbreMois = (N+12)/12
        nbreMois = int(nbreMois)
        liste_annne = []
        for i in range(0,nbreMois):
            a = date_time_obj.year + i
            liste_annne.append(a)
        df5["Periode (en années)"] = liste_annne
        df5 = df5.set_index("Periode (en années)")

        df3 = pd.DataFrame({"Financement":['Locataire', "Économie d'impôts", 'Investisseur'], 'Montant':[float("{:.2f}".format(sum(my_new_list[0:dureeMonument]))), 
        float("{:.0f}".format(sum(df5["Économie d'impôts"][0:dureeMonument]))),float("{:.2f}".format(sum(Absolu_effortepargne[0:dureeMonument])))]})
        fig3 = px.pie(df3, values='Montant', names = "Financement", title='Financement de votre opération au terme')
        
        Sum_EffortEpargneMoins = sum(df5["Depense"])
        Sum_EffortEpargnePlus = sum(df5["Recettes"])
        Sum_EffortEpargne = sum(df5["Effort d'epargne"])

        df = pd.DataFrame({"Effort d'épargne":['Entrée', 'Sortie',"Effort d'epargne"], 'Montant':[float("{:.2f}".format(Sum_EffortEpargnePlus)), float("{:.2f}".format(Sum_EffortEpargneMoins)),
        float("{:.2f}".format(Sum_EffortEpargne))]})
        fig = px.bar(df, x="Effort d'épargne", y='Montant',color = "Effort d'épargne", title = "Gain et Perte en trésorerie")
        put_text("CALCUL DE L'EFFORT D'EPARGNE").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_collapse('Voir le tableau', [put_html(df5.to_html(border = 0))])

        put_text("RECETTES ET DEPENSES MENSUELLES EN MOYENNE PAR MOIS SUR 15 ANS DE MONUMENTS HISTORIQUES").style('color: dark; font-size: 20px; font-weight:bold;  padding:0; line-height:50px;')
        put_table([
        ['Recettes', put_table([['Loyer perçus', 'Reduction impôts'], 
        ["{:,.0f}".format(math.trunc(sum(df5['Loyer perçus'][0:15])/(dureeMonument)/12)), "{:,.0f}".format(math.trunc(sum(df5["Économie d'impôts"][0:15])/(dureeMonument)/12))]]), 
        "Charges" , put_table([['Remboursement du prêt', 'Charges','Fiscalité foncière'], 
        ["{:,.0f}".format(math.trunc(sum(df5["Mensualité"][0:15])/(dureeMonument)/12)), "{:,.0f}".format(math.trunc(sum(df5['Total Charges Locatives'][0:15])/(dureeMonument)/12)),
        "{:,.0f}".format(math.trunc(sum(df5["Fiscalité Foncière"][0:15])/(dureeMonument)/12))]])]
        ])
        put_table([
                ["Recettes mensuelles", "Dépenses mensuelles"],
                ["{:,.0f}".format(math.trunc(sum(df5["Recettes"][0:15])/(dureeMonument)/12)),"{:,.0f}".format(math.trunc(sum(df5["Depense"][0:15])/(dureeMonument)/12))],
            ])

        put_table([
                ["Votre effort d'epargne"],
                ["{:,.0f}".format(math.trunc(sum(df5["Effort d'epargne"][0:15])/(dureeMonument)/12))],
            ])

        put_text("RENTABILITÉ LOCATIVE DE L'INVESTISSEMENT").style('color: dark; font-size: 20px; font-weight:bold;')
        renta = ((Loyermax*12)/prixDuBien)*100
        if(renta <3):
            put_table([
                ["Rentabilité sur investissement"],
                ["{:.2f}%".format(renta),style(put_text('Mauvaise rentabilité'), 'color:red')],
            ])
        else:
            put_table([
                ["Rentabilité sur investissement"],
                ["{:.2f}%".format(renta),style(put_text('Bonne rentabilité'), 'color:green')],
            ])
        html = fig3.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)

        put_text("PREVISIONNEL DU PRIX DE VOTRE BIEN").style('color: dark; font-size: 20px; font-weight:bold;')
        prixPireCas = listeprixdubieninitial[0]
        prixMoyenCas = listeprixdubieninitial[0] + 0.05*listeprixdubieninitial[0]
        prixMeilleurCas = listeprixdubieninitial[0] + 0.1*listeprixdubieninitial[0]
        put_table([
                ["PIRE DES CAS","CAS MOYEN","MEILLEUR CAS"],
                ["{:,.0f}".format(math.trunc(prixPireCas)),"{:,.0f}".format(math.trunc(prixMoyenCas)),"{:,.0f}".format(math.trunc(prixMeilleurCas))],
                ["0%","5%","10%"],
            ])

        put_text("ÉVOLUTION DU PRIX DU BIEN SUR LES 10 PREMIÈRES ANNÉES").style('color: dark; font-size: 20px; font-weight:bold;')
        put_table([
                ["Année 1","Année 2","Année 3","Année 4","Année 5","Année 6","Année 7","Année 8","Année 9","Année 10",
                ],
                ["{:,.0f}".format(math.trunc(listeprixdubieninitial[0])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[1])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[2])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[3])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[4])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[5])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[6])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[7])),"{:,.0f}".format(math.trunc(listeprixdubieninitial[8])),
                "{:,.0f}".format(math.trunc(listeprixdubieninitial[9]))]
            ])
        
        T2 = T*1/100
        rng = pd.date_range(date_time_obj, periods=N, freq='MS')
        rng.name = "Date"
        df8 = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
        df8.reset_index(inplace=True)
        df8.index += 1
        df8.index.name = "Periode (Mois)"

        df8["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, prixTotalBien)+ prixTotalBien*((AssuDeces/100)/12)
        df8["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12,df8.index,N, prixTotalBien)
        df8["Intérêts"] = -1 * numpy_financial.ipmt(T2/12,df8.index, N, prixTotalBien) 
        df8 = df8.round(2)

        df8["Capital restant dû"] = 0
        df8.loc[1, "Capital restant dû"] = prixTotalBien - df8.loc[1, "Capital Amorti"]

        for period in range(2, len(df8)+1):
            previous_balance = df8.loc[period-1, "Capital restant dû"]
            principal_paid = df8.loc[period, "Capital Amorti"]
            
            if previous_balance == 0:
                df8.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] == 0
                continue
            elif principal_paid <= previous_balance:
                df8.loc[period, "Capital restant dû"] = previous_balance - principal_paid
        
        df8["Date"] = pd.to_datetime(df8["Date"],format='%d-%m-%Y')
        
        T2 = T*1/100
        liste_date = []
        x = list(rrule(freq=YEARLY, count=(N+12)/12, dtstart=df8.iloc[0]["Date"]))
        for ld in x:
            liste_date.append(ld)
        df_somme = pd.DataFrame(
            {
        'Prix du bien' : listeprixdubieninitial,
        "Date" :liste_date, 
            })
        

        products_dict = dict(zip(df8.Date,df8["Capital restant dû"]))
        df_somme["Capital restant dû"] = df_somme["Date"].map(products_dict)
        df_somme.index += 1
        df_somme.index.name = "Periode (Année)"
        df_somme["Somme disponible en cas de revente"] = df_somme["Prix du bien"] - df_somme["Capital restant dû"] 
        df_somme = df_somme.drop(columns="Date", axis = 1)
        df_somme["Periode (en années)"] = liste_annne
        df_somme = df_somme.set_index("Periode (en années)")
        df_somme["Capital restant dû"].iloc[-1] = 0
        df_somme["Somme disponible en cas de revente"] = df_somme["Prix du bien"] - df_somme["Capital restant dû"] 
        
        put_text("SOMME DISPONIBLE EN CAS DE REVENTE").style('color: dark; font-size: 20px; font-weight:bold;')
        put_collapse('Voir le tableau', [put_html(df_somme.to_html(border = 0))])
        put_text("TABLEAU D'AMORTISSEMENT").style('color: dark; font-size: 20px; font-weight:bold;')
        put_collapse('Voir le tableau', [put_html(df8.to_html(border = 0))])

    if (choix == "17 - Comparateur d'epargne") :
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        put_markdown("# COMPARATEUR D'EPARGNE")
        pd.options.display.float_format = "{:,.2f}".format 
        livretA = 0.96
        livretB = 0.1
        livretLLD = 1
        SCPI = 4
        AssuranceVieFondPropre = 1.7
        PEL = 1
        FondCommunPlacement = 2.3


        montant = float(input("Montant à placer : "))
        nombreAnnee = int(input("Nombre d'années d'investissement : "))
    
        liste_livretA2 = []
        liste_livretB2 = []
        list_LLD = []
        list_scpi = []
        list_assuranceVie = []
        list_pel = []
        list_fondcommun = []

        montantLivretA = montant
        montantLivretB = montant
        montantLLD = montant
        montantSCPI = montant
        montantAssuranceVie = montant
        montantPel = montant
        montantFondCommun = montant

        liste_livretA = [montantLivretA]
        liste_livretB = [montantLivretB]
        LLD = [montantLLD]
        scpi = [montantSCPI]
        assuranceVie = [montantAssuranceVie]
        pel = [montantPel]
        fondCommun = [montantFondCommun]

        for i in range(1,nombreAnnee):
            for j in liste_livretA:
                montantLivretA = montantLivretA * (livretA/100) + montantLivretA
                liste_livretA2.append(montantLivretA)
                
            for j in liste_livretB:
                montantLivretB = montantLivretB * (livretB/100) + montantLivretB
                liste_livretB2.append(montantLivretB)
            
            for j in LLD:
                montantLLD = montantLLD * (livretLLD/100) + montantLLD
                list_LLD.append(montantLLD)
                
            montantSCPI2 = montant * (SCPI/100)
            for j in scpi:
                c = montant + montantSCPI2*i
                list_scpi.append(c)
                
            for j in assuranceVie:
                montantAssuranceVie = montantAssuranceVie * (AssuranceVieFondPropre/100) + montantAssuranceVie
                list_assuranceVie.append(montantAssuranceVie)
                
            for j in pel:
                montantPel = montantPel * (PEL/100) + montantPel
                list_pel.append(montantPel)
                
            for j in fondCommun:
                montantFondCommun = montantFondCommun * (FondCommunPlacement/100) + montantFondCommun
                list_fondcommun.append(montantFondCommun)
            

        liste_livretA.extend(liste_livretA2)
        liste_livretB.extend(liste_livretB2)
        LLD.extend(list_LLD)
        scpi.extend(list_scpi)
        assuranceVie.extend(list_assuranceVie)
        pel.extend(list_pel)
        fondCommun.extend(list_fondcommun)
            
        df = pd.DataFrame({
            "Livret A (plafond à 22950 €)" : liste_livretA,
            "Livret B (non plafonée)" : liste_livretB,
            "Livret LLD (plafond à 12000 €)" : LLD,
            "SCPI (non plafonée)" : scpi,
            "Assurance Vie fond euro (non plafonée)": assuranceVie,
            "PEL (plafond à 61200 €)" : pel,
            "Fond commun Placement (non plafonée)" : fondCommun,
            
        })

        df = df.reset_index()
        df.index += 1
        df.index.name = "Periode (Année)"
        df = df.drop(columns = "index", axis = 1)
        
        put_text("TABLEAU COMPARATIF").style('color: dark; font-size: 20px; font-weight:bold;')
        put_html(df.to_html(border = 0))
        fig3 = px.line(df, x=range(0,nombreAnnee), y=["Livret A (plafond à 22950 €)", "Livret B (non plafonée)","Livret LLD (plafond à 12000 €)","SCPI (non plafonée)","Assurance Vie fond euro (non plafonée)","PEL (plafond à 61200 €)","Fond commun Placement (non plafonée)"],title = "Comparatif des rendements",
        labels={
                     "x": "Nombre d'années",
                     "value": "Valeur",
                     "variable": "Type d'epargne"
                 },)
        html = fig3.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)
        put_text("CONFIEZ NOUS VOTRE PROJET D'EPARGNE").style('color: dark; font-size: 20px; font-weight:bold;')
        put_image(open("visite.png", 'rb').read())

    if (choix == "18 - Calcul des prix des villes au mètre carré") :

        liste_tendue = [ " Beauregard " ," Beynost " ," Dagneux " ," Fareins " ," Ferney-Voltaire " ," Frans " ," Jassans-Riottier " ," La Boisse " ," Massieux " ," Messimy-sur-Saône " ," Miribel Misérieux " ," Montluel " ," Neyron " ," Ornex " ,
        " Parcieux " ," Prévessin-Moëns Reyrieux " ," Saint-Bernard " ," Saint-Didier-de-Formans " ," Saint-Genis-Pouilly " ," Saint-Maurice-de-Beynost " ," Sainte-Euphémie " ," Sergy " ," Thoiry " ," Toussieux " ," Trévoux " ," Antibes " ," Aspremont " ,
        " Auribeau-sur-Siagne " ," Beaulieu-sur-Mer " ," Beausoleil " ," Berre-les-Alpes " ," Biot " ," Cabris " ," Cagnes-sur-Mer " ," Cannes " ," Cantaron " ," Cap-d'Ail " ," Carros " , " Castagniers " ," Castellar " ," Châteauneuf-Grasse " ,
        " Châteauneuf-Villevieille " ," Colomars " ," Contes " ," Drap " ," Èze " ," Falicon " ," Gattières " ," Gorbio " ," Gourdon " ," Grasse " ," La Colle-sur-Loup " ," La Gaude " ," La Roquette-sur-Siagne " ," La Trinité " ," La Turbie " ,
        " Le Bar-sur-Loup " ," Le Cannet " ," Le Rouret " ," Le Tignet " ," Mandelieu-la-Napoule " ," Menton " ," Mouans-Sartoux " ," Mougins " ," Nice " ," Opio " ," Pégomas " ," Peymeinade " ," Roquebrune-Cap-Martin " ," Roquefort-les-Pins " ,
        " Saint-André-de-la-Roche " ," Saint-Jean-Cap-Ferrat " ," Saint-Jeannet " ," Saint-Laurent-du-Var " ," Saint-Paul-de-Vence " ," Sainte-Agnès " ," Spéracèdes " ," Théoule-sur-Mer " ," Tourrette-Levens " ," Tourrettes-sur-Loup " ,
        " Valbonne " ," Vallauris " ," Vence " ," Villefranche-sur-Mer " ," Villeneuve-Loubet " ," Aix-en-Provence " ," Allauch " ," Arles " ," Aubagne " ," Auriol " ," Beaurecueil " ," Berre-l'Étang " ," Bouc-Bel-Air " ," Cabriès " ,
        " Cadolive " ," Ceyreste " ," Châteauneuf-le-Rouge " ," Châteauneuf-les-Martigues " ," Éguilles " ," Fos-sur-Mer " ," Fuveau " ," Gardanne " ," Gémenos " ," Gignac-la-Nerthe " ," Gréasque " ," Istres " ," La Bouilladisse " ,
        " La Ciotat " ," La DestrousseLa Penne-sur-Huveaune " ," Le Tholonet " ," Les Pennes-Mirabeau " ," Marignane " ," Marseille " ," Martigues " ," Meyreuil " ," Mimet " ," Miramas " ," Peynier " ," Peypin " ," Plan-de-Cuques " ," Port-de-Bouc " ,
        " Rognac " ," Roquevaire " ," Rousset " ," Saint-Chamas " ," Saint-Marc-Jaumegarde " ," Saint-Mitre-les-Remparts " ," Saint-Savournin " ," Saint-Victoret " ," Septèmes-les-Vallons " ," Simiane-Collongue " ," Trets " ," Velaux " ," Venelles " ,
        " Vitrolles " ," Angoulins " ," Aytré " ," Châtelaillon-Plage " ," Dompierre-sur-Mer " ," La Rochelle " ," Lagord " ," Nieul-sur-Mer " ," Périgny " ," Puilboreau " ," Salles-sur-Mer " ," Ajaccio " ," Bastia " ," Biguglia " ,
        " Brando " ," Furiani " ," San-Martino-di-Lota " ," Santa-Maria-di-Lota " ," Ville-di-Pietrabugno " ," Fourques " ," Aucamville " ," Aussonne " ," Auzeville-Tolosane " ," Auzielle " ," Balma " ," Beaupuy " ," Beauzelle " ," Belberaud " ,
        " Blagnac " ," Brax " , " Bruguières " , " Castanet-Tolosan " , " Castelginest " , " Castelmaurou " , " Cépet " , " Colomiers " , " Cornebarrieu " , " Cugnaux " , " Daux " , " Deyme " , " Eaunes " , " Escalquens " , " Fenouillet " ,
        " Fonbeauzard " , " Frouzins " , " Gagnac-sur-Garonne " , " Gratentour " , " L'Union " , " La Salvetat-Saint-Gilles " , " Labarthe-sur-Lèze " , " Labastide-Saint-Sernin " , " Labège " , " Lacroix-Falgarde " , " Lapeyrouse-Fossat " , 
        " Launaguet " ," Lauzerville " , " Léguevin " , " Lespinasse " ," Mervilla " ," Mondonville " ," Montberon " ," Montrabé " ," Muret " ," Péchabou " ," Pechbonnieu " ," Pechbusque " ," Pibrac " ," Pin-Balma " ," Pins-Justaret " ,
        " Pinsaguel " ," Plaisance-du-Touch " ," Pompertuzat " ," Portet-sur-Garonne " ," Quint-Fonsegrives " ," Ramonville-Saint-Agne " ," Roques " ," Roquettes " ," Rouffiac-Tolosan " ," Saint-Alban " ," Saint-Geniès-Bellevue " ," Saint-Jean " ," Saint-Jory " ,
        " Saint-Loup-Cammas " ," Saint-Orens-de-Gameville " ," Saint-Sauveur " ," Seilh " ," Seysses " ," Toulouse " ," Tournefeuille " ," Vieille-Toulouse " ," Vigoulet-Auzil " ," Villate " ," Villeneuve-Tolosane " ," Ambarès-et-Lagrave " ,
        " Arcachon " ," Artigues-près-Bordeaux " ," Arveyres " ," Bassens " ," Baurech " ," Bègles " ," Blanquefort " ," Bonnetan " ," Bordeaux " ," Bouliac " ," Bruges " ," Cadarsac " ," Cadaujac " ," Cambes " ," Camblanes-et-Meynac " ,
        " Canéjan " ," Carbon-Blanc " ," Carignan-de-Bordeaux " ," Cénac " ," Cenon " ," Cestas " ," Eysines " ," Fargues-Saint-Hilaire " ," Floirac " ," Gradignan " ," Gujan-Mestras " ," Izon " ," La Teste-de-Buch " ," Langoiran " ,
        " Latresne " , " Le Bouscat " ," Le Haillan " ," Le Pian-Médoc " ," Le Taillan-Médoc " ," Le Teich " ," Le Tourne " ," Léognan " ," Lestiac-sur-Garonne " ," Lignan-de-Bordeaux " ," Lormont " ," Martignas-sur-Jalle " ," Martillac " ,
        " Mérignac " , " Montussan " , " Nérigean " , " Paillet " , " Parempuyre " , " Pessac " , " Pompignac " , " Quinsac " , " Saint-Aubin-de-Médoc " , " Saint-Caprais-de-Bordeaux " , " Saint-Jean-d'Illac " , " Saint-Loubès " ,
        " Saint-Médard-d'Eyrans " , " Saint-Médard-en-Jalles " , " Saint-Quentin-de-Baron " , " Saint-Sulpice-et-Cameyrac " , " Saint-Vincent-de-Paul " , " Sainte-Eulalie " , " Sallebœuf " , " Tabanac " , " Talence " , " Tresses " ,
        " Vayres " , " Villenave-d'Ornon " , " Yvrac " , " Assas " , " Balaruc-le-Vieux " , " Balaruc-les-Bains " , " Castelnau-le-Lez " , " Clapiers " , " Fabrègues " , " Frontignan " , " Gigean " , " Grabels " , " Jacou " ,
        " Juvignac " , " Lattes " , " Lavérune " , " Le Crès " , " Montbazin " , " Montferrier-sur-Lez " , " Montpellier " , " Pérols " , " Poussan " , " Prades-le-Lez " , " Saint-Clément-de-Rivière " , " Saint-Gély-du-Fesc " , " Saint-Jean-de-Védas " ,
        " Saint-Vincent-de-Barbeyrargues " , " Saussan " , " Sète " , " Teyran " , " Vendargues " , " Villeneuve-lès-Maguelone " , " Beaucroissant " , " Biviers " , " Bresson " , " Champ-sur-Drac " , " Charnècles " , " Chasse-sur-Rhône " ,
        " Chirens " , " Claix " , " Corenc " , " Coublevie " , " Domène " , " Échirolles " , " Eybens " , " Fontaine " , " Fontanil-Cornillon " , " Froges " , " Gières " , " Grenoble " , " Jarrie " , " La Buisse " , " La Murette " ,
        " La Pierre " , " La Tronche " , " Le Champ-près-Froges " , " Le Pont-de-Claix " , " Le Versoud " , " Meylan " , " Moirans " , " Montbonnot-Saint-Martin " , " Murianette " , " Noyarey " , " Poisat " , " Pommiers-la-Placette " , " Réaumont " , " Renage " , " Rives " , " Saint-Blaise-du-Buis " , " Saint-Cassien " ,
        " Saint-Égrève " ," Saint-Ismier " ," Saint-Jean-de-Moirans " ," Saint-Martin-d'Hères " ," Saint-Martin-le-Vinoux " ," Saint-Nazaire-les-Eymes " ," Sassenage " ," Seyssinet-Pariset " ," Seyssins " ," Varces-Allières-et-Risset " ,
        " Venon " , " Veurey-Voroize " , " Villard-Bonnot " , " Voiron " , " Voreppe " , " Vourey " , " Saint-André-de-Seignanx " , " Saint-Martin-de-Seignanx " , " Tarnos " , " Basse-Goulaine " , " Batz-sur-Mer " , " Bouaye " , " Bouguenais " ,
        " Carquefou " , " Couëron " , " Donges " , " Guérande " , " Haute-Goulaine " , " Indre " , " La Baule-Escoublac " , " La Chapelle-sur-Erdre " , " La Montagne " , " Le Croisic " , " Le Pouliguen " , " Les Sorinières " , " Montoir-de-Bretagne " ,
        " Nantes " , " Orvault " , " Pont-Saint-Martin " , " Pornichet " , " Port-Saint-Père " , " Rezé " , " Saint-Aignan-Grandlieu " , " Saint-André-des-Eaux " , " Saint-Herblain " , " Saint-Jean-de-Boiseau " , " Saint-Léger-les-Vignes " ,
        " Saint-Nazaire " , " Saint-Sébastien-sur-Loire " , " Sainte-Luce-sur-Loire " , " Sautron " , " Thouaré-sur-Loire " , " Trignac " , " Vertou " , " Anstaing " , " Avelin " , " Baisieux " , " Bondues " , " Bousbecque " , " Capinghem " ,
        " Chéreng " , " Comines " , " Croix " , " Emmerin " , " Englos " , " Faches-Thumesnil " , " Forest-sur-Marque " , " Gruson " , " Hallennes-lez-Haubourdin " , " Halluin " , " Haubourdin " , " Hem " , " La Madeleine " , " Lambersart " ,
        " Lannoy " ," Leers " ," Lesquin " ," Lezennes " ," Lille " ," Linselles " ," Lompret " ," Loos " ," Lys-lez-Lannoy " ," Marcq-en-Barœul " ," Marquette-lez-Lille " ," Mons-en-Barœul " ," Mouvaux " ," Neuville-en-Ferrain " ," Noyelles-lès-Seclin " ," Pérenchies " ," Prémesques " ,
        " Quesnoy-sur-Deûle " ," Ronchin " ," Roncq " ," Roubaix " ," Sailly-lez-Lannoy " ," Saint-André-lez-Lille " ," Santes " ," Seclin " ," Sequedin " ," Templemars " ," Toufflers " ," Tourcoing " ," Tressin " ,
        " Vendeville " ," Verlinghem " ," Villeneuve-d'Ascq " ," Wambrechies " ," Wasquehal " ," Wattignies " ," Wattrelos " ," Wervicq-Sud " ," Willems " ," Allonne " " Beauvais " ," Goincourt " ," Tillé " ," Ahetze " ," Anglet " ," Arbonne " ,
        " Arcangues " , " Ascain " , " Bassussarry " , " Bayonne " , " Biarritz " , " Bidart " , " Biriatou " , " Boucau " , " Ciboure " , " Guéthary " , " Hendaye " , " Jatxou " , " Lahonce " , " Larressore " , " Mouguerre " , " Saint-Jean-de-Luz " , " Saint-Pierre-d'Irube " , " Urcuit " , " Urrugne " , " Ustaritz " , " Villefranque " , " Achenheim " ,
        " Bischheim " , " Eckbolsheim " , " Eschau " , " Fegersheim " , " Hœnheim " , " Illkirch-Graffenstaden " , " Lampertheim " , " Lingolsheim " , " Lipsheim " , " Mittelhausbergen " , " Mundolsheim " , " Niederhausbergen " , " Oberhausbergen " ,
        " Oberschaeffolsheim " , " Ostwald " , " Plobsheim " , " Reichstett " , " Schiltigheim " , " Souffelweyersheim " , " Strasbourg " , " Vendenheim " , " Wolfisheim " , " Albigny-sur-Saône " , " Ambérieux " , " Anse " , " Arnas " ,
        " Belmont-d'Azergues " , " Brignais " , " Brindas " , " Bron " , " Cailloux-sur-Fontaines " , " Caluire-et-Cuire " , " Champagne-au-Mont-d'Or " ," Chaponnay " ," Chaponost " ," Charbonnières-les-Bains " ," Charly " ," Charnay " ," Chassagny " ," Chasselay " ,
        " Chassieu " ," Chazay-d'Azergues " ," Civrieux-d'Azergues " ," Cogny " ," Collonges-au-Mont-d'Or " ," Communay " ," Corbas " ," Couzon-au-Mont-d'Or " ," Craponne " ," Curis-au-Mont-d'Or " ," Dardilly " ," Décines-Charpieu " ," Denicé " ,
        " Dommartin " ," Écully " ," Feyzin " ," Fleurieu-sur-Saône " ," Fontaines-Saint-Martin " ," Fontaines-sur-Saône " ," Francheville " ," Genas " ," Genay " ," Givors " ," Gleizé " ," Grézieu-la-Varenne " ," Grigny " ," Irigny " ," Jarnioux " ,
        " La Mulatière " , " La Tour-de-Salvagny " , " Lacenas " , " Lachassagne " , " Lentilly " , " Les Chères " , " Liergues " , " Limas " , " Limonest " , " Lissieu " , " Loire-sur-Rhône " , " Lozanne "  " Lucenay " , " Lyon " , " Marcilly-d'Azergues " ,
        " Marcy " , " Marcy-l'Étoile " , " Marennes " , " Messimy " , " Meyzieu " , " Millery " , " Mions " , " Montagny " , " Montanay " , " Morancé " , " Neuville-sur-Saône " , " Orliénas " , " Oullins " , " Pierre-Bénite " , " Pommiers " ,
        " Pouilly-le-Monial " , " Rillieux-la-Pape " , " Rochetaillée-sur-Saône " , " Saint-Cyr-au-Mont-d'Or " , " Saint-Didier-au-Mont-d'Or " , " Saint-Fons " , " Saint-Genis-Laval " , " Saint-Genis-les-Ollières " , " Saint-Jean-des-Vignes " , " Saint-Priest " , " Saint-Romain-au-Mont-d'Or " ,
        " Saint-Romain-en-Gier " , " Saint-Symphorien-d'Ozon " , " Sainte-Consorce " , " Sainte-Foy-lès-Lyon " , " Sathonay-Camp " , " Sathonay-Village " , " Sérézin-du-Rhône " , " Simandres " , " Solaize " , " Soucieu-en-Jarrest " , " Taluyers " ,
        " Tassin-la-Demi-Lune " , " Ternay " , " Thurins " , " Vaugneray " , " Vaulx-en-Velin " , " Vénissieux " , " Vernaison " , " Villefranche-sur-Saône " , " Villeurbanne " , " Vourles " , " Allinges " , " Ambilly " , " Annecy " , " Annecy-le-Vieux " ,
        " Annemasse " , " Anthy-sur-Léman " , " Archamps " , " Argonay " , " Armoy " , " Arthaz-Pont-Notre-Dame " , " Bonne " , " Bossey " , " Chavanod " , " Chevaline " , " Collonges-sous-Salève " , " Contamine-sur-Arve " , " Cran-Gevrier " ,
        " Cranves-Sales " , " Doussard " , " Duingt " , " Épagny " , " Étrembières " , " Évian-les-Bains " , " Excenevex " , " Faucigny " , " Fillinges " , " Gaillard " , " Juvigny " , " Lathuile " , " Lovagny " , " Lucinges " , " Lugrin " ,
        " Machilly " , " Marcellaz " , " Margencel " , " Marin " , " Maxilly-sur-Léman " , " Metz-Tessy " , " Meythet " , " Monnetier-Mornex " , " Nangy " , " Neuvecelle " , " Neydens " , " Pers-Jussy " , " Poisy " , " Pringy " , " Publier " ,
        " Reignier-Ésery " , " Saint-Cergues " , " Saint-Jorioz " , " Saint-Julien-en-Genevois " , " Sciez " , " Sévrier " , " Seynod " , " Sillingy " , " Thonon-les-Bains " , " Vétraz-Monthoux " , " Ville-la-Grand " , " Paris " , " Boissise-le-Roi " ,
        " Brou-sur-Chantereine " ," Bussy-Saint-Georges " ," Bussy-Saint-Martin " ," Carnetin " ," Cesson " ," Chalifert " ," Champs-sur-Marne " ," Chanteloup-en-Brie " ," Chelles " ," Chessy " ," Collégien " ," Combs-la-Ville " ," Conches-sur-Gondoire " ," Courtry " ," Crégy-lès-Meaux " ," Croissy-Beaubourg " ,
        " Dammarie-les-Lys " ," Dampmart " ," Émerainville " ," Ferrières-en-Brie " ," Gouvernes " ," Guermantes " ," La Rochette " ," Lagny-sur-Marne " ," Le Mée-sur-Seine " ," Le Mesnil-Amelot "," Lésigny " ," Lieusaint " ," Livry-sur-Seine " ,
        " Lognes " ," Meaux " , " Melun " , " Mitry-Mory " , " Moissy-Cramayel " , " Montévrain " , " Nandy " , " Nanteuil-lès-Meaux " , " Noisiel " , " Ozoir-la-Ferrière " , " Poincy " , " Pomponne " , " Pontault-Combault " , " Pringy " ,
        " Roissy-en-Brie " , " Rubelles " , " Saint-Fargeau-Ponthierry " , " Saint-Thibault-des-Vignes " , " Savigny-le-Temple " , " Servon " , " Thorigny-sur-Marne " , " Torcy " , " Trilport " , " Vaires-sur-Marne " , " Vaux-le-Pénil " ,
        " Vert-Saint-Denis " , " Villenoy " , " Villeparisis " , " Achères " , " Andrésy " , " Aubergenville " , " Auffreville-Brasseuil " , " Bazoches-sur-Guyonne " , " Bois-d'Arcy " , " Bougival " , " Buc " , " Buchelay " , " Carrières-sous-Poissy " , " Carrières-sur-Seine " ,
        " Chambourcy " , " Chanteloup-les-Vignes " , " Chapet " , " Chatou " , " Chevreuse " , " Coignières " , " Conflans-Sainte-Honorine " , " Croissy-sur-Seine " , " Élancourt " , " Évecquemont " , " Flins-sur-Seine " , " Follainville-Dennemont " ,
        " Fontenay-le-Fleury " , " Fourqueux " , " Gaillon-sur-Montcient " , " Gargenville " , " Guyancourt " , " Hardricourt " , " Houilles " , " Issou " , " Jouars-Pontchartrain " , " Jouy-en-Josas " , " Juziers " , " L'Étang-la-Ville " , " La Celle-Saint-Cloud " ,
        " La Verrière " , " Le Chesnay " , " Le Mesnil-le-Roi " , " Le Mesnil-Saint-Denis " , " Le Pecq " , " Le Port-Marly " , " Le Tremblay-sur-Mauldre " , " Le Vésinet " , " Les Clayes-sous-Bois " , " Les Loges-en-Josas " , " Les Mureaux " ,
        " Limay " ," Louveciennes " ," Magnanville " ," Magny-les-Hameaux " ," Maisons-Laffitte " ," Mantes-la-Jolie " ," Mantes-la-Ville " ," Mareil-Marly " ," Marly-le-Roi " ," Maurecourt " ," Maurepas " ," Médan " ," Meulan-en-Yvelines " ,
        " Mézy-sur-Seine " ," Montesson " ," Montigny-le-Bretonneux " ," Neauphle-le-Château " ," Neauphle-le-Vieux " ," Orgeval " ," Plaisir " ," Poissy " ," Porcheville " ," Rocquencourt " ," Saint-Cyr-l'École " ," Saint-Germain-en-Laye " ,
        " Saint-Rémy-l'Honoré " ," Saint-Rémy-lès-Chevreuse " ," Sartrouville " ," Tessancourt-sur-Aubette " ," Trappes " ," Triel-sur-Seine " ," Vaux-sur-Seine " , " Vélizy-Villacoublay " , " Verneuil-sur-Seine " , " Vernouillet " ,
        " Versailles " ," Vert " ," Villennes-sur-Seine " ," Villepreux " ," Villiers-Saint-Frédéric " ," Viroflay " ," Voisins-le-Bretonneux " ," Bandol " ," Belgentier " ," Carqueiranne " ," Cuers " ," Draguignan " ," Évenos " ," Flayosc " ,
        " Fréjus " ," Hyères " ," La Cadière-d'Azur " ," La Crau " ," La Farlède " ," La Garde " ," La Motte " ," La Seyne-sur-Mer " ," La Valette-du-Var " ," Le Beausset " ," Le Castellet " ," Le Muy " ," Le Pradet " ," Le Revest-les-Eaux " ,
        " Les Arcs " ," Ollioules " ," Puget-sur-Argens " ," Saint-Cyr-sur-Mer " ," Saint-Mandrier-sur-Mer " ," Saint-Raphaël " ," Saint-Zacharie " ," Sanary-sur-Mer " ," Six-Fours-les-Plages " ," Solliès-Pont " ," Solliès-Toucas " ,
        " Solliès-Ville " ," Toulon " ," Trans-en-Provence " ," Vidauban " , " Arpajon " , " Athis-Mons " , " Ballainvilliers " , " Bièvres " , " Bondoufle " , " Boussy-Saint-Antoine " , " Brétigny-sur-Orge " , " Breuillet " , " Breux-Jouy " ,
        " Brunoy " , " Bruyères-le-Châtel " , " Bures-sur-Yvette " , " Champlan " , " Chilly-Mazarin " , " Corbeil-Essonnes " , " Courcouronnes " , " Crosne " , " Draveil " , " Écharcon " , " Égly " , " Épinay-sous-Sénart " , " Épinay-sur-Orge " ,
        " Étiolles " , " Évry " , " Fleury-Mérogis " , " Fontenay-le-Vicomte " , " Gif-sur-Yvette " , " Gometz-le-Châtel " , " Grigny " , " Igny " , " Juvisy-sur-Orge " , " La Norville " , " La Ville-du-Bois " , " Le Coudray-Montceaux " ,
        " Le Plessis-Pâté " ," Les Ulis " , " Leuville-sur-Orge " , " Linas " , " Lisses " , " Longjumeau " , " Longpont-sur-Orge " , " Marcoussis " , " Massy " , " Mennecy " , " Montgeron " , " Montlhéry " , " Morangis " , " Morsang-sur-Orge " ,
        " Morsang-sur-Seine " ," Nozay " ," Ollainville " ," Ormoy " ," Orsay " ," Palaiseau " ," Paray-Vieille-Poste " ," Quincy-sous-Sénart " ," Ris-Orangis " ," Saclay " ," Saint-Aubin " ," Saint-Germain-lès-Arpajon " ," Saint-Germain-lès-Corbeil " ,
        " Saint-Michel-sur-Orge " , " Saint-Pierre-du-Perray " , " Saint-Yon " , " Sainte-Geneviève-des-Bois " , " Saintry-sur-Seine " , " Saulx-les-Chartreux " , " Savigny-sur-Orge " , " Soisy-sur-Seine " , " Varennes-Jarcy " , " Vauhallan " ,
        " Verrières-le-Buisson " , " Vigneux-sur-Seine " , " Villabé " , " Villebon-sur-Yvette " , " Villejust " , " Villemoisson-sur-Orge " , " Villiers-le-Bâcle " , " Villiers-sur-Orge " , " Viry-Châtillon " , " Wissous " , " Yerres " ,
        " Antony " , " Asnières-sur-Seine " , " Bagneux " , " Bois-Colombes " , " Boulogne-Billancourt " , " Bourg-la-Reine " , " Châtenay-Malabry " , " Châtillon " , " Chaville " , " Clamart " , " Clichy " , " Colombes " , " Courbevoie " ,
        " Fontenay-aux-Roses " ," Garches " ," Gennevilliers " ," Issy-les-Moulineaux " ," La Garenne-Colombes " ," Le Plessis-Robinson " ," Levallois-Perret " ," Malakoff " ," Marnes-la-Coquette " ," Meudon " ," Montrouge " ," Nanterre " ,
        " Neuilly-sur-Seine " ," Puteaux " ," Rueil-Malmaison " ," Saint-Cloud " ," Sceaux " ," Sèvres " ," Suresnes " ," Vanves " ," Vaucresson " ," Ville-d'Avray " ," Villeneuve-la-Garenne " ," Aubervilliers " ," Aulnay-sous-Bois " ,
        " Bagnolet " ," Bobigny " ," Bondy " ," Clichy-sous-Bois " ," Coubron " ," Drancy " ," Dugny " ," Épinay-sur-Seine " ," Gagny " ," Gournay-sur-Marne " ," L'Île-Saint-Denis" ," La Courneuve " ," Le Blanc-Mesnil " ," Le Bourget " ,
        " Le Pré-Saint-Gervais " ," Le Raincy " ," Les Lilas " ," Les Pavillons-sous-Bois " ," Livry-Gargan " ," Montfermeil " ," Montreuil " ," Neuilly-Plaisance " ," Neuilly-sur-Marne " ," Noisy-le-Grand " ," Noisy-le-Sec " ," Pantin " ,
        " Pierrefitte-sur-Seine " ," Romainville " ," Rosny-sous-Bois " ," Saint-Denis " ," Saint-Ouen " ," Sevran " ," Stains " ," Tremblay-en-France " ," Vaujours " ," Villemomble " ," Villepinte " ," Villetaneuse " ," Ablon-sur-Seine " ,
        " Alfortville " ," Arcueil " ," Boissy-Saint-Léger " ," Bonneuil-sur-Marne " ," Bry-sur-Marne " ," Cachan " ," Champigny-sur-Marne " ," Charenton-le-Pont " ," Chennevières-sur-Marne " ," Chevilly-Larue " ," Choisy-le-Roi " ," Créteil " ,
        " Fontenay-sous-Bois " ," Fresnes " ," Gentilly " ," Ivry-sur-Seine " ," Joinville-le-Pont " ," L'Haÿ-les-Roses " ," La Queue-en-Brie " ," Le Kremlin-Bicêtre " ," Le Perreux-sur-Marne " ," Le Plessis-Trévise " ," Limeil-Brévannes " ," Maisons-Alfort " ," Mandres-les-Roses " ,
        " Marolles-en-Brie " ," Nogent-sur-Marne " ," Noiseau " ," Orly " ," Ormesson-sur-Marne " ," Périgny " ," Rungis " ," Saint-Mandé " ," Saint-Maur-des-Fossés " ," Saint-Maurice " ," Santeny " ," Sucy-en-Brie " ," Thiais " ," Valenton " ," Villecresnes " ,
        " Villejuif " ," Villeneuve-le-Roi " ," Villeneuve-Saint-Georges " ," Villiers-sur-Marne " ," Vincennes " ," Vitry-sur-Seine " ," Andilly " ," Argenteuil " ," Arnouville " ," Auvers-sur-Oise " ," Beauchamp " ," Bessancourt " ," Bezons " ,
        " Bonneuil-en-France " ," Bouffémont " ," Butry-sur-Oise " ," Cergy " ," Champagne-sur-Oise " ," Cormeilles-en-Parisis " ," Courdimanche " ," Deuil-la-Barre " ," Domont " ," Eaubonne " ," Écouen " ," Enghien-les-Bains " ," Épiais-lès-Louvres " ,
        " Éragny " ," Ermont " ," Ézanville " ," Franconville " ," Frépillon " ," Garges-lès-Gonesse " ," Gonesse " ," Goussainville " ," Groslay " ," Herblay " , " Jouy-le-Moutier " , " L'Isle-Adam " , " La Frette-sur-Seine " , " Le Plessis-Bouchard " , " Le Thillay " ,
        " Margency " , " Mériel " , " Méry-sur-Oise " , " Montigny-lès-Cormeilles " , " Montlignon " , " Montmagny " , " Montmorency " , " Nesles-la-Vallée " , " Neuville-sur-Oise " , " Osny " ,
        " Parmain " ," Pierrelaye " ," Piscop " ," Pontoise " ," Puiseux-Pontoise " ," Roissy-en-France " ," Saint-Brice-sous-Forêt " ," Saint-Gratien " ," Saint-Leu-la-Forêt " ," Saint-Ouen-l'Aumône " ," Saint-Prix " ," Sannois " ," Sarcelles " ,
        " Soisy-sous-Montmorency " ," Taverny " ," Valmondois " ," Vaudherland " ," Vauréal " ," Villiers-Adam " ," Villiers-le-Bel ","Paris 20e arrondissement","Paris 19e arrondissement","Paris 11e arrondissement","Paris 18e arrondissement",
        "Paris 17e arrondissement","Paris 10e arrondissement","Paris 9e arrondissement","Paris 8e arrondissement","Paris 3e arrondissement","Paris 2e arrondissement","Paris 1er arrondissement","Paris 13e arrondissement","Paris 12e arrondissement","Paris 15e arrondissement","Paris 14e arrondissement",
        "Paris 7e arrondissement","Paris 6e arrondissement","Paris 5e arrondissement","Paris 4e arrondissement","Paris 16e arrondissement","Lyon 9e arrondissement","Lyon 6e arrondissement","Lyon 4e arrondissement","Lyon 1er arrondissement",
        "Lyon 8e arrondissement","Lyon 7e arondissement","Lyon 5e arrondissement","Lyon 3 arrondissement","Lyon 2e arrondissement","Marseille 13e arrondissement","Marseille 15e arrondissement","Marseille 14e arrondissement","Marseille 16e arrondissement",
        "Marseille 12e arrondissement","Marseille 11e arrondissement","Marseille 10e arrondissement","Marseille 7e arrondissement","Marseille 6e arrondissement","Marseille 5e arrondissement","Marseille 4e arrondissement","Marseille 3e arrondissement",
        "Marseille 2e arrondissement","Marseille 1e arrondissement","Marseille 9e arrondissement","Marseille 8e arrondissement"]
        
        #2017
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        df17 = pd.read_csv("df17.csv",sep=";")
        df17["Commune"] = df17["Commune"].str.lower()
        df17['Commune'] = df17['Commune'].str.capitalize() 
        #df17 = df17[["Commune", "Prixm2", "Code_postal"]]
        df17 = df17.rename(columns = {"Commune" : "Ville", "Prixm2" :"Prix du m\u00b2 (en euros)"})   
        liste17 = df17["Ville"].tolist()
        liste17.sort()
        #2018
        df18 = pd.read_csv("df18.csv",sep=";")
        df18 = df18[["Commune","Prixm2_Moy","Code_postal"]]
        df18["Commune"] = df18["Commune"].str.lower()
        df18['Commune'] = df18['Commune'].str.capitalize()
        df18 = df18.rename(columns = {"Commune" : "Ville", "Prixm2_Moy" :"Prix du m\u00b2 (en euros)"})   
        liste18 = df18["Ville"].tolist()
        liste18.sort()
        #2019
        df19 = pd.read_csv("df.csv",sep=";")
        df19 = df19.rename(columns ={"INSEE_COM":"Code INSEE","NOM_COM_M":"Ville","PrixMoyen_M2":"Prix du m\u00b2 (en euros)","INSEE_DEP":"Departement"})
        df19 = df19[["Ville","Departement","Prix du m\u00b2 (en euros)"]]
        df19["Ville"] = df19["Ville"].str.lower()
        df19['Ville'] = df19['Ville'].str.capitalize()
        liste3 = df19["Ville"].tolist()
        liste3.sort()
        #2020
        df20 = pd.read_csv("communes2020.csv", sep = ";")
        df20["Commune"] = df20["Commune"].str.lower()
        df20['Commune'] = df20['Commune'].str.capitalize()
        liste = df20["Commune"].tolist()
        #2021
        # df21 = pd.read_csv("full21.csv", sep = ",")
        # df21 = df21[df21["nature_mutation"] == "Vente"]
        # df21 = df21[df21["type_local"] == "Appartement"]
        # df21 = df21[["code_postal","nom_commune","valeur_fonciere","surface_reelle_bati"]]
        # df21["Prix du metre carre"] = df21["valeur_fonciere"]/df21["surface_reelle_bati"]
        # df21 = df21.groupby(['nom_commune']).mean()
        # df21 = df21.reset_index()
        # df21["nom_commune"] = df21["nom_commune"].str.lower()
        # df21['nom_commune'] = df21['nom_commune'].str.capitalize()
        # liste2 = df21["nom_commune"].tolist()
        #
        #liste_tendue = [[word.capitalize() for word in text.split()] for text in liste_tendue]
        #liste_tendue = [item for sublist in liste_tendue for item in sublist]
        #liste_tendue.sort()
        liste_tendue = [word[:1].upper() + word[1:] for word in liste_tendue ]
        liste_tendue = [x.strip(' ') for x in liste_tendue]
        liste_tendue.sort()
        choix = select("Selectionner la ville :", liste_tendue)
        if choix in liste:
            df2 = df20[df20["Commune"] == choix]
            df2 = df2[["Commune","code_postal","Prix du metre carre"]]
            df2.rename(columns = {'Commune' : 'Ville', 'code_postal' : 'Code Postal', "Prix du metre carre": "Prix du m\u00b2 en 2020"}, inplace = True)
        # if choix in liste2:
        #     df3 = df21[df21["nom_commune"] == choix]
        #     df3 = df3[["nom_commune","code_postal","Prix du metre carre"]]
        #     df3.rename(columns = {'nom_commune' : 'Ville', 'code_postal' : 'Code Postal', "Prix du metre carre": "Prix du m\u00b2 en 2021"}, inplace = True)
        #     df2["Prix du m\u00b2 en 2021"] = int(df3["Prix du m\u00b2 en 2021"].values)
        if choix in liste3:
            df4 = df19[df19["Ville"] == choix]
            df4 = df4[["Ville","Prix du m\u00b2 (en euros)"]]
            df4.rename(columns = {"Prix du m\u00b2 (en euros)": "Prix du m\u00b2 en 2019"}, inplace = True)
            #df2["Prix du m\u00b2 en 2019"] = int(df4["Prix du m\u00b2 en 2019"].values)
            df2["Prix du m\u00b2 en 2019"] = df4["Prix du m\u00b2 en 2019"].iloc[0]
            
        if choix in liste17:
            df5 = df17[df17["Ville"] == choix]
            df5 = df5[["Ville","Prix du m\u00b2 (en euros)"]]
            df5.rename(columns = {"Prix du m\u00b2 (en euros)": "Prix du m\u00b2 en 2017"}, inplace = True)
            #df2["Prix du m\u00b2 en 2017"] = int(df5["Prix du m\u00b2 en 2017"].values)
            df2["Prix du m\u00b2 en 2017"] = int(df5["Prix du m\u00b2 en 2017"].iloc[0])
            
        if choix in liste18:
            df6 = df18[df18["Ville"] == choix]
            df6 = df6[["Ville","Prix du m\u00b2 (en euros)"]]
            df6.rename(columns = {"Prix du m\u00b2 (en euros)": "Prix du m\u00b2 en 2018"}, inplace = True)
            #df2["Prix du m\u00b2 en 2018"] = int(df6["Prix du m\u00b2 en 2018"].values)
            df2["Prix du m\u00b2 en 2018"] = int(df6["Prix du m\u00b2 en 2018"].iloc[0])
            

        df2 = df2[["Ville","Code Postal","Prix du m² en 2017","Prix du m² en 2018","Prix du m² en 2019","Prix du m² en 2020"]]
        #df2["Code Postal"] = int(df2["Code Postal"])
        #df2 = df2[["Ville","Code Postal","Prix du m² en 2017","Prix du m² en 2019","Prix du m² en 2020","Prix du m² en 2021"]]

        df2["Zone tendue"] = df2['Ville'].apply(lambda x: any([k in x for k in liste_tendue]))
        df2 = df2.replace({True:"Oui", False : "Non"})
        df2["Rentabilité"] = (df2["Prix du m² en 2020"] - df2["Prix du m² en 2017"] > 0) & (df2["Zone tendue"] == "Oui")
        df2 = df2.replace({True:"Favorable", False : "Non Favorable"})
        df2 = df2.style.hide_index()
        put_html(df2.to_html())
        df2 = df2.data
        data = [df2["Prix du m\u00b2 en 2017"].values,df2["Prix du m\u00b2 en 2018"].values,df2["Prix du m\u00b2 en 2019"].values,df2["Prix du m\u00b2 en 2020"].values ]
        annee = ["2017","2018","2019","2020"]
        data2 = pd.DataFrame({"Prix" : data, "Année" : annee})
        data2["Prix"] = data2["Prix"].astype(int)
        fig2 = px.bar(data2,x="Année", y="Prix",title = "Évolution du prix du m\u00b2 à {} en \N{euro sign}".format(choix))
        fig2.update_xaxes(type='category')
        html = fig2.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)

        with urlopen('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson') as response:
            geojson = json.load(response)
        df1 = pd.DataFrame([x['properties'] for x in geojson['features']])
        df1['randNumCol'] = np.random.randint(0, 10, df1.shape[0]).astype('str')

        df1 = df1.rename(columns = {"code" : "Code Postal", "nom" : "Ville"})
        df1 = df1[["Code Postal", "Ville"]]

        df200 = pd.read_csv("df20.csv", sep=";")
        df200["Code Postal"] = df200["Code Postal"].str.zfill(2)
        
        df_merge = pd.merge(df1, df200, on='Code Postal')
        
        fig = px.choropleth_mapbox(df_merge, geojson=geojson, featureidkey='properties.code', locations='Code Postal', 
                    color='Prix', center = {"lat":47, "lon":1}, zoom=4.4, mapbox_style="carto-positron",width=700, 
                    opacity=0.9,color_continuous_scale="Viridis", title = "Prix des régions en m\u00b2 (en euros)")

        fig.update_layout(mapbox_style="open-street-map",
                    showlegend=True,
                    margin={"r":0,"t":0,"l":0,"b":0}, 
                    width=700, 
                 height=485,
                    title = "Prix du m\u00b2 dans les régions en France en \N{euro sign} en 2022",
                    )
        put_text("Prix du m\u00b2 dans les régions en France en \N{euro sign} en 2022").style('color: dark; font-size: 20px; font-weight:bold;')
        html = fig.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)
        

        df18 = df18.loc[df18['Ville'].isin(liste_tendue)]

        df17 = df17.loc[df17['Ville'].isin(liste_tendue)]

        #df20 = pd.read_csv("communes2020.csv", sep = ";")
        #df20["Commune"] = df20["Commune"].str.lower()
        #df20['Commune'] = df20['Commune'].str.capitalize()
        df20 = df20.rename(columns = {"Commune" : "Ville", "Prix du metre carre" : "Prix du m² (en euros)"})
        df20 = df20.loc[df20['Ville'].isin(liste_tendue)]
        
        
        df19 = df19.loc[df19['Ville'].isin(liste_tendue)]

        df_merge = pd.merge(df17,df18[["Prix du m² (en euros)","Ville"]], on = "Ville")
        df_merge2 = pd.merge(df_merge,df19[["Prix du m² (en euros)","Ville"]], on = "Ville")
        df_merge2 = df_merge2.rename(columns = {"Prix du m² (en euros)_x" : "Prix du m² (en euros) en 2017", "Prix du m² (en euros)_y" : "Prix du m² (en euros) en 2018","Prix du m² (en euros)" : "Prix du m² (en euros) en 2019"})
        df_merge3 = pd.merge(df_merge2,df20[["Prix du m² (en euros)","Ville"]], on = "Ville")
        df_merge3 = df_merge3.rename(columns = {"Prix du m² (en euros)" : "Prix du m² (en euros) en 2020"})
        df_merge3 = df_merge3.loc[:,~df_merge3.columns.duplicated()]
        df_merge3 = df_merge3.drop_duplicates(subset=['Ville'])
        df_merge3 = df_merge3.rename(columns = {"Code_postal" : "Code Postal"})
        df_merge3 = df_merge3[["Ville", "Code Postal", "Prix du m² (en euros) en 2017", "Prix du m² (en euros) en 2018", "Prix du m² (en euros) en 2019", "Prix du m² (en euros) en 2020"]]
        df_merge3["Différence de montant entre 2020 et 2017"] = df_merge3["Prix du m² (en euros) en 2020"] - df_merge3["Prix du m² (en euros) en 2017"]

        df_pire = df_merge3.sort_values("Différence de montant entre 2020 et 2017").head(10)
        df_pire = df_pire[["Ville","Différence de montant entre 2020 et 2017"]]
        df_meilleur = df_merge3.sort_values("Différence de montant entre 2020 et 2017").iloc[::-1].head(10)
        df_meilleur = df_meilleur[["Ville","Différence de montant entre 2020 et 2017"]]
        
        df_pire = df_pire.style.hide_index()
        df_meilleur = df_meilleur.style.hide_index()
        
        put_text("      ")
        put_text("Top 10 des villes où investir").style('color: dark; font-size: 20px; font-weight:bold;')
        put_html(df_meilleur.to_html())
        put_text("      ")
        put_text("Top 10 des villes avec le moins bon rendement").style('color: dark; font-size: 20px; font-weight:bold;')
        put_html(df_pire.to_html())

        url = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peuplées"
        data = requests.get(url).text
        soup = BeautifulSoup(data, 'html.parser')
        tables = soup.find_all('table')
        table = soup.find('table', class_='mw-collapsible')
        df = pd.DataFrame(columns=['Rang 2022', 'Code INSEE', 'Commune', 'Departement', 'Statut', 'Région', "2019", "2013", "2008", "1999"])
        for row in table.tbody.find_all('tr'):    
            columns = row.find_all('td')
            
            if(columns != []):
                rang2022 = columns[0].text.strip()
                insee = columns[1].text.strip()
                commune = columns[2].text.strip()
                departement = columns[3].text.strip()
                statut = columns[4].text.strip()
                region = columns[5].text.strip()
                pop2019 = columns[6].text.strip()
                pop2013 = columns[7].text.strip()
                pop2008 = columns[8].text.strip()
                pop1999 = columns[9].text.strip()

                df = df.append({'Rang 2022': rang2022,  'Code INSEE': insee, 'Commune': commune, 'Departement': departement, 'Statut': statut, 'Région': region, "2019": pop2019, "2013" : pop2013, "2008":pop2008, "1999":pop1999}, ignore_index=True)
        
        df["2019"] = [str(x).replace(u"\xa0",u"") for x in df["2019"]]
        df["2019"] = [str(x).replace(" ","") for x in df["2019"]]

        df["2013"] = [str(x).replace(u"\xa0",u"") for x in df["2013"]]
        df["2013"] = [str(x).replace(" ","") for x in df["2013"]]

        df["2008"] = [str(x).replace(u"\xa0",u"") for x in df["2008"]]
        df["2008"] = [str(x).replace(" ","") for x in df["2008"]]

        df["1999"] = [str(x).replace(u"\xa0",u"") for x in df["1999"]]
        df["1999"] = [str(x).replace(" ","") for x in df["1999"]]

        df = df.set_index("Code INSEE")

        df = df.drop("97611")
        df = df.drop("98818")
        df = df.drop("98805")
        df = df.drop("97610")
        df = df.drop("97801")
        df = df.drop("97311")
        df = df.drop("97307")
        df = df.drop("97408")
        df = df.drop("97413")

        df["2019"] = df["2019"].astype(int)
        df["2013"] = df["2013"].astype(int)
        df["2008"] = df["2008"].astype(int)
        df["1999"] = df["1999"].astype(int)

        df["Evolution de la population en % de 1990 à 2019"] = ((df["2019"] - df["1999"])/df["1999"])*100
        df_meilleur2 = df.sort_values("Evolution de la population en % de 1990 à 2019").iloc[::-1].head(50)
        df_meilleur2 = df_meilleur2.reset_index(drop=True)
        df_meilleur2 = df_meilleur2[["Commune","Departement","1999","2008","2013","2019","Evolution de la population en % de 1990 à 2019"]]
        df_meilleur2["Departement"] = df_meilleur2["Departement"].replace("Métropole de Lyon[Note 2]", "Métropole de Lyon")
        df_meilleur2["Departement"] = df_meilleur2["Commune"].replace("Dunkerque[Note 4]", "Dunkerque")

        df_meilleur2 = df_meilleur2.style.hide_index()
        put_text("    ")
        put_text("Top 50 des villes ayant gagné le plus d'habitants depuis 1990").style('color: dark; font-size: 20px; font-weight:bold;')
        put_collapse('Voir le tableau', [put_html(df_meilleur2.to_html())])

        # data = [df["1999"].values,df["2008"].values,df["2013"].values,df["2019"].values ]
        # annee = ["1999","2008","2013","2019"]
        # data2 = pd.DataFrame({"Population" : data, "Année" : annee})
        # fig2 = px.bar(data2,x="Année", y="Population")
        # fig2.update_xaxes(type='category')
        # html2 = fig2.to_html(include_plotlyjs="require", full_html=False)
        # put_html(html2)


                
    if (choix == "19 - Simulateur SCPI Pinel") :
        put_markdown('# SCPI PINEL')
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        revenu = float(input("Quel est le revenu net annuel du foyer : "))
        revenu2 = 0.9*revenu
        if revenu2 > 126520:
            revenuAvantAbbatement = revenu - 12652
        else :
            revenuAvantAbbatement = 0.9*revenu
        statut = saisirStatutFamilial()
        npers = int(input("Nombre de personnes a charge? "))
        if statut == CONCUBINAGE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
        ###########CELIBATAIRE
        if statut == CELIBATAIRE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
                
        ############MARIE
        
        if statut == MARIE:
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 52140:
                    impots = (revenuAvantAbbatement*0.11)-2249.50
                    TMI = 11
                if 52140 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-12156.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-28556
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-41382.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2.5:
                if revenuAvantAbbatement < 25563:
                    impots = 0
                    TMI = 0
                if 25563 < revenuAvantAbbatement <= 57561:
                    impots = (revenuAvantAbbatement*0.11)-2811.88
                    TMI = 11
                if 57562 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-13748.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-30148
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-42974.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 62978:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 62979 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-15340.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-31740
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-44566.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 73818:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 73819 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-18524.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-34924
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-47750.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==5:
                if revenuAvantAbbatement < 51125:
                    impots = 0
                    TMI = 0
                if 51125 < revenuAvantAbbatement <= 84655:
                    impots = (revenuAvantAbbatement*0.11)-5623.75
                    TMI = 11
                if 84656 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-21708.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-38108
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-50934.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==6:
                if revenuAvantAbbatement < 61350:
                    impots = 0
                    TMI = 0
                if 61350 < revenuAvantAbbatement <= 94495:
                    impots = (revenuAvantAbbatement*0.11)-6748.5
                    TMI = 11
                if 94496 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-24892.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-40292
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-54118.88
                    TMI = 45
        #put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        montant = float(input("Quel est le montant que vous souhaitez investir ?"))
        economie9 = []
        economie12 = []
        economie14 = []
        economie912 = []
        for i in range(0,9):
            economie = (2/100)*montant
            economie9.append(economie)
        for j in range(10,13):
            economie = (1/100)*montant
            economie12.append(economie) 
        for x in range(13,15):
            economie = 0
            economie14.append(economie)

        economie12.extend(economie14)
        economie9.extend(economie12)


        df = pd.DataFrame({
            "Impôt dû" : impots,
            "Économie d'impôts SCPI" : economie9,
            
        })

        df.index +=1

        df["Impôt restant dû"] = df["Impôt dû"] - df["Économie d'impôts SCPI"]
        df["Gain fiscal cumulé"] = df["Économie d'impôts SCPI"].cumsum()

        DateSouscription = "01-01-2022"
        DateSouscription = DateSouscription.replace("/","-")
        date_time_obj = datetime.datetime.strptime(DateSouscription, '%d-%m-%Y')

        liste_annne = []
        for i in range(0,14):
            a = date_time_obj.year + i
            liste_annne.append(a)
        liste_annne

        df["Période"] = liste_annne
        df = df.set_index("Période")

        put_text("IMPACT FISCAL").style('color: dark; font-size: 20px; font-weight:bold;')
        put_html(df.to_html(border = 0))

    if (choix == "20 - Simulateur SCPI Malraux") :
        put_markdown('# SCPI MALRAUX')
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        revenu = float(input("Quel est le revenu net annuel du foyer : "))
        revenu2 = 0.9*revenu
        if revenu2 > 126520:
            revenuAvantAbbatement = revenu - 12652
        else :
            revenuAvantAbbatement = 0.9*revenu
        statut = saisirStatutFamilial()
        npers = int(input("Nombre de personnes a charge? "))
        if statut == CONCUBINAGE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
        ###########CELIBATAIRE
        if statut == CELIBATAIRE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
                
        ############MARIE
        
        if statut == MARIE:
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                if 20450 < revenuAvantAbbatement <= 52140:
                    impots = (revenuAvantAbbatement*0.11)-2249.50
                    TMI = 11
                if 52140 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-12156.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-28556
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-41382.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==2.5:
                if revenuAvantAbbatement < 25563:
                    impots = 0
                    TMI = 0
                if 25563 < revenuAvantAbbatement <= 57561:
                    impots = (revenuAvantAbbatement*0.11)-2811.88
                    TMI = 11
                if 57562 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-13748.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-30148
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-42974.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                if 30675 < revenuAvantAbbatement <= 62978:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                if 62979 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-15340.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-31740
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-44566.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                if 40900 < revenuAvantAbbatement <= 73818:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                if 73819 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-18524.10
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-34924
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-47750.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==5:
                if revenuAvantAbbatement < 51125:
                    impots = 0
                    TMI = 0
                if 51125 < revenuAvantAbbatement <= 84655:
                    impots = (revenuAvantAbbatement*0.11)-5623.75
                    TMI = 11
                if 84656 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-21708.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-38108
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-50934.88
                    TMI = 45
                
            if quotientFamilial(statut, npers) ==6:
                if revenuAvantAbbatement < 61350:
                    impots = 0
                    TMI = 0
                if 61350 < revenuAvantAbbatement <= 94495:
                    impots = (revenuAvantAbbatement*0.11)-6748.5
                    TMI = 11
                if 94496 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-24892.1
                    TMI = 30
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-40292
                    TMI = 41
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-54118.88
                    TMI = 45
        montant = float(input("Quel est le montant que vous souhaitez investir ?"))
        choix = radio("Je réduis mes impôts sur :", options=["1 an", "2 ans", "3 ans", "4 ans"])
        if (choix == "1 an"):
            economie1 = []
            economie2 = []
            for i in range(0,1):
                economie = (18/100)*montant
                economie1.append(economie)
            for j in range(2,11):
                economie=0
                economie2.append(economie)

            economie1.extend(economie2)

            df = pd.DataFrame({
                "Impôt dû" : impots,
                "Économie d'impôts SCPI" : economie1,

            })

            df.index +=1

            df["Impôt restant dû"] = df["Impôt dû"] - df["Économie d'impôts SCPI"]
            df["Impôt restant dû"][df["Impôt restant dû"] < 0] = 0

            df["Gain fiscal cumulé"] = df["Économie d'impôts SCPI"].cumsum()
            df["Gain fiscal cumulé"].iloc[1::] = 0

            DateSouscription = "01-01-2022"
            DateSouscription = DateSouscription.replace("/","-")
            date_time_obj = datetime.datetime.strptime(DateSouscription, '%d-%m-%Y')

            liste_annne = []
            for i in range(0,10):
                a = date_time_obj.year + i
                liste_annne.append(a)
            liste_annne

            df["Période"] = liste_annne
            df = df.set_index("Période")
            put_text("IMPACT FISCAL").style('color: dark; font-size: 20px; font-weight:bold;')
            put_html(df.to_html(border = 0))
            put_info("Si votre impôt restant dû est égal à 0, cela s'explique car le gain fiscal est supérieur à l'impôt à payer. En SCPI Malraux, il convient donc d'imputer intelligement sur le bon montant de SCPI chaque année et sur 4 ans maximum.")
            #put_text("Si votre impôt restant dû est égal à 0, cela s'explique car le gain fiscal est supérieur à l'impôt à payer. En SCPI Malraux, il convient donc d'imputer intelligement sur le bon montant de SCPI chaque année et sur 4 ans maximum.")
        
        if (choix == "2 ans"):
            economie1 = []
            economie2 = []
            for i in range(0,2):
                economie = (18/100)*montant
                economiee = economie/2
                economie1.append(economiee)
            for j in range(3,11):
                economie=0
                economie2.append(economie)

            economie1.extend(economie2)

            df = pd.DataFrame({
                "Impôt dû" : impots,
                "Économie d'impôts SCPI" : economie1,

            })

            df.index +=1

            df["Impôt restant dû"] = df["Impôt dû"] - df["Économie d'impôts SCPI"]
            df["Impôt restant dû"][df["Impôt restant dû"] < 0] = 0

            df["Gain fiscal cumulé"] = df["Économie d'impôts SCPI"].cumsum()
            df["Gain fiscal cumulé"].iloc[2::] = 0

            DateSouscription = "01-01-2022"
            DateSouscription = DateSouscription.replace("/","-")
            date_time_obj = datetime.datetime.strptime(DateSouscription, '%d-%m-%Y')

            liste_annne = []
            for i in range(0,10):
                a = date_time_obj.year + i
                liste_annne.append(a)
            liste_annne

            df["Période"] = liste_annne
            df = df.set_index("Période")
            put_html(df.to_html(border = 0))
            #put_text("Votre impôt est égal à 0 car le gain fiscal est supérieur à l'impôt à payer. En SCPI Malraux, il convient donc d'imputer intelligement sur le bon montant de SCPI chaque année et sur 4 ans maximum.")

        if (choix == "3 ans"):
            economie1 = []
            economie2 = []
            for i in range(0,3):
                economie = (18/100)*montant
                economiee = economie/3
                economie1.append(economiee)
            for j in range(4,11):
                economie=0
                economie2.append(economie)

            economie1.extend(economie2)

            df = pd.DataFrame({
                "Impôt dû" : impots,
                "Économie d'impôts SCPI" : economie1,

            })

            df.index +=1

            df["Impôt restant dû"] = df["Impôt dû"] - df["Économie d'impôts SCPI"]
            df["Impôt restant dû"][df["Impôt restant dû"] < 0] = 0

            df["Gain fiscal cumulé"] = df["Économie d'impôts SCPI"].cumsum()
            df["Gain fiscal cumulé"].iloc[3::] = 0

            DateSouscription = "01-01-2022"
            DateSouscription = DateSouscription.replace("/","-")
            date_time_obj = datetime.datetime.strptime(DateSouscription, '%d-%m-%Y')

            liste_annne = []
            for i in range(0,10):
                a = date_time_obj.year + i
                liste_annne.append(a)
            liste_annne

            df["Période"] = liste_annne
            df = df.set_index("Période")
            put_html(df.to_html(border = 0))
        
        if (choix == "4 ans"):
            economie1 = []
            economie2 = []
            for i in range(0,4):
                economie = (18/100)*montant
                economiee = economie/4
                economie1.append(economiee)
            for j in range(5,11):
                economie=0
                economie2.append(economie)

            economie1.extend(economie2)

            df = pd.DataFrame({
                "Impôt dû" : impots,
                "Économie d'impôts SCPI" : economie1,

            })

            df.index +=1

            df["Impôt restant dû"] = df["Impôt dû"] - df["Économie d'impôts SCPI"]
            df["Impôt restant dû"][df["Impôt restant dû"] < 0] = 0
    
            df["Gain fiscal cumulé"] = df["Économie d'impôts SCPI"].cumsum()
            df["Gain fiscal cumulé"].iloc[4::] = 0

            DateSouscription = "01-01-2022"
            DateSouscription = DateSouscription.replace("/","-")
            date_time_obj = datetime.datetime.strptime(DateSouscription, '%d-%m-%Y')

            liste_annne = []
            for i in range(0,10):
                a = date_time_obj.year + i
                liste_annne.append(a)
            liste_annne

            df["Période"] = liste_annne
            df = df.set_index("Période")
            put_html(df.to_html(border = 0))
    
    if (choix == "21 - Simulateur d'epargne") :
        put_markdown("# SIMULATEUR D'EPARGNE")
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        payment_per_month = float(input("Épargne mensuelle € : "))
        payment_per_month = -payment_per_month
        present_value = float(input("Capital initial en € : "))
        present_value = -present_value
        interest_rate = float(input("Rendement annuel moyen en % : "))
        interest_rate = (interest_rate*0.01)/12
        n_periods = int(input("Durée de l'épargne en années : "))
        n_periods = n_periods*12

        future_value = npf.fv(interest_rate, n_periods, payment_per_month, present_value)
        #versements = (-payment_per_month*n_periods)-present_value
        versements = -present_value - payment_per_month*n_periods
        interets_cumules = future_value - versements
        interest_rate = interest_rate*12*100
        interest_rate = int(interest_rate)
        if (-payment_per_month >= 150) & (-present_value < 20000):
            put_table([
                    ["Epargne Mensuelle","Capital Initial","Rendement annuel moyen", "Durée de l'épargne (en années)"],
                    [round(-payment_per_month),round(-present_value),"{:.2f}%".format(interest_rate), round(n_periods/12)],
                ])

            put_table([
                    ["Capital final","Versements cumulés","Intérêts cumulés"],
                    [round(future_value),round(versements),round(interets_cumules)],
                ])
            put_success("Vous êtes éligible, laissez nous vos coordonnées pour qu'on puisse vous recontacter")
        elif ((-present_value >= 20000) & (-payment_per_month < 150)):
            put_table([
                    ["Epargne Mensuelle","Capital Initial","Rendement annuel moyen", "Durée de l'épargne (en années)"],
                    [round(-payment_per_month),round(-present_value),"{:.2f}%".format(interest_rate), round(n_periods/12)],
                ])

            put_table([
                    ["Capital final","Versements cumulés","Intérêts cumulés"],
                    [round(future_value),round(versements),round(interets_cumules)],
                ])
            put_success("Vous êtes éligible, laissez nous vos coordonnées pour qu'on puisse vous recontacter")
        elif ((-present_value >= 20000) & (-payment_per_month >= 150)):
            put_table([
                    ["Epargne Mensuelle","Capital Initial","Rendement annuel moyen", "Durée de l'épargne (en années)"],
                    [round(-payment_per_month),round(-present_value),"{:.2f}%".format(interest_rate), round(n_periods/12)],
                ])

            put_table([
                    ["Capital final","Versements cumulés","Intérêts cumulés"],
                    [round(future_value),round(versements),round(interets_cumules)],
                ])
            put_success("Vous êtes éligible, laissez nous vos coordonnées pour qu'on puisse vous recontacter")
        else :
            put_table([
                    ["Epargne Mensuelle","Capital Initial","Rendement annuel moyen", "Durée de l'épargne (en années)"],
                    [round(-payment_per_month),round(-present_value),"{:.2f}%".format(interest_rate), round(n_periods/12)],
                ])

            put_table([
                    ["Capital final","Versements cumulés","Intérêts cumulés"],
                    [round(future_value),round(versements),round(interets_cumules)],
                ])


        annee = ["Dernière d'année"]
        data2 = pd.DataFrame({"Capital Final" : [future_value], 
                      "Versement cumulés" : [versements],
                    "Intérêts cumulés" : [interets_cumules],
                    "Année" : annee})
        fig = px.bar(data2[["Versement cumulés","Intérêts cumulés"]], title = "Votre épargne à la dernière année",
                    labels = {"index" : "Dernière année",
                    "value" : "Valeur en €"})
        html = fig.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)

    if (choix == "22 - Meilleur dispositif selon vos informations") :
        put_markdown('# Meilleur Dispositif')
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        revenu1 = float(input("Quel est le revenu net annuel du foyer : "))
        revenu2 = 0.9*revenu1
        if revenu2 > 126520:
            revenuAvantAbbatement = revenu1 - 12652
        else :
            revenuAvantAbbatement = 0.9*revenu1
        statut = saisirStatutFamilial()
        npers = int(input("Nombre de personnes a charge? "))
        if statut == CONCUBINAGE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "Meublé à l'amortissement"
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence EHPAD"
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EHPAD"
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Malraux"

            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "Meublé à l'amortissement"
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence EPHAD"
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Malraux"

            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "SCPI Pinel"
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence EPHAD"
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Malraux"

            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence étudiante"
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Malraux"
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Résidence EPHAD"

            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence étudiante"
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                    dispositif1 = "Malraux"
                    dispositif2 = "Pinel"
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Résidence EPHAD"
        ###########CELIBATAIRE
        if statut == CELIBATAIRE:
            if quotientFamilial(statut, npers) ==1:
                if revenuAvantAbbatement < 10225:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 10225 < revenuAvantAbbatement <= 26070:
                    impots = (revenuAvantAbbatement*0.11)-1124.75
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "Meublé à l'amortissement"
                if 26070 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-6078.05
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence EHPAD"
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-14278
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EHPAD"
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-20691.44
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Malraux"

            if quotientFamilial(statut, npers) ==1.5:
                if revenuAvantAbbatement < 15338:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 15338 < revenuAvantAbbatement <= 31491:
                    impots = (revenuAvantAbbatement*0.11)-1687.13
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "Meublé à l'amortissement"
                if 31492 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-7670.05
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence EPHAD"
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-15870
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-22283.44
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Malraux"

            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 20450 < revenuAvantAbbatement <= 36908:
                    impots = (revenuAvantAbbatement*0.11)-2249.5
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "SCPI Pinel"
                if 36909 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-9262.05
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence EPHAD"
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-17462
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-23875.44
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Malraux"

            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 30675 < revenuAvantAbbatement <= 47748:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence étudiante"
                if 47749 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-12446.05
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Malraux"
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-20646
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-27059.44
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Résidence EPHAD"

            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 40900 < revenuAvantAbbatement <= 58585:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence étudiante"
                if 58586 < revenuAvantAbbatement <= 74545:
                    impots = (revenuAvantAbbatement*0.3)-15630.05
                    TMI = 30
                    dispositif1 = "Malraux"
                    dispositif2 = "Pinel"
                if 74545 < revenuAvantAbbatement <= 160336:
                    impots = (revenuAvantAbbatement*0.41)-23830
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 160336:
                    impots = (revenuAvantAbbatement*0.45)-30243.44
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Résidence EPHAD"

        ############MARIE

        if statut == MARIE:
            if quotientFamilial(statut, npers) ==2:
                if revenuAvantAbbatement < 20450:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 20450 < revenuAvantAbbatement <= 52140:
                    impots = (revenuAvantAbbatement*0.11)-2249.50
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "SCPI Pinel"
                if 52140 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-12156.1
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Malraux"
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-28556
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-41382.88
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Résidence EPHAD"

            if quotientFamilial(statut, npers) ==2.5:
                if revenuAvantAbbatement < 25563:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 25563 < revenuAvantAbbatement <= 57561:
                    impots = (revenuAvantAbbatement*0.11)-2811.88
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "SCPI Pinel"
                if 57562 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-13748.10
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Malraux"
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-30148
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "SCPI Malraux"
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-42974.88
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Résidence EPHAD"

            if quotientFamilial(statut, npers) ==3:
                if revenuAvantAbbatement < 30675:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 30675 < revenuAvantAbbatement <= 62978:
                    impots = (revenuAvantAbbatement*0.11)-3374.25
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "SCPI Pinel"
                if 62979 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-15340.1
                    TMI = 30
                    dispositif1 = "Malraux"
                    dispositif2 = "Pinel"
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-31740
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "SCPI Malraux"
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-44566.88
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Résidence EPHAD"

            if quotientFamilial(statut, npers) ==4:
                if revenuAvantAbbatement < 40900:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 40900 < revenuAvantAbbatement <= 73818:
                    impots = (revenuAvantAbbatement*0.11)-4499
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "Résidence EPHAD"
                if 73819 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-18524.10
                    TMI = 30
                    dispositif1 = "Malraux"
                    dispositif2 = "Pinel"
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-34924
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "SCPI Malraux"
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-47750.88
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Résidence EPHAD"

            if quotientFamilial(statut, npers) ==5:
                if revenuAvantAbbatement < 51125:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 51125 < revenuAvantAbbatement <= 84655:
                    impots = (revenuAvantAbbatement*0.11)-5623.75
                    TMI = 11
                    dispositif1 = "Résidence étudiante"
                    dispositif2 = "Résidence EPHAD"
                if 84656 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-21708.1
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence EPHAD"
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-38108
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-50934.88
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Résidence EPHAD"

            if quotientFamilial(statut, npers) ==6:
                if revenuAvantAbbatement < 61350:
                    impots = 0
                    TMI = 0
                    dispositif1 = "Aucun dispositif"
                    dispositif2 = "Aucun dispositif"
                if 61350 < revenuAvantAbbatement <= 94495:
                    impots = (revenuAvantAbbatement*0.11)-6748.5
                    TMI = 11
                    dispositif1 = "Pinel"
                    dispositif2 = "Résidence étudiante"
                if 94496 < revenuAvantAbbatement <= 149090:
                    impots = (revenuAvantAbbatement*0.3)-24892.1
                    TMI = 30
                    dispositif1 = "Pinel"
                    dispositif2 = "Malraux"
                if 149090 < revenuAvantAbbatement <= 320672:
                    impots = (revenuAvantAbbatement*0.41)-40292
                    TMI = 41
                    dispositif1 = "Malraux"
                    dispositif2 = "Résidence EPHAD"
                if revenuAvantAbbatement > 320672:
                    impots = (revenuAvantAbbatement*0.45)-54118.88
                    TMI = 45
                    dispositif1 = "Monument historique"
                    dispositif2 = "Résidence EPHAD"
        
        residentFiscal = str(input("Etes vous résident fiscal français (Oui/Non) ? "))
        residentFiscal = residentFiscal.lower()
        residencePrincipale = str(input("Etes vous propriétaire de votre résidence prinicpale (Oui/Non) ? "))
        residencePrincipale = residencePrincipale.lower()
        age = int(input("Votre âge : "))

        if (impots >= 5000):
            choix_opti = radio("Vous payez {} € d'impots. Voulez-vous faire de l'optimisation fiscale ?".format(impots), options = ["Oui", "Non"])
            if choix_opti == "Oui" : 
                epargne = float(input("Le montant de votre epargne : "))
                df_user = pd.DataFrame({"Age" : [age],
                                "Resident Fiscale en France" : [residentFiscal],
                                "Statut" : [statut.lower()],
                                "Personnes à charge" : [npers],
                                "Revenus nets annuels du foyer avant impôts" : [revenu1],
                                "TMI" : [TMI],
                                "Impots" : [impots],
                                "Montant Epargne" : [epargne],
                                "Propriétaire de résidence principale" : [residencePrincipale], 
                                "Dispositif 1" : [dispositif1],
                                "Dispositif 2" : [dispositif2],})
                if df_user["Age"].values > 60:
                    df_user["Dispositif 1"] = "Aucun dispositif"
                    df_user["Dispositif 2"] = "Aucun dispositif"     
                if (epargne >= 30000) & (impots < 5000):
                    df_user["Dispositif Epargne 1"] = "SCPI rendement"
                    df_user["Dispositif Epargne 2"] = "Aucun autre dispositif"
                elif (epargne >= 30000) & (impots >= 5000):
                    df_user["Dispositif Epargne 1"] = "SCPI rendement"
                    df_user["Dispositif Epargne 2"] = "SCPI Fiscales"
                else :
                    df_user["Dispositif Epargne 1"] = "Aucun Dispositif"
                    df_user["Dispositif Epargne 2"] = "Aucun Dispositif"
            else:
                df_user = pd.DataFrame({"Age" : [age],
                                "Resident Fiscale en France" : [residentFiscal],
                                "Statut" : [statut.lower()],
                                "Personnes à charge" : [npers],
                                "Revenus nets annuels du foyer avant impôts" : [revenu1],
                                "TMI" : [TMI],
                                "Impots" : [impots],
                                "Propriétaire de résidence principale" : [residencePrincipale]})
        else :
            epargne = float(input("Le montant de votre epargne : "))
            if epargne >= 30000:
                choix_opti = radio("Vous avez {} € d'épargne. Voulez-vous faire de l'optimisation fiscale ?".format(int(epargne)), options = ["Oui", "Non"])
                if choix_opti == "Oui" : 
                    df_user = pd.DataFrame({"Age" : [age],
                                "Resident Fiscale en France" : [residentFiscal],
                                "Statut" : [statut.lower()],
                                "Personnes à charge" : [npers],
                                "Revenus nets annuels du foyer avant impôts" : [revenu1],
                                "TMI" : [TMI],
                                "Impots" : [impots],
                                "Montant Epargne" : [epargne],
                                "Propriétaire de résidence principale" : [residencePrincipale],   
                                "Dispositif 1" : [dispositif1],
                                "Dispositif 2" : [dispositif2],})
                    if df_user["Age"].values > 60:
                        df_user["Dispositif 1"] = "Aucun dispositif"
                        df_user["Dispositif 2"] = "Aucun dispositif"     
                    if (epargne >= 30000) & (impots < 5000):
                        df_user["Dispositif Epargne 1"] = "SCPI rendement"
                        df_user["Dispositif Epargne 2"] = "Aucun autre dispositif"
                    elif (epargne >= 30000) & (impots >= 5000):
                        df_user["Dispositif Epargne 1"] = "SCPI rendement"
                        df_user["Dispositif Epargne 2"] = "SCPI Fiscales"
                    else :
                        df_user["Dispositif Epargne 1"] = "Aucun Dispositif"
                        df_user["Dispositif Epargne 2"] = "Aucun Dispositif"
                else :
                    df_user = pd.DataFrame({"Age" : [age],
                                "Resident Fiscale en France" : [residentFiscal],
                                "Statut" : [statut.lower()],
                                "Personnes à charge" : [npers],
                                "Revenus nets annuels du foyer avant impôts" : [revenu1],
                                "TMI" : [TMI],
                                "Impots" : [impots],
                                "Propriétaire de résidence principale" : [residencePrincipale]})
            else : 
                df_user = pd.DataFrame({"Age" : [age],
                                "Resident Fiscale en France" : [residentFiscal],
                                "Statut" : [statut.lower()],
                                "Personnes à charge" : [npers],
                                "Revenus nets annuels du foyer avant impôts" : [revenu1],
                                "TMI" : [TMI],
                                "Impots" : [impots],
                                "Propriétaire de résidence principale" : [residencePrincipale]})

        df_user = df_user.style.hide_index()
        put_html(df_user.to_html())

    if (choix == "23 - Comparateur de rentabilité entre le neuf et l'ancien") :
        put_markdown("# Comparateur de rentabilité entre le neuf et l'ancien")
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        choixNeufAncien = radio("Votre est bien est neuf ou ancien ?", options = ["Neuf", "Ancien"])
        if choixNeufAncien == "Neuf" :
            zoneB1 = ['Toulouse', 'Nantes', 'Strasbourg', 'Bordeaux', 'Rennes', 'Reims', 'Le Havre', 'Grenoble', 'Dijon', 'Nîmes', 'Clermont-Ferrand', 'Limoges', 'Tours', 'Amiens', 'Metz', 'Perpignan', 'Orléans', 'Rouen', 'Mulhouse', 'Caen', 'Nancy', 'Roubaix', 'Tourcoing', 'Avignon', 'La Rochelle', "Villeneuve-d'Ascq", 'Vénissieux', 'Chambéry', 'Pessac', 'Beauvais', 'Arles', 'Annecy', 'Saint-Malo', 'Bayonne', 'Valenciennes', 'Sète', 'Saint-Herblain', 'Bastia', 'Salon-de-Provence', 'Vaulx-en-Velin', 'Douai', 'Talence', 'Caluire-et-Cuire', 'Wattrelos', 'Compiègne', 'Chartres', 'Rezé', 'Anglet', 'Bron', 'Draguignan', "Saint-Martin-d'Hères", 'Joué-lès-Tours', 'Échirolles', 'Villefranche-sur-Saône', 'Colomiers', 'Thonon-les-Bains', 'Lens', 'Creil', 'Schiltigheim', 'Meyzieu', 'Vandoeuvre-lès-Nancy', 'Rillieux-la-Pape', 'Orange', 'Carpentras', "Villenave-d'Ornon", 'Sotteville-lès-Rouen', 'Aix-les-Bains', 'Saint-Médard-en-Jalles', 'Saint-Étienne-du-Rouvray', 'Illkirch-Graffenstaden', 'Bourgoin-Jallieu', 'Biarritz', 'Béthune', 'Tournefeuille', 'Décines-Charpieu', 'Saint-Sébastien-sur-Loire', 'Armentières', 'Cavaillon', 'Lunel', 'Oullins', 'Bègles', 'Orvault', 'La Teste-de-Buch', 'Le Grand-Quevilly', 'Muret', 'Étampes', 'Agde', 'Gradignan', 'Le Bouscat', 'Frontignan', 'Montigny-lès-Metz', 'Blagnac', 'Cenon', 'Le Petit-Quevilly', 'Vertou', 'Sainte-Foy-lès-Lyon', 'Hérouville-Saint-Clair', 'Bois-Guillaume-Bihorel', 'Mons-en-Baroeul', 'Fleury-les-Aubrais', 'Saint-Genis-Laval', 'Lormont', 'Annecy-le-Vieux', 'Halluin', 'Croix', 'Eysines', 'Gujan-Mestras', 'Tassin-la-Demi-Lune', 'Voiron', 'Olivet', 'Saint-Jean-de-Braye', 'Mont-Saint-Aignan', 'Givors', 'Albertville', 'Pertuis', 'Couëron', 'Nogent-sur-Oise', 'Seynod', 'Bouguenais', 'Carquefou', 'Sorgues', 'Villefontaine', 'Meylan', 'Écully', 'Hem', 'Chamalières', 'Ronchin', 'La Chapelle-sur-Erdre', 'Cluses', 'Bischheim', 'Faches-Thumesnil', 'Cran-Gevrier', 'Saint-Fons', 'Elbeuf', 'Bruz', 'Saint-Jean-de-la-Ruelle', 'Lingolsheim', 'Cestas', 'Montereau-Fault-Yonne', 'La Baule-Escoublac', 'Saint-Cyr-sur-Loire', 'Lucé', 'Montivilliers', 'Brignoles', 'Senlis', 'Guérande', 'Plaisance-du-Touch', 'Hendaye', 'Saint-Égrève', 'Sallanches', 'Cugnaux', 'Cesson-Sévigné', 'Saint-Pierre-des-Corps', 'Bruges', 'Saran', 'Canteleu', 'Coulommiers', 'Laxou', 'Saint-Maximin-la-Sainte-Baume', 'Saint-Avertin', 'Villers-lès-Nancy', 'Bailleul', 'Pornic', 'Crépy-en-Valois', 'Olonne-sur-Mer', 'Haubourdin', "Les Sables-d'Olonne", 'Balma', 'Chenôve', "Château-d'Olonne", 'Saint-Gilles', 'Mouvaux', 'Ambarès-et-Lagrave', 'Lys-lez-Lannoy', 'Wattignies', 'Saint-Jean-de-Luz', 'Amboise', 'Canet-en-Roussillon', 'Roncq', 'Woippy', 'Nemours', 'Sainte-Luce-sur-Loire', 'Biscarrosse', 'Montataire', 'Villeneuve-lès-Avignon', 'Comines', 'Provins', 'Ramonville-Saint-Agne', 'Genas', 'Seclin', 'Pont-Sainte-Maxence', 'Seyssinet-Pariset', 'Tarnos', 'Mions', 'Méricourt', 'La Motte-Servolex', 'Gisors', 'Fonsorbes', 'Ostwald', 'Saint-Martin-de-Crau', 'Brignais', 'Ifs', 'Sassenage', 'Saint-Orens-de-Gameville', 'Maromme', 'Oissel', 'Castanet-Tolosan', 'Talant', 'Monteux', 'Obernai', 'Le Pont-de-Claix', 'Arcachon', 'Mèze', 'Hoenheim', 'Saint-Rémy-de-Provence', 'Chambray-lès-Tours', 'Vedène', 'La Roche-sur-Foron', 'Saint-Jacques-de-la-Lande', 'Dinard', 'Villers-Cotterêts', 'Montlouis-sur-Loire', 'Pacé', 'Vidauban', 'Fondettes', 'Pernes-les-Fontaines', 'Corbas', 'Pornichet', 'Mainvilliers', 'Déville-lès-Rouen', 'Saint-Jean', 'Betton', 'Chevigny-Saint-Sauveur', 'Neuville-en-Ferrain', 'Chantepie', 'La Riche', 'Tinqueux', 'Quetigny', 'Dourdan', 'Argelès-sur-Mer', 'Voreppe', 'Marquette-lez-Lille', 'Marly', 'Brumath', 'Pierre-Bénite', 'Craponne', 'Grand-Couronne', 'Bondues', 'Caudebec-lès-Elbeuf', 'La Chapelle-Saint-Mesmin', 'Biganos', 'Eybens', 'Chassieu', 'Pélissanne', 'Saint-Max', 'Wambrechies', 'Maxéville', 'Mondeville', 'Fosses', 'Portet-sur-Garonne', 'Le Luc', 'Le Haillan', 'Louvres', 'Ouistreham', 'Darnétal', 'Léognan', 'Lambesc', 'Le Muy', 'Fontaine-lès-Dijon', 'Leers', 'Feyzin', 'Longvic', 'La Ferté-sous-Jouarre', 'Petit-Couronne', 'Lorgues', 'Le Taillan-Médoc', 'Castelginest', 'Urrugne', "Gonfreville-l'Orcher", 'Miribel', 'Aytré', 'Saint-Laurent-de-la-Salanque', 'Saint-Grégoire', 'Dardilly', 'Villeneuve-Tolosane', 'Léguevin', 'Marguerittes', 'Port-Saint-Louis-du-Rhône', 'Crolles', 'Aigues-Mortes', 'Évian-les-Bains', 'Chécy', 'Le Thor', 'La Ravoire', 'Meythet', 'Lançon-Provence', 'Pibrac', 'Les Angles', 'Saint-Pierre-lès-Elbeuf', "La Chapelle-d'Armentières", 'Irigny', 'Le Grau-du-Roi', 'Basse-Goulaine', 'Capbreton', 'Frouzins', 'Honfleur', 'Vern-sur-Seiche', 'Harfleur', 'Saint-Loubès', 'Linselles', 'Ballan-Miré', 'Nangis', 'Pérenchies', 'Margny-lès-Compiègne', 'Saint-Aubin-lès-Elbeuf', 'Chaponost', 'Elne', 'Vif', 'Aucamville', 'Ingré', 'Entraigues-sur-la-Sorgue', 'Parempuyre', 'Noisy-le-Roi', 'Charvieu-Chavagneux', 'Thouaré-sur-Loire', 'Le Rheu', 'Seysses', 'Boucau', 'Saint-Vincent-de-Tyrosse', 'Vizille', 'Gleizé', 'Morières-lès-Avignon', 'Moirans', 'Borgo', 'Houplines', 'Sainte-Adresse', 'Éguilles', 'Les Sorinières', 'Le Mesnil-Esnard', 'Souffelweyersheim', 'Scionzier', 'Rochefort-du-Gard', 'Nieppe', 'Thorigné-Fouillard', 'Ballancourt-sur-Essonne', 'Trignac', 'Saint-Gilles-Croix-de-Vie', 'Chartres-de-Bretagne', 'Biguglia', 'Mordelles', 'Lagord', 'Launaguet', 'Gaillon', 'La Fare-les-Oliviers', 'Villard-Bonnot', 'Saint-Denis-en-Val', 'Neuville-sur-Saône', 'Artigues-près-Bordeaux', 'Martignas-sur-Jalle', 'Montluel', 'Liancourt', 'Geispolsheim', 'Donges', 'Poisy', 'Montoir-de-Bretagne', 'Sautron', 'Quesnoy-sur-Deûle', 'Luisant', 'Notre-Dame-de-Bondeville', "Saint-Jean-d'Illac", 'Ciboure', 'Seyssins', 'Bassens', 'Bassens', 'Carbon-Blanc', 'Balaruc-les-Bains', 'La Salvetat-Saint-Gilles', 'Le Teich', 'Les Arcs', 'Sérignan', 'Saint-Ismier', 'Huningue', 'Trévoux', 'Saint-Bonnet-de-Mure', 'Le Perray-en-Yvelines', 'Domène', 'Aussonne', 'Itteville', 'La Mulatière', 'La Tronche', 'Champagne-sur-Seine', 'Noyal-Châtillon-sur-Seiche', 'Eckbolsheim', 'La Verpillière', "Saint-Didier-au-Mont-d'Or", 'Bonsecours', 'Pignan', 'Varces-Allières-et-Risset', 'Bétheny', 'Ustaritz', 'Othis', 'Saint-Aubin-de-Médoc', 'Audenge', 'Publier', 'Bidart', 'Les Essarts-le-Roi', 'Lesquin', 'Marignier', 'Anse', 'Fontaines-sur-Saône', 'Baillargues', 'Tignieu-Jameyzieu', 'Acigné', 'Villers-Saint-Paul', 'Bouillargues', 'Gières', 'Escalquens', 'Franqueville-Saint-Pierre', 'Thônes', 'Veigné', 'Marsillargues', 'Jassans-Riottier', 'Bouaye', 'Rives', 'Châtelaillon-Plage', 'Cormontreuil', 'Cognin', 'La Montagne', 'Saint-Pierre-en-Faucigny', 'Malaunay', 'Montauroux', 'Manduel', 'La Wantzenau', 'Mazan', 'Saint-Quentin-Fallavier', 'Le Pian-Médoc', 'Cournonterral', 'Maule', 'Castries', 'Sarrians', 'Cornebarrieu', 'Saint-Alban-Leysse', 'Milhaud', 'Octeville-sur-Mer', 'Lèves', 'Thyez', 'Gigean', 'Nieul-sur-Mer', 'Jonage', 'Longueau', 'Pierrefeu-du-Var', 'Pont-Saint-Martin', 'Marennes', 'Santes', 'Brindas', 'Saint-Pierre-lès-Nemours', "Saint-Cyr-au-Mont-d'Or", 'Trans-en-Provence', 'Calvi', 'Mornant', 'Rosny-sur-Seine', 'Haute-Goulaine', "Saint-Martin-d'Uriage", 'Eaunes', 'Puilboreau', 'Vendenheim', 'Saint-Cannat', 'Lardy', 'Furiani', 'Marly-la-Ville', 'Épernon', 'Fegersheim', 'Colombelles', 'Cléon', 'Chasse-sur-Rhône', 'Saint-Martin-le-Vinoux', 'Courthézon', "Saint-Georges-d'Orques", 'Saint-Jory', 'Beauzelle', 'Izon', 'Lentilly', 'Dompierre-sur-Mer', 'Vias', "Saint-Symphorien-d'Ozon", 'Le Puy-Sainte-Réparade', 'Saint-Nom-la-Bretèche', 'Challes-les-Eaux', 'Luynes', 'Fayence', 'Saint-Laurent-de-Mure', 'Bléré', 'Mouy', 'Saint-Jean-de-Boiseau', 'Aubignan', 'Marsannay-la-Côte', 'Cadaujac', 'Saint-Pryvé-Saint-Mesmin', "Champagne-au-Mont-d'Or", 'Marnaz']
            zoneA = ['Marseille', 'Lyon', 'Nice', 'Montpellier', 'Lille', 'Toulon', 'Villeurbanne', 'Aix-en-Provence', 'Argenteuil', 'Créteil', 'Vitry-sur-Seine', 'Aulnay-sous-Bois', 'Champigny-sur-Marne', 'Antibes', 'Cannes', 'Ajaccio', 'Drancy', 'Noisy-le-Grand', 'La Seyne-sur-Mer', 'Cergy', 'Sarcelles', 'Hyères', 'Épinay-sur-Seine', 'Meaux', 'Bondy', 'Fréjus', 'Grasse', 'Le Blanc-Mesnil', 'Sartrouville', 'Sevran', 'Martigues', 'Bobigny', 'Cagnes-sur-Mer', 'Aubagne', 'Corbeil-Essonnes', 'Alfortville', 'Istres', 'Le Cannet', 'Mantes-la-Jolie', 'Livry-Gargan', 'Gennevilliers', 'Choisy-le-Roi', 'Rosny-sous-Bois', 'Melun', 'Marcq-en-Baroeul', 'Noisy-le-Sec', 'Garges-lès-Gonesse', 'Gagny', 'La Courneuve', 'Poissy', 'Savigny-sur-Orge', 'Pontault-Combault', 'Conflans-Sainte-Honorine', 'Stains', 'Six-Fours-les-Plages', 'Tremblay-en-France', 'Marignane', 'Neuilly-sur-Marne', 'La Ciotat', 'Montigny-le-Bretonneux', 'Annemasse', 'Villeneuve-Saint-Georges', 'Houilles', 'Viry-Châtillon', 'Plaisir', 'Pontoise', 'Palaiseau', 'Les Mureaux', 'Athis-Mons', 'Saint-Laurent-du-Var', 'Clichy-sous-Bois', 'Trappes', 'Thiais', 'Menton', 'Savigny-le-Temple', 'Yerres', 'Draveil', 'Lambersart', 'Guyancourt', 'Bezons', 'Vigneux-sur-Seine', 'Pierrefitte-sur-Seine', 'Villiers-le-Bel', 'Vallauris', 'Ermont', 'Villiers-sur-Marne', 'Sannois', 'Ris-Orangis', 'Herblay', 'Élancourt', 'Gonesse', 'Rambouillet', 'Taverny', 'Montfermeil', 'Sucy-en-Brie', 'Brunoy', 'Villeneuve-la-Garenne', 'Romainville', 'Miramas', 'Bussy-Saint-Georges', 'Les Ulis', 'Brétigny-sur-Orge', 'Champs-sur-Marne', 'Villeparisis', 'Eaubonne', "Saint-Ouen-l'Aumône", 'Cormeilles-en-Parisis', 'Montgeron', 'Roissy-en-Brie', 'La Madeleine', 'Les Pavillons-sous-Bois', 'Mandelieu-la-Napoule', 'Combs-la-Ville', 'Deuil-la-Barre', 'Longjumeau', 'La Celle-Saint-Cloud', 'Orly', 'Loos', 'Gif-sur-Yvette', 'Montmorency', 'Morsang-sur-Orge', 'La Valette-du-Var', 'Le Mée-sur-Seine', 'Limeil-Brévannes', 'Dammarie-les-Lys', 'Gardanne', 'Lagny-sur-Marne', 'Saint-Michel-sur-Orge', 'Allauch', 'Ozoir-la-Ferrière', 'Wasquehal', 'Mantes-la-Ville', 'Les Pennes-Mirabeau', 'Montigny-lès-Cormeilles', 'Vence', 'Maurepas', 'Le Plessis-Trévise', 'Chilly-Mazarin', 'Mitry-Mory', 'Mougins', 'Villeneuve-le-Roi', 'Chevilly-Larue', "Saint-Cyr-l'École", 'Chennevières-sur-Marne', 'Les Clayes-sous-Bois', 'Soisy-sous-Montmorency', 'Port-de-Bouc', 'Moissy-Cramayel', 'La Crau', 'Éragny', 'Mauguio', 'Osny', 'Jouy-le-Moutier', 'Bonneuil-sur-Marne', 'Boissy-Saint-Léger', 'Limay', 'Vauréal', 'Brie-Comte-Robert', 'Castelnau-le-Lez', 'Orsay', 'Sanary-sur-Mer', 'Lattes', 'Verrières-le-Buisson', 'Noisiel', 'Verneuil-sur-Seine', 'Fos-sur-Mer', 'Carrières-sur-Seine', 'Carrières-sous-Poissy', 'Montesson', 'Fontainebleau', 'Domont', 'Villeneuve-Loubet', 'Juvisy-sur-Orge', 'Le Bourget', 'Saint-Leu-la-Forêt', 'Saint-Brice-sous-Forêt', 'Lognes', 'Avon', 'Montmagny', 'Bouc-Bel-Air', "Bois-d'Arcy", "Berre-l'Étang", 'Arnouville', 'Courcouronnes', 'Méru', 'Beausoleil', 'Mennecy', 'Sainte-Maxime', 'Valbonne', 'Ollioules', 'Fontenay-le-Fleury', 'Saint-Fargeau-Ponthierry', 'Vaires-sur-Marne', 'Villetaneuse', 'Roquebrune-Cap-Martin', 'Roquebrune-sur-Argens', 'Châteauneuf-les-Martigues', 'Saint-Julien-en-Genevois', 'Épinay-sous-Sénart', 'Andrésy', 'Valenton', 'Auriol', 'Voisins-le-Bretonneux', 'Aubergenville', 'Vernouillet', 'Saint-Cyr-sur-Mer', 'Rognac', 'Triel-sur-Seine', 'Saint-André-lez-Lille', 'Solliès-Pont', 'Le Pradet', 'La Queue-en-Brie', 'Carros', 'Gaillard', 'Claye-Souilly', 'Cogolin', 'Chantilly', 'Porto-Vecchio', 'Septèmes-les-Vallons', 'Plan-de-Cuques', 'Vaux-le-Pénil', 'Persan', 'Dugny', 'Arpajon', 'Gex', 'Mouans-Sartoux', 'Épinay-sur-Orge', 'Cuers', 'Trets', 'La Trinité', 'Villepreux', 'Carqueiranne', 'La Londe-les-Maures', 'Ormesson-sur-Marne', 'Biot', 'Villebon-sur-Yvette', 'Bures-sur-Yvette', 'Villecresnes', 'Gouvieux', 'Chanteloup-les-Vignes', 'Chambly', 'Fuveau', 'Lamorlaye', 'Saint-Germain-lès-Arpajon', 'Villeneuve-lès-Maguelone', 'Méry-sur-Oise', 'Ézanville', 'Beaumont-sur-Oise', 'Saint-Genis-Pouilly', 'Bondoufle', 'Cesson', 'Magny-les-Hameaux', 'Crosne', 'Thorigny-sur-Marne', 'Le Beausset', 'Saint-Gély-du-Fesc', 'Gignac-la-Nerthe', 'Fleury-Mérogis', 'Cabriès', 'Meulan-en-Yvelines', 'Montévrain', 'Saint-Jean-de-Védas', 'Beauchamp', 'Groslay', 'Velaux', 'La Farlède', 'Saint-Pierre-du-Perray', 'Roquevaire', 'Pérols', 'Ferney-Voltaire', 'Divonne-les-Bains', 'Bougival', 'La Grande-Motte', 'Venelles', 'Jouy-en-Josas', 'Dammartin-en-Goële', 'Le Crès', 'Tournan-en-Brie', 'Quincy-sous-Sénart', 'Ville-la-Grand', 'Pierrelaye', 'Marcoussis', 'Gretz-Armainvilliers', 'Peymeinade', 'Saint-Rémy-lès-Chevreuse', 'Serris', 'Saint-Chamas', 'Sausset-les-Pins', 'Le Plessis-Bouchard', 'La Colle-sur-Loup', 'Cassis', 'Juvignac', 'Bandol', 'Bormes-les-Mimosas', 'Lésigny', 'Vétraz-Monthoux', 'Écouen', 'Lisses', 'Louveciennes', 'Saint-Germain-lès-Corbeil', 'Émerainville', 'Montlhéry', 'Paray-Vieille-Poste', 'Reignier-Ésery', 'La Ville-du-Bois', 'Contes', 'Pégomas', 'Vert-Saint-Denis', 'Soisy-sur-Seine', 'Cavalaire-sur-Mer', 'Villemoisson-sur-Orge', 'Prévessin-Moëns', 'La Gaude', 'Auvers-sur-Oise', 'Bailly-Romainvilliers', 'Bessancourt', 'Carnoux-en-Provence', 'Gargenville', 'Vaujours', 'Puget-sur-Argens', 'Le Mesnil-Saint-Denis', 'Saint-Victoret', 'Courdimanche', 'Grabels', 'Magny-le-Hongre', 'Limours', 'Linas', 'Longpont-sur-Orge', 'Épône', 'Gournay-sur-Marne', 'Le Mesnil-le-Roi', 'Roquefort-les-Pins', 'Carry-le-Rouet', 'La Penne-sur-Huveaune', 'Fabrègues', 'Saint-Thibault-des-Vignes', 'Courtry', 'Boussy-Saint-Antoine', 'Gémenos', 'Wissous', 'Palavas-les-Flots', 'Ambilly', 'La Bouilladisse', 'Magnanville', 'La Verrière', 'Chambourcy', 'Bouffémont', 'Esbly', 'Chevreuse', 'Nandy', 'Vendargues', 'Cranves-Sales', 'Saint-Mandrier-sur-Mer', 'Rungis', 'Saint-Mitre-les-Remparts', 'Parmain', 'Thoiry', 'Nanteuil-lès-Meaux', 'Simiane-Collongue', "La Cadière-d'Azur", 'Villefranche-sur-Mer', 'Le Lavandou', 'Menucourt', 'Buc', 'Peypin', 'Clapiers', 'Jouars-Pontchartrain', 'Solliès-Toucas', 'Meyreuil', 'Égly', 'Ensuès-la-Redonne', 'Saint-André-de-la-Roche', 'Jacou', 'Villennes-sur-Seine', 'Ablon-sur-Seine', 'Saintry-sur-Seine', 'La Roquette-sur-Siagne', 'Saint-Clément-de-Rivière', 'Quincy-Voisins', 'Roquefort-la-Bédoule', 'Saulx-les-Chartreux', 'Villabé', 'Saint-Zacharie', 'Le Port-Marly', 'Trilport', "Cap-d'Ail", 'Vaux-sur-Seine', 'Mériel', 'Le Coudray-Montceaux', 'Tourrette-Levens', 'Coubron', 'Levens', 'Champagne-sur-Oise', 'Noiseau', 'Prades-le-Lez', 'La Frette-sur-Seine', 'Teyran', 'Issou', 'Mimet', 'Saint-Tropez', 'Coignières', 'Le Rove', 'Mandres-les-Roses', 'Crégy-lès-Meaux', 'Maurecourt', 'Brou-sur-Chantereine', 'Fourqueux', 'Crécy-la-Chapelle', 'Drap', 'Cessy', 'Ceyreste', 'Villenoy', 'Grimaud', 'Le Plessis-Pâté', 'Cruseilles', 'Gréasque', 'Le Thillay', 'Leuville-sur-Orge', 'La Norville', 'Tourrettes-sur-Loup', 'Gattières', 'Le Rouret', 'Coye-la-Forêt', 'Villiers-sur-Orge', 'Collonges-sous-Salève', 'Ornex', 'Juziers', 'Forges-les-Bains', 'Ballainvilliers', 'Beaulieu-sur-Mer', 'Santeny', 'Le Revest-les-Eaux', 'Veigy-Foncenex', 'Boissise-le-Roi', 'Mareil-Marly', 'La Croix-Valmer', 'Sospel', 'Bornel', 'Saint-Germain-sur-Morin', 'Mézières-sur-Seine', 'Saint-Paul-de-Vence', 'Pomponne', 'Montferrier-sur-Lez', 'Saclay', 'Orry-la-Ville', 'Valleiry', 'Bruyères-le-Châtel', 'Montry', 'Colomars', 'Saint-Cergues', 'Fillinges', 'Saint-Savournin', 'Châteauneuf-Grasse', 'Le Tignet', 'Étiolles', 'La Turbie', 'Dampmart', 'Peynier', 'Collégien', 'Porcheville', 'Neauphle-le-Château', 'Auribeau-sur-Siagne', 'La Destrousse', 'Bonne', 'Tigery', 'Bonifacio', 'La Chapelle-en-Serval', 'Le Bar-sur-Loup', 'Margency', 'Gassin', 'Roissy-en-France', 'Frépillon', 'Villiers-Saint-Frédéric', 'Lavérune', 'Pers-Jussy', 'Montlignon', 'Breuillet', "Les Adrets-de-l'Estérel", 'Vulaines-sur-Seine', 'Coupvray', 'Saint-Martin-du-Var', 'Gometz-le-Châtel', 'Champlan', 'Héricy', 'Èze', 'Solliès-Ville', 'Longperrier', 'Belgentier', 'Buchelay', 'Chanteloup-en-Brie', 'Flins-sur-Seine', 'Bernes-sur-Oise', 'Varennes-Jarcy', 'Samoreau', 'Monnetier-Mornex', 'Le Tholonet', 'Archamps', 'Le Mesnil-en-Thelle', 'Péron']
            zoneAbis = ['Paris', 'Chatou', 'Croissy-sur-Seine', 'Le Chesnay', 'Le Pecq', 'Le Vésinet', 'Maisons-Laffitte', 'Marly-le-Roi', 'Rocquencourt', 'Saint-Germain-en-Laye', 'Vélizy-Villacoublay', 'Versailles', 'Viroflay', 'Antony', 'Asnières-sur-Seine', 'Bagneux', 'Bois-Colombes', 'Boulogne-Billancourt', 'Bourg-la-Reine', 'Châtenay-Malabry', 'Châtillon', 'Chaville', 'Clamart', 'Clichy', 'Colombes', 'Courbevoie', 'Fontenay-aux-Roses', 'Garches', 'Issy-les-Moulineaux', 'La Garenne-Colombes', 'Le Plessis-Robinson', 'Levallois-Perret', 'Malakoff', 'Marnes-la-Coquette', 'Meudon', 'Montrouge', 'Nanterre', 'Neuilly-sur-Seine', 'Puteaux', 'Rueil-Malmaison', 'Saint-Cloud', 'Sceaux', 'Sèvres', 'Suresnes', 'Vanves', 'Vaucresson', "Ville-d'Avray", 'Aubervilliers', 'Bagnolet', 'Le Pré-Saint-Gervais', 'Le Raincy', 'Les Lilas', 'Montreuil', 'Neuilly-Plaisance', 'Pantin', 'Saint-Denis', 'Saint-Ouen', 'Villemomble', 'Arcueil', 'Bry-sur-Marne', 'Cachan', 'Charenton-le-Pont', 'Fontenay-sous-Bois', 'Gentilly', 'Ivry-sur-Seine', 'Joinville-le-Pont', "L'Haÿ-les-Roses", 'Le Kremlin-Bicêtre', 'Le Perreux-sur-Marne', 'Maisons-Alfort', 'Nogent-sur-Marne', 'Saint-Mandé', 'Saint-Maur-des-Fossés', 'Saint-Maurice', 'Villejuif', 'Vincennes', 'Enghien-les-Bains']
            zoneB1 = sorted(zoneB1)
            zoneAbis = sorted(zoneAbis)
            zoneA = sorted(zoneA)
            list_total = zoneB1+zoneAbis+zoneA
            list_total = sorted(list_total)
            choix = select("Selectionnez la ville de votre investissement Pinel :", list_total)
            list_dict = {"A" : zoneA,"A bis":zoneAbis,"B1":zoneB1}
            prix = float(input("Le prix de votre bien :"))
            for key, value in list_dict.items():
                if choix in value:
            #choixZone = radio("Selectionner la zone Pinel", options=['zone A bis', 'zone A', "zone B1"])
            #if (choixZone == "zone A bis") :
                    if key == "A bis":
                        surfaceHabitable = float(input("Votre surface habitable :"))
                        surfaceTerasse = float(input("Votre surface exterieur (balcons, terasse), hors jardin : "))
                        prixAbis = 17.55
                        surfaceTerasse2 = surfaceTerasse/2
                        if(surfaceTerasse2 < 9):
                            surfaceTotale = surfaceHabitable + surfaceTerasse2
                            coeff = (19/surfaceTotale) + 0.7
                            Loyermax = prixAbis*coeff*surfaceTotale
                            renta = ((Loyermax*12)/prix)*100
                            #put_text("Le plafond de loyer sera de {0:.2f} euros".format(Loyermax))
                            put_table([
                            ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone","Rentabilité du bien dans le neuf"],
                            [float("{:.2f}".format(Loyermax)),surfaceTotale, key,"{:.2f}%".format(renta)]
                        ])
                            #put_button("Retour",onclick = lambda: run_js('window.location.reload()'))
                        if (surfaceTerasse2 > 9):
                            surfaceTerasse3 = 4.5
                            surfaceTotale = surfaceHabitable + surfaceTerasse3
                            coeff = (19/surfaceTotale) + 0.7
                            Loyermax2 = prixAbis*coeff*surfaceTotale
                            renta = ((Loyermax2*12)/prix)*100
                            put_table([
                            ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone","Rentabilité du bien dans le neuf"],
                            [float("{:.2f}".format(Loyermax2)),surfaceTotale, key,"{:.2f}%".format(renta)]
                        ])
                            #put_button("Retour",onclick = lambda: run_js('window.location.reload()'))
                            #put_text("Le plafond de loyer sera de {0:.2f} euros".format(Loyermax2))
                    #elif (choixZone == "zone A") :
                    if key == "A":
                        surfaceHabitable = float(input("Votre surface habitable :"))
                        surfaceTerasse = float(input("Votre surface exterieur (balcons, terasse), hors jardin : "))
                        prixA = 13.04
                        surfaceTerasse2 = surfaceTerasse/2
                        if(surfaceTerasse2 < 9):
                            surfaceTotale = surfaceHabitable + surfaceTerasse2
                            coeff = (19/surfaceTotale) + 0.7
                            Loyermax = prixA*coeff*surfaceTotale
                            renta = ((Loyermax*12)/prix)*100
                            #put_text("Le plafond de loyer sera de {0:.2f} euros".format(Loyermax))
                            put_table([
                            ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone","Rentabilité du bien dans le neuf"],
                            [float("{:.2f}".format(Loyermax)),surfaceTotale,key,"{:.2f}%".format(renta)]
                        ])
                            #put_button("Retour",onclick = lambda: run_js('window.location.reload()'))
                        if (surfaceTerasse2 > 9):
                            surfaceTerasse3 = 4.5
                            surfaceTotale = surfaceHabitable + surfaceTerasse3
                            coeff = (19/surfaceTotale) + 0.7
                            Loyermax2 = prixA*coeff*surfaceTotale
                            renta = ((Loyermax2*12)/prix)*100
                            put_table([
                            ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone","Rentabilité du bien dans le neuf"],
                            [float("{:.2f}".format(Loyermax2)),surfaceTotale,key,"{:.2f}%".format(renta)]
                        ])
                        # put_button("Retour",onclick = lambda: run_js('window.location.reload()'))
                            #put_text("Le plafond de loyer sera de {0:.2f} euros".format(Loyermax2))
                    #elif (choixZone == "zone B1") :
                    if key == "B1":
                        surfaceHabitable = float(input("Votre surface habitable :"))
                        surfaceTerasse = float(input("Votre surface exterieur (balcons, terasse), hors jardin : "))    
                        prixB1 = 10.51
                        surfaceTerasse2 = surfaceTerasse/2
                        if(surfaceTerasse2 < 9):
                            surfaceTotale = surfaceHabitable + surfaceTerasse2
                            coeff = (19/surfaceTotale) + 0.7
                            Loyermax = prixB1*coeff*surfaceTotale
                            renta = ((Loyermax*12)/prix)*100
                            #put_text("Le plafond de loyer sera de {0:.2f} euros".format(Loyermax))
                            put_table([
                            ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone","Rentabilité du bien dans le neuf"],
                            [float("{:.2f}".format(Loyermax)),surfaceTotale,key,"{:.2f}%".format(renta)]
                        ])
                        # put_button("Retour",onclick = lambda: run_js('window.location.reload()'))
                        if (surfaceTerasse2 > 9):
                            surfaceTerasse3 = 4.5
                            surfaceTotale = surfaceHabitable + surfaceTerasse3
                            coeff = (19/surfaceTotale) + 0.7
                            Loyermax2 = prixB1*coeff*surfaceTotale
                            renta = ((Loyermax2*12)/prix)*100
                            put_table([
                            ["Plafond de loyer en euros (hors charges)","Surface pondéré","Zone","Rentabilité du bien dans le neuf"],
                            [float("{:.2f}".format(Loyermax2)),surfaceTotale,key,"{:.2f}%".format(renta)]
                        ])
                        

        if choixNeufAncien == "Ancien" :
            loyer = float(input("Montant de votre loyer :"))
            prix = float(input("Le prix de votre bien : "))
            renta = ((loyer*12)/prix)*100
            put_table([
                ["Rentabilité sur investissement pour le bien dans l'ancien"],
                ["{:.2f}%".format(renta)],
            ])
            put_tabs([
        {'title': 'Text', 'content': 'Hello world'},
        {'title': 'Markdown', 'content': put_markdown('~~Strikethrough~~')},
        {'title': 'More content', 'content': [
            put_table([
                ['Commodity', 'Price'],
                ['Apple', '5.5'],
                ['Banana', '7'],
            ]),
            put_link('pywebio', 'https://github.com/wang0618/PyWebIO')
        ]}, 
        ])

    if (choix == "24 - Simulateur d'impôts sur la plus-value immobilière") :
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        typeBien = radio("Quel type de bien vendez-vous", options = ["Terrain à batir", "Maison / Appartement"])
        if (typeBien == "Terrain à batir"):
            DateAcquisition = input("Date d'acquisition du bien (dd-mm-yyyy)")
            DateAcquisition = DateAcquisition.replace("/","-")
            DateCession = input("Date de cession du bien (dd-mm-yyyy)")
            DateCession = DateCession.replace("/","-")

            DateTimeDateAcquisition = datetime.datetime.strptime(DateAcquisition, '%d-%m-%Y')
            DateTimeDateCession = datetime.datetime.strptime(DateCession, '%d-%m-%Y')
        
            date_time_annee = DateTimeDateCession.year - DateTimeDateAcquisition.year
            date_time_mois = DateTimeDateCession.month - DateTimeDateAcquisition.month

            if date_time_mois < 0:
                date_time_annee2 = (date_time_annee*12 - ((12 - DateTimeDateCession.month)+(12 - DateTimeDateAcquisition.month)))/12
            else :
                date_time_annee2 = (date_time_annee*12 + date_time_mois)/12

            datetime1 = floor(date_time_annee2)
                            
            if datetime1 <= 5:
                abbatementIR = 0
                abbatementPrelevement = 0
            if datetime1 == 6:
                abbatementIR = (6/100)
                abbatementPrelevement = (1.65/100)
            if datetime1 == 7:
                abbatementIR = (12/100)
                abbatementPrelevement = (3.3/100)
            if datetime1 == 8:
                abbatementIR = (18/100)
                abbatementPrelevement = (4.95/100)
            if datetime1 == 9:
                abbatementIR = (24/100)
                abbatementPrelevement = (6.6/100)
            if datetime1 == 10:
                abbatementIR = (30/100)
                abbatementPrelevement = (8.25/100)
            if datetime1 == 11:
                abbatementIR = (36/100)
                abbatementPrelevement = (9.9/100)
            if datetime1 == 12:
                abbatementIR = (42/100)
                abbatementPrelevement = (11.55/100)
            if datetime1 == 13:
                abbatementIR = (48/100)
                abbatementPrelevement = (13.2/100)
            if datetime1 == 14:
                abbatementIR = (54/100)
                abbatementPrelevement = (14.85/100)
            if datetime1 == 15:
                abbatementIR = (60/100)
                abbatementPrelevement = (16.5/100)
            if datetime1 == 16:
                abbatementIR = (66/100)
                abbatementPrelevement = (18.15/100)
            if datetime1 == 17:
                abbatementIR = (72/100)
                abbatementPrelevement = (19.80/100)
            if datetime1 == 18:
                abbatementIR = (78/100)
                abbatementPrelevement = (21.45/100)
            if datetime1 == 19:
                abbatementIR = (84/100)
                abbatementPrelevement = (23.1/100)
            if datetime1 == 20:
                abbatementIR = (90/100)
                abbatementPrelevement = (24.75/100)
            if datetime1 == 21:
                abbatementIR = (96/100)
                abbatementPrelevement = (26.4/100)
            if datetime1 == 22:
                abbatementIR = (100/100)
                abbatementPrelevement = (28/100)
            if datetime1 == 23:
                abbatementIR = (100/100)
                abbatementPrelevement = (37/100)
            if datetime1 == 24:
                abbatementIR = (100/100)
                abbatementPrelevement = (46/100)
            if datetime1 == 25:
                abbatementIR = (100/100)
                abbatementPrelevement = (46/100)
            if datetime1 == 26:
                abbatementIR = (100/100)
                abbatementPrelevement = (46/100)
            if datetime1 == 27:
                abbatementIR = (100/100)
                abbatementPrelevement = (46/100)
            if datetime1 == 28:
                abbatementIR = (100/100)
                abbatementPrelevement = (46/100)
            if datetime1 == 29:
                abbatementIR = (100/100)
                abbatementPrelevement = (46/100)
            if datetime1 == 30:
                abbatementIR = (100/100)
                abbatementPrelevement = (46/100)
            
            PrixAcquisition1 = float(input("Prix d'acquisition :"))
            PrixCession1 = float(input("Prix de cession :"))
            
            prop = radio("Etes vous le seul propriétaire ?", options = ["Oui", "Non"])
            
            if (prop == "Oui"):
                acquisition = radio("Comment le bien a-t-il été acquis ?", options = ["Achat", "Donation / Succession"])   
                if acquisition == "Achat" :
                    frais = (7.5/100)*PrixAcquisition1
                    travaux = float(input("Montant de vos travaux :"))
                    #if ((15/100)*PrixAcquisition) > travaux:
                    #    travaux = (15/100)*PrixAcquisition
                    #else :
                    #    travaux = travaux
                    PrixAcquisition = PrixAcquisition1 + travaux + frais
                    PlusValue = PrixCession1 - PrixAcquisition

                    data = {
                        "Acquisition":[PrixAcquisition1,frais,travaux,PrixAcquisition],
                        "Cession" : [PrixCession1,0,"",PrixCession1],
                        "Plus-value imposable" : ["","","",PlusValue]
                    }

                    df = pd.DataFrame(data, index = ["Prix","Frais","Travaux","Total"])  
                    df.style.hide_index()
                    put_html(df.to_html())               
                                        
                if acquisition == "Donation / Succession":
                    frais = float(input("Montant de vos frais :"))
                    travaux = float(input("Montant de vos travaux :"))
                    PrixAcquisition = PrixAcquisition1 + travaux + frais
                    PlusValue = PrixCession1 - PrixAcquisition

                    data = {
                        "Acquisition":[PrixAcquisition1,frais,travaux,PrixAcquisition],
                        "Cession" : [PrixCession1,0,"",PrixCession1],
                        "Plus-value imposable" : ["","","",PlusValue]
                    }

                    df = pd.DataFrame(data, index = ["Prix","Frais","Travaux","Total"])
                    df.style.hide_index()  
                    put_html(df.to_html()) 

                                    
                reductionDetentionIR = abbatementIR*PlusValue
                pluValueTaxableIR = PlusValue - reductionDetentionIR
                MontantimpotIR = (19/100)*pluValueTaxableIR

                reductionDetentionPS = abbatementPrelevement*PlusValue
                pluValueTaxablePS = PlusValue - reductionDetentionPS
                MontantimpotPS = (17.2/100)*pluValueTaxablePS    
                impotsTotal = int(MontantimpotIR + MontantimpotPS)

                data2 = {
                        "Impôt sur le revenu":["{:.1%}".format(abbatementIR),reductionDetentionIR,PlusValue-reductionDetentionIR,"{0:.0%}".format(0.19),0.19*(PlusValue-reductionDetentionIR)],
                        "Prélèvements sociaux" : ["{:.1%}".format(abbatementPrelevement),reductionDetentionPS,PlusValue-reductionDetentionPS,"{:.1%}".format(0.172),0.172*(PlusValue-reductionDetentionPS)],
                    }

                df2 = pd.DataFrame(data2, index = ["Taux de réduction lié à la durée de détention","Montant de la réduction liée à la durée de détention","Plus-Value taxable","Taux de l'impôt","Montant de l'impôt"])
                df2.style.hide_index()  
                put_html(df2.to_html()) 
                put_text("Total à payer :", impotsTotal)

            if (prop == "Non"):
                quota = float(input("Quelle est votre quote part en pourcentage ?"))
                quota2 = quota/100
                acquisition = radio("Comment le bien a-t-il été acquis ?", options = ["Achat", "Donation / Succession"])
                if acquisition == "Achat" : 
                    PrixAcquisition = PrixAcquisition1*quota2
                    frais = (7.5/100)*PrixAcquisition1
                    travaux = float(input("Montant de vos travaux :"))
                    #if ((15/100)*PrixAcquisition) > travaux:
                    #    travaux = (15/100)*PrixAcquisition
                    #else :
                    #    travaux = travaux
                    PrixAcquisition = PrixAcquisition + travaux + frais
                    PrixCession = PrixCession1*quota2
                    PlusValue = PrixCession - PrixAcquisition 

                    data = {
                        "Acquisition":[PrixAcquisition,frais,travaux,PrixAcquisition],
                        "Cession" : [PrixCession,0,"",PrixCession],
                        "Plus-value imposable" : ["","","",PlusValue]
                    }

                    df = pd.DataFrame(data, index = ["Prix","Frais","Travaux","Total"])  
                    df.style.hide_index()
                    put_html(df.to_html()) 
                        
                if acquisition == "Donation / Succession":
                    frais = float(input("Montant de vos frais :"))
                    travaux = float(input("Montant de vos travaux :"))
                    PrixAcquisition = PrixAcquisition1*quota2
                    #if ((15/100)*PrixAcquisition) > travaux:
                    #        travaux = (15/100)*PrixAcquisition
                    #else :
                    #    travaux = travaux
                    PrixAcquisition = PrixAcquisition + travaux + frais
                    PrixCession = PrixCession1*quota2
                    PlusValue = PrixCession - PrixAcquisition

                    data = {
                        "Acquisition":[PrixAcquisition,frais,travaux,PrixAcquisition],
                        "Cession" : [PrixCession,0,"",PrixCession],
                        "Plus-value imposable" : ["","","",PlusValue]
                    }

                    df = pd.DataFrame(data, index = ["Prix","Frais","Travaux","Total"])  
                    df.style.hide_index()
                    put_html(df.to_html()) 
                
                reductionDetentionIR = abbatementIR*PlusValue
                pluValueTaxableIR = PlusValue - reductionDetentionIR
                MontantimpotIR = (19/100)*pluValueTaxableIR

                reductionDetentionPS = abbatementPrelevement*PlusValue
                pluValueTaxablePS = PlusValue - reductionDetentionPS
                MontantimpotPS = (17.2/100)*pluValueTaxablePS    
                impotsTotal = int(MontantimpotIR + MontantimpotPS)
                data2 = {
                        "Impôt sur le revenu":["{:.1%}".format(abbatementIR),reductionDetentionIR,PlusValue-reductionDetentionIR,"{0:.0%}".format(0.19),0.19*(PlusValue-reductionDetentionIR)],
                        "Prélèvements sociaux" : ["{:.1%}".format(abbatementPrelevement),reductionDetentionPS,PlusValue-reductionDetentionPS,"{:.1%}".format(0.172),0.172*(PlusValue-reductionDetentionPS)],
                    }
                df2 = pd.DataFrame(data2, index = ["Taux de réduction lié à la durée de détention","Montant de la réduction liée à la durée de détention","Plus-Value taxable","Taux de l'impôt","Montant de l'impôt"])
                df2.style.hide_index()
                put_html(df2.to_html()) 
                put_text("Total à payer :", impotsTotal)
            
        if (typeBien == "Maison / Appartement"):
            residencePrincipale = radio("Est-ce votre résidence principale ?", options = ["Oui", "Non"])  
            if residencePrincipale == "Oui":
                put_success("D’après les informations renseignées, vous êtes exonéré d’impôt sur la plus-value immobilière.")
            if residencePrincipale == "Non": 
                DateAcquisition = input("Date d'acquisition du bien (dd-mm-yyyy)")
                DateAcquisition = DateAcquisition.replace("/","-")
                DateCession = input("Date de cession du bien (dd-mm-yyyy)")
                DateCession = DateCession.replace("/","-")

                DateTimeDateAcquisition = datetime.datetime.strptime(DateAcquisition, '%d-%m-%Y')
                DateTimeDateCession = datetime.datetime.strptime(DateCession, '%d-%m-%Y')
            
                date_time_annee = DateTimeDateCession.year - DateTimeDateAcquisition.year
                date_time_mois = DateTimeDateCession.month - DateTimeDateAcquisition.month

                if date_time_mois < 0:
                    date_time_annee2 = (date_time_annee*12 - ((12 - DateTimeDateCession.month)+(12 - DateTimeDateAcquisition.month)))/12
                else :
                    date_time_annee2 = (date_time_annee*12 + date_time_mois)/12

                datetime1 = floor(date_time_annee2)

                if datetime1 <= 5:
                    abbatementIR = 0
                    abbatementPrelevement = 0
                if datetime1 == 6:
                    abbatementIR = (6/100)
                    abbatementPrelevement = (1.65/100)
                if datetime1 == 7:
                    abbatementIR = (12/100)
                    abbatementPrelevement = (3.3/100)
                if datetime1 == 8:
                    abbatementIR = (18/100)
                    abbatementPrelevement = (4.95/100)
                if datetime1 == 9:
                    abbatementIR = (24/100)
                    abbatementPrelevement = (6.6/100)
                if datetime1 == 10:
                    abbatementIR = (30/100)
                    abbatementPrelevement = (8.25/100)
                if datetime1 == 11:
                    abbatementIR = (36/100)
                    abbatementPrelevement = (9.9/100)
                if datetime1 == 12:
                    abbatementIR = (42/100)
                    abbatementPrelevement = (11.55/100)
                if datetime1 == 13:
                    abbatementIR = (48/100)
                    abbatementPrelevement = (13.2/100)
                if datetime1 == 14:
                    abbatementIR = (54/100)
                    abbatementPrelevement = (14.85/100)
                if datetime1 == 15:
                    abbatementIR = (60/100)
                    abbatementPrelevement = (16.5/100)
                if datetime1 == 16:
                    abbatementIR = (66/100)
                    abbatementPrelevement = (18.15/100)
                if datetime1 == 17:
                    abbatementIR = (72/100)
                    abbatementPrelevement = (19.80/100)
                if datetime1 == 18:
                    abbatementIR = (78/100)
                    abbatementPrelevement = (21.45/100)
                if datetime1 == 19:
                    abbatementIR = (84/100)
                    abbatementPrelevement = (23.1/100)
                if datetime1 == 20:
                    abbatementIR = (90/100)
                    abbatementPrelevement = (24.75/100)
                if datetime1 == 21:
                    abbatementIR = (96/100)
                    abbatementPrelevement = (26.4/100)
                if datetime1 == 22:
                    abbatementIR = (100/100)
                    abbatementPrelevement = (28/100)
                if datetime1 == 23:
                    abbatementIR = (100/100)
                    abbatementPrelevement = (37/100)
                if datetime1 == 24:
                    abbatementIR = (100/100)
                    abbatementPrelevement = (46/100)
                if datetime1 == 25:
                    abbatementIR = (100/100)
                    abbatementPrelevement = (46/100)
                if datetime1 == 26:
                    abbatementIR = (100/100)
                    abbatementPrelevement = (46/100)
                if datetime1 == 27:
                    abbatementIR = (100/100)
                    abbatementPrelevement = (46/100)
                if datetime1 == 28:
                    abbatementIR = (100/100)
                    abbatementPrelevement = (46/100)
                if datetime1 == 29:
                    abbatementIR = (100/100)
                    abbatementPrelevement = (46/100)
                if datetime1 == 30:
                    abbatementIR = (100/100)
                    abbatementPrelevement = (46/100)

                PrixAcquisition1 = float(input("Prix d'acquisition :"))
                PrixCession1 = float(input("Prix de cession :"))

                prop = radio("Etes vous le seul propriétaire ?", options = ["Oui", "Non"])  
                if (prop == "Oui"):
                    acquisition = radio("Comment le bien a-t-il été acquis ?",options = ["Achat", "Donation / Succession"])
                    if acquisition == "Achat" : 
                        frais = (7.5/100)*PrixAcquisition1
                        travaux = float(input("Montant de vos travaux :"))
                        if ((15/100)*PrixAcquisition1) > travaux:
                            travaux = (15/100)*PrixAcquisition1
                        else :
                            travaux = travaux
                        PrixAcquisition = PrixAcquisition1 + travaux + frais
                        PlusValue = PrixCession1 - PrixAcquisition 

                        data = {
                        "Acquisition":[PrixAcquisition1,frais,travaux,PrixAcquisition],
                        "Cession" : [PrixCession1,0,"",PrixCession1],
                        "Plus-value imposable" : ["","","",PlusValue]
                        }

                        df = pd.DataFrame(data, index = ["Prix","Frais","Travaux","Total"])  
                        df.style.hide_index()
                        put_html(df.to_html()) 
                    
                            
                    if acquisition == "Donation / Succession":
                        frais = float(input("Montant de vos frais :"))
                        travaux = float(input("Montant de vos travaux :"))
                        if ((15/100)*PrixAcquisition1) > travaux:
                                travaux = (15/100)*PrixAcquisition1
                        else :
                            travaux = travaux
                        PrixAcquisition = PrixAcquisition1 + travaux + frais
                        PlusValue = PrixCession1 - PrixAcquisition

                        data = {
                            "Acquisition":[PrixAcquisition1,frais,travaux,PrixAcquisition],
                            "Cession" : [PrixCession1,0,"",PrixCession1],
                            "Plus-value imposable" : ["","","",PlusValue]
                            }

                        df = pd.DataFrame(data, index = ["Prix","Frais","Travaux","Total"])  
                        df.style.hide_index()
                        put_html(df.to_html()) 

                    reductionDetentionIR = abbatementIR*PlusValue
                    pluValueTaxableIR = PlusValue - reductionDetentionIR
                    MontantimpotIR = (19/100)*pluValueTaxableIR

                    reductionDetentionPS = abbatementPrelevement*PlusValue
                    pluValueTaxablePS = PlusValue - reductionDetentionPS
                    MontantimpotPS = (17.2/100)*pluValueTaxablePS    
                    impotsTotal = int(MontantimpotIR + MontantimpotPS)

                    data2 = {
                        "Impôt sur le revenu":["{:.1%}".format(abbatementIR),reductionDetentionIR,PlusValue-reductionDetentionIR,"{0:.0%}".format(0.19),0.19*(PlusValue-reductionDetentionIR)],
                        "Prélèvements sociaux" : ["{:.1%}".format(abbatementPrelevement),reductionDetentionPS,PlusValue-reductionDetentionPS,"{:.1%}".format(0.172),0.172*(PlusValue-reductionDetentionPS)],
                    }

                    df2 = pd.DataFrame(data2, index = ["Taux de réduction lié à la durée de détention","Montant de la réduction liée à la durée de détention","Plus-Value taxable","Taux de l'impôt","Montant de l'impôt"])
                    df2.style.hide_index()
                    put_html(df2.to_html()) 
                    put_text("Total à payer :", impotsTotal)

                
                if (prop == "Non"):
                    quota = float(input("Quelle est votre quote part en pourcentage ?"))
                    quota2 = quota/100
                    acquisition = radio("Comment le bien a-t-il été acquis ?", options = ["Achat","Donation / Succession"])
                    if acquisition == "Achat" : 
                        PrixAcquisition = PrixAcquisition1*quota2
                        frais = (7.5/100)*PrixAcquisition
                        travaux = float(input("Montant de vos travaux :"))
                        if ((15/100)*PrixAcquisition) > travaux:
                            travaux = (15/100)*PrixAcquisition
                        else :
                            travaux = travaux
                        PrixAcquisition = PrixAcquisition + travaux + frais
                        PrixCession = PrixCession1*quota2
                        PlusValue = PrixCession - PrixAcquisition 

                        data = {
                            "Acquisition":[PrixAcquisition,frais,travaux,PrixAcquisition],
                            "Cession" : [PrixCession,0,"",PrixCession],
                            "Plus-value imposable" : ["","","",PlusValue]
                            }

                        df = pd.DataFrame(data, index = ["Prix","Frais","Travaux","Total"])  
                        df.style.hide_index()
                        put_html(df.to_html()) 


                    if acquisition == "Donation / Succession":
                        frais = float(input("Montant de vos frais :"))
                        travaux = float(input("Montant de vos travaux :"))
                        PrixAcquisition = PrixAcquisition*quota2
                        if ((15/100)*PrixAcquisition) > travaux:
                                travaux = (15/100)*PrixAcquisition
                        else :
                            travaux = travaux
                        PrixAcquisition = PrixAcquisition + travaux + frais
                        PrixCession = PrixCession*quota2
                        PlusValue = PrixCession - PrixAcquisition

                        data = {
                            "Acquisition":[PrixAcquisition,frais,travaux,PrixAcquisition],
                            "Cession" : [PrixCession,0,"",PrixCession],
                            "Plus-value imposable" : ["","","",PlusValue]
                            }

                        df = pd.DataFrame(data, index = ["Prix","Frais","Travaux","Total"])  
                        df.style.hide_index()
                        put_html(df.to_html()) 
                    reductionDetentionIR = abbatementIR*PlusValue
                    pluValueTaxableIR = PlusValue - reductionDetentionIR
                    MontantimpotIR = (19/100)*pluValueTaxableIR

                    reductionDetentionPS = abbatementPrelevement*PlusValue
                    pluValueTaxablePS = PlusValue - reductionDetentionPS
                    MontantimpotPS = (17.2/100)*pluValueTaxablePS    
                    impotsTotal = int(MontantimpotIR + MontantimpotPS)

                    data2 = {
                        "Impôt sur le revenu":["{:.1%}".format(abbatementIR),reductionDetentionIR,PlusValue-reductionDetentionIR,"{0:.0%}".format(0.19),0.19*(PlusValue-reductionDetentionIR)],
                        "Prélèvements sociaux" : ["{:.1%}".format(abbatementPrelevement),reductionDetentionPS,PlusValue-reductionDetentionPS,"{:.1%}".format(0.172),0.172*(PlusValue-reductionDetentionPS)],
                    }

                    df2 = pd.DataFrame(data2, index = ["Taux de réduction lié à la durée de détention","Montant de la réduction liée à la durée de détention","Plus-Value taxable","Taux de l'impôt","Montant de l'impôt"])
                    df2.style.hide_index()
                    put_html(df2.to_html()) 
                    put_text("Total à payer :", impotsTotal)

    if (choix == "25 - Étude Patrimoiniale") :
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        data = input_group("Informations",
        [
         input('Nom(s) Prenom(s)', name='nom'),
         input('Numéro de téléphone', name='numero'),
         input('E-mail', name='mail'),
         ])

        df_info = pd.DataFrame({
            "Nom(s) Prenom(s)" : [data["nom"]],
            'Numéro de téléphone' : [data["numero"]],
            'E-mail' : [data['mail']],
        })

        data2 = input_group("Etat Civil Personne 1",
        [
         input('Nom', name='nom'),
         input('Prenom', name='prenom'),
         input('Adresse', name='adresse'),
         input("Code postal", name='codepostal'),
         input("Ville", name ="ville"),
         input("Age", name = "age"),
         input("Secteur d'activité", name = "secteur"),
         input("Employeur", name = "employeur"),
         #input("Situation familiale", name = "situation"),
         radio("Situation familiale", options = ["MARIE","CELIBATAIRE","CONCUBINAGE","PACSER"], name = "situation"),
         input("Nombres d'enfants", name = "enfants", type = NUMBER),
         input("Âge enfant 1", name = "enfants1", type = NUMBER),
         input("Âge enfant 2", name = "enfants2", type = NUMBER),
         input("Âge enfant 3", name = "enfants3", type = NUMBER),
         input("Âge enfant 4", name = "enfants4", type = NUMBER),
         input("Âge enfant 5", name = "enfants5", type = NUMBER),
         input("Âge enfant 6", name = "enfants6", type = NUMBER),
         ])

        df_etatcivil_personne1 = pd.DataFrame({
            "Nom" : [data2["nom"]],
            "Prénom" : [data2["prenom"]],
            "Adresse" : [data2["adresse"]],
            "Code Postal" : [data2["codepostal"]],
            "Ville" : data2["ville"],
            "Age" : [data2["age"]],
            "Secteur d'activité" : [data2["secteur"]],
            "Employeur" : [data2["employeur"]],
            "Situation familiale" : [data2["situation"]],
            "Nombres d'enfants": [data2["enfants"]],
            "Age enfant 1" : [data2["enfants1"]],
            "Age enfant 2" : [data2["enfants2"]],
            "Age enfant 3" : [data2["enfants3"]],
            "Age enfant 4" : [data2["enfants4"]],
            "Age enfant 5" : [data2["enfants5"]],
            "Age enfant 6" : [data2["enfants6"]],
        })

        data3 = input_group("Etat Civil Personne 2",
        [
         input('Nom', name='nom'),
         input('Prenom', name='prenom'),
         input('Adresse', name='adresse'),
         input("Code postal", name='codepostal'),
         input("Ville", name ="ville"),
         input("Age", name = "age"),
         input("Secteur d'activité", name = "secteur"),
         input("Employeur", name = "employeur"),
         input("Nombres d'enfants", name = "enfants", type = NUMBER),
         ])

        df_etatcivil_personne2 = pd.DataFrame({
            "Nom" : [data3["nom"]],
            "Prénom" : [data3["prenom"]],
            "Adresse" : [data3["adresse"]],
            "Code Postal" : [data3["codepostal"]],
            "Ville" : data3["ville"],
            "Age" : [data3["age"]],
            "Secteur d'activité" : [data3["secteur"]],
            "Employeur" : [data3["employeur"]],
            "Situation familiale" : [data2["situation"]],
            "Nombres d'enfants": [data2["enfants"]],
            "Age enfant 1" : [data2["enfants1"]],
            "Age enfant 2" : [data2["enfants2"]],
            "Age enfant 3" : [data2["enfants3"]],
            "Age enfant 4" : [data2["enfants4"]],
            "Age enfant 5" : [data2["enfants5"]],
            "Age enfant 6" : [data2["enfants6"]],
        })

        frames = [df_etatcivil_personne1,df_etatcivil_personne2]
        df_etatcivil = pd.concat(frames)

        data4 = input_group("Revenus Personne 1",
        [
         input('Régime', name='regime'),
         input('Revenus net annuel', name='revenusNetAnnuel', type = NUMBER),
         ])
        df_revenus_personne1 = pd.DataFrame({
            "Régime" : [data4["regime"]],
            "Revenus annuel net" : [data4["revenusNetAnnuel"]],
        })
        data5 = input_group("Revenus Personne 2",
        [
         input('Régime', name='regime'),
         input('Revenus net annuel', name='revenusNetAnnuel', type = NUMBER),
         ])
        df_revenus_personne2 = pd.DataFrame({
            "Régime" : [data5["regime"]],
            "Revenus annuel net" : [data4["revenusNetAnnuel"]],
        })
        
        frames2 = [df_revenus_personne1,df_revenus_personne2]
        df_revenus_personne = pd.concat(frames2)

        put_tabs([
        {'title': 'Informations', 'content': put_html(df_info.style.hide_index().to_html()) },
        {'title': 'Etat Civil', 'content': put_html(df_etatcivil.style.hide_index().to_html()) },
        {'title': 'Revenus', 'content': put_html(df_revenus_personne.style.hide_index().to_html()) },
         ])


    if (choix == "26 - Simulateur de calcul de Prêt à taux zéro") :
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        zoneAbisA = ['Marseille', 'Lyon', 'Nice', 'Montpellier', 'Lille', 'Toulon', 'Villeurbanne', 'Aix-en-Provence', 'Argenteuil', 'Créteil', 'Vitry-sur-Seine', 'Aulnay-sous-Bois', 'Champigny-sur-Marne', 'Antibes', 'Cannes', 'Ajaccio', 'Drancy', 'Noisy-le-Grand', 'La Seyne-sur-Mer', 'Cergy', 'Sarcelles', 'Hyères', 'Épinay-sur-Seine', 'Meaux', 'Bondy', 'Fréjus', 'Grasse', 'Le Blanc-Mesnil', 'Sartrouville', 'Sevran', 'Martigues', 'Bobigny', 'Cagnes-sur-Mer', 'Aubagne', 'Corbeil-Essonnes', 'Alfortville', 'Istres', 'Le Cannet', 'Mantes-la-Jolie', 'Livry-Gargan', 'Gennevilliers', 'Choisy-le-Roi', 'Rosny-sous-Bois', 'Melun', 'Marcq-en-Baroeul', 'Noisy-le-Sec', 'Garges-lès-Gonesse', 'Gagny', 'La Courneuve', 'Poissy', 'Savigny-sur-Orge', 'Pontault-Combault', 'Conflans-Sainte-Honorine', 'Stains', 'Six-Fours-les-Plages', 'Tremblay-en-France', 'Marignane', 'Neuilly-sur-Marne', 'La Ciotat', 'Montigny-le-Bretonneux', 'Annemasse', 'Villeneuve-Saint-Georges', 'Houilles', 'Viry-Châtillon', 'Plaisir', 'Pontoise', 'Palaiseau', 'Les Mureaux', 'Athis-Mons', 'Saint-Laurent-du-Var', 'Clichy-sous-Bois', 'Trappes', 'Thiais', 'Menton', 'Savigny-le-Temple', 'Yerres', 'Draveil', 'Lambersart', 'Guyancourt', 'Bezons', 'Vigneux-sur-Seine', 'Pierrefitte-sur-Seine', 'Villiers-le-Bel', 'Vallauris', 'Ermont', 'Villiers-sur-Marne', 'Sannois', 'Ris-Orangis', 'Herblay', 'Élancourt', 'Gonesse', 'Rambouillet', 'Taverny', 'Montfermeil', 'Sucy-en-Brie', 'Brunoy', 'Villeneuve-la-Garenne', 'Romainville', 'Miramas', 'Bussy-Saint-Georges', 'Les Ulis', 'Brétigny-sur-Orge', 'Champs-sur-Marne', 'Villeparisis', 'Eaubonne', "Saint-Ouen-l'Aumône", 'Cormeilles-en-Parisis', 'Montgeron', 'Roissy-en-Brie', 'La Madeleine', 'Les Pavillons-sous-Bois', 'Mandelieu-la-Napoule', 'Combs-la-Ville', 'Deuil-la-Barre', 'Longjumeau', 'La Celle-Saint-Cloud', 'Orly', 'Loos', 'Gif-sur-Yvette', 'Montmorency', 'Morsang-sur-Orge', 'La Valette-du-Var', 'Le Mée-sur-Seine', 'Limeil-Brévannes', 'Dammarie-les-Lys', 'Gardanne', 'Lagny-sur-Marne', 'Saint-Michel-sur-Orge', 'Allauch', 'Ozoir-la-Ferrière', 'Wasquehal', 'Mantes-la-Ville', 'Les Pennes-Mirabeau', 'Montigny-lès-Cormeilles', 'Vence', 'Maurepas', 'Le Plessis-Trévise', 'Chilly-Mazarin', 'Mitry-Mory', 'Mougins', 'Villeneuve-le-Roi', 'Chevilly-Larue', "Saint-Cyr-l'École", 'Chennevières-sur-Marne', 'Les Clayes-sous-Bois', 'Soisy-sous-Montmorency', 'Port-de-Bouc', 'Moissy-Cramayel', 'La Crau', 'Éragny', 'Mauguio', 'Osny', 'Jouy-le-Moutier', 'Bonneuil-sur-Marne', 'Boissy-Saint-Léger', 'Limay', 'Vauréal', 'Brie-Comte-Robert', 'Castelnau-le-Lez', 'Orsay', 'Sanary-sur-Mer', 'Lattes', 'Verrières-le-Buisson', 'Noisiel', 'Verneuil-sur-Seine', 'Fos-sur-Mer', 'Carrières-sur-Seine', 'Carrières-sous-Poissy', 'Montesson', 'Fontainebleau', 'Domont', 'Villeneuve-Loubet', 'Juvisy-sur-Orge', 'Le Bourget', 'Saint-Leu-la-Forêt', 'Saint-Brice-sous-Forêt', 'Lognes', 'Avon', 'Montmagny', 'Bouc-Bel-Air', "Bois-d'Arcy", "Berre-l'Étang", 'Arnouville', 'Courcouronnes', 'Méru', 'Beausoleil', 'Mennecy', 'Sainte-Maxime', 'Valbonne', 'Ollioules', 'Fontenay-le-Fleury', 'Saint-Fargeau-Ponthierry', 'Vaires-sur-Marne', 'Villetaneuse', 'Roquebrune-Cap-Martin', 'Roquebrune-sur-Argens', 'Châteauneuf-les-Martigues', 'Saint-Julien-en-Genevois', 'Épinay-sous-Sénart', 'Andrésy', 'Valenton', 'Auriol', 'Voisins-le-Bretonneux', 'Aubergenville', 'Vernouillet', 'Saint-Cyr-sur-Mer', 'Rognac', 'Triel-sur-Seine', 'Saint-André-lez-Lille', 'Solliès-Pont', 'Le Pradet', 'La Queue-en-Brie', 'Carros', 'Gaillard', 'Claye-Souilly', 'Cogolin', 'Chantilly', 'Porto-Vecchio', 'Septèmes-les-Vallons', 'Plan-de-Cuques', 'Vaux-le-Pénil', 'Persan', 'Dugny', 'Arpajon', 'Gex', 'Mouans-Sartoux', 'Épinay-sur-Orge', 'Cuers', 'Trets', 'La Trinité', 'Villepreux', 'Carqueiranne', 'La Londe-les-Maures', 'Ormesson-sur-Marne', 'Biot', 'Villebon-sur-Yvette', 'Bures-sur-Yvette', 'Villecresnes', 'Gouvieux', 'Chanteloup-les-Vignes', 'Chambly', 'Fuveau', 'Lamorlaye', 'Saint-Germain-lès-Arpajon', 'Villeneuve-lès-Maguelone', 'Méry-sur-Oise', 'Ézanville', 'Beaumont-sur-Oise', 'Saint-Genis-Pouilly', 'Bondoufle', 'Cesson', 'Magny-les-Hameaux', 'Crosne', 'Thorigny-sur-Marne', 'Le Beausset', 'Saint-Gély-du-Fesc', 'Gignac-la-Nerthe', 'Fleury-Mérogis', 'Cabriès', 'Meulan-en-Yvelines', 'Montévrain', 'Saint-Jean-de-Védas', 'Beauchamp', 'Groslay', 'Velaux', 'La Farlède', 'Saint-Pierre-du-Perray', 'Roquevaire', 'Pérols', 'Ferney-Voltaire', 'Divonne-les-Bains', 'Bougival', 'La Grande-Motte', 'Venelles', 'Jouy-en-Josas', 'Dammartin-en-Goële', 'Le Crès', 'Tournan-en-Brie', 'Quincy-sous-Sénart', 'Ville-la-Grand', 'Pierrelaye', 'Marcoussis', 'Gretz-Armainvilliers', 'Peymeinade', 'Saint-Rémy-lès-Chevreuse', 'Serris', 'Saint-Chamas', 'Sausset-les-Pins', 'Le Plessis-Bouchard', 'La Colle-sur-Loup', 'Cassis', 'Juvignac', 'Bandol', 'Bormes-les-Mimosas', 'Lésigny', 'Vétraz-Monthoux', 'Écouen', 'Lisses', 'Louveciennes', 'Saint-Germain-lès-Corbeil', 'Émerainville', 'Montlhéry', 'Paray-Vieille-Poste', 'Reignier-Ésery', 'La Ville-du-Bois', 'Contes', 'Pégomas', 'Vert-Saint-Denis', 'Soisy-sur-Seine', 'Cavalaire-sur-Mer', 'Villemoisson-sur-Orge', 'Prévessin-Moëns', 'La Gaude', 'Auvers-sur-Oise', 'Bailly-Romainvilliers', 'Bessancourt', 'Carnoux-en-Provence', 'Gargenville', 'Vaujours', 'Puget-sur-Argens', 'Le Mesnil-Saint-Denis', 'Saint-Victoret', 'Courdimanche', 'Grabels', 'Magny-le-Hongre', 'Limours', 'Linas', 'Longpont-sur-Orge', 'Épône', 'Gournay-sur-Marne', 'Le Mesnil-le-Roi', 'Roquefort-les-Pins', 'Carry-le-Rouet', 'La Penne-sur-Huveaune', 'Fabrègues', 'Saint-Thibault-des-Vignes', 'Courtry', 'Boussy-Saint-Antoine', 'Gémenos', 'Wissous', 'Palavas-les-Flots', 'Ambilly', 'La Bouilladisse', 'Magnanville', 'La Verrière', 'Chambourcy', 'Bouffémont', 'Esbly', 'Chevreuse', 'Nandy', 'Vendargues', 'Cranves-Sales', 'Saint-Mandrier-sur-Mer', 'Rungis', 'Saint-Mitre-les-Remparts', 'Parmain', 'Thoiry', 'Nanteuil-lès-Meaux', 'Simiane-Collongue', "La Cadière-d'Azur", 'Villefranche-sur-Mer', 'Le Lavandou', 'Menucourt', 'Buc', 'Peypin', 'Clapiers', 'Jouars-Pontchartrain', 'Solliès-Toucas', 'Meyreuil', 'Égly', 'Ensuès-la-Redonne', 'Saint-André-de-la-Roche', 'Jacou', 'Villennes-sur-Seine', 'Ablon-sur-Seine', 'Saintry-sur-Seine', 'La Roquette-sur-Siagne', 'Saint-Clément-de-Rivière', 'Quincy-Voisins', 'Roquefort-la-Bédoule', 'Saulx-les-Chartreux', 'Villabé', 'Saint-Zacharie', 'Le Port-Marly', 'Trilport', "Cap-d'Ail", 'Vaux-sur-Seine', 'Mériel', 'Le Coudray-Montceaux', 'Tourrette-Levens', 'Coubron', 'Levens', 'Champagne-sur-Oise', 'Noiseau', 'Prades-le-Lez', 'La Frette-sur-Seine', 'Teyran', 'Issou', 'Mimet', 'Saint-Tropez', 'Coignières', 'Le Rove', 'Mandres-les-Roses', 'Crégy-lès-Meaux', 'Maurecourt', 'Brou-sur-Chantereine', 'Fourqueux', 'Crécy-la-Chapelle', 'Drap', 'Cessy', 'Ceyreste', 'Villenoy', 'Grimaud', 'Le Plessis-Pâté', 'Cruseilles', 'Gréasque', 'Le Thillay', 'Leuville-sur-Orge', 'La Norville', 'Tourrettes-sur-Loup', 'Gattières', 'Le Rouret', 'Coye-la-Forêt', 'Villiers-sur-Orge', 'Collonges-sous-Salève', 'Ornex', 'Juziers', 'Forges-les-Bains', 'Ballainvilliers', 'Beaulieu-sur-Mer', 'Santeny', 'Le Revest-les-Eaux', 'Veigy-Foncenex', 'Boissise-le-Roi', 'Mareil-Marly', 'La Croix-Valmer', 'Sospel', 'Bornel', 'Saint-Germain-sur-Morin', 'Mézières-sur-Seine', 'Saint-Paul-de-Vence', 'Pomponne', 'Montferrier-sur-Lez', 'Saclay', 'Orry-la-Ville', 'Valleiry', 'Bruyères-le-Châtel', 'Montry', 'Colomars', 'Saint-Cergues', 'Fillinges', 'Saint-Savournin', 'Châteauneuf-Grasse', 'Le Tignet', 'Étiolles', 'La Turbie', 'Dampmart', 'Peynier', 'Collégien', 'Porcheville', 'Neauphle-le-Château', 'Auribeau-sur-Siagne', 'La Destrousse', 'Bonne', 'Tigery', 'Bonifacio', 'La Chapelle-en-Serval', 'Le Bar-sur-Loup', 'Margency', 'Gassin', 'Roissy-en-France', 'Frépillon', 'Villiers-Saint-Frédéric', 'Lavérune', 'Pers-Jussy', 'Montlignon', 'Breuillet', "Les Adrets-de-l'Estérel", 'Vulaines-sur-Seine', 'Coupvray', 'Saint-Martin-du-Var', 'Gometz-le-Châtel', 'Champlan', 'Héricy', 'Èze', 'Solliès-Ville', 'Longperrier', 'Belgentier', 'Buchelay', 'Chanteloup-en-Brie', 'Flins-sur-Seine', 'Bernes-sur-Oise', 'Varennes-Jarcy', 'Samoreau', 'Monnetier-Mornex', 'Le Tholonet', 'Archamps', 'Le Mesnil-en-Thelle', 'Péron','Paris', 'Chatou', 'Croissy-sur-Seine', 'Le Chesnay', 'Le Pecq', 'Le Vésinet', 'Maisons-Laffitte', 'Marly-le-Roi', 'Rocquencourt', 'Saint-Germain-en-Laye', 'Vélizy-Villacoublay', 'Versailles', 'Viroflay', 'Antony', 'Asnières-sur-Seine', 'Bagneux', 'Bois-Colombes', 'Boulogne-Billancourt', 'Bourg-la-Reine', 'Châtenay-Malabry', 'Châtillon', 'Chaville', 'Clamart', 'Clichy', 'Colombes', 'Courbevoie', 'Fontenay-aux-Roses', 'Garches', 'Issy-les-Moulineaux', 'La Garenne-Colombes', 'Le Plessis-Robinson', 'Levallois-Perret', 'Malakoff', 'Marnes-la-Coquette', 'Meudon', 'Montrouge', 'Nanterre', 'Neuilly-sur-Seine', 'Puteaux', 'Rueil-Malmaison', 'Saint-Cloud', 'Sceaux', 'Sèvres', 'Suresnes', 'Vanves', 'Vaucresson', "Ville-d'Avray", 'Aubervilliers', 'Bagnolet', 'Le Pré-Saint-Gervais', 'Le Raincy', 'Les Lilas', 'Montreuil', 'Neuilly-Plaisance', 'Pantin', 'Saint-Denis', 'Saint-Ouen', 'Villemomble', 'Arcueil', 'Bry-sur-Marne', 'Cachan', 'Charenton-le-Pont', 'Fontenay-sous-Bois', 'Gentilly', 'Ivry-sur-Seine', 'Joinville-le-Pont', "L'Haÿ-les-Roses", 'Le Kremlin-Bicêtre', 'Le Perreux-sur-Marne', 'Maisons-Alfort', 'Nogent-sur-Marne', 'Saint-Mandé', 'Saint-Maur-des-Fossés', 'Saint-Maurice', 'Villejuif', 'Vincennes', 'Enghien-les-Bains']
        zoneAbisA = sorted(zoneAbisA)
        zoneB1 = ['Toulouse', 'Nantes', 'Strasbourg', 'Bordeaux', 'Rennes', 'Reims', 'Le Havre', 'Grenoble', 'Dijon', 'Nîmes', 'Clermont-Ferrand', 'Limoges', 'Tours', 'Amiens', 'Metz', 'Perpignan', 'Orléans', 'Rouen', 'Mulhouse', 'Caen', 'Nancy', 'Roubaix', 'Tourcoing', 'Avignon', 'La Rochelle', "Villeneuve-d'Ascq", 'Vénissieux', 'Chambéry', 'Pessac', 'Beauvais', 'Arles', 'Annecy', 'Saint-Malo', 'Bayonne', 'Valenciennes', 'Sète', 'Saint-Herblain', 'Bastia', 'Salon-de-Provence', 'Vaulx-en-Velin', 'Douai', 'Talence', 'Caluire-et-Cuire', 'Wattrelos', 'Compiègne', 'Chartres', 'Rezé', 'Anglet', 'Bron', 'Draguignan', "Saint-Martin-d'Hères", 'Joué-lès-Tours', 'Échirolles', 'Villefranche-sur-Saône', 'Colomiers', 'Thonon-les-Bains', 'Lens', 'Creil', 'Schiltigheim', 'Meyzieu', 'Vandoeuvre-lès-Nancy', 'Rillieux-la-Pape', 'Orange', 'Carpentras', "Villenave-d'Ornon", 'Sotteville-lès-Rouen', 'Aix-les-Bains', 'Saint-Médard-en-Jalles', 'Saint-Étienne-du-Rouvray', 'Illkirch-Graffenstaden', 'Bourgoin-Jallieu', 'Biarritz', 'Béthune', 'Tournefeuille', 'Décines-Charpieu', 'Saint-Sébastien-sur-Loire', 'Armentières', 'Cavaillon', 'Lunel', 'Oullins', 'Bègles', 'Orvault', 'La Teste-de-Buch', 'Le Grand-Quevilly', 'Muret', 'Étampes', 'Agde', 'Gradignan', 'Le Bouscat', 'Frontignan', 'Montigny-lès-Metz', 'Blagnac', 'Cenon', 'Le Petit-Quevilly', 'Vertou', 'Sainte-Foy-lès-Lyon', 'Hérouville-Saint-Clair', 'Bois-Guillaume-Bihorel', 'Mons-en-Baroeul', 'Fleury-les-Aubrais', 'Saint-Genis-Laval', 'Lormont', 'Annecy-le-Vieux', 'Halluin', 'Croix', 'Eysines', 'Gujan-Mestras', 'Tassin-la-Demi-Lune', 'Voiron', 'Olivet', 'Saint-Jean-de-Braye', 'Mont-Saint-Aignan', 'Givors', 'Albertville', 'Pertuis', 'Couëron', 'Nogent-sur-Oise', 'Seynod', 'Bouguenais', 'Carquefou', 'Sorgues', 'Villefontaine', 'Meylan', 'Écully', 'Hem', 'Chamalières', 'Ronchin', 'La Chapelle-sur-Erdre', 'Cluses', 'Bischheim', 'Faches-Thumesnil', 'Cran-Gevrier', 'Saint-Fons', 'Elbeuf', 'Bruz', 'Saint-Jean-de-la-Ruelle', 'Lingolsheim', 'Cestas', 'Montereau-Fault-Yonne', 'La Baule-Escoublac', 'Saint-Cyr-sur-Loire', 'Lucé', 'Montivilliers', 'Brignoles', 'Senlis', 'Guérande', 'Plaisance-du-Touch', 'Hendaye', 'Saint-Égrève', 'Sallanches', 'Cugnaux', 'Cesson-Sévigné', 'Saint-Pierre-des-Corps', 'Bruges', 'Saran', 'Canteleu', 'Coulommiers', 'Laxou', 'Saint-Maximin-la-Sainte-Baume', 'Saint-Avertin', 'Villers-lès-Nancy', 'Bailleul', 'Pornic', 'Crépy-en-Valois', 'Olonne-sur-Mer', 'Haubourdin', "Les Sables-d'Olonne", 'Balma', 'Chenôve', "Château-d'Olonne", 'Saint-Gilles', 'Mouvaux', 'Ambarès-et-Lagrave', 'Lys-lez-Lannoy', 'Wattignies', 'Saint-Jean-de-Luz', 'Amboise', 'Canet-en-Roussillon', 'Roncq', 'Woippy', 'Nemours', 'Sainte-Luce-sur-Loire', 'Biscarrosse', 'Montataire', 'Villeneuve-lès-Avignon', 'Comines', 'Provins', 'Ramonville-Saint-Agne', 'Genas', 'Seclin', 'Pont-Sainte-Maxence', 'Seyssinet-Pariset', 'Tarnos', 'Mions', 'Méricourt', 'La Motte-Servolex', 'Gisors', 'Fonsorbes', 'Ostwald', 'Saint-Martin-de-Crau', 'Brignais', 'Ifs', 'Sassenage', 'Saint-Orens-de-Gameville', 'Maromme', 'Oissel', 'Castanet-Tolosan', 'Talant', 'Monteux', 'Obernai', 'Le Pont-de-Claix', 'Arcachon', 'Mèze', 'Hoenheim', 'Saint-Rémy-de-Provence', 'Chambray-lès-Tours', 'Vedène', 'La Roche-sur-Foron', 'Saint-Jacques-de-la-Lande', 'Dinard', 'Villers-Cotterêts', 'Montlouis-sur-Loire', 'Pacé', 'Vidauban', 'Fondettes', 'Pernes-les-Fontaines', 'Corbas', 'Pornichet', 'Mainvilliers', 'Déville-lès-Rouen', 'Saint-Jean', 'Betton', 'Chevigny-Saint-Sauveur', 'Neuville-en-Ferrain', 'Chantepie', 'La Riche', 'Tinqueux', 'Quetigny', 'Dourdan', 'Argelès-sur-Mer', 'Voreppe', 'Marquette-lez-Lille', 'Marly', 'Brumath', 'Pierre-Bénite', 'Craponne', 'Grand-Couronne', 'Bondues', 'Caudebec-lès-Elbeuf', 'La Chapelle-Saint-Mesmin', 'Biganos', 'Eybens', 'Chassieu', 'Pélissanne', 'Saint-Max', 'Wambrechies', 'Maxéville', 'Mondeville', 'Fosses', 'Portet-sur-Garonne', 'Le Luc', 'Le Haillan', 'Louvres', 'Ouistreham', 'Darnétal', 'Léognan', 'Lambesc', 'Le Muy', 'Fontaine-lès-Dijon', 'Leers', 'Feyzin', 'Longvic', 'La Ferté-sous-Jouarre', 'Petit-Couronne', 'Lorgues', 'Le Taillan-Médoc', 'Castelginest', 'Urrugne', "Gonfreville-l'Orcher", 'Miribel', 'Aytré', 'Saint-Laurent-de-la-Salanque', 'Saint-Grégoire', 'Dardilly', 'Villeneuve-Tolosane', 'Léguevin', 'Marguerittes', 'Port-Saint-Louis-du-Rhône', 'Crolles', 'Aigues-Mortes', 'Évian-les-Bains', 'Chécy', 'Le Thor', 'La Ravoire', 'Meythet', 'Lançon-Provence', 'Pibrac', 'Les Angles', 'Saint-Pierre-lès-Elbeuf', "La Chapelle-d'Armentières", 'Irigny', 'Le Grau-du-Roi', 'Basse-Goulaine', 'Capbreton', 'Frouzins', 'Honfleur', 'Vern-sur-Seiche', 'Harfleur', 'Saint-Loubès', 'Linselles', 'Ballan-Miré', 'Nangis', 'Pérenchies', 'Margny-lès-Compiègne', 'Saint-Aubin-lès-Elbeuf', 'Chaponost', 'Elne', 'Vif', 'Aucamville', 'Ingré', 'Entraigues-sur-la-Sorgue', 'Parempuyre', 'Noisy-le-Roi', 'Charvieu-Chavagneux', 'Thouaré-sur-Loire', 'Le Rheu', 'Seysses', 'Boucau', 'Saint-Vincent-de-Tyrosse', 'Vizille', 'Gleizé', 'Morières-lès-Avignon', 'Moirans', 'Borgo', 'Houplines', 'Sainte-Adresse', 'Éguilles', 'Les Sorinières', 'Le Mesnil-Esnard', 'Souffelweyersheim', 'Scionzier', 'Rochefort-du-Gard', 'Nieppe', 'Thorigné-Fouillard', 'Ballancourt-sur-Essonne', 'Trignac', 'Saint-Gilles-Croix-de-Vie', 'Chartres-de-Bretagne', 'Biguglia', 'Mordelles', 'Lagord', 'Launaguet', 'Gaillon', 'La Fare-les-Oliviers', 'Villard-Bonnot', 'Saint-Denis-en-Val', 'Neuville-sur-Saône', 'Artigues-près-Bordeaux', 'Martignas-sur-Jalle', 'Montluel', 'Liancourt', 'Geispolsheim', 'Donges', 'Poisy', 'Montoir-de-Bretagne', 'Sautron', 'Quesnoy-sur-Deûle', 'Luisant', 'Notre-Dame-de-Bondeville', "Saint-Jean-d'Illac", 'Ciboure', 'Seyssins', 'Bassens', 'Bassens', 'Carbon-Blanc', 'Balaruc-les-Bains', 'La Salvetat-Saint-Gilles', 'Le Teich', 'Les Arcs', 'Sérignan', 'Saint-Ismier', 'Huningue', 'Trévoux', 'Saint-Bonnet-de-Mure', 'Le Perray-en-Yvelines', 'Domène', 'Aussonne', 'Itteville', 'La Mulatière', 'La Tronche', 'Champagne-sur-Seine', 'Noyal-Châtillon-sur-Seiche', 'Eckbolsheim', 'La Verpillière', "Saint-Didier-au-Mont-d'Or", 'Bonsecours', 'Pignan', 'Varces-Allières-et-Risset', 'Bétheny', 'Ustaritz', 'Othis', 'Saint-Aubin-de-Médoc', 'Audenge', 'Publier', 'Bidart', 'Les Essarts-le-Roi', 'Lesquin', 'Marignier', 'Anse', 'Fontaines-sur-Saône', 'Baillargues', 'Tignieu-Jameyzieu', 'Acigné', 'Villers-Saint-Paul', 'Bouillargues', 'Gières', 'Escalquens', 'Franqueville-Saint-Pierre', 'Thônes', 'Veigné', 'Marsillargues', 'Jassans-Riottier', 'Bouaye', 'Rives', 'Châtelaillon-Plage', 'Cormontreuil', 'Cognin', 'La Montagne', 'Saint-Pierre-en-Faucigny', 'Malaunay', 'Montauroux', 'Manduel', 'La Wantzenau', 'Mazan', 'Saint-Quentin-Fallavier', 'Le Pian-Médoc', 'Cournonterral', 'Maule', 'Castries', 'Sarrians', 'Cornebarrieu', 'Saint-Alban-Leysse', 'Milhaud', 'Octeville-sur-Mer', 'Lèves', 'Thyez', 'Gigean', 'Nieul-sur-Mer', 'Jonage', 'Longueau', 'Pierrefeu-du-Var', 'Pont-Saint-Martin', 'Marennes', 'Santes', 'Brindas', 'Saint-Pierre-lès-Nemours', "Saint-Cyr-au-Mont-d'Or", 'Trans-en-Provence', 'Calvi', 'Mornant', 'Rosny-sur-Seine', 'Haute-Goulaine', "Saint-Martin-d'Uriage", 'Eaunes', 'Puilboreau', 'Vendenheim', 'Saint-Cannat', 'Lardy', 'Furiani', 'Marly-la-Ville', 'Épernon', 'Fegersheim', 'Colombelles', 'Cléon', 'Chasse-sur-Rhône', 'Saint-Martin-le-Vinoux', 'Courthézon', "Saint-Georges-d'Orques", 'Saint-Jory', 'Beauzelle', 'Izon', 'Lentilly', 'Dompierre-sur-Mer', 'Vias', "Saint-Symphorien-d'Ozon", 'Le Puy-Sainte-Réparade', 'Saint-Nom-la-Bretèche', 'Challes-les-Eaux', 'Luynes', 'Fayence', 'Saint-Laurent-de-Mure', 'Bléré', 'Mouy', 'Saint-Jean-de-Boiseau', 'Aubignan', 'Marsannay-la-Côte', 'Cadaujac', 'Saint-Pryvé-Saint-Mesmin', "Champagne-au-Mont-d'Or", 'Marnaz']
        zoneB1 = sorted(zoneB1)
        zoneB2= ['Corbières',"Esparron-de-Verdon","Forcalquier","Gréoux-les-Bains","LaBrillanne","LesMées","Mane","Manosque","Oraison","Peyruis","Pierrevert","Sainte-Tulle","Saint-Martin-de-Brômes","Sisteron","Valensole","Villeneuve","Volx","Briançon","Gap","Andon","Bendejun","Bézaudun-les-Alpes","Blausasc","Bouyon","Breil-sur-Roya","Castillon","Caussols","Cipières","Coaraze","Conségudes","Courmes","Coursegoules","Duranus","Escragnolles","Gréolières","LaBollène-Vésubie","Lantosque","LesFerres","L'Escarène","Lucéram","Moulinet","Peille","Peillon","Revest-les-Roches","Roquestéron-Grasse","Toudon","Touët-de-l'Escarène","Tourette-du-Château","Utelle","Cornas","Guilherand-Granges","LeTeil","Mauves","Rochemaure","Saint-Jean-de-Muzols","Saint-Péray","Soyons","Tournon-sur-Rhône","Charleville-Mézières","LaFrancheville","LesAyvelles","Montcy-Notre-Dame","Prix-lès-Mézières","Saint-Laurent","Villers-Semeuse","Warcq","Barberey-Saint-Sulpice","Bréviandes","Buchères","Creney-près-Troyes","LaChapelle-Saint-Luc","LaRivière-de-Corps","Lavau","LesNoës-près-Troyes","Pont-Sainte-Marie","Rosières-près-Troyes","Saint-André-les-Vergers","Sainte-Maure","Sainte-Savine","Saint-Germain","Saint-Julien-les-Villas","Saint-Parres-aux-Tertres","Troyes","Verrières","Villechétif","Armissan","Bages","Berriac","Carcassonne","Cazilhac","Coursan","Fleury","Gruissan","Leucate","Narbonne","Pennautier","Peyriac-de-Mer","Port-la-Nouvelle","Salles-d'Aude","Sigean","Vinassan","LeMonastère","Luc-la-Primaube","Olemps","Onet-le-Château","Rodez","Sébazac-Concourès","Alleins","Aureille","Aurons","Barbentane","Cabannes","Châteaurenard","Eygalières","Eyguières","Eyragues","Fontvieille","Graveson","Jouques","LaRoque-d'Anthéron","Lamanon","LesBaux-de-Provence","Maillane","Mallemort","Maussane-les-Alpilles","Mollégès","Mouriès","Noves","Orgon","Paradou","Plan-d'Orgon","Puyloubier","Rognonas","Saint-Andiol","Saint-Antonin-sur-Bayon","Saintes-Maries-de-la-Mer","Saint-Paul-lès-Durance","Sénas","Tarascon","Vauvenargues","Vernègues","Verquières","Ablon","Argences","Auberville","Authie","Baron-sur-Odon","Benerville-sur-Mer","Bénouville","Bernières-sur-Mer","Biéville-Beuville","Blainville-sur-Orne","Blonville-sur-Mer","Bonneville-sur-Touques","Bretteville-l'Orgueilleuse","Cabourg","Cagny","Cambes-en-Plaine","Canapville","Colleville-Montgomery","Courseulles-sur-Mer","Cresserons","Cuverville","Démouville","Dives-sur-Mer","Douvres-la-Délivrande","Équemauville","Éterville","Fontaine-Étoupefour","Frénouville","Giberville","Gonneville-sur-Honfleur","Hermanville-sur-Mer","Houlgate","LaRivière-Saint-Sauveur","Langrune-sur-Mer","Lion-sur-Mer","Luc-sur-Mer","Mathieu","Merville-Franceville-Plage","Mouen","Moult","Périers-sur-le-Dan","Plumetot","Pont-l'Évêque","Rots","Saint-Arnoult","Saint-Aubin-d'Arquenay","Saint-Aubin-sur-Mer","Saint-Contest","Saint-Vaast-en-Auge","Sannerville","Touques","Tourgéville","Tourville-sur-Odon","Trouville-sur-Mer","Varaville","Villers-sur-Mer","Villerville","Villons-les-Buissons","Angoulême","Fléac","Gond-Pontouvre","LaCouronne","Linars","L'Isle-d'Espagnac","Magnac-sur-Touvre","Mornac","Nersac","Puymoyen","Ruelle-sur-Touvre","Saint-Michel","Saint-Yrieix-sur-Charente","Soyaux","Touvre","Trois-Palis","Arces","Arvert","Barzan","Boutenac-Touvent","Breuillet","Breuil-Magné","Brie-sous-Mortagne","Chaillevette","Chenac-Saint-Seurin-d'Uzet","Cozes","Dolus-d'Oléron","Échillais","Épargnes","Esnandes","Étaules","Floirac","Fontcouverte","Grézac","Île-d'Aix","LaBrée-les-Bains","LaJarne","LaTremblade","LeChâteau-d'Oléron","LeChay","LeGrand-Village-Plage","L'Éguille","LesGonds","LesMathes","Marsilly","Médis","Meschers-sur-Gironde","Mornac-sur-Seudre","Mortagne-sur-Gironde","Rochefort","Royan","Saint-Augustin","Saint-Denis-d'Oléron","Saintes","Sainte-Soulle","Saint-Georges-de-Didonne","Saint-Georges-d'Oléron","Saint-Laurent-de-la-Prée","Saint-Palais-sur-Mer","Saint-Pierre-d'Oléron","Saint-Rogatien","Saint-Romain-sur-Gironde","Saint-Sulpice-de-Royan","Saint-Trojan-les-Bains","Saint-Vivien","Saint-Xandre","Saujon","Semussac","Talmont-sur-Gironde","Tonnay-Charente","Vaux-sur-Mer","Vergeroux","Yves","Annoix","Arçay","Berry-Bouy","Bourges","Fussy","LaChapelle-Saint-Ursin","LeSubdray","Marmagne","Morthomiers","Plaimpied-Givaudins","Saint-Doulchard","Saint-Germain-du-Puy","Saint-Just","Saint-Michel-de-Volangis","Trouy","Brive-la-Gaillarde","Larche","Malemort-sur-Corrèze","Saint-Pantaléon-de-Larche","Ussac","Albitreccia","Altagène","Ambiegna","Arbellara","Arbori","Argiusta-Moriccio","Arro","Aullène","Azilone-Ampaza","Azzana","Balogna","Bastelica","Belvédère-Campomoro","Bilia","Bocognano","Calcatoggio","Campo","Cannelle","Carbini","Carbuccia","Cardo-Torgia","Cargèse","Cargiaca","Casaglione","Casalabriva","Cauro","Ciamannacce","Coggia","Cognocoli-Monticchi","Conca","Corrano","Coti-Chiavari","Cozzano","Cristinacce","Eccica-Suarella","Évisa","Figari","Foce","Forciolo","Fozzano","Frasseto","Granace","Grossa","Grosseto-Prugna","Guagno","Guargualé","Guitera-les-Bains","Lecci","Letia","Levie","Lopigna","Loreto-di-Tallano","Marignana","Mela","Moca-Croce","Monacia-d'Aullène","Murzo","Ocana","Olivese","Olmeto","Olmiccia","Orto","Osani","Ota","Palneca","Partinello","Pastricciola","Petreto-Bicchisano","Piana","Pianottoli-Caldarello","Pietrosella","Pila-Canale","Poggiolo","Quasquara","Quenza","Renno","Rezza","Rosazia","Sainte-Lucie-de-Tallano","Salice","Sampolo","San-Gavino-di-Carbini","Santa-Maria-Figaniella","Santa-Maria-Siché","Sant'Andréa-d'Orcino","Sari-d'Orcino","Sari-Solenzara","Serra-di-Ferro","Serra-di-Scopamène","Serriera","Soccia","Sollacaro","Sorbollano","Sotta","Tasso","Tavera","Tolla","Ucciani","Urbalacone","Vero","Vico","Viggianello","Zérubia","Zévaco","Zicavo","Zigliara","Zonza","Zoza","Aghione","Aiti","Alando","Albertacce","Aléria","Altiani","Alzi","Ampriani","Antisanti","Asco","Avapessa","Barbaggio","Barrettali","Belgodère","Bigorno","Bisinchi","Bustanico","Cagnano","Calacuccia","Cambia","Campana","Campi","Campile","Campitello","Canale-di-Verde","Canari","Canavaggia","Carcheto-Brustico","Carpineto","Carticasi","Casabianca","Casalta","Casamaccioli","Casanova","Casevecchie","Castellare-di-Mercurio","Castello-di-Rostino","Castifao","Castiglione","Castineta","Castirla","Cateri","Centuri","Cervione","Chiatra","Chisa","Corscia","Corte","Costa","Croce","Crocicchia","Erbajolo","Érone","Ersa","Farinole","Favalello","Felce","Feliceto","Ficaja","Focicchia","Galéria","Gavignano","Ghisonaccia","Ghisoni","Giocatojo","Giuncaggio","Isolaccio-di-Fiumorbo","LaPorta","Lama","Lano","Lavatoggio","Lento","Linguizzetta","Loreto-di-Casinca","Lozzi","Lugo-di-Nazza","Luri","Manso","Matra","Mausoléo","Mazzola","Meria","Moïta","Moltifao","Monacia-d'Orezza","Monte","Montegrosso","Morosaglia","Morsiglia","Muracciole","Murato","Muro","Nessa","Nocario","Noceta","Nonza","Novale","Novella","Occhiatana","Ogliastro","Olcani","Oletta","Olmeta-di-Capocorso","Olmeta-di-Tuda","Olmi-Cappella","Olmo","Omessa","Ortale","Ortiporio","Palasca","Pancheraccia","Parata","Patrimonio","Penta-Acquatella","Perelli","Pero-Casevecchie","Pianello","Piano","Piazzali","Piazzole","Piedicorte-di-Gaggio","Piedicroce","Piedigriggio","Piedipartino","Pie-d'Orezza","Pietracorbara","Pietra-di-Verde","Pietralba","Pietraserena","Pietricaggio","Pietroso","Piève","Pino","Piobetta","Pioggiola","Poggio-di-Nazza","Poggio-di-Venaco","Poggio-d'Oletta","Poggio-Marinaccio","Polveroso","Popolasca","Porri","Prato-di-Giovellina","Prunelli-di-Casacconi","Prunelli-di-Fiumorbo","Pruno","Quercitello","Rapaggio","Rapale","Riventosa","Rogliano","Rospigliani","Rusio","Rutali",
        "Saint-Florent","Saliceto","San-Damiano","San-Gavino-d'Ampugnani","San-Gavino-di-Fiumorbo","San-Gavino-di-Tenda","San-Giovanni-di-Moriani","San-Giuliano","San-Lorenzo","San-Nicolao","Santa-Lucia-di-Mercurio","Santa-Maria-Poggio","Sant'Andréa-di-Bozio","Sant'Andréa-di-Cotone","Sant'Antonino","Santa-Reparata-di-Moriani","Santo-Pietro-di-Tenda","Santo-Pietro-di-Venaco","Scata","Scolca","Sermano","Serra-di-Fiumorbo","Silvareccio","Sisco","Solaro","Sorio","Soveria","Speloncato","Stazzona","Tallone","Tarrano","Tomino","Tox","Tralonca","Urtaca","Vallecalle","Valle-d'Alesani","Valle-di-Campoloro","Valle-di-Rostino","Valle-d'Orezza","Vallica","Velone-Orneto","Venaco","Ventiseri","Verdèse","Vezzani","Vignale","Ville-di-Paraso","Vivario","Volpajola","Zalana","Zilia","Zuani","Ahuy","Beaune","Bressey-sur-Tille","Bretenière","Crimolois","Fénay","Hauteville-lès-Dijon","Magny-sur-Tille","Dinan","Hillion","Île-de-Bréhat","Kermaria-Sulard","LaMéaugon","Lancieux","Langueux","Lannion","Léhon","Louannec","Penvénan","Perros-Guirec","Plédran","Plérin","Plessix-Balisson","Plestin-les-Grèves","Pleumeur-Bodou","Ploubalay","Ploubezre","Ploufragan","Ploulec'h","Ploumilliau","Plouzélambre","Plufur","Pordic","Rospez","Saint-Brieuc","Saint-Donan","Saint-Julien","Saint-Michel-en-Grève","Saint-Quay-Perros","Taden","Trébeurden","Trédrez-Locquémeau","Tréduder","Trégastel","Trégueux","Trélévern","Trémel","Tréméloir","Trémuson","Trévou-Tréguignec","Yffiniac","Bassillac","Bergerac","Boulazac","Champcevinel","Chancelade","Coulounieix-Chamiers","Cours-de-Pile","Creysse","Gardonne","Ginestet","LaFeuillade","LaForce","Lamonzie-Saint-Martin","Lembras","Marsac-sur-l'Isle","Mouleydier","Notre-Dame-de-Sanilhac","Pazayac","Périgueux","Port-Sainte-Foy-et-Ponchapt","Prigonrieux","Saint-Antoine-de-Breuilh","Saint-Germain-et-Mons","Saint-Laurent-des-Vignes","Saint-Nexans","Saint-Pierre-d'Eyraud","Saint-Sauveur","Trélissac","Allenjoie","Amagney","Arbouans","Arguel","Audeux","Audincourt","Auxon-Dessous","Auxon-Dessus","Avanne-Aveney","Badevel","Bart","Bavans","Besançon","Bethoncourt","Beure","Bourguignon","Boussières","Braillans","Brognard","Busy","Chalèze","Chalezeule","Champagney","Champoux","Champvans-les-Moulins","Châtillon-le-Duc","Chaucenne","Chaudefontaine","Chemaudin","Courcelles-lès-Montbéliard","Dambenois","Dampierre-les-Bois","Dannemarie-sur-Crète","Dasle","Deluz","Devecey","Dommartin","Doubs","École-Valentin","Étupes","Exincourt","Fesches-le-Châtel","Fontain","Franois","Gennes","Grand-Charmont","Grandfontaine","Hérimoncourt","Houtaud","LaChevillotte","LaVèze","Larnod","LeGratteris","Mamirolle","Mandeure","Marchaux","Mathay","Mazerolles-le-Salin","Métabief","Miserey-Salines","Montbéliard","Montfaucon","Montferrand-le-Château","Morre","Morteau","Nancray","Noironte","Nommay","Novillars","Osselle","Pelousey","Pirey","Pontarlier","Pouilley-les-Vignes","Pugey","Rancenay","Roche-lez-Beaupré","Routelle","Sainte-Suzanne","Saône","Seloncourt","Serre-les-Sapins","Sochaux","Taillecourt","Tallenay","Thise","Thoraise","Torpes","Vaire-Arcier","Vaire-le-Petit","Valentigney","Vandoncourt","Vaux-les-Prés","Vieux-Charmont","Vorges-les-Pins","Voujeaucourt","Ancône","Beaumont-lès-Valence","Beauvallon","Bourg-de-Péage","Bourg-lès-Valence","Chabeuil","Chatuzange-le-Goubet","Étoile-sur-Rhône","Génissieux","Malissard","Montboucher-sur-Jabron","Montéléger","Montélier","Montélimar","Montmeyran","Mours-Saint-Eusèbe","Peyrins","Portes-lès-Valence","Romans-sur-Isère","Saint-Marcel-lès-Valence","Tain-l'Hermitage","Valence","Acquigny","Aigleville","Amécourt","Amfreville-sur-Iton","Angerville-la-Campagne","Arnières-sur-Iton","Aubevoye","Authevernes","Aviron","Bazincourt-sur-Epte","Bernouville","Berthenonville","Beuzeville","Bézu-la-Forêt","Bézu-Saint-Éloi","Bois-le-Roi","Boncourt","Boulleville","Bretagnolles","Breuilpont","Bueil","Bus-Saint-Rémy","Cahaignes","Cantiers","Caugé","Chaignes","Château-sur-Epte","Chauvincourt-Provemont","Cierrey","Civières","Corneville-sur-Risle","Coudray","Courcelles-sur-Seine","Criquebeuf-sur-Seine","Croth","Dampsmesnil","Dangu","Dardez","Doudeauville-en-Vexin","Écos","Émalleville","Épieds","Étrépagny","Évreux","Ézy-sur-Eure","Farceaux","Fatouville-Grestain","Fauville","Fiquefleur-Équainville","Fontenay","Fourges","Fours-en-Vexin","Gadencourt","Gamaches-en-Vexin","Garennes-sur-Eure","Gauciel","Gauville-la-Campagne","Gravigny","Guerny","Guichainville","Hacqueville","Hébécourt","Hécourt","Heudicourt","Huest","Incarville","Irreville","Ivry-la-Bataille","LaBoissière","LaChapelle-du-Bois-des-Faulx","LaCouture-Boussey","LaHaye-le-Comte","LaNeuve-Grange","LaTrinité","LeBoulay-Morin","LeManoir","LeMesnil-Fuguet","LePlessis-Grohan","LeThil","LeTorpt","LeVal-David","LeVaudreuil","LeVieil-Évreux","Léry","LesBaux-Sainte-Croix","LesDamps","LesThilliers-en-Vexin","LesVentes","L'Habit","Lignerolles","Longchamps","Louviers","Mainneville","Manneville-la-Raoult","Manneville-sur-Risle","Marcilly-sur-Eure","Martagny","Merey","Mesnil-sous-Vienne","Miserey","Mouettes","Mouflaines","Mousseaux-Neuville","Neaufles-Saint-Martin","Neuilly","Nojeon-en-Vexin","Normanville","Noyers","Parville","Pinterville","Pîtres","Pont-Audemer","Pont-de-l'Arche","Puchay","Reuilly","Richeville","Sacquenville","Saint-Aubin-sur-Gaillon","Saint-Denis-le-Ferment","Sainte-Barbe-sur-Gaillon","Sainte-Marie-de-Vatimesnil","Saint-Étienne-du-Vauvray","Saint-Germain-des-Angles","Saint-Germain-Village","Saint-Laurent-des-Bois","Saint-Luc","Saint-Maclou","Saint-Mards-de-Blacarville","Saint-Martin-la-Campagne","Saint-Pierre-du-Val","Saint-Pierre-du-Vauvray","Saint-Sébastien-de-Morsent","Saint-Vigor","Sancourt","Sassey","Serez","Suzay","Tourneville","Toutainville","Val-de-Reuil","Vesly","Vieux-Villez","Villegats","Villers-en-Vexin","Villers-sur-le-Roule","Villiers-en-Désoeuvre","Abondant","Ardelu","Aunay-sous-Auneau","Auneau","Bailleau-Armenonville","Barmainville","Baudreville","Berchères-sur-Vesgre","Béville-le-Comte","Bleury-Saint-Symphorien","Boncourt","Bouglainval","Boutigny-Prouais","Bréchamps","Broué","Bû","Champagne","Champseru","Charpont","Chartainvilliers","Châtenay","Chaudon","Cherisy","Coulombs","Croisilles","Denonville","Dreux","Droue-sur-Drouette","Écluzelles","Écrosnes","Faverolles","Gallardon","Garancières-en-Beauce","Gas","Germainville","Gilles","Gommerville","Gouillons","Goussainville","Guainville","Havelu","Houx","Intréville","LaChapelle-d'Aunainville","LaChapelle-Forainvilliers","LaChaussée-d'Ivry","LeBoullay-Thierry","LeGué-de-Longroi","LeMesnil-Simon","LesPinthières","Léthuin","Levainville","Levesville-la-Chenard","Lormaye","Louville-la-Chenard","Luray","Maintenon","Maisons","Marchezais","Mérouville","Mévoisins","Mézières-en-Drouais","Moinville-la-Jeulin","Mondonville-Saint-Jean","Morainville","Néron","Neuvy-en-Beauce","Nogent-le-Roi","Oinville-sous-Auneau","Orlu","Ormoy","Ouarville","Ouerre","Oulins","Oysonville","Pierres","Roinville","Rouvray-Saint-Denis","Rouvres","Sainte-Gemme-Moronval","Saint-Laurent-la-Gâtine","Saint-Léger-des-Aubées","Saint-Lubin-de-la-Haye","Saint-Lucien","Saint-Martin-de-Nigelles","Saint-Ouen-Marchefroy","Saint-Piat","Sainville","Santeuil","Saussay","Senantes","Serazereux","Serville","Sorel-Moussel","Soulaires","Umpeau","Vernouillet","Vierville","Villemeux-sur-Eure","Villiers-le-Morhier","Voise","Yermenonville","Ymeray","Bénodet","Bohars","Brest","Clohars-Fouesnant","Combrit","Concarneau","Ergué-Gabéric","Fouesnant","Gouesnach","Gouesnou","Guengat","Guilers","Guilvinec","Guipavas","Île-de-Batz","Île-de-Sein","Île-Molène","Île-Tudy","LaForêt-Fouesnant","LeRelecq-Kerhuon","Loctudy",
        "Loperhet","Ouessant","Penmarch","Pleuven","Plobannalec-Lesconil","Plogonnec","Plomelin","Plomeur","Plonéis","Plougastel-Daoulas","Plouzané","Pluguffan","Pont-l'Abbé","Quimper","Saint-Jean-Trolimon","Treffiagat","Trégunc","Alès","Anduze","Aramon","Bagard","Bagnols-sur-Cèze","Beaucaire","Bellegarde","Boisset-et-Gaujac","Cendras","Clarensac","Laudun-l'Ardoise","LeCailar","Méjannes-lès-Alès","Orsan","Rousson","Saint-Christol-lès-Alès","Saint-Gilles","Saint-Hilaire-de-Brethmas","Saint-Jean-du-Pin","Saint-Julien-les-Rosiers","Saint-Laurent-d'Aigouze","Saint-Martin-de-Valgalgues","Saint-Nazaire","Saint-Privat-des-Vieux","Salindres","Saze","Tresques","Vauvert","Castelnau-d'Estrétefonds","Ambès","Andernos-les-Bains","Arès","Aubie-et-Espessas","Cubzac-les-Ponts","Lalande-de-Pomerol","Lanton","Lège-Cap-Ferret","LesBillaux","Libourne","Marcheprime","Pineuilh","Pomerol","Saint-André-de-Cubzac","Saint-Antoine","Saint-Avit-Saint-Nazaire","Saint-Denis-de-Pile","Sainte-Foy-la-Grande","Saint-Émilion","Saint-Louis-de-Montferrand","Saint-Philippe-du-Seignal","Saint-Sulpice-de-Faleyrens","Bassan","Béziers","Boujan-sur-Libron","Bouzigues","Candillargues","Cers","Corneilhan","Lansargues","Lieuran-lès-Béziers","Lignan-sur-Orb","Loupian","Maraussan","Montady","Mudaison","Poussan","Valergues","Valras-Plage","Vendres","Villeneuve-lès-Béziers","Bourgbarré","Brécé","Cancale","Châteauneuf-d'Ille-et-Vilaine","Cintré","Clayes","Corps-Nuds","Hirel","LaChapelle-Thouarault","LaFresnais","LaGouesnière","LaRichardais","LaVille-ès-Nonais","Laillé","LeTronchet","LeVerger","Lillemer","Miniac-Morvan","Nouvoitou","Noyal-sur-Vilaine","Parthenay-de-Bretagne","Plerguer","Pleurtuit","Saint-Armel","Saint-Benoît-des-Ondes","Saint-Briac-sur-Mer","Saint-Coulomb","Saint-Guinoux","Saint-Jouan-des-Guérets","Saint-Lunaire","Saint-Méloir-des-Ondes","Saint-Père","Saint-Suliac","Saint-Sulpice-la-Forêt","Châteauroux","Déols","LePoinçonnet","Saint-Maur","Cangey","Chargé","Civray-de-Touraine","Dierre","Druye","LaCroix-en-Touraine","Limeray","Monts","Noizay","Saint-Étienne-de-Chigny","Saint-Martin-le-Beau","Saint-Ouen-les-Vignes","Chanas","Chatte","Four","Jardin","LaChapelle-de-la-Tour","LaTour-du-Pin","LeGrand-Lemps","LePéage-de-Roussillon","LesRoches-de-Condrieu","Pontcharra","Pont-Évêque","Roussillon","Sablons","Saint-Clair-de-la-Tour","Saint-Clair-du-Rhône","Saint-Jean-de-Soudain","Saint-Marcellin","Saint-Maurice-l'Exil","Saint-Prim","Salaise-sur-Sanne","Satolas-et-Bonce","Seyssuel","Vienne","Vinay","Authume","Baverans","Bois-d'Amont","Brevans","Choisey","Crissey","Dole","Foucherans","LesRousses","Prémanon","Villette-lès-Dole","Dax","Mont-de-Marsan","Narrosse","Orx","Saint-Barthélemy","Saint-Paul-lès-Dax","Saint-Pierre-du-Mont","Saint-Vincent-de-Paul","Sanguinet","Seyresse","Soustons","Averdon","Blois","Candé-sur-Beuvron","Cellettes","Chailles","Cheverny","Chitenay","Cormeray","Cour-Cheverny","Fossé","Huisseau-sur-Cosson","LaChaussée-Saint-Victor","LesMontils","Marolles","Menars","Monthou-sur-Bièvre","Saint-Bohaire","Saint-Denis-sur-Loire","Saint-Gervais-la-Forêt","Saint-Lubin-en-Vergonnois","Saint-Sulpice-de-Pommeray","Sambin","Seur","Valaire","Villebarou","Villerbon","Vineuil","Andrézieux-Bouthéon","Bonson","Cellieu","Châteauneuf","Chazelles-sur-Lyon","Commelle-Vernay","Farnay","Firminy","Fraisses","Genilac","LaFouillouse","LaGrand-Croix","LaRicamarie","LaTalaudière","LaTour-en-Jarez","LeChambon-Feugerolles","LeCoteau","L'Étrat","L'Horme","Lorette","Mably","Montbrison","Montrond-les-Bains","Pouilly-les-Nonains","Renaison","Riorges","Rive-de-Gier","Roanne","Roche-la-Molière","Saint-Alban-les-Eaux","Saint-André-d'Apchon","Saint-Chamond","Saint-Étienne","Saint-Galmier","Saint-Genest-Lerpt","Saint-Haon-le-Châtel","Saint-Haon-le-Vieux","Saint-Jean-Bonnefonds","Saint-Joseph","Saint-Just-Saint-Rambert","Saint-Léger-sur-Roanne","Saint-Martin-la-Plaine","Saint-Paul-en-Jarez","Saint-Priest-en-Jarez","Savigneux","Sorbiers","Sury-le-Comtal","Unieux","Veauche","Villars","Villerest","Aurec-sur-Loire","Monistrol-sur-Loire","Pont-Salomon","Saint-Ferréol-d'Auroure","Saint-Just-Malmont","Ancenis","Assérac","Besné","Clisson","Grandchamps-des-Fontaines","Herbignac","LaChapelle-des-Marais","LaChapelle-Heulin","LaHaie-Fouassière","LaPlaine-sur-Mer","LaTurballe","Mesquer","Mouzillon","Nort-sur-Erdre","Piriac-sur-Mer","Pontchâteau","Préfailles","Saint-Brevin-les-Pins","Saint-Joachim","Saint-Lyphard","Saint-Malo-de-Guersac","Saint-Mars-du-Désert","Saint-Michel-Chef-Chef","Saint-Molf","Savenay","Sucé-sur-Erdre","Treillières","Vigneux-de-Bretagne","Amilly","Andonville","Autruy-sur-Juine","Boisseaux","Bou","Cepoy","Châlette-sur-Loing","Chanteau","Conflans-sur-Loing","Corquilleroy","Desmonts","Erceville","LaFerté-Saint-Aubin","Malesherbes","Marigny-les-Usages","Montargis","Morville-en-Beauce","Orville","Pannecières","Pannes","Paucourt","Rouvres-Saint-Jean","Thignonville","Villemandeur","Vimory","Agen","Boé","Bon-Encontre","Brax","Castelculier","Colayrac-Saint-Cirq","Estillac","Foulayronnes","Lafox","LePassage","Pont-du-Casse","Roquefort","Saint-Hilaire-de-Lusignan","Saint-Pierre-de-Clairac","Avrillé","Beaucouzé","Béhuard","Bouchemaine","Briollay","Cantenay-Épinard","Chanteloup-les-Bois","Cholet","Écouflant","Feneu","Juigné-sur-Loire","LaMeignanne","LaMembrolle-sur-Longuenée","LaRomagne","LaSéguinière","LaTessoualle","LeMay-sur-Èvre","LePlessis-Grammoire","LePlessis-Macé","LesPonts-de-Cé","Mazières-en-Mauges","Montreuil-Juigné","Mûrs-Erigné","Nuaillé","Pellouailles-les-Vignes","Saint-Barthélemy-d'Anjou","Saint-Christophe-du-Bois","Saint-Clément-de-la-Place","Sainte-Gemmes-sur-Loire","Saint-Jean-de-Linières","Saint-Lambert-la-Potherie","Saint-Léger-des-Bois","Saint-Léger-sous-Cholet","Saint-Martin-du-Fouilloux","Saint-Sylvain-d'Anjou","Sarrigné","Savennières","Soucelles","Soulaines-sur-Aubance","Toutlemonde","Trélazé","Trémentines","Vezins","Villevêque","Agneaux","Bréville-sur-Mer","Carolles","Cherbourg-Octeville","Donville-les-Bains","Équeurdreville-Hainneville","Granville","Jullouville","LaGlacerie","Longueville","Martinvast","Querqueville","Saint-Georges-Montcocq","Saint-Lô","Saint-Pair-sur-Mer","Tollevast","Tourlaville","Yquelon","Ay","Châlons-en-Champagne","Compertrix","Coolus","Dizy","Épernay","Fagnières","LeVézier","L'Épine","Magenta","Mardeuil","Mareuil-sur-Ay","Moncetz-Longevas","Moussy","Pierry","Recy","Réveillon","Saint-Étienne-au-Temple","Saint-Gibrien","Saint-Martin-sur-le-Pré","Saint-Memmie","Sarry","Villeneuve-la-Lionne","Vinay","Witry-lès-Reims","Bonchamp-lès-Laval","Changé","Laval","L'Huisserie","Louverné","Saint-Berthevin","Art-sur-Meurthe","Auboué","Bainville-sur-Madon","Belleville","Blénod-lès-Pont-à-Mousson","Bouxières-aux-Dames","Briey","Chaligny","Champigneulles","Chanteheux","Chavigny","Cosnes-et-Romain","Custines","Dieulouard","Dombasle-sur-Meurthe","Dommartemont","Dommartin-lès-Toul","Écrouves","Essey-lès-Nancy","Eulmont","Fléville-devant-Nancy","Frouard","Gondreville","Gorcy","Haucourt-Moulaine","Heillecourt","Herserange","Homécourt","Houdemont","Hussigny-Godbrange","Jarville-la-Malgrange","Joeuf","Laneuveville-devant-Nancy","Lay-Saint-Christophe","Lexy","Liverdun","Longlaville","Longwy","Ludres","Lunéville","Maidières","Malleloy","Malzéville","Marbache","Messein","Mexy","Montauville","Mont-Saint-Martin","Moutiers","Neuves-Maisons","Pompey","Pont-à-Mousson","Pont-Saint-Vincent","Pulnoy","Réhon","Rosières-aux-Salines","Saint-Ail","Saint-Nicolas-de-Port","Saulnes","Saulxures-lès-Nancy","Seichamps","Thil","Tomblaine","Toul","Varangéville","Villerupt","Arradon","Arzon","Auray","Baden","Bono",
        "Brandérion","Brech","Camoël","Carnac","Caudan","Cléguer","Crach","Elven","Férel","Gâvres","Gestel","Groix","Guidel","Hennebont","Île-aux-Moines","Île-d'Arz","Île-d'Houat","Inzinzac-Lochrist","LaTrinité-sur-Mer","LaTrinité-Surzur","Lanester","Languidic","Larmor-Baden","Larmor-Plage","LeHézo","Locmariaquer","Locmiquélic","Lorient","Meucon","Monterblanc","Noyalo","Pénestin","Plescop","Ploemeur","Ploeren","Plougoumelen","Plouharnel","Pluneret","Pont-Scorff","Port-Louis","Quéven","Quiberon","Riantec","Saint-Armel","Saint-Avé","Saint-Gildas-de-Rhuys","Saint-Nolff","Saint-Philibert","Saint-Pierre-Quiberon","Sarzeau","Séné","Sulniac","Surzur","Theix","Trédion","Treffléan","Vannes","Achen","Algrange","Alsting","Altviller","Amanvillers","Amnéville","Ancy-sur-Moselle","Angevillers","Apach","Ars-Laquenexy","Ars-sur-Moselle","Audun-le-Tiche","Augny","Aumetz","Ay-sur-Moselle","Basse-Ham","Behren-lès-Forbach","Béning-lès-Saint-Avold","Bertrange","Betting","Bliesbruck","Blies-Ébersing","Blies-Guersviller","Boulange","Bousbach","Bousse","Bronvaux","Carling","Châtel-Saint-Germain","Chieulles","Clouange","Cocheren","Coin-lès-Cuvry","Coin-sur-Seille","Creutzwald","Cuvry","Diebling","Diesen","Dornot","Ennery","Ernestviller","Etting","Etzling","Falck","Fameck","Farébersviller","Farschviller","Fèves","Féy","Florange","Folkling","Folschviller","Fontoy","Forbach","Frauenberg","Freyming-Merlebach","Gandrange","Gravelotte","Grosbliederstroff","Grundviller","Guebenhouse","Guénange","Guenviller","Hagondange","Hambach","Ham-sous-Varsberg","Hargarten-aux-Mines","Hauconcourt","Havange","Hayange","Henriville","Hettange-Grande","Hombourg-Haut","Hundling","Illange","Ippling","Jouy-aux-Arches","Jussy","Kalhausen","Kerbach","Knutange","Kuntzig","LaMaxe","Lachambre","Laquenexy","Laudrefang","LeBan-Saint-Martin","Lessy","L'Hôpital","Lixing-lès-Rouhling","Lommerange","Longeville-lès-Metz","Longeville-lès-Saint-Avold","Lorry-lès-Metz","Loupershouse","Macheren","Maizières-lès-Metz","Manom","Marange-Silvange","Marieulles","Metzing","Mey","Mondelange","Montois-la-Montagne","Morsbach","Moulins-lès-Metz","Moyeuvre-Grande","Moyeuvre-Petite","Neufchef","Neufgrange","Nilvange","Noisseville","Norroy-le-Veneur","Nouilly","Nousseviller-Saint-Nabor","Novéant-sur-Moselle","OEting","Ottange","Peltre","Petite-Rosselle","Pierrevillers","Plappeville","Plesnois","Porcelette","Pouilly","Pournoy-la-Chétive","Puttelange-aux-Lacs","Ranguevaux","Rédange","Rémelfing","Rettel","Richemont","Rochonvillers","Rombas","Roncourt","Rosbruck","Rosselange","Rouhling","Rozérieulles","Russange","Rustroff","Saint-Avold","Sainte-Marie-aux-Chênes","Sainte-Ruffine","Saint-Julien-lès-Metz","Saint-Privat-la-Montagne","Sarralbe","Sarreguemines","Sarreinsming","Saulny","Schmittviller","Schoeneck","Scy-Chazelles","Seingbouse","Semécourt","Serémange-Erzange","Sierck-les-Bains","Spicheren","Stiring-Wendel","Talange","Tenteling","Terville","Théding","Thionville","Trémery","Tressange","Uckange","Valmont","Vantoux","Vany","Varsberg","Vaux","Vernéville","Vitry-sur-Orne","Volmerange-les-Mines","Wiesviller","Willerwald","Wittring","Woelfling-lès-Sarreguemines","Woustviller","Yutz","Zetting","Challuy","Coulanges-lès-Nevers","Fourchambault","Garchizy","Germigny-sur-Loire","Nevers","Pougues-les-Eaux","Saincaize-Meauce","Sermoise-sur-Loire","Varennes-Vauzelles","Abscon","Allennes-les-Marais","Anhiers","Aniche","Annoeullin","Anzin","Arleux","Armbouts-Cappel","Artres","Assevent","Attiches","Auberchicourt","Aubers","Aubigny-au-Bac","Aubry-du-Hainaut","Auby","Aulnoye-Aymeries","Aulnoy-lez-Valenciennes","Avelin","Avesnes-le-Sec","Awoingt","Bachant","Bachy","Bauvin","Beaucamps-Ligny","Bellaing","Bergues","Bersée","Beuvrages","Bierne","Bois-Grenier","Bouchain","Bourbourg","Boussières-sur-Sambre","Boussois","Bray-Dunes","Bruay-sur-l'Escaut","Bruille-lez-Marchiennes","Bruille-Saint-Amand","Brunémont","Bugnicourt","Cambrai","Camphin-en-Carembault","Camphin-en-Pévèle","Cantin","Cappelle-en-Pévèle","Cappelle-la-Grande","Carnin","Cerfontaine","Château-l'Abbaye","Chemy","Cobrieux","Colleret","Condé-sur-l'Escaut","Coudekerque-Branche","Coudekerque-Village","Courchelettes","Craywick","Crespin","Cuincy","Curgies","Dechy","Denain","Deûlémont","Don","Douchy-les-Mines","Dunkerque","Écaillon","Éclaibes","Élesmes","Émerchicourt","Ennetières-en-Weppes","Ennevelin","Erchin","Erquinghem-le-Sec","Erre","Escaudain","Escaudoeuvres","Escautpont","Escobecques","Esquerchin","Estrées","Estreux","Famars","Faumont","Féchain","Feignies","Fenain","Férin","Ferrière-la-Grande","Ferrière-la-Petite","Flers-en-Escrebieux","Flines-lès-Mortagne","Flines-lez-Raches","Fournes-en-Weppes","Fresnes-sur-Escaut","Fressain","Fretin","Fromelles","Genech","Ghyvelde","Goeulzin","Gondecourt","Grande-Synthe","Grand-Fort-Philippe","Gravelines","Guesnain","Hamel","Hantay","Hasnon","Haspres","Haulchin","Hautmont","Haveluy","Hazebrouck","Hélesmes","Hergnies","Hérin","Herlies","Herrin","Hordain","Hornaing","Houplin-Ancoisne","Hoymille","Illies","Jeumont","LaBassée","LaNeuville","LaSentinelle","Lallaing","Lambres-lez-Douai","Lauwin-Planque","LeMaisnil","Lecelles","Lécluse","Leffrinckoucke","Leval","Lewarde","Lieu-Saint-Amand","Limont-Fontaine","Loffre","Loon-Plage","Lourches","Louvroil","Maing","Mairieux","Marcq-en-Ostrevent","Marly","Marpent","Marquette-en-Ostrevant","Marquillies","Masny","Mastaing","Maubeuge","Maulde","Mérignies","Merville","Méteren","Millonfosse","Monceau-Saint-Waast","Monchaux-sur-Écaillon","Moncheaux","Monchecourt","Mons-en-Pévèle","Montigny-en-Ostrevent","Mortagne-du-Nord","Mouchin","Neuf-Mesnil","Neuville-Saint-Rémy","Neuville-sur-Escaut","Nivelle","Noyelles-sur-Selle","Obrechies","Odomez","Oisy","Onnaing","Orchies","Ostricourt","Pecquencourt","Péronne-en-Mélantois","Petite-Forêt","Phalempin","Pont-à-Marcq","Pont-sur-Sambre","Préseau","Prouvy","Proville","Provin","Quaëdypre","Quarouble","Quérénaing","Quiévrechain","Râches","Radinghem-en-Weppes","Raillencourt-Sainte-Olle","Raimbeaucourt","Raismes","Recquignies","Rieulay","Roeulx","Rombies-et-Marchipont","Roost-Warendin","Roucourt","Rousies","Rouvignies","Sailly-lez-Cambrai","Sainghin-en-Weppes","Saint-Amand-les-Eaux","Saint-Aybert","Saint-Georges-sur-l'Aa","Saint-Jans-Cappel","Saint-Remy-du-Nord","Saint-Saulve","Salomé","Saultain","Sebourg","Sin-le-Noble","Socx","Somain","Steenwerck","Templeuve","Téteghem","Thiant","Thivencelle","Thumeries","Thun-Saint-Amand","Tilloy-lez-Cambrai","Tourmignies","Trith-Saint-Léger","Verchain-Maugré","Vicq","Vieux-Condé","Vieux-Mesnil","Villers-au-Tertre","Wahagnies","Wallers","Wannehain","Warneton","Wasnes-au-Bac","Wavrechain-sous-Denain","Wavrechain-sous-Faulx","Wavrin","Waziers","Wicres","Zuydcoote","Abbecourt","Acy-en-Multien","Amblainville","Andeville","Anserville","Antilly","Apremont","Auger-Saint-Vincent","Aumont-en-Halatte","Auneuil","Auteuil","Autheuil-en-Valois","AuxMarais","Bachivillers","Bargny","Baron","Beaumont-les-Nonains","Berneuil-en-Bray","Béthancourt-en-Valois","Betz","Boissy-Fresnoy","Boissy-le-Bois","Bonlier","Bonneuil-en-Valois","Borest","Boubiers","Bouconvillers","Bouillancy","Boullarre","Boursonne","Boury-en-Vexin","Boutencourt","Brégy","Cauvigny","Chambors","Chavençon","Chèvreville","Corbeil-Cerf","Courcelles-lès-Gisors","Courteuil","Crouy-en-Thelle","Cuvergnon","Delincourt","Dieudonné","Duvy","Éméville","Énencourt-Léage","Énencourt-le-Sec","Éragny-sur-Epte","Ercuis","Ermenonville","Esches","Étavigny","Ève","Fay-les-Étangs","Feigneux","Flavacourt","Fleurines","Fleury","Fontaine-Chaalis","Fontaine-Saint-Lucien","Fosseuse","Foulangues","Fouquenies","Fresneaux-Montchevreuil",
        "Fresne-Léguillon","Fresnoy-en-Thelle","Fresnoy-la-Rivière","Fresnoy-le-Luat","Frocourt","Gilocourt","Glaignes","Gondreville","Guignecourt","Hadancourt-le-Haut-Clocher","Hardivillers-en-Vexin","Hénonville","Herchies","Hodenc-l'Évêque","Ivors","Ivry-le-Temple","Jaméricourt","Jonquières","Jouy-sous-Thelle","Juvignies","LaHoussoye","LaNeuville-d'Aumont","LaNeuville-Garnier","LaVilleneuve-sous-Thury","Laboissière-en-Thelle","Labosse","Lachapelle-Saint-Pierre","Lagny-le-Sec","Lalande-en-Son","Lattainville","Lavilletertre","LeCoudray-sur-Thelle","LeDéluge","LeMesnil-Théribus","LeMont-Saint-Adrien","LePlessis-Belleville","LeVaumain","LeVauroux","Lévignen","Liancourt-Saint-Pierre","Lierville","Loconville","Lormaison","Maisoncelle-Saint-Pierre","Mareuil-sur-Ourcq","Marolles","Milly-sur-Thérain","Monneville","Montagny-en-Vexin","Montagny-Sainte-Félicité","Montherlant","Montjavoult","Montlognon","Monts","Morangles","Morienval","Mortefontaine","Mortefontaine-en-Thelle","Nanteuil-le-Haudouin","Neufchelles","Neuilly-en-Thelle","Neuville-Bosc","Nivillers","Noailles","Novillers","Ognes","Ormoy-le-Davien","Ormoy-Villers","Orrouy","Parnes","Péroy-les-Gombries","Pierrefitte-en-Beauvaisis","Plailly","Ponchon","Pontarmé","Porcheux","Pouilly","Puiseux-en-Bray","Puiseux-le-Hauberger","Rainvillers","Réez-Fosse-Martin","Reilly","Ressons-l'Abbaye","Rochy-Condé","Rocquemont","Rosières","Rosoy-en-Multien","Rouville","Rouvres-en-Multien","Russy-Bémont","Saint-Crépin-Ibouvillers","Sainte-Geneviève","Saint-Germain-la-Poterie","Saint-Jean-aux-Bois","Saint-Léger-en-Bray","Saint-Martin-le-Nud","Saint-Maximin","Saint-Paul","Saint-Pierre-es-Champs","Saint-Sauveur","Saint-Sulpice","Savignies","Senots","Serans","Sérifontaine","Séry-Magneval","Silly-le-Long","Silly-Tillard","Talmontiers","Therdonne","Thibivillers","Thiers-sur-Thève","Thury-en-Valois","Tourly","Troissereux","Trumilly","Ully-Saint-Georges","Valdampierre","Varinfroy","Vauciennes","Vaudancourt","Vaumoise","Verderel-lès-Sauqueuse","Versigny","Ver-sur-Launette","Vez","Vieux-Moulin","Villeneuve-les-Sablons","Villers-Saint-Genest","Villers-sur-Trie","Villotran","Warluis","Ablain-Saint-Nazaire","Acheville","Achicourt","Agny","Aire-sur-la-Lys","Aix-Noulette","Allouagne","Angres","Annay","Annequin","Annezin","Anzin-Saint-Aubin","Arques","Arras","Athies","Auchel","Auchy-les-Mines","Avion","Bailleul-Sir-Berthoult","Baincthun","Bajus","Barlin","Beaumetz-lès-Loges","Beaurains","Bénifontaine","Berck","Beugin","Beuvry","Billy-Berclau","Billy-Montigny","Blendecques","Bois-Bernard","Boulogne-sur-Mer","Bouvigny-Boyeffles","Brebières","Bruay-la-Buissière","Bully-les-Mines","Burbure","Calais","Calonne-Ricouart","Camblain-Châtelain","Cambrin","Camiers","Campagne-lès-Wardrecques","Carency","Carvin","Cauchy-à-la-Tour","Caucourt","Chocques","Clairmarais","Condette","Conteville-lès-Boulogne","Coquelles","Corbehem","Coulogne","Courcelles-lès-Lens","Courrières","Cucq","Cuinchy","Dainville","Dannes","Diéval","Divion","Dourges","Douvrin","Drocourt","Drouvin-le-Marais","Duisans","Echinghen","Ecquedecques","Éleu-dit-Leauwette","Éperlecques","Équihen-Plage","Essars","Estevelles","Estrée-Cauchy","Étaples","Étrun","Évin-Malmaison","Fampoux","Farbus","Festubert","Feuchy","Fouquereuil","Fouquières-lès-Béthune","Fouquières-lès-Lens","Fresnicourt-le-Dolmen","Fréthun","Gauchin-Légal","Gavrelle","Givenchy-en-Gohelle","Givenchy-lès-la-Bassée","Gonnehem","Gosnay","Gouy-Servins","Grenay","Guînes","Haillicourt","Haisnes","Hallines","Hames-Boucres","Harnes","Helfaut","Hénin-Beaumont","Hermin","Hersin-Coupigny","Hesdigneul-lès-Béthune","Hesdigneul-lès-Boulogne","Hesdin-l'Abbé","Hinges","Houchin","Houdain","Houlle","Hulluch","Isbergues","Isques","LaCapelle-lès-Boulogne","LaComté","LaCouture","Labeuvrière","Labourse","Lapugnoy","LePortel","LeTouquet-Paris-Plage","Leforest","Libercourt","Liévin","Lillers","Locon","Loison-sous-Lens","Longuenesse","Loos-en-Gohelle","Lorgies","Lozinghem","Maisnil-lès-Ruitz","Marck","Marles-les-Mines","Maroeuil","Mazingarbe","Mercatel","Méricourt","Merlimont","Meurchin","Monchy-le-Preux","Montigny-en-Gohelle","Moringhem","Moulle","Nesles","Neufchâtel-Hardelot","Neuve-Chapelle","Neuville-Vitasse","Noeux-les-Mines","Noyelles-Godault","Noyelles-lès-Vermelles","Noyelles-sous-Lens","Oblinghem","Oignies","Ourton","Outreau","Oye-Plage","Pernes-lès-Boulogne","Pittefaux","Pont-à-Vendin","Rang-du-Fliers","Rebreuve-Ranchicourt","Richebourg","Rouvroy","Ruitz","Sailly-Labourse","Sains-en-Gohelle","Sainte-Catherine","Saint-Étienne-au-Mont","Saint-Laurent-Blangy","Saint-Léonard","Saint-Martin-au-Laërt","Saint-Martin-Boulogne","Saint-Nicolas","Saint-Omer","Sallaumines","Salperwick","Sangatte","Serques","Servins","Souchez","Tatinghem","Thélus","Tilloy-lès-Mofflaines","Tilques","Vaudricourt","Vendin-lès-Béthune","Vendin-le-Vieil","Vermelles","Verquigneul","Verquin","Verton","Vieille-Chapelle","Villers-au-Bois","Vimy","Violaines","Vitry-en-Artois","Wailly","Wancourt","Wardrecques","Willerval","Wimereux","Wimille","Wingles","Wizernes","Aubière","Aulnat","Beaumont","Blanzat","Cébazat","Ceyrat","Châteaugay","Châtel-Guyon","Cournon-d'Auvergne","Durtol","Enval","Gerzat","LeCendre","Lempdes","Marsat","Ménétrol","Mozac","Nohanent","Pérignat-lès-Sarliève","Pont-du-Château","Riom","Romagnat","Royat","Andoins","Angaïs","Arbus","Aressy","Arros-de-Nay","Artiguelouve","Assat","Aussevielle","Baliros","Baudreix","Bénéjacq","Billère","Bizanos","Boeil-Bezing","Bordères","Bordes","Bourdettes","Briscous","Buros","Cambo-les-Bains","Coarraze","Denguin","Gabaston","Gan","Gelos","Halsou","Hasparren","Idron","Igon","Jurançon","Lagos","Laroin","Larressore","Lée","Lescar","Lons","Maucor","Mazères-Lezons","Meillon","Mirepeix","Montardon","Morlaàs","Narcastet","Navailles-Angos","Nay","Ousse","Pardies-Piétat","Pau","Poey-de-Lescar","Rontignon","Saint-Abit","Saint-Jammes","Saint-Pée-sur-Nivelle","Sauvagnon","Sendets","Serres-Castet","Serres-Morlaàs","Siros","Urt","Uzos","Aureilhan","Barbazan-Debat","Bordères-sur-l'Échez","Bours","Chis","Horgues","Laloubère","Momères","Odos","Orleix","Sarrouilles","Séméac","Soues","Tarbes","Alénya","Bages","Baho","Baixas","Banyuls-sur-Mer","Bompas","Cabestany","Canohès","Cerbère","Céret","Claira","Collioure","Corneilla-del-Vercol","Espira-de-l'Agly","LeBoulou","LeSoler","Millas","Montescot","Palau-del-Vidre","Peyrestortes","Pézilla-la-Rivière","Pia","Pollestres","Port-Vendres","Rivesaltes","Saint-André","Sainte-Marie","Saint-Estève","Saint-Féliu-d'Amont","Saint-Féliu-d'Avall","Saint-Hippolyte","Saint-Nazaire","Saleilles","Théza","Thuir","Torreilles","Toulouges","Villelongue-de-la-Salanque","Villeneuve-la-Rivière","Altorf","Avolsheim","Baldenheim","Barr","Benfeld","Bernardswiller","Bilwisheim","Bischoffsheim","Bischwiller","Blaesheim","Boersch","Châtenois","Dachstein","Dahlenheim","Dieffenthal","Dinsheim-sur-Bruche","Donnenheim","Dorlisheim","Drusenheim","Duppigheim","Duttlenheim","Ebersheim","Ebersmunster","Eckwersheim","Ergersheim","Ernolsheim-Bruche","Erstein","Gambsheim","Gertwiller","Grendelbruch","Gresswiller","Griesheim-près-Molsheim","Haguenau","Hoerdt","Innenheim","Kaltenhouse","Kilstett","Kintzheim","Kirchheim","Krautergersheim","Kriegsheim","LaVancelle","Marckolsheim","Marlenheim","Meistratzheim","Mittelschaeffolsheim","Mollkirch","Molsheim","Mommenheim","Mussig","Muttersholtz","Mutzig","Niedernai","Oberhoffen-sur-Moder","Odratzheim","Offendorf","Ohlungen","Olwisheim","Orschwiller","Ottrott","Rosenwiller","Rosheim","Rottelsheim","Saint-Nabor","Scharrachbergheim-Irmstett","Scherwiller","Schweighouse-sur-Moder","Sélestat","Seltz","Siltzheim","Soultz-les-Bains",
        "Wangen","Wasselonne","Wissembourg","Wolxheim","Aubure","Baldersheim","Bartenheim","Beblenheim","Bennwihr","Bergheim","Berrwiller","Bitschwiller-lès-Thann","Blotzheim","Bollwiller","Brunstatt","Buhl","Buschwiller","Cernay","Colmar","Dannemarie","Didenheim","Ensisheim","Feldkirch","Guebwiller","Guémar","Habsheim","Hégenheim","Herrlisheim-près-Colmar","Hésingue","Horbourg-Wihr","Houssen","Hunawihr","Illhaeusern","Illzach","Ingersheim","Issenheim","Jebsheim","Kaysersberg","Kembs","Kingersheim","Lautenbach","Lautenbachzell","Leimbach","Linthal","Lutterbach","Mittelwihr","Morschwiller-le-Bas","Munster","Ostheim","Pfastatt","Pulversheim","Reiningue","Ribeauvillé","Richwiller","Riedisheim","Riquewihr","Rixheim","Rodern","Rorschwihr","Rosenau","Rouffach","Ruelisheim","Sainte-Croix-en-Plaine","Saint-Hippolyte","Sausheim","Sierentz","Soultz-Haut-Rhin","Staffelfelden","Steinbach","Sundhoffen","Thann","Thannenkirch","Turckheim","Uffholtz","Ungersheim","Vieux-Thann","Village-Neuf","Wattwiller","Wettolsheim","Willer-sur-Thur","Wintzenheim","Wittelsheim","Wittenheim","Zellenberg","Zillisheim","Ampuis","Condrieu","Fleurieux-sur-l'Arbresle","Saint-Cyr-sur-le-Rhône","Sainte-Colombe","Saint-Romain-en-Gal","Tupin-et-Semons","Châlonvillars","Héricourt","Chalon-sur-Saône","Champforgeuil","Charnay-lès-Mâcon","Châtenoy-en-Bresse","Châtenoy-le-Royal","Chevagny-les-Chevrières","Crissey","Fragnes","Hurigny","LaLoyère","Lux","Mâcon","Oslon","Saint-Marcel","Saint-Rémy","Sancé","Varennes-lès-Mâcon","Vinzelles","Aigné","Allonnes","Arnage","Champagné","Changé","Coulaines","Guécélard","LaChapelle-Saint-Aubin","LaMilesse","Laigné-en-Belin","LeMans","Moncé-en-Belin","Mulsanne","Rouillon","Ruaudin","Saint-Gervais-en-Belin","Saint-Pavace","Saint-Saturnin","Sargé-lès-le-Mans","Teloché","Yvré-l'Évêque","Albens","Allondaz","Bourdeau","LaChapelle-du-Mont-du-Chat","Marthod","Montcel","Montmélian","Ontex","Saint-Offenge-Dessous","Saint-Offenge-Dessus","Thénésol","Trévignin","Ugine","Allèves","Aviernoz","Bernex","Bluffy","Boëge","Bogève","Brenthonne","Brizon","Burdignin","Cervens","Chainaz-les-Frasses","Champanges","Chapeiry","Chaumont","Chavannaz","Chevenoz","Chilly","Clarafond-Arcine","Contamine-Sarzin","Cusy","Draillant","Duingt","Éloise","Entrevernes","Étercy","Évires","Fessy","Féternes","Gruffy","Habère-Lullin","Habère-Poche","Hauteville-sur-Fier","Héry-sur-Alby","LaChapelle-Saint-Maurice","LaForclaz","LaRivière-Enverse","LaTour","LaVernaz","Lathuile","LeReposoir","LesOllières","LesVillards-sur-Thônes","Leschaux","Lugrin","Lully","Lyaud","Magland","Marcellaz-Albanais","Marlioz","Maxilly-sur-Léman","Mégevette","Meillerie","Menthonnex-sous-Clermont","Mésigny","Minzier","Mont-Saxonnex","Mûres","Nancy-sur-Cluses","Nâves-Parmelan","Nonglard","Orcier","Passy","Peillonnex","Perrignier","Reyvroz","Saint-André-de-Boëge","Saint-Eusèbe","Saint-Eustache","Saint-Gingolph","Saint-Jean-de-Tholome","Saint-Paul-en-Chablais","Saint-Sigismond","Saint-Sylvestre","Sallenôves","Saxel","Servoz","Thollon-les-Mémises","Thorens-Glières","Thusy","Vacheresse","Vailly","Vaulx","Villard","Ville-en-Sallaz","Vinzier","Viuz-en-Sallaz","Viuz-la-Chiésaz","Arques-la-Bataille","Barentin","Bolbec","Criquebeuf-en-Caux","Dieppe","Eu","Fécamp","Flocques","Gouy","Hautot-sur-Seine","Houppeville","Incheville","LaBouille","LaNeuville-Chant-d'Oisel","LeTréport","LesAuthieux-sur-le-Port-Saint-Ouen","Lillebonne","Mannevillette","Martin-Église","Montmain","Notre-Dame-de-Gravenchon","Offranville","Pavilly","Ponts-et-Marais","Quévreville-la-Poterie","Rogerville","Roncherolles-sur-le-Vivier","Rouxmesnil-Bouteilles","Sahurs","Saint-Aubin-Celloville","Saint-Aubin-sur-Scie","Saint-Jacques-sur-Darnétal","Saint-Léonard","Saint-Pierre-de-Manneville","Villers-Écalles","Ymare","Yport","Achères-la-Forêt","Amillis","Amponville","Andrezel","Arbonne-la-Forêt","Argentières","Armentières-en-Brie","Arville","Aubepierre-Ozouer-le-Repos","Aufferville","Augers-en-Brie","Aulnoy","Baby","Balloy","Bannost-Villegagnon","Barbey","Barcy","Bassevelle","Bazoches-lès-Bray","Beauchery-Saint-Martin","Beaumont-du-Gâtinais","Beautheil","Beauvoir","Bellot","Bernay-Vilbert","Beton-Bazoches","Bezalles","Blandy","Blennes","Boisdon","Boissy-aux-Cailles","Boissy-le-Châtel","Boitron","Bombon","Bougligny","Boulancourt","Bouleurs","Bourron-Marlotte","Boutigny","Bransles","Bray-sur-Seine","Bréau","Burcy","Bussières","Buthiers","Cerneux","Cessoy-en-Montois","Chailly-en-Brie","Chaintreaux","Chalautre-la-Grande","Chalautre-la-Petite","Chalmaison","Chambry","Champcenest","Champdeuil","Champeaux","Changis-sur-Marne","Charmentray","Charny","Chartronges","Châteaubleau","Château-Landon","Châtenay-sur-Seine","Châtenoy","Châtillon-la-Borde","Châtres","Chauffry","Chaumes-en-Brie","Chenoise","Chenou","Chevrainvilliers","Chevru","Chevry-en-Sereine","Choisy-en-Brie","Citry","Clos-Fontaine","Cocherel","Compans","Congis-sur-Thérouanne","Coubert","Coulombs-en-Valois","Coulommes","Courcelles-en-Bassée","Courchamp","Courpalay","Courquetaine","Courtacon","Courtomer","Coutençon","Crèvecur-en-Brie","Crisenoy","Crouy-sur-Ourcq","Cucharmoy","Cuisy","Dagny","Dammartin-sur-Tigeaux","Dhuisy","Diant","Donnemarie-Dontilly","Dormelles","Doue","Douy-la-Ramée","Échouboulains","Égligny","Égreville","Épisy","Esmans","Étrépilly","Everly","Évry-Grégy-sur-Yerre","Favières","Faÿ-lès-Nemours","Féricy","Flagy","Fontaine-Fourches","Fontains","Fontenailles","Fontenay-Trésigny","Forfry","Forges","Fouju","Fresnes-sur-Marne","Frétoy","Fromont","Fublaines","Garentreville","Gastins","Germigny-l'Évêque","Germigny-sous-Coulombs","Gesvres-le-Chapitre","Giremoutiers","Gironville","Gouaix","Grandpuits-Bailly-Carrois","Gravon","Gressy","Grez-sur-Loing","Grisy-Suisnes","Grisy-sur-Seine","Guérard","Guercheville","Guignes","Gurcy-le-Châtel","Hautefeuille","Hermé","Hondevilliers","Ichy","Isles-les-Meldeuses","Iverny","Jablines","Jaignes","Jaulnes","Jouy-le-Châtel","Jouy-sur-Morin","Juilly","Jutigny","LaBrosse-Montceaux","LaChapelle-Gauthier","LaChapelle-Iger","LaChapelle-la-Reine","LaChapelle-Moutils","LaChapelle-Rablais","LaChapelle-Saint-Sulpice","LaCroix-en-Brie","LaFerté-Gaucher","LaGenevraye","LaGrande-Paroisse","LaHaute-Maison","LaHoussaye-en-Brie","LaMadeleine-sur-Loing","LaTombe","LaTrétoire","Larchant","Laval-en-Brie","LeChâtelet-en-Brie","LeMesnil-Amelot","LePlessis-aux-Bois","LePlessis-Feu-Aussoux","LePlessis-l'Évêque","LePlessis-Placy","LeVaudoué","Léchelle","LesChapelles-Bourbon","LesÉcrennes","LesMarêts","LesOrmes-sur-Voulzie","Lescherolles","Lesches","Leudon-en-Brie","Limoges-Fourches","Lissy","Liverdy-en-Brie","Lizines","Lizy-sur-Ourcq","Longueville","Lorrez-le-Bocage-Préaux","Louan-Villegruis-Fontaine","Luisetaines","Lumigny-Nesles-Ormeaux","Luzancy","Machault","Maincy","Maisoncelles-en-Brie","Maisoncelles-en-Gâtinais","Maison-Rouge","Marchémoret","Marcilly","Marles-en-Brie","Marolles-en-Brie","Marolles-sur-Seine","Mary-sur-Marne","Mauperthuis","Mauregard","May-en-Multien","Meigneux","Meilleray","Melz-sur-Seine","Méry-sur-Marne","Messy","Misy-sur-Yonne","Moisenay","Mondreville","Mons-en-Montois","Montarlot","Montceaux-lès-Meaux","Montceaux-lès-Provins","Montcourt-Fromonville","Montdauphin","Montenils","Montereau-sur-le-Jard","Montgé-en-Goële","Monthyon","Montigny-le-Guesdier","Montigny-Lencoup","Montigny-sur-Loing","Montmachoux","Montolivet","Mormant","Mortcerf","Mortery","Mousseaux-lès-Bray","Moussy-le-Vieux","Mouy-sur-Seine","Nanteau-sur-Essonne","Nanteau-sur-Lunain","Nanteuil-sur-Marne","Nantouillet","Neufmoutiers-en-Brie","Noisy-Rudignon","Noisy-sur-École","Nonville","Noyen-sur-Seine","Obsonville","Ocquerre","Oissery","Orly-sur-Morin",
        "Ormesson","Ozouer-le-Voulgis","Paley","Pamfou","Paroy","Passy-sur-Seine","Pécy","Penchard","Pézarches","Pierre-Levée","Poigny","Poligny","Précy-sur-Marne","Presles-en-Brie","Puisieux","Quiers","Rampillon","Rebais","Recloses","Remauville","Rouvres","Rozay-en-Brie","Rumont","Rupéreux","Saâcy-sur-Marne","Sablonnières","Saint-Ange-le-Viel","Saint-Augustin","Saint-Barthélemy","Saint-Cyr-sur-Morin","Saint-Denis-lès-Rebais","Sainte-Aulde","Sainte-Colombe","Saint-Fiacre","Saint-Germain-Laxis","Saint-Germain-sous-Doue","Saint-Hilliers","Saint-Jean-les-Deux-Jumeaux","Saint-Just-en-Brie","Saint-Léger","Saint-Loup-de-Naud","Saint-Mard","Saint-Mars-Vieux-Maisons","Saint-Martin-des-Champs","Saint-Martin-du-Boschet","Saint-Méry","Saint-Mesmes","Saint-Ouen-en-Brie","Saint-Ouen-sur-Morin","Saint-Pathus","Saint-Rémy-la-Vanne","Saints","Saint-Sauveur-lès-Bray","Saint-Siméon","Saint-Soupplets","Salins","Sammeron","Sancy","Sancy-lès-Provins","Savins","Sept-Sorts","Signy-Signets","Sigy","Sivry-Courtry","Sognolles-en-Montois","Soignolles-en-Brie","Soisy-Bouy","Solers","Souppes-sur-Loing","Sourdun","Tancrou","Thénisy","Thieux","Thoury-Férottes","Tigeaux","Touquin","Tousson","Treuzy-Levelay","Trilbardou","Trocy-en-Multien","Ury","Ussy-sur-Marne","Valence-en-Brie","Vanvillé","Varreddes","Vaucourtois","Vaudoy-en-Brie","Vaux-sur-Lunain","Vendrest","Verdelot","Verneuil-l'Étang","Vieux-Champagne","Vignely","Villebéon","Villecerf","Villemaréchal","Villemareuil","Villemer","Villenauxe-la-Petite","Villeneuve-le-Comte","Villeneuve-les-Bordes","Villeneuve-Saint-Denis","Villeneuve-sous-Dammartin","Villeneuve-sur-Bellot","Villeroy","Ville-Saint-Jacques","Villiers-Saint-Georges","Villiers-sous-Grez","Villiers-sur-Seine","Villuis","Vimpelles","Vinantes","Vincy-Manœuvre","Voinsles","Voulton","Voulx","Vulaines-lès-Provins","Yèbles","Ablis","Adainville","Allainville","Andelu","Arnouville-lès-Mantes","Auteuil","Autouillet","Bazainville","Béhoust","Blaru","Boinville-en-Mantois","Boinville-le-Gaillard","Boinvilliers","Boissets","Boissy-sans-Avoir","Bonnelles","Bourdonné","Bréval","Bullion","Chaufour-lès-Bonnières","Civry-la-Forêt","Clairefontaine-en-Yvelines","Condé-sur-Vesgre","Courgent","Cravent","Dammartin-en-Serve","Dannemarie","Flacourt","Flexanville","Flins-Neuve-Église","Galluis","Gambais","Gambaiseuil","Garancières","Gommecourt","Goupillières","Goussonville","Grandchamp","Gressey","Grosrouvre","Hargeville","Herbeville","Hermeray","Jeufosse","Jumeauville","LaBoissière-École","LaCelle-les-Bordes","LaHauteville","LaQueue-les-Yvelines","LaVilleneuve-en-Chevrie","Lainville-en-Vexin","LeTartre-Gaudran","LeTertre-Saint-Denis","LesBréviaires","Lommoye","Longnes","Longvilliers","Marcq","Mareil-sur-Mauldre","Maulette","Millemont","Mittainville","Moisson","Mondreville","Montainville","Montalet-le-Bois","Montchauvet","Mulcent","Neauphlette","Orcemont","Orgerus","Orphin","Orsonville","Orvilliers","Osmoy","Paray-Douaville","Poigny-la-Forêt","Ponthévrard","Port-Villez","Prunay-en-Yvelines","Prunay-le-Temple","Richebourg","Rochefort-en-Yvelines","Rosay","Sailly","Saint-Arnoult-en-Yvelines","Sainte-Mesme","Saint-Illiers-la-Ville","Saint-Illiers-le-Bois","Saint-Léger-en-Yvelines","Saint-Martin-de-Bréthencourt","Saint-Martin-des-Champs","Septeuil","Sonchamp","Tacoignières","Thoiry","Tilly","Vieille-Église-en-Yvelines","Villette","Villiers-le-Mahieu","Aiffres","Chauray","Niort","Abbeville","Allonville","Beauchamps","Bertangles","Blangy-Tronville","Bouvaincourt-sur-Bresle","Bovelles","Caours","Clairy-Saulchoix","Creuse","Drucat","Estrées-sur-Noye","Glisy","Grand-Laviers","Grattepanche","Guignemicourt","Hébécourt","Mareuil-Caubert","Mers-les-Bains","Oust-Marest","Pissy","Poulainville","Remiencourt","Revelles","Rumigny","Sains-en-Amiénois","Saint-Fuscien","Saint-Sauflieu","Saveuse","Thézy-Glimont","Vers-sur-Selles","Albi","Arthès","Burlats","Cambon","Cambounet-sur-le-Sor","Castelnau-de-Lévis","Castres","Cunac","LeSequestre","Lescure-d'Albigeois","Marssac-sur-Tarn","Puygouzon","Roquecourbe","Saint-Juéry","Saïx","Terssac","Viviers-lès-Montagnes","","Bressols","Corbarieu","Lacourt-Saint-Pierre","Léojac","Montauban","Montbeton","Saint-Étienne-de-Tulmont","Saint-Nauphary","Villemade","Bagnols-en-Forêt","Besse-sur-Issole","Callas","Camps-la-Source","Carnoules","Collobrières","Flassans-sur-Issole","Forcalqueiret","Garéoult","Gonfaron","LaRoquebrussanne","LeThoronet","LesMayons","Méounes-lès-Montrieux","Mons","Néoules","Pignans","Plan-d'Aups-Sainte-Baume","Puget-Ville","Rians","Riboux","Rocbaron","Sainte-Anastasie-sur-Issole","Saint-Paul-en-Forêt","Vinon-sur-Verdon","Crillon-le-Brave","LaRoque-sur-Pernes","LeBeaucet","Maubec","Saint-Hippolyte-le-Graveyron","Saint-Pierre-de-Vassols","Saumane-de-Vaucluse","Vacqueyras","Bretignolles-sur-Mer","Challans","Jard-sur-Mer","LaBarre-de-Monts","LaRoche-sur-Yon","LaTranche-sur-Mer","LeFenouiller","LePerrier","LesHerbiers","L'Île-d'Yeu","Notre-Dame-de-Monts","Notre-Dame-de-Riez","Saint-Hilaire-de-Riez","Saint-Jean-de-Monts","Saint-Vincent-sur-Jard","Sallertaine","Soullans","Talmont-Saint-Hilaire","Béruges","Biard","Buxerolles","Chasseneuil-du-Poitou","Croutelle","Fontaine-le-Comte","Jaunay-Clan","Mignaloux-Beauvoir","Migné-Auxances","Montamisé","Saint-Benoît","Vouneuil-sous-Biard","Boisseuil","Bosmie-l'Aiguille","Chaptelat","Condat-sur-Vienne","Couzeix","Feytiat","Isle","LePalais-sur-Vienne","Rilhac-Rancon","Panazol","Chantraine","Chavelot","Dinozé","Dogneville","Épinal","Girmont","Golbey","Igney","Jeuxey","LesForges","Thaon-les-Vosges","Appoigny","Auxerre","Maillot","Malay-le-Grand","Monéteau","Paron","Saint-Clément","Saint-Georges-sur-Baulche","Saint-Martin-du-Tertre","Sens","Andelnans","Argiésans","Bavilliers","Belfort","Bermont","Botans","Bourogne","Charmois","Châtenois-les-Forges","Chaux","Chèvremont","Cravanche","Danjoutin","Delle","Denney","Dorans","Éloie","Essert","Évette-Salbert","Grandvillars","Joncherey","Lachapelle-sous-Chaux","Meroux","Méziré","Morvillars","Moval","Offemont","Pérouse","Roppe","Sermamagny","Sevenans","Trévenans","Valdoie","Vétrigne","Vézelois","Abbéville-la-Rivière","Angerville","Angervilliers","Arrancourt","Authon-la-Plaine","Blandy","Boigneville","Bois-Herpin","Boissy-la-Rivière","Boissy-le-Cutté","Boissy-le-Sec","Boutervilliers","Bouville","Brouy","Buno-Bonnevaux","Chalo-Saint-Mars","Chalou-Moulineux","Champmotteux","Chatignonville","Chauffour-lès-Étréchy","Congerville-Thionville","Corbreuse","Courances","Dannemois","Estouches","Fontaine-la-Rivière","Gironville-sur-Essonne","Guillerval","LaForêt-le-Roi","LaForêt-Sainte-Croix","LeVal-Saint-Germain","LesGranges-le-Roi","Maisse","Marolles-en-Beauce","Méréville","Mérobert","Mespuits","Milly-la-Forêt","Moigny-sur-École","Mondeville","Monnerville","Oncy-sur-École","Ormoy-la-Rivière","Orveau","Plessis-Saint-Benoist","Prunay-sur-Essonne","Puiselet-le-Marais","Pussay","Richarville","Roinvilliers","Saclas","Saint-Cyr-la-Rivière","Saint-Cyr-sous-Dourdan","Saint-Escobille","Saint-Hilaire","Souzy-la-Briche","Valpuiseaux","Videlles","Villeconin","Villeneuve-sur-Auver","Ambleville","Amenucourt","Arronville","Arthies","Avernes","Banthelu","Bellefontaine","Belloy-en-France","Berville","Bray-et-Lû","Bréançon","Brignancourt","Buhy","Charmont","Chars","Châtenay-en-France","Chaussy","Chérence","Cléry-en-Vexin","Commeny","Cormeilles-en-Vexin","Épiais-Rhus","Épinay-Champlâtreux","Frémécourt","Gadancourt","Genainville","Gouzangrez","Grisy-les-Plâtres","Guiry-en-Vexin","Haravilliers","Haute-Isle","Hodent","Jagny-sous-Bois","LaChapelle-en-Vexin","LaRoche-Guyon","Lassy","LeBellay-en-Vexin","LeHeaulme","LePerchay","LePlessis-Luzarches","Magny-en-Vexin",
        "Mareil-en-France","Marines","Maudétour-en-Vexin","Menouville","Montreuil-sur-Epte","Moussy","Neuilly-en-Vexin","Noisy-sur-Oise","Nucourt","Omerville","Saint-Clair-sur-Epte","Saint-Gervais","Saint-Martin-du-Tertre","Santeuil","Théméricourt","Theuville","Us","Vigny","Villaines-sous-Bois","Villers-en-Arthies","Villiers-le-Sec","Wy-dit-Joli-Village","Ambérieu-en-Bugey","Ars-sur-Formans","Balan","Beauregard","Béligneux","Bellegarde-sur-Valserine","Bourg-en-Bresse","Bressolles","Chézery-Forens","Civrieux","Confort","Frans","Lancrans","Lélex","Massieux","Meximieux","Mijoux","Mionnay","Misérieux","Niévroz","Oyonnax","Parcieux","Péronnas","Pérouges","Pizay","Rancé","Saint-André-de-Corcy","Saint-Bernard","Saint-Denis-lès-Bourg","Saint-Didier-de-Formans","Sainte-Croix","Sainte-Euphémie","Saint-Jean-de-Thurigneux","Saint-Just","Saint-Laurent-sur-Saône","Thil","Toussieux","Tramoyes","Villars-les-Dombes","Viriat","Athies-sous-Laon","Belleu","Bézu-le-Guéry","Blesmes","Brasles","Brumetz","Bussiares","Castres","Chambry","Château-Thierry","Chézy-en-Orxois","Chierry","Contescourt","Corcy","Coupru","Courchamps","Courmelles","Coyolles","Crouttes-sur-Marne","Crouy","Cuffies","Dallon","Dammard","Domptin","Essigny-le-Petit","Essômes-sur-Marne","Étampes-sur-Marne","Fayet","Fieulaine","Fonsomme","Fontaine-Notre-Dame","Gandelu","Gauchy","Grugies","Harly","Hautevesnes","Homblières","LaCelle-sous-Montmirail","LaFerté-Milon","Laon","Largny-sur-Automne","Lesdins","Longpont","Marcy","Marigny-en-Orxois","Mercin-et-Vaux","Mesnil-Saint-Laurent","Monnes","Montigny-l'Allier","Montreuil-aux-Lions","Morcourt","Neuilly-Saint-Front","Neuville-Saint-Amand","Nogentel","Omissy","Passy-en-Valois","Pavant","Priez","Remaucourt","Rouvroy","Saint-Gengoulph","Saint-Quentin","Soissons","Vauxbuin","Veuilly-la-Poterie","Vichel-Nanteuil","Viels-Maisons","Vierzy","Villeneuve-Saint-Germain","Abrest","Bellerive-sur-Allier","Creuzier-le-Neuf","Creuzier-le-Vieux","Cusset","Désertines","Domérat","Hauterive","Lavault-Sainte-Anne","LeVernet","Montluçon","Prémilhat","Quinssaines","Saint-Victor","Saint-Yorre","Serbannes","Vichy"]
        zoneB2 = sorted(zoneB2)
        zoneC = ["L’Abergement-Clémenciat","L’Abergement-de-Varey","Ambérieux-en-Dombes","Ambléon","Ambronay","Ambutrix","Andert-et-Condon","Anglefort","Apremont","Aranc","Arandas","Arbent","Arbignieu","Arbigny","Argis","Armix","Artemare","Asnières-sur-Saône","Attignat","Bâgé-la-Ville","Bâgé-le-Châtel","Baneins","Beaupont","Bellignat","Belley","Belleydoux","Belmont-Luthézieu","Bénonces","Bény","Béon","Béréziat","Bettant","Bey","Billiat","Birieux","Biziat","Blyes","Boissey","Bolozon","Bouligneux","Bourg-Saint-Christophe","Boyeux-Saint-Jérôme","Boz","Brégnier-Cordon","Brénaz","Brénod","Brens","Brion","Briord","Buellas","La Burbanche","Ceignes","Cerdon","Certines","Ceyzériat","Ceyzérieu","Chalamont","Chaleins","Chaley","Challes-la-Montagne","Champagne-en-Valromey","Champdor","Champfromier","Chanay","Chaneins","Chanoz-Châtenay","La Chapelle-du-Châtelard","Charix","Charnoz-sur-Ain","Château-Gaillard","Châtenay","Châtillon-en-Michaille","Châtillon-la-Palud","Châtillon-sur-Chalaronne","Chavannes-sur-Reyssouze","Chavannes-sur-Suran","Chaveyriat","Chavornay","Chazey-Bons","Chazey-sur-Ain","Cheignieu-la-Balme","Chevillard","Chevroux","Cize","Cleyzieu","Coligny","Colomieu","Conand","Condamine","Condeissiat","Confrançon","Contrevoz","Conzieu","Corbonod","Corcelles","Corlier","Cormaranche-en-Bugey","Cormoranche-sur-Saône","Cormoz","Corveissiat","Courmangoux","Courtes","Crans","Cras-sur-Reyssouze","Cressin-Rochefort","Crottet","Cruzilles-lès-Mépillat","Culoz","Curciat-Dongalon","Curtafond","Cuzieu","Dommartin","Dompierre-sur-Veyle","Dompierre-sur-Chalaronne","Domsure","Dortan","Douvres","Drom","Druillat","Échallon","Étrez","Évosges","Faramans","Fareins","Feillens","Flaxieu","Foissiat","Francheleins","Garnerans","Genouilleux","Béard-Géovreissiat","Géovreisset","Germagnat","Giron","Gorrevod","Le Grand-Abergement","Grand-Corent","Grièges","Groissiat","Groslée","Guéreins","Hautecourt-Romanèche","Hauteville-Lompnes","Hostiaz","Hotonnes","Illiat","Injoux-Génissiat","Innimond","Izenave","Izernore","Izieu","Jasseron","Jayat","Journans","Joyeux","Jujurieux","Labalme","Lagnieu","Laiz","Lalleyriat","Lantenay","Lapeyrouse","Lavours","Lent","Lescheroux","Leyment","Leyssard","Lhôpital","Lhuis","Lochieu","Lompnas","Lompnieu","Loyettes","Lurcy","Magnieu","Maillat","Malafretaz","Mantenay-Montlin","Manziat","Marboz","Marchamp","Marignieu","Marlieux","Marsonnas","Martignat","Massignieu-de-Rives","Matafelon-Granges","Meillonnas","Mérignat","Messimy-sur-Saône","Bohas-Meyriat-Rignat","Mézériat","Mogneneins","Montagnat","Montagnieu","Montanges","Montceaux","Montcet","Le Montellier","Monthieux","Montmerle-sur-Saône","Montracol","Montréal-la-Cluse","Montrevel-en-Bresse","Nurieux-Volognat","Murs-et-Gélignieux","Nantua","Nattages","Neuville-les-Dames","Neuville-sur-Ain","Les Neyrolles","Nivollet-Montgriffon","Oncieu","Ordonnaz","Outriaz","Ozan","Parves","Perrex","Le Petit-Abergement","Peyriat","Peyrieu","Peyzieux-sur-Saône","Pirajoux","Plagne","Le Plantay","Le Poizat","Polliat","Pollieu","Poncin","Pont-d’Ain","Pont-de-Vaux","Pont-de-Veyle","Port","Pouillat","Prémeyzel","Prémillieu","Pressiat","Priay","Pugieu","Ramasse","Relevant","Replonges","Revonnas","Reyssouze","Rignieux-le-Franc","Romans","Rossillon","Ruffieu","Saint-Alban","Saint-André-de-Bâgé","Saint-André-d’Huiriat","Saint-André-le-Bouchoux","Saint-André-sur-Vieux-Jonc","Saint-Bénigne","Saint-Benoît","Saint-Bois","Saint-Champ","Saint-Cyr-sur-Menthon","Saint-Denis-en-Bugey","Saint-Didier-d’Aussiat","Saint-Didier-sur-Chalaronne","Saint-Éloi","Saint-Étienne-du-Bois","Saint-Étienne-sur-Chalaronne","Saint-Étienne-sur-Reyssouze","Saint-Genis-sur-Menthon","Saint-Georges-sur-Renon","Saint-Germain-de-Joux","Saint-Germain-les-Paroisses","Saint-Germain-sur-Renon","Saint-Jean-de-Niost","Saint-Jean-le-Vieux","Saint-Jean-sur-Reyssouze","Saint-Jean-sur-Veyle","Sainte-Julie","Saint-Julien-sur-Reyssouze","Saint-Julien-sur-Veyle","Saint-Marcel","Saint-Martin-de-Bavel","Saint-Martin-du-Frêne","Saint-Martin-du-Mont","Saint-Martin-le-Châtel","Saint-Maurice-de-Gourdans","Saint-Maurice-de-Rémens","Saint-Nizier-le-Bouchoux","Saint-Nizier-le-Désert","Sainte-Olive","Saint-Paul-de-Varax","Saint-Rambert-en-Bugey","Saint-Rémy","Saint-Sorlin-en-Bugey","Saint-Sulpice","Saint-Trivier-de-Courtes","Saint-Trivier-sur-Moignans","Saint-Vulbas","Salavre","Samognat","Sandrans","Sault-Brénaz","Savigneux","Seillonnaz","Sermoyer","Serrières-de-Briord","Serrières-sur-Ain","Servas","Servignat","Seyssel","Simandre-sur-Suran","Songieu","Sonthonnax-la-Montagne","Souclin","Sulignat","Surjoux","Sutrieu","Talissieu","Tenay","Thézillieu","Thoissey","Torcieu","Tossiat","La Tranclière","Treffort-Cuisiat","Valeins","Vandeins","Varambon","Vaux-en-Bugey","Verjon","Vernoux","Versailleux","Vescours","Vésines","Vieu-d’Izenave","Vieu","Villebois","Villemotier","Villeneuve","Villereversure","Villes","Villette-sur-Ain","Villieu-Loyes-Mollon","Virieu-le-Grand","Virieu-le-Petit","Virignin","Vongnes","Vonnas","Abbécourt","Achery","Acy","Agnicourt-et-Séchelles","Aguilcourt","Aisonville-et-Bernoville","Aizelles","Aizy-Jouy","Alaincourt","Allemant","Ambleny","Ambrief","Amifontaine","Amigny-Rouy","Ancienville","Andelain","Anguilcourt-le-Sart","Anizy-le-Château","Annois","Any-Martin-Rieux","Archon","Arcy-Sainte-Restitue","Armentières-sur-Ourcq","Arrancy","Artemps","Artonges","Assis-sur-Serre","Attilly","Aubencheul-aux-Bois","Aubenton","Aubigny-aux-Kaisnes","Aubigny-en-Laonnois","Audignicourt","Audigny","Augy","Aulnois-sous-Laon","Les Autels","Autremencourt","Autreppes","Autreville","Azy-sur-Marne","Bagneux","Bancigny","Barenton-Bugny","Barenton-Cel","Barenton-sur-Serre","Barisis","Barzy-en-Thiérache","Barzy-sur-Marne","Bassoles-Aulers","Baulne-en-Brie","Bazoches-sur-Vesles","Beaumé","Beaumont-en-Beine","Beaurevoir","Beaurieux","Beautor","Beauvois-en-Vermandois","Becquigny","Belleau","Bellenglise","Bellicourt","Benay","Bergues-sur-Sambre","Berlancourt","Berlise","Bernot","Berny-Rivière","Berrieux","Berry-au-Bac","Bertaucourt-Epourdon","Berthenicourt","Bertricourt","Berzy-le-Sec","Besmé","Besmont","Besny-et-Loizy","Béthancourt-en-Vaux","Beugneux","Beuvardes","Bézu-Saint-Germain","Bichancourt","Bieuxy","Bièvres","Billy-sur-Aisne","Billy-sur-Ourcq","Blanzy-lès-Fismes","Blérancourt","Bohain-en-Vermandois","Bois-lès-Pargny","Boncourt","Bonneil","Bonnesvalyn","Bony","Bosmont-sur-Serre","Bouconville-Vauclair","Boué","Bouffignereux","Bouresches","Bourg-et-Comin","Bourguignon-sous-Coucy","Bourguignon-sous-Montbavin","La Bouteille","Braine","Brancourt-en-Laonnois","Brancourt-le-Grand","Braye-en-Laonnois","Braye-en-Thiérache","Bray-Saint-Christophe","Braye","Brécy","Brenelle","Breny","Brie","Brissay-Choigny","Brissy-Hamégicourt","Brunehamel","Bruyères-sur-Fère","Bruyères-et-Montbérault","Bruys","Bucilly","Bucy-le-Long","Bucy-lès-Cerny","Bucy-lès-Pierrepont","Buire","Buironfosse","Burelles","Buzancy","Caillouël-Crépigny","Camelin","La Capelle","Le Catelet","Caulaincourt","Caumont","Celles-lès-Condé","Celles-sur-Aisne","Cerizy","Cerny-en-Laonnois","Cerny-lès-Bucy","Cerseuil","Cessières","Chacrise","Chaillevois","Chalandry","Chamouille","Champs","Chaourse","La Chapelle-Monthodon","La Chapelle-sur-Chézy","Charly-sur-Marne","Le Charmel","Charmes","Chartèves","Chassemy","Châtillon-lès-Sons","Châtillon-sur-Oise","Chaudardes","Chaudun","Chauny","Chavignon","Chavigny","Chavonne","Chérêt","Chermizy-Ailles","Chéry-Chartreuve","Chéry-lès-Pouilly","Chéry-lès-Rozoy","Chevennes","Chevregny","Chevresis-Monceau","Chézy-sur-Marne","Chigny","Chivres-en-Laonnois","Chivres-Val","Chivy-lès-Étouvelles","Chouy","Cierges","Cilly","Ciry-Salsogne","Clacy-et-Thierret","Clairfontaine",
        "Clamecy","Clastres","Clermont-les-Fermes","Coeuvres-et-Valsery","Coincy","Coingt","Colligis-Crandelain","Colonfay","Commenchon","Concevreux","Condé-en-Brie","Condé-sur-Aisne","Condé-sur-Suippe","Condren","Connigis","Corbeny","Coucy-le-Château-Auffrique","Coucy-lès-Eppes","Coucy-la-Ville","Coulonges-Cohan","Courbes","Courboin","Courcelles-sur-Vesle","Courmont","Courtemont-Varennes","Courtrizy-et-Fussigny","Couvrelles","Couvron-et-Aumencourt","Cramaille","Craonne","Craonnelle","Crécy-au-Mont","Crécy-sur-Serre","Crépy","Crézancy","Croix-Fonsomme","La Croix-sur-Ourcq","Crupilly","Cugny","Cuirieux","Cuiry-Housse","Cuiry-lès-Chaudardes","Cuiry-lès-Iviers","Cuissy-et-Geny","Cuisy-en-Almont","Cutry","Cys-la-Commune","Dagny-Lambercy","Dampleux","Danizy","Dercy","Deuillet","Dhuizel","Dizy-le-Gros","Dohis","Dolignon","Dommiers","Dorengt","Douchy","Dravegny","Droizy","Dury","Ébouleau","Effry","Englancourt","Épagny","Éparcy","Épaux-Bézu","Épieds","L’Épine-aux-Bois","Eppes","Erlon","Erloy","Esquéhéries","Essigny-le-Grand","Essises","Estrées","Étaves-et-Bocquiaux","Étouvelles","Étréaupont","Étreillers","Étrépilly","Étreux","Évergnicourt","Faucoucourt","Faverolles","La Fère","Fère-en-Tardenois","La Ferté-Chevresis","Fesmy-le-Sart","Festieux","Filain","La Flamengrie","Flavigny-le-Grand-et-Beaurain","Flavy-le-Martel","Fleury","Fluquières","Folembray","Fontaine-lès-Clercs","Fontaine-lès-Vervins","Fontaine-Uterte","Fontenelle","Fontenelle-en-Brie","Fontenoy","Foreste","Fossoy","Fourdrain","Francilly-Selency","Franqueville","Fresnes-en-Tardenois","Fresnes","Fresnoy-le-Grand","Fressancourt","Frières-Faillouël","Froidestrées","Froidmont-Cohartille","Gercy","Gergny","Germaine","Gibercourt","Gizy","Gland","Glennes","Goudelancourt-lès-Berrieux","Goudelancourt-lès-Pierrepont","Goussancourt","Gouy","Grandlup-et-Fay","Grandrieux","Gricourt","Grisolles","Gronard","Grougis","Guignicourt","Guise","Guivry","Guny","Guyencourt","Hannapes","Happencourt","Haramont","Harcigny","Hargicourt","Hartennes-et-Taux","Hary","Lehaucourt","Hauteville","Haution","La Hérie","Le Hérie-la-Viéville","Hinacourt","Hirson","Holnon","Houry","Housset","Iron","Itancourt","Iviers","Jaulgonne","Jeancourt","Jeantes","Joncourt","Jouaignes","Jumencourt","Jumigny","Jussy","Juvigny","Juvincourt-et-Damary","Laffaux","Laigny","Lanchy","Landifay-et-Bertaignemont","Landouzy-la-Cour","Landouzy-la-Ville","Landricourt","Laniscourt","Lappion","Latilly","Launoy","Laval-en-Laonnois","Lavaqueresse","Laversine","Lemé","Lempire","Lerzy","Leschelle","Lesges","Lesquielles-Saint-Germain","Leuilly-sous-Coucy","Leury","Leuze","Levergies","Lhuys","Licy-Clignon","Lierval","Liesse-Notre-Dame","Liez","Limé","Lislet","Lizy","Logny-lès-Aubenton","Longueval-Barbonval","Lor","Louâtre","Loupeigne","Lucy-le-Bocage","Lugny","Luzoir","Ly-Fontaine","Maast-et-Violaine","Mâchecourt","Macogny","Macquigny","Magny-la-Fosse","Maissemy","Maizy","La Malmaison","Malzy","Manicamp","Marchais","Marchais-en-Brie","Marcy-sous-Marle","Marest-Dampcourt","Mareuil-en-Dôle","Marfontaine","Margival","Marizy-Sainte-Geneviève","Marizy-Saint-Mard","Marle","Marly-Gomont","Martigny","Martigny-Courpierre","Mauregny-en-Haye","Mayot","Mennessis","Menneville","Mennevret","Merlieux-et-Fouquerolles","Merval","Mesbrecourt-Richecourt","Meurival","Mézières-sur-Oise","Mézy-Moulins","Missy-aux-Bois","Missy-lès-Pierrepont","Missy-sur-Aisne","Molain","Molinchart","Monampteuil","Monceau-le-Neuf-et-Faucouzy","Monceau-lès-Leups","Monceau-le-Waast","Monceau-sur-Oise","Mondrepuis","Mons-en-Laonnois","Montaigu","Montbavin","Montbrehain","Montchâlons","Montcornet","Mont-d’Origny","Montescourt-Lizerolles","Montfaucon","Montgobert","Montgru-Saint-Hilaire","Monthenault","Monthiers","Monthurel","Montigny-en-Arrouaise","Montigny-le-Franc","Montigny-Lengrain","Montigny-lès-Condé","Montigny-sous-Marle","Montigny-sur-Crécy","Montlevon","Montloué","Mont-Notre-Dame","Mont-Saint-Jean","Mont-Saint-Martin","Mont-Saint-Père","Morgny-en-Thiérache","Morsain","Mortefontaine","Mortiers","Moulins","Moussy-Verneuil","Moÿ-de-l’Aisne","Muret-et-Crouttes","Muscourt","Nampcelles-la-Cour","Nampteuil-sous-Muret","Nanteuil-la-Fosse","Nanteuil-Notre-Dame","Nauroy","Nesles-la-Montagne","Neufchâtel-sur-Aisne","Neuflieux","Neuve-Maison","La Neuville-Bosmont","La Neuville-en-Beine","La Neuville-Housset","La Neuville-lès-Dorengt","Neuville-sur-Ailette","Neuville-sur-Margival","Neuvillette","Nizy-le-Comte","Nogent-l’Artaud","Noircourt","Noroy-sur-Ourcq","Le Nouvion-en-Thiérache","Nouvion-et-Catillon","Nouvion-le-Comte","Nouvion-le-Vineux","Nouvron-Vingré","Noyales","Noyant-et-Aconin","Ruilly","Ognes","Ohis","Oigny-en-Valois","Oisy","Ollezy","Orainville","Orgeval","Origny-en-Thiérache","Origny-Sainte-Benoite","Osly-Courtil","Ostel","Oulches-la-Vallée-Foulon","Oulchy-la-Ville","Oulchy-le-Château","Paars","Paissy","Pancy-Courtecon","Papleux","Parcy-et-Tigny","Parfondeval","Parfondru","Pargnan","Pargny-Filain","Pargny-la-Dhuys","Pargny-les-Bois","Parpeville","Pasly","Passy-sur-Marne","Perles","Pernant","Pierremande","Pierrepont","Pignicourt","Pinon","Pithon","Pleine-Selve","Le Plessier-Huleu","Ploisy","Plomion","Ployart-et-Vaurseine","Pommiers","Pont-Arcy","Pontavert","Pontru","Pontruet","Pont-Saint-Mard","Pouilly-sur-Serre","Prémont","Prémontré","Presles-et-Boves","Presles-et-Thierny","Prisces","Proisy","Proix","Prouvais","Proviseux-et-Plesnoy","Puiseux-en-Retz","Puisieux-et-Clanlieu","Quierzy","Quincy-Basse","Quincy-sous-le-Mont","Raillimont","Ramicourt","Regny","Remies","Remigny","Renansart","Renneval","Résigny","Ressons-le-Long","Retheuil","Reuilly-Sauvigny","Révillon","Ribeauville","Ribemont","Rocourt-Saint-Martin","Rocquigny","Rogécourt","Rogny","Romeny-sur-Marne","Romery","Ronchères","Roucy","Rougeries","Roupy","Rouvroy-sur-Serre","Royaucourt-et-Chailvet","Rozet-Saint-Albin","Rozières-sur-Crise","Rozoy-Bellevalle","Grand-Rozoy","Rozoy-sur-Serre","Saconin-et-Breuil","Sains-Richaumont","Saint-Agnan","Saint-Algis","Saint-Aubin","Saint-Bandry","Saint-Christophe-à-Berry","Saint-Clément","Sainte-Croix","Saint-Erme-Outre-et-Ramecourt","Saint-Eugène","Sainte-Geneviève","Saint-Gobain","Saint-Gobert","Saint-Mard","Saint-Martin-Rivière","Saint-Michel","Saint-Nicolas-aux-Bois","Saint-Paul-aux-Bois","Saint-Pierre-Aigle","Saint-Pierre-lès-Franqueville","Saint-Pierremont","Sainte-Preuve","Saint-Rémy-Blanzy","Saint-Simon","Saint-Thibaut","Saint-Thomas","Samoussy","Sancy-les-Cheminots","Saponay","Saulchery","Savy","Seboncourt","Selens","La Selve","Septmonts","Septvaux","Sequehart","Serain","Seraucourt-le-Grand","Serches","Sergy","Seringes-et-Nesles","Sermoise","Serval","Servais","Séry-lès-Mézières","Silly-la-Poterie","Sinceny","Sissonne","Sissy","Soize","Sommelans","Sommeron","Sommette-Eaucourt","Sons-et-Ronchères","Sorbais","Soucy","Soupir","Le Sourd","Surfontaine","Suzy","Taillefontaine","Tannières","Tartiers","Tavaux-et-Pontséricourt","Tergnier","Terny-Sorny","Thenailles","Thenelles","Thiernu","Le Thuel","Torcy-en-Valois","Toulis-et-Attencourt","Travecy","Trefcon","Trélou-sur-Marne","Troësnes","Trosly-Loire","Trucy","Tugny-et-Pont","Tupigny","Ugny-le-Gay","Urcel","Urvillers","Vadencourt","Vailly-sur-Aisne","La Vallée-au-Blé","La Vallée-Mulâtre","Variscourt","Vassens","Vasseny","Vassogne","Vaucelles-et-Beffecourt","Vaudesson","Vauxrezis","Vauxaillon","Vaux-Andigny","Vauxcéré","Vaux-en-Vermandois","Vauxtin","Vendelles","Vendeuil","Vendhuile","Vendières","Vendresse-Beaulne","Vénérolles","Venizel","Verdilly","Le Verguier","Grand-Verly","Petit-Verly","Vermand","Verneuil-sous-Coucy","Verneuil-sur-Serre","Versigny","Vervins","Vesles-et-Caumont","Veslud","Vézaponin","Vézilly","Vic-sur-Aisne",
        "Viel-Arcy","Viffort","Vigneux-Hocquet","La Ville-aux-Bois-lès-Dizy","La Ville-aux-Bois-lès-Pontavert","Villemontoire","Villeneuve-sur-Fère","Villequier-Aumont","Villeret","Villers-Agron-Aiguizy","Villers-en-Prayères","Villers-Hélon","Villers-le-Sec","Villers-lès-Guise","Villers-Saint-Christophe","Villers-sur-Fère","Ville-Savoye","Villiers-Saint-Denis","Vincy-Reuil-et-Magny","Viry-Noureuil","Vivaise","Vivières","Voharies","Vorges","Voulpaix","Voyenne","Vregny","Vuillery","Wassigny","Watigny","Wiège-Faty","Wimy","Wissignicourt","Agonges","Ainay-le-Château","Andelaroche","Archignat","Arfeuilles","Arpheuilles-Saint-Priest","Arronnes","Aubigny","Audes","Aurouër","Autry-Issards","Avermes","Avrilly","Bagneux","Barberier","Barrais-Bussolles","Bayet","Beaulon","Beaune-d’Allier","Bègues","Bellenaves","Bert","Bessay-sur-Allier","Besson","Bézenet","Billezois","Billy","Biozat","Bizeneuille","Blomard","Bost","Boucé","Le Bouchaud","Bourbon-l’Archambault","Braize","Bransat","Bresnay","Bressolles","Le Brethon","Le Breuil","Broût-Vernet","Brugheas","Busset","Buxières-les-Mines","La Celle","Cérilly","Cesset","La Chabanne","Chambérat","Chamblet","Chantelle","Chapeau","La Chapelaude","La Chapelle","La Chapelle-aux-Chasses","Chappes","Chareil-Cintrat","Charmeil","Charmes","Charroux","Chassenard","Château-sur-Allier","Châtel-de-Neuvre","Châtel-Montagne","Châtelperron","Châtelus","Châtillon","Chavenon","Chavroches","Chazemais","Chemilly","Chevagnes","Chezelle","Chézy","Chirat-l’Église","Chouvigny","Cindré","Cognat-Lyonne","Colombier","Commentry","Contigny","Cosne-d’Allier","Coulandon","Coulanges","Couleuvre","Courçais","Coutansouze","Couzon","Créchy","Cressanges","Deneuille-lès-Chantelle","Deneuille-les-Mines","Deux-Chaises","Diou","Dompierre-sur-Besbre","Le Donjon","Doyet","Droiturier","Durdat-Larequille","Ébreuil","Échassières","Escurolles","Espinasse-Vozelle","Estivareilles","Étroussat","Ferrières-sur-Sichon","La Ferté-Hauterive","Fleuriel","Fourilles","Franchesse","Gannat","Gannay-sur-Loire","Garnat-sur-Engièvre","Gennetines","Gipcy","Givarlais","Gouise","La Guillermie","Hérisson","Huriel","Hyds","Isle-et-Bardais","Isserpent","Jaligny-sur-Besbre","Jenzat","Laféline","Lalizolle","Lamaids","Langy","Lapalisse","Laprugne","Lavoine","Lenax","Lételon","Liernolles","Lignerolles","Limoise","Loddes","Loriges","Louchy-Montfand","Louroux-Bourbonnais","Louroux-de-Beaune","Louroux-de-Bouble","Louroux-Hodement","Luneau","Lurcy-Lévis","Lusigny","Magnet","Maillet","Malicorne","Marcenat","Marcillat-en-Combraille","Marigny","Mariol","Le Mayet-d’École","Le Mayet-de-Montagne","Mazerier","Mazirat","Meaulne","Meillard","Meillers","Mercy","Mesples","Molinet","Molles","Monestier","Monétay-sur-Allier","Monétay-sur-Loire","Montaiguët-en-Forez","Montaigu-le-Blin","Montbeugny","Montcombroux-les-Mines","Monteignet-sur-l’Andelot","Le Montet","Montilly","Montmarault","Montoldre","Montord","Montvicq","Moulins","Murat","Nades","Nassigny","Naves","Néris-les-Bains","Neuilly-en-Donjon","Neuilly-le-Réal","Neure","Neuvy","Nizerolles","Noyant-d’Allier","Paray-le-Frésil","Paray-sous-Briailles","Périgny","La Petite-Marche","Pierrefitte-sur-Loire","Le Pin","Poëzat","Pouzy-Mésangy","Reugny","Rocles","Rongères","Ronnet","Saint-Angel","Saint-Aubin-le-Monial","Saint-Bonnet-de-Four","Saint-Bonnet-de-Rochefort","Saint-Bonnet-Tronçais","Saint-Caprais","Saint-Christophe","Saint-Clément","Saint-Désiré","Saint-Didier-en-Donjon","Saint-Didier-la-Forêt","Saint-Éloy-d’Allier","Saint-Ennemond","Saint-Étienne-de-Vicq","Saint-Fargeol","Saint-Félix","Saint-Genest","Saint-Gérand-de-Vaux","Saint-Gérand-le-Puy","Saint-Germain-des-Fossés","Saint-Germain-de-Salles","Saint-Hilaire","Saint-Léger-sur-Vouzance","Saint-Léon","Saint-Léopardin-d’Augy","Saint-Loup","Saint-Marcel-en-Murat","Saint-Marcel-en-Marcillat","Saint-Martin-des-Lais","Saint-Martinien","Saint-Menoux","Saint-Nicolas-des-Biefs","Saint-Palais","Saint-Plaisir","Saint-Pont","Saint-Pourçain-sur-Besbre","Saint-Pourçain-sur-Sioule","Saint-Priest-d’Andelot","Saint-Priest-en-Murat","Saint-Prix","Saint-Rémy-en-Rollat","Saint-Sauvier","Saint-Sornin","Sainte-Thérence","Saint-Voir","Saligny-sur-Roudon","Sanssat","Saulcet","Saulzet","Sauvagny","Sazeret","Servilly","Seuillet","Sorbier","Souvigny","Sussat","Target","Taxat-Senat","Teillet-Argenty","Terjat","Le Theil","Theneuille","Thiel-sur-Acolin","Thionne","Tortezais","Toulon-sur-Allier","Treban","Treignat","Treteau","Trévol","Trézelles","Tronget","Urçay","Ussel-d’Allier","Valignat","Valigny","Vallon-en-Sully","Varennes-sur-Allier","Varennes-sur-Tèche","Vaumas","Vaux","Veauce","Venas","Vendat","Verneix","Verneuil-en-Bourbonnais","Vernusse","Le Veurdre","Vicq","Vieure","Le Vilhain","Villebret","Villefranche-d’Allier","Villeneuve-sur-Allier","Viplaix","Vitray","Voussac","Ygrande","Yzeure","Aiglun","Allemagne-en-Provence","Allons","Allos","Angles","Annot","Archail","Aubenas-les-Alpes","Aubignosc","Authon","Auzet","Banon","Barcelonnette","Barles","Barras","Barrême","Bayons","Beaujeu","Beauvezer","Bellaffaire","Bevons","Beynes","Blieux","Bras-d’Asse","Braux","La Bréole","Brunet","Le Brusquet","Le Caire","Castellane","Le Castellard-Mélan","Le Castellet","Castellet-lès-Sausses","Val-de-Chalvagne","Céreste","Le Chaffaut-Saint-Jurson","Champtercier","Château-Arnoux-Saint-Auban","Châteaufort","Châteauneuf-Miravail","Châteauneuf-Val-Saint-Donat","Châteauredon","Chaudon-Norante","Clamensane","Clumanc","Colmars","La Condamine-Châtelard","Cruis","Curel","Dauphin","Demandolx","Digne-les-Bains","Draix","Enchastrayes","Entrages","Entrepierres","Entrevaux","Entrevennes","L’Escale","Estoublon","Faucon-du-Caire","Faucon-de-Barcelonnette","Fontienne","Le Fugeret","Ganagobie","La Garde","Gigors","L’Hospitalet","Jausiers","La Javie","Lambruisse","Lardiers","Le Lauzet-Ubaye","Limans","Lurs","Majastres","Malijai","Mallefougasse-Augès","Mallemoisson","Marcoux","Méailles","Melve","Meyronnes","Mézel","Mirabeau","Mison","Montagnac-Montpezat","Montclar","Montfort","Montfuron","Montjustin","Montlaux","Montsalier","Moriez","La Motte-du-Caire","Moustiers-Sainte-Marie","La Mure-Argens","Nibles","Niozelles","Noyers-sur-Jabron","Les Omergues","Ongles","Oppedette","La Palud-sur-Verdon","Peipin","Peyroules","Pierrerue","Prads-Haute-Bléone","Puimichel","Puimoisson","Quinson","Redortiers","Reillanne","Méolans-Revel","Revest-des-Brousses","Revest-du-Bion","Revest-Saint-Martin","Riez","La Robine-sur-Galabre","La Rochegiron","Rougon","Roumoules","Saint-André-les-Alpes","Saint-Benoît","Sainte-Croix-à-Lauze","Sainte-Croix-du-Verdon","Hautes-Duyes","Saint-Étienne-les-Orgues","Saint-Geniez","Saint-Jacques","Saint-Jeannet","Saint-Julien-d’Asse","Saint-Julien-du-Verdon","Saint-Jurs","Saint-Laurent-du-Verdon","Saint-Lions","Saint-Maime","Saint-Martin-les-Eaux","Saint-Martin-lès-Seyne","Saint-Michel-l’Observatoire","Saint-Paul-sur-Ubaye","Saint-Pons","Saint-Vincent-les-Forts","Saint-Vincent-sur-Jabron","Salignac","Saumane","Sausses","Selonnet","Senez","Seyne","Sigonce","Sigoyer","Simiane-la-Rotonde","Soleilhas","Sourribes","Tartonne","Thèze","Thoard","Thorame-Basse","Thorame-Haute","Les Thuiles","Turriers","Ubraye","Uvernet-Fours","Vachères","Valavoire","Valbelle","Valernes","Vaumeilh","Verdaches","Vergons","Le Vernet","Villars-Colmars","Villemus","Volonne","Abriès","Aiguilles","Ancelle","Antonaves","L’Argentière-la-Bessée","Arvieux","Aspremont","Aspres-lès-Corps","Aspres-sur-Buëch","Avançon","Baratier","Barcillonnette","Barret-sur-Méouge","La Bâtie-Montsaléon","La Bâtie-Neuve","La Bâtie-Vieille","La Beaume","Le Bersac","Bréziers","Bruis","Buissard","Ceillac","Cervières","Chabestan","Chabottes","Champcella","Champoléon","Chanousse","Châteauneuf-de-Chabre",
        "Châteauneuf-d’Oze","Châteauroux-les-Alpes","Châteauvieux","Château-Ville-Vieille","Chauffayer","Chorges","Les Costes","Crévoux","Crots","Embrun","Éourres","L’Épine","Esparron","Espinasses","Étoile-Saint-Cyrice","Eygliers","Eyguians","La Fare-en-Champsaur","La Faurie","Forest-Saint-Julien","Fouillouse","Freissinières","La Freissinouse","Furmeyer","Le Glaizil","La Grave","La Chapelle-en-Valgaudémar","Guillestre","La Haute-Beaume","Jarjayes","Lagrand","Laragne-Montéglin","Lardier-et-Valença","Laye","Lazer","Lettret","Manteyer","Méreuil","Molines-en-Queyras","Monêtier-Allemont","Le Monêtier-les-Bains","Montbrand","Montclus","Mont-Dauphin","Montgardin","Montgenèvre","Montjay","Montmaur","Montmorin","Montrond","La Motte-en-Champsaur","Moydans","Neffes","Névache","Nossage-et-Bénévent","Le Noyer","Orcières","Orpierre","Les Orres","Oze","Pelleautier","Pelvoux","La Piarre","Le Poët","Poligny","Prunières","Puy-Saint-André","Puy-Saint-Eusèbe","Puy-Saint-Pierre","Puy-Saint-Vincent","Puy-Sanières","Rabou","Rambaud","Réallon","Remollon","Réotier","Ribeyret","Ribiers","Risoul","Ristolas","Rochebrune","La Roche-de-Rame","La Roche-des-Arnauds","La Rochette","Rosans","Rousset","Saint-André-d’Embrun","Saint-André-de-Rosans","Saint-Apollinaire","Saint-Auban-d’Oze","Saint-Bonnet-en-Champsaur","Saint-Chaffrey","Saint-Clément-sur-Durance","Sainte-Colombe","Saint-Crépin","Dévoluy","Saint-Étienne-le-Laus","Saint-Eusèbe-en-Champsaur","Saint-Firmin","Saint-Genis","Saint-Jacques-en-Valgodemard","Saint-Jean-Saint-Nicolas","Saint-Julien-en-Beauchêne","Saint-Julien-en-Champsaur","Saint-Laurent-du-Cros","Saint-Léger-les-Mélèzes","Sainte-Marie","Saint-Martin-de-Queyrières","Saint-Maurice-en-Valgodemard","Saint-Michel-de-Chaillol","Saint-Pierre-d’Argençon","Saint-Pierre-Avez","Saint-Sauveur","Saint-Véran","Le Saix","Saléon","Salérans","La Salle-les-Alpes","La Saulce","Le Sauze-du-Lac","Savines-le-Lac","Savournon","Serres","Sigottier","Sigoyer","Sorbiers","Tallard","Théus","Trescléoux","Upaix","Val-des-Prés","Vallouise","Valserres","Vars","Ventavon","Veynes","Les Vigneaux","Villar-d’Arêne","Villar-Loubière","Villar-Saint-Pancrace","Vitrolles","Aiglun","Amirat","Ascros","Auvare","Bairols","Belvédère","Beuil","Briançonnet","Caille","Châteauneuf-d’Entraunes","Clans","Collongues","La Croix-sur-Roudoule","Cuébris","Daluis","Entraunes","Fontan","Gars","Guillaumes","Ilonse","Isola","Lieuche","Malaussène","Marie","Le Mas","Massoins","Les Mujouls","La Penne","Péone","Pierlas","Pierrefeu","Puget-Rostang","Puget-Théniers","Rigaud","Rimplas","Roquebillière","Roquestéron","Roubion","Roure","Saint-Antonin","Saint-Auban","Saint-Dalmas-le-Selvage","Saint-Étienne-de-Tinée","Saint-Léger","Saint-Martin-d’Entraunes","Saint-Martin-Vésubie","Saint-Sauveur-sur-Tinée","Sallagriffon","Saorge","Sauze","Séranon","Sigale","Thiéry","Touët-sur-Var","La Tour","Tournefort","Valdeblore","Valderoure","Venanson","Villars-sur-Var","Villeneuve-d’Entraunes","La Brigue","Tende",]
        zoneC = sorted(zoneC)

        list_dict = {"Zone A bis et A" : zoneAbisA,"Zone B1":zoneB1,"Zone B2":zoneB2,"Zone C":zoneC}
        list_total = zoneC+zoneB1+zoneAbisA+zoneB2
        list_total = sorted(list_total)
        residencePrincipale = radio("Avez-vous été propriétaire de votre résidence principale au cours des 2 dernières années ?", options = ["Oui", "Non"])
        if (residencePrincipale == "Oui"):
            put_warning("Vous ne devez pas avoir été propriétaire au cours des deux années précédentes, sauf si vous êtes titulaire d’une carte d’invalidité 2ème ou 3ème catégorie, si vous êtes allocataire de l’allocation adulte handicapé ou d’éducation spéciale ou si vous avez été victime de catastrophes rendant votre logement inhabitable.")
        if (residencePrincipale == "Non"):  
            npers = int(input("Combien de personnes habiteront dans le nouveau logement ?"))
            nature = radio("Nature du bien :", options = ["Neuf", "Ancien"])
            choix = select("Selectionnez la ville de votre investissement Pinel :", list_total)
            if nature == "Neuf":
                for key, value in list_dict.items():
                    if choix in value:
                        if key == "Zone A bis et A":
                            if npers == 1:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 37000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    #prixDuBien = prixDuBien - apport
                                
                                    if prixDuBien < 150000:
                                        ptz = 0.4*prixDuBien
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:

                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*150000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:

                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_success("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 2:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 51800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 210000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*210000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 3:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 62900:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 255000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*255000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 4:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 74000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 300000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*300000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 5:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 85100:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 345000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*345000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 6:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 96200:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 345000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*345000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 7:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 107300:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 345000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*345000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 8:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 118400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 345000 :
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*150000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 9:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 118400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 345000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*345000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 10:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 118400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 345000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*345000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                        if key == "Zone B1":
                            if npers == 1:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 30000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 135000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*135000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 2:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 42000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 189000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*189000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 3:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 51000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 230000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*230000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 4:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 60000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 270000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*270000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 5:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 69000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 311000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*311000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 6:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 78000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 311000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*311000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 7:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 87000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 311000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*311000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))

                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 8:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 96000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 311000 :
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*311000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 9:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 96000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 311000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*311000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 10:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 96000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 311000:
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*311000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                        if key == "Zone B2":
                            if npers == 1:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 27000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 110000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*110000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 2:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 37800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 154000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*154000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 3:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 45900:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 187000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*187000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 4:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 54000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 220000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*220000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 5:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 62100:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 253000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*253000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 6:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 70200:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 253000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*253000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 7:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 78300:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 253000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*253000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 8:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 86400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 253000 :
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*253000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 9:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 86400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 253000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*253000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 10:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 86400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 253000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*253000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                        if key == "Zone C":
                            if npers == 1:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 24000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 100000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*100000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 2:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 33600:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 140000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*140000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 3:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 40800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 170000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*170000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 4:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 48000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 200000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*200000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 5:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 55200:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 230000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*230000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 6:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 62400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 230000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*230000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 7:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 69600:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 230000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*230000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 8:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 76800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 230000 :
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*230000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))

                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 9:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 76800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 230000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*230000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 10:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 76800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    if prixDuBien < 230000:
                                        ptz = 0.2*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        ptz = 0.4*230000
                                        pretPrincipale = prixDuBien - ptz - apport
                                        if ptz <= pretPrincipale:
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                        else:
                                            ptz = pretPrincipale
                                            put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

            if nature == "Ancien":
                for key, value in list_dict.items():
                    if choix in value:
                        if key == "Zone A bis et A":
                            if npers == 1:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 2:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 3:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 4:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 5:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 6:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 7:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 8:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 9:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 10:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                        if key == "Zone B1":
                            if npers == 1:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 2:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 3:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 4:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 5:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 6:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 7:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 8:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 9:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 10:
                                put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                        if key == "Zone B2":
                            if npers == 1:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 27000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 2:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 37800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 3:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 45900:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 4:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 54000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 5:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 62100:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 6:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 70200:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 7:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 78300:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 8:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 86400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 9:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 86400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 10:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 86400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                        if key == "Zone C":
                            if npers == 1:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 24000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 2:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 33600:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 3:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 40800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 4:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 48000:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                            if npers == 5:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 55200:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 6:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 62400:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 7:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 69600:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 8:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 76800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 9:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 76800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")

                            if npers == 10:
                                revenu = float(input("Revenu fiscal de référence du foyer en 2020 :"))
                                if revenu < 76800:
                                    prixDuBien = float(input("Prix d'achat du bien :"))
                                    apport = float(input("Votre apport :"))
                                    prixDuBien = prixDuBien - apport
                                    travaux = float(input("Le montant de vos travaux"))
                                    if travaux >= (0.25*prixDuBien):
                                        ptz = 0.4*prixDuBien
                                        put_success("Bonne nouvelle, vous êtes éligible au PTZ pour un montant de {} €".format(ptz))
                                    else :
                                        put_warning("Il semble que vous ne soyez pas éligible au PTZ.")
                                else :
                                    put_warning("Il semble que vous ne soyez pas éligible au PTZ.")


    if (choix == "27 - Calcul assurance de prêt immobilier") :
        put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")
        montant = float(input("Le montant emprunté :"))
        annee = int(input("Le nombre d'années de votre crédit :"))
        taux = float(input("Le taux d'intérêt (hors assurance) :"))
        assuParMois = montant*((taux/100)/12)
        assuTotale = assuParMois*annee*12
        put_table([
            ["Montant emprunté","Nombres d'années","Cotisation estimée €/mois","Coût de votre assurance de prêt"],
            [int(montant),int(annee),float("{:.2f}".format(assuParMois)),float("{:.2f}".format(assuTotale))]
        ])
        



if __name__ == '__main__':
    platform.start_server(main, port=8080, debug=True,remote_access=True,reconnect_timeout = True) 
    #platform.flask.start_server(main,port=8080, debug=False,remote_access=True,session_expire_seconds=None)

    
    

