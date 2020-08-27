import bottle
from model import Uporabnik, Slascicar
from datetime import date

DATOTEKA_S_SLADICAMI = 'stanje.json'

try:
    slascicar = Slascicar.nalozi_stanje(DATOTEKA_S_SLADICAMI)
except FileNotFoundError:
    slascicar = Slascicar()

@bottle.get('/')
def zacetna_stran():
    return bottle.template('osnovna_stran.html', slascicar=slascicar)

@bottle.get('/stanje/')
def stran_s_stanjem():
    return bottle.template('naslednja_stran.html', slascicar=slascicar)

@bottle.post('/dodaj-prodajo/')
def dodaj_prodajo():
    slascicar.dodaj_prodajo(bottle.request.forms.getunicode('vrsta'))
    bottle.redirect('/')

@bottle.post('/dodaj-strosek/')
def dodaj_strosek():
    ime_stroska = bottle.request.forms.getunicode('ime')
    znesek =  int(bottle.request.forms.getunicode('znesek'))
    slascicar.dodaj_strosek(ime_stroska, znesek)
    slascicar.shrani_stanje(DATOTEKA_S_SLADICAMI)
    bottle.redirect('/')

@bottle.post('/dodaj-sladico/')
def dodaj_sladico():
    ime = bottle.request.forms.getunicode('ime')
    datum = date.today().strftime("%m/%d/%Y")
    cena = int(bottle.request.forms.getunicode('cena'))
    strosek = slascicar.poisci_strosek(bottle.request.forms['strosek'])
    prodaja = slascicar.poisci_prodajo(bottle.request.forms['prodaja'])
    slascicar.dodaj_sladico(ime, datum, cena, strosek, prodaja)
    slascicar.shrani_stanje(DATOTEKA_S_SLADICAMI)
    bottle.redirect('/')

@bottle.post('/prodaj-sladico/')
def prodaj_sladico():
    sladica = slascicar.poisci_sladico(bottle.request.forms['sladica'])
    prodaja = slascicar.poisci_prodajo(bottle.request.forms['prodaja'])
    slascicar.prodaj_sladico(sladica, prodaja)
    slascicar.shrani_stanje(DATOTEKA_S_SLADICAMI)
    bottle.redirect('/')

bottle.run(debug=True, reloader=True)