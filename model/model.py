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
            #se e' la prima combinazione (-1), salvo i valori in modo da usarli come punto di rif
            #oppure se il costo corrente è minore di quello ottimo, entro così da poter rivalutare il minimo costo
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale)
            return

        for id in prezzi_settimana:
            #prendo valore del distributore nella chaive id, nella lista corrispondente al giorno voluto
            costo = prezzi_settimana[id][giorno - 1] * 100
            #fosse None vuol dire che siamo al primo giorno, non fa pagare lo spostamento
            #entra se non siamo al primo giorno e il distributore di oggi e' diverso da quello di ieri
            if ultimo_distributore is not None and id != ultimo_distributore:
                costo += 5

            #aggiungo distributore scelto alla lista della settimana
            sequenza_parziale.append(id)
            self.__ricorsione(sequenza_parziale, giorno + 1, id, costo_corrente + costo, prezzi_settimana)
            #dopo che la funzione ricorsiva ha finito, tolgo l'ultimo distributore appena inserito. In modo che la lista torna pulita e riparte dall'altro distributore
            sequenza_parziale.pop()


    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        diz = {}
        for dis in self._distributori:
            diz[dis.id] = []
            for prez in dis.get_prezzi():
                if prez.data.month == mese and prez.data.day >=1 and prez.data.day <=7:
                    diz[dis.id].append(prez.prezzo_litro)
        return diz



