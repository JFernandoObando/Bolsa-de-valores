from __future__ import print_function
import random
import time
import Pyro4


@Pyro4.expose
#Clase de bolsa de valores
class StockMarket(object):
    def __init__(self, marketname, symbols):
        self._name = marketname
        self._symbols = symbols

    def quotes(self):
        while True:
            #Funcion para crear datos aleatorios
            symbol = random.choice(self.symbols)
            yield symbol, round(random.uniform(5, 150), 2)
            time.sleep(random.random()/1.0)

    #Retorna el nombre de la bolsa de valores
    @property
    def name(self):
        return self._name
    #Retorna el simbolo de la bolsa
    @property
    def symbols(self):
        return self._symbols


if __name__ == "__main__":
    #Crea la bolsa de valores con los simbolos de cada una
    nasdaq = StockMarket("NASDAQ", ["AAPL", "CSCO", "MSFT", "GOOG"])
    newyork = StockMarket("NYSE", ["IBM", "HPQ", "BP"])
    #Declaro el objeto pyro con el uri y sus funcionalidades para realizar la 
    #aplicacion distribuida
    with Pyro4.Daemon() as daemon:
     
        nasdaq_uri = daemon.register(nasdaq)
        newyork_uri = daemon.register(newyork)
        with Pyro4.locateNS() as ns:
            ns.register("ejemplo.bolsa.nasdaq", nasdaq_uri)
            ns.register("ejemplo.bolsa.newyork", newyork_uri)
        print("Bolsa iniciada.")
       
        daemon.requestLoop()