import bottle
from model import Uporabnik, Slascicar

DATOTEKA_S_SLADICAMI = 'stanje.json'

try:
    slascicar = Slascicar.nalozi_stanje(DATOTEKA_S_SLADICAMI)
except FileNotFoundError:
    slascicar = Slascicar()

@bottle.get('/')
def zacetna_stran():
    return bottle.template('osnovna_stran.html', slascicar=slascicar)

bottle.run(debug=True, reloader=True)