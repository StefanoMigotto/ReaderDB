import mysql.connector
import re
from colorama import *
import os
import json
from tabulate import tabulate
init()


def riquadra(title):
    print(" ")
    print(Back.WHITE + Fore.WHITE + "###############" + Fore.BLACK + title + Fore.WHITE +"###############")
    print(Back.RESET)



def LeggiItems(json):
    json_max_lenght = len(json["items"])
    json_count = 0
    table = []
    for json_count in range(json_max_lenght):
        if(len(json["items"][json_count]) != 0):
            table.append([json["items"][json_count]["name"],#nome oggetto nel db
            str(json["items"][json_count]["count"]),#quantità dell'oggetto es 10 di cibo
            json["items"][json_count]["label"], #nome visualizzato in gioco
            str(json["items"][json_count]["quality"])], #usura o qualità dell'oggetto
            )
    print(tabulate(table, headers=["Nome Oggetto DB","Quantità Oggetto","Nome Visualizzato", "Qualità o Durabilità"]))
            
print("Connessione con il database locale in corso...")

get_config = open("config.json", "r")
config = json.loads(get_config.read())
database = mysql.connector.connect(
    host=config["host"],
    user=config["username"],
    password=config["password"],
    database=config["database"]
)

cc = database.cursor()

while True:
    print("1 - Ricerca Persona [Identifier]")
    print("2 - Visualizza tutti gli utenti e relative informazioni")
    scelta = input("Inserisci Numero Selezionato: ")

    if scelta == "clear":
        os.system("cls")

    if(scelta == "1"):
        ##### RICERCA #####
        while True:
            persona = input("-[ ")
            #prende la le info base della persona
            if persona == "clear":
                os.system("cls")
            if persona == "exit":
                break
            cc.execute("select * from users")
            utenti = cc.fetchall()
            utenti_count_for = 1
            for utenti in utenti:
                if utenti[1] == persona:
                    riquadra("Informazioni Generali")
                    print("ID DATABASE: " + utenti[0])
                    print("Identifier: " + utenti[1])
                    print("Nome RP: " + utenti[9] + utenti[10])
                    print("Gruppo: " + utenti[3])
                    print("Stato Lavorativo: " + utenti[5])
                    print("Nato il: " + utenti[11])
                    print("Sesso: " + utenti[12])
                    print("Saldo: " + utenti[2])

                    riquadra("Informazioni Generali")
                else:
                    utenti_count_for = utenti_count_for+1

            #prende l'inventario
            cc.execute("select identifier from inventories")
            identifier = cc.fetchall()
            counter_loop = 0
            for identifier in identifier:
                if identifier[0] == persona:
                    cc.execute("select data from inventories")
                    data = cc.fetchall()
                    riquadra(Back.CYAN + "Inventario" + Back.WHITE)
                    #print("Data: " + data[counter_loop][0])
                    LeggiItems(json.loads(data[counter_loop][0]))
                    riquadra(Back.CYAN + "Inventario" + Back.WHITE)
                else:
                    counter_loop = counter_loop+1


    #visualizzazione globale
    if(scelta == "2"):

        riquadra(Back.RED + "Tutti i Giocatori" + Back.WHITE)
        cc.execute("select * from users")
        utenti = cc.fetchall()
        persona_count = 0
        table = []
        max_persone = len(utenti)
        for persona in range(max_persone):
            data = json.loads(utenti[persona][2])
            table.append([
            utenti[persona][1],
            utenti[persona][9],
            utenti[persona][10],
            utenti[persona][5],
            str(data.get("money")),
            str(data.get("bank")),
            str(data.get("black_money"))])
        print(tabulate(table, headers=["Identifier","Nome","Cognome","Lavoro","Soldi", "Banca", "Soldi Sporchi"]))
        riquadra(Back.RED + "Tutti i Giocatori" + Back.WHITE)
           


    


