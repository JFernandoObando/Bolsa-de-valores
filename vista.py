from __future__ import print_function
from unicodedata import name
import Pyro4

#Clase del visitante
class Viewer(object):
    def __init__(self):
        self.markets = set()
        self.symbols = set()
#Inicio de las cotizaciones realizando la mezcla de la bolsa el simbolo y el valor
    def start(self):
        print("Inicio de cotizaciones:", self.symbols)
        quote_sources = {
            market.name: market.quotes() for market in self.markets
        }
        while True:
            for market, quote_source in quote_sources.items():
                quote = next(quote_source) 
                symbol, value = quote
                if symbol in self.symbols:
                    print("{0}.{1}: {2}".format(market, symbol, value))

#Funcion para realizar la busqueda de la bolsa
def find_stockmarkets():
  
    markets = []
    with Pyro4.locateNS() as ns:
        for market, market_uri in ns.list(prefix="ejemplo.bolsa.").items():
            print("Buscando bolsa", market)
            markets.append(Pyro4.Proxy(market_uri))
   
    if not markets:
        
        raise ValueError("Bolsa no encontrada")
    return markets

#Menu para mostrar la bolsa por ciudades y la mezcla
def main():
    viewer = Viewer()
    viewer.markets = find_stockmarkets()
    print("Elija una bolsa de valores")
    print("1.-NYSE")
    print("2.-NASDAQ")
    print("3.- NYSE & NASDAQ")
    print("Para salir presione Ctrl + C")
    op=input("Elija una opcion ")
    while True:
        if op == "1":
            viewer.symbols = {"IBM", "HPQ", "BP"}
            viewer.start()
        if op == "2":
            viewer.symbols = {"AAPL", "CSCO", "MSFT", "GOOG"}
            viewer.start()          
        if op == "3":
            viewer.symbols = {"IBM", "MSFT", "GOOG","HPQ", "BP"}
            viewer.start()
     
        if op > "3":
            print("#####Opcion Incorrecta#####")
            print("Programa finalizado")     


if __name__ == "__main__":
    main()