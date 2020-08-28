import bottle
import os
import random
from model import Uporabnik, Slascicar
from datetime import date

uporabniki = {}
for ime_datoteke in os.listdir('shranjeni_uporabniki'):
    st_uporabnika, koncnica = os.path.splitext(ime_datoteke)
    uporabniki[st_uporabnika] = Slascicar.nalozi_stanje(os.path.join
    ('shranjeni_uporabniki', ime_datoteke))

def trenutni_uporbnik():
    st_uporabnika = bottle.request.get_cookie('st_uporabnika')
    if st_uporabnika is None:
        st_uporabnika = str(random.randint(0, 2 ** 40))
        uporabniki[st_uporabnika] = Slascicar()
        bottle.response.set_cookie('st_uporabnika', st_uporabnika, path='/')
    return uporabniki[st_uporabnika]

def shrani_trenutnega_uporabnika():
    st_uporabnika = bottle.request.get_cookie('st_uporabnika')
    slascicar = uporabniki[st_uporabnika]
    slascicar.shrani_stanje(os.path.join('shranjeni_uporabniki', f'{st_uporabnika}.json'))

@bottle.get('/')
def zacetna_stran():
    bottle.redirect('/sladkosned/')

@bottle.get('/sladkosned/')
def osnovna_stran():
    slascicar = trenutni_uporbnik()
    return bottle.template('osnovna_stran.html', slascicar=slascicar)

@bottle.get('/pomoc/')
def pomoc():
    return bottle.template('pomoc.html')

@bottle.get('/stanje/')
def stran_s_stanjem():
    slascicar = trenutni_uporbnik()
    return bottle.template('naslednja_stran.html', slascicar=slascicar)

@bottle.post('/dodaj-prodajo/')
def dodaj_prodajo():
    slascicar = trenutni_uporbnik()
    slascicar.dodaj_prodajo(bottle.request.forms.getunicode('vrsta'))
    shrani_trenutnega_uporabnika()
    bottle.redirect('/stanje/')

@bottle.post('/dodaj-strosek/')
def dodaj_strosek():
    slascicar = trenutni_uporbnik()
    ime_stroska = bottle.request.forms.getunicode('ime')
    znesek =  int(bottle.request.forms.getunicode('znesek'))
    slascicar.dodaj_strosek(ime_stroska, znesek)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/stanje/')

@bottle.post('/dodaj-sladico/')
def dodaj_sladico():
    slascicar = trenutni_uporbnik()
    ime = bottle.request.forms.getunicode('ime')
    datum = date.today().strftime("%m/%d/%Y")
    cena = int(bottle.request.forms.getunicode('cena'))
    strosek = slascicar.poisci_strosek(bottle.request.forms['strosek'])
    prodaja = slascicar.poisci_prodajo(bottle.request.forms['prodaja'])
    kolicina = int(bottle.request.forms.getunicode('kolicina'))
    slascicar.dodaj_sladico(ime, datum, cena, strosek, prodaja, kolicina)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/stanje/')

@bottle.post('/prodaj-sladico/')
def prodaj_sladico():
    slascicar = trenutni_uporbnik()
    sladica = slascicar.poisci_sladico(bottle.request.forms['sladica'])
    prodaja = slascicar.poisci_prodajo(bottle.request.forms['prodaja'])
    kolicina = int(bottle.request.forms.getunicode('kolicina'))
    slascicar.prodaj_sladico(sladica, prodaja, kolicina)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/stanje/')

bottle.run(debug=True, reloader=True)