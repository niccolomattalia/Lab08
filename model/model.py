from database.distributore_DAO import DistributoreDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        listaTuple = []
        for dis in self._distributori:
            somma = 0
            conta = 0
            media = 0
            for prez in dis.get_prezzi():
                m = prez.data.month
                if m == mese:
                    somma += prez.prezzo_litro
                    conta +=1
            if conta == 0:
                continue
            else:
                media = somma / conta
                listaTuple.append((dis.nome, media))
        return listaTuple



    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        if giorno > 7:
            self.__sequenza_ottima = sequenza_parziale
            self.__costo_ottimo = costo_corrente
            return
        else:
            if ultimo_distributore == 1:
                costo1 = prezzi_settimana["id_distributore1"][giorno-1]*100
                costo2 = 5 + prezzi_settimana["id_distributore2"][giorno-1]*100
                if costo1 > costo2:
                    costo_corrente += costo2
                    sequenza_parziale.append(2)
                    ultimo_distributore = 2
                else:
                    costo_corrente += costo1
                    sequenza_parziale.append(1)
                    ultimo_distributore = 1


            elif ultimo_distributore == 2:
                costo1 = 5 +prezzi_settimana["id_distributore1"][giorno-1]*100
                costo2 = prezzi_settimana["id_distributore2"][giorno-1]*100
                if costo1 > costo2:
                    costo_corrente += costo2
                    sequenza_parziale.append(2)
                    ultimo_distributore = 2
                else:
                    costo_corrente += costo1
                    sequenza_parziale.append(1)
                    ultimo_distributore = 1


            else:
                costo1 = prezzi_settimana["id_distributore1"][giorno-1]*100
                costo2 = prezzi_settimana["id_distributore2"][giorno-1]*100
                if costo1 > costo2:
                    costo_corrente += costo2
                    sequenza_parziale.append(2)
                    ultimo_distributore = 2
                else:
                    costo_corrente += costo1
                    sequenza_parziale.append(1)
                    ultimo_distributore = 1
        giorno+=1
        print(sequenza_parziale)
        self.__ricorsione(sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana)


    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        diz = {
            "id_distributore1": [],
            "id_distributore2": []
        }
        distrib = 0
        for dis in self._distributori:
            distrib +=1
            lista_prezzi = dis.get_prezzi()
            cont = 0
            if distrib == 1:
                for prez in lista_prezzi:
                    if prez.data.month == mese:
                        if cont < 7:
                            diz["id_distributore1"].append(prez.prezzo_litro)
                        cont += 1
            elif distrib == 2:
                for prez in lista_prezzi:
                    if prez.data.month == mese:
                        if cont < 7:
                            diz["id_distributore2"].append(prez.prezzo_litro)
                        cont += 1
        return diz

