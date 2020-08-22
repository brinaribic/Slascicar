from datetime import date
from model import Slaščičar

LOGO = '''
_______  ___      _______  ______   ___   _  _______  _______  __    _  _______  ______  
|       ||   |    |   _   ||      | |   | | ||       ||       ||  |  | ||       ||      | 
|  _____||   |    |  |_|  ||  _    ||   |_| ||   _   ||  _____||   |_| ||    ___||  _    |
| |_____ |   |    |       || | |   ||      _||  | |  || |_____ |       ||   |___ | | |   |
|_____  ||   |___ |       || |_|   ||     |_ |  |_|  ||_____  ||  _    ||    ___|| |_|   |
 _____| ||       ||   _   ||       ||    _  ||       | _____| || | |   ||   |___ |       |
|_______||_______||__| |__||______| |___| |_||_______||_______||_|  |__||_______||______| 

'''

DATOTEKA_S_SLADICAMI = 'stanje.json'

try:
    slaščičar = Slaščičar.nalozi_stanje(DATOTEKA_S_SLADICAMI)
except FileNotFoundError:
    slaščičar = Slaščičar()

def logo(niz):
    return f'\033[1;35m{niz}\033[0m'

def krepko(niz):
    return f'\033[1m{niz}\033[0m'

def modro(niz):
    return f'\033[1;94m{niz}\033[0m'

def rdece(niz):
    return f'\033[1;91m{niz}\033[0m'

def vnesi_stevilo(pozdrav):
    while True:
        try:
            stevilo = input(pozdrav)
            return int(stevilo)
        except ValueError:
            print(f'Prosim, da vnesete število!')

def izberi(seznam):
    for indeks, (oznaka, _) in enumerate(seznam, 1):
        print(f'{indeks}) {oznaka}')
    while True:
        izbira = vnesi_stevilo('> ')
        if 1 <= izbira <= len(seznam):
            _, element = seznam[izbira - 1]
            return element
        else:
            print(f'Izberi število med 1 in {len(seznam)}')

def prikaz_skupnega_dobička(dobiček):
    if dobiček > 0:
        return f'trenutno je skupni dobiček: {modro(dobiček)} €'
    elif dobiček < 0:
        return f'trenutno je skupni dobiček: {rdece(dobiček)} €'
    else:
        return f'trenutno je skupni dobiček: {dobiček} €'

def prikaz_sladic(sladica):
    if sladica in slaščičar.prodane_sladice():
        return f'Ta {sladica} je prodana.'
    else:
        return f'Ta {rdece(sladica)} ni prodana!'

def zacetna_stran():
    print(logo(LOGO))
    print ()
    print(krepko('Pozdravljeni v programu Sladkosned!'))
    print()
    print('Za izhod pritisnite Ctrl-C')
    print(80 * '=')


def osnovne_meni():
    while True:
        try:
            print('Kaj bi radi naredili?')
            print()
            moznosti = [
                ('dodaj prodajo', dodaj_prodajo),
                ('dodaj strošek', dodaj_strošek),
                ('dodaj sladico', dodaj_sladico),
                ('poglej ne prodane sladice', neprodane_sladice),
                ('poglej vse sladice', vse_sladice),
                ('poglej dobiček/skupne stroške', stanje_denarja),
            ]
            izbira = izberi(moznosti)
            izbira()
            print(80 * '=')
            print()
            input('Pritisnite Enter za shranjevanje in vrnitev v osnovni meni')
            print(80 * '=')
            slaščičar.shrani_stanje(DATOTEKA_S_SLADICAMI)
        except ValueError as e:
            print(rdece(e.args[0]))
            print(80 * '=')
        except KeyboardInterrupt:
            print()
            print('Nasvidenje')
            break

def dodaj_prodajo():
    vrsta = input('Vnesite način prodaje sladice (npr. osebni prevzem, dostava na dom, ...)> ')
    slaščičar.dodaj_prodajo(vrsta)

def dodaj_strošek():
    ime = input('Vnesite ime stroška (npr. sestavine, dodatni delavec, ...)> ')
    znesek = vnesi_stevilo('znesek> ')
    slaščičar.dodaj_strošek(ime, znesek)

def izberi_strošek(stroški):
    return izberi([(strošek, strošek)for strošek in stroški],)

def izberi_prodajo(prodaje):
    return izberi([(prodaja, prodaja)for prodaja in prodaje],)

def dodaj_sladico():
    print('Vnesite podatke o sladici:')
    print()
    ime = input('Ime sladice>')
    datum = date.today()
    cena = vnesi_stevilo('Prodajna cena>')
    print('Izberite strošek:')
    strošek = izberi_strošek(slaščičar.vsi_stroški)
    print("Izberite na kakšen način ste prodali sladico. Če sladice še niste prodali, izberite možnost 'None'.")
    prodaja = izberi_prodajo([None] + slaščičar.prodaje)
    slaščičar.dodaj_sladico(ime, datum, cena, strošek, prodaja)
    print('Sladica uspešno dodana!')


def neprodane_sladice():
    for sladica  in slaščičar.vse_sladice:
        if sladica.prodaja is None:
            print(f'{sladica.ime}: {sladica.cena}€')

def vse_sladice():
    print(slaščičar.vse_sladice)

def stanje_denarja():
    print(f'Vaš dobiček je {prikaz_skupnega_dobička(slaščičar.dobiček())}')


zacetna_stran()
osnovne_meni()
           



