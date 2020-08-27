from datetime import date
from model import Slascicar

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
    slascicar = Slascicar.nalozi_stanje(DATOTEKA_S_SLADICAMI)
except FileNotFoundError:
    slascicar = Slascicar()

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
            print(f'Prosim, da vnesete stevilo!')

def izberi(seznam):
    for indeks, (oznaka, _) in enumerate(seznam, 1):
        print(f'{indeks}) {oznaka}')
    while True:
        izbira = vnesi_stevilo('> ')
        if 1 <= izbira <= len(seznam):
            _, element = seznam[izbira - 1]
            return element
        else:
            print(f'Izberi stevilo med 1 in {len(seznam)}')

def prikaz_skupnega_dobicka(dobicek):
    if dobicek > 0:
        return f'{modro(dobicek)}€'
    elif dobicek < 0:
        return f'{rdece(dobicek)}€'
    else:
        return f'{dobicek}€'

def prikaz_sladice(sladica):
    if sladica in slascicar.prodane_sladice():
        return f'{modro(sladica)}'
    else:
        return f'{rdece(sladica)}'

def zacetna_stran():
    print(logo(LOGO))
    print ()
    print(krepko('Dobrodošli v programu Sladkosned!'))
    print()
    print('Za izhod pritisnite Ctrl-C')
    print(80 * '=')

def osnovne_meni():
    while True:
        try:
            print(prikaz_sladic())
            print(80 * '=')
            print('Kaj bi radi naredili?')
            print()
            moznosti = [
                ('dodaj prodajo', dodaj_prodajo),
                ('dodaj strosek', dodaj_strosek),
                ('dodaj sladico', dodaj_sladico),
                ('poglej neprodane sladice', neprodane_sladice),
                ('prodaj sladico', prodaj_sladico),
                ('poglej vse sladice', vse_sladice),
                ('poglej stanje', stanje),
            ]
            izbira = izberi(moznosti)
            izbira()
            print(80 * '=')
            print()
            input('Pritisnite Enter za shranjevanje in vrnitev v osnovni meni')
            print(80 * '=')
            slascicar.shrani_stanje(DATOTEKA_S_SLADICAMI)
        except ValueError as e:
            print(rdece(e.args[0]))
            print(80 * '=')
        except KeyboardInterrupt:
            print()
            print('Nasvidenje!')
            break

def prikaz_sladic():
    for sladica in slascicar.vse_sladice:
        if sladica.prodaja.vrsta  == 'prazno':
            print(f'{rdece(sladica.ime)}: {sladica.cena}€, dne {sladica.datum}')
        else:
            print(f'{modro(sladica.ime)}: {sladica.cena}€, dne {sladica.datum}')
    print(f'Dobicek: {prikaz_skupnega_dobicka(slascicar.dobicek())}')
 
def dodaj_prodajo():
    vrsta = input("Vnesite nacin prodaje sladice (npr. osebni prevzem,...), ce sladica ni prodana vnesite 'prazno'> ")
    slascicar.dodaj_prodajo(vrsta)

def dodaj_strosek():
    ime = input('Vnesite ime stroska (npr. sestavine, dodatni delavec, ...)> ')
    znesek = vnesi_stevilo('znesek> ')
    slascicar.dodaj_strosek(ime, znesek)

def dodaj_sladico():
    print('Vnesite podatke o sladici:')
    print()
    ime = input('Ime sladice>')
    datum = date.today()
    cena = vnesi_stevilo('Prodajna cena>')
    print('Izberite strosek:')
    strosek = izberi_strosek(slascicar.vsi_stroski)
    print("Izberite na kaksen nacin ste prodali sladico.")
    prodaja = izberi_prodajo(slascicar.prodaje)
    slascicar.dodaj_sladico(ime, datum, cena, strosek, prodaja)
    print('Sladica uspesno dodana!')

def izberi_strosek(stroski):
    return izberi([(strosek, strosek)for strosek in stroski],)

def izberi_prodajo(prodaje):
    return izberi([(prodaja, prodaja)for prodaja in prodaje],)

def neprodane_sladice():
    if len(slascicar.neprodane_sladice()) == 0:
        raise ValueError('Vse sladice so že prodane!')
    for sladica in slascicar.vse_sladice:
        if sladica.prodaja.vrsta == 'prazno':
            print(f'{rdece(sladica.ime)}: {sladica.cena}€')

def izberi_neprodano_sladico(sladice):
    return izberi([(sladica, sladica) for sladica in sladice])

def prodaj_sladico():
    if len(slascicar.neprodane_sladice()) == 0:
        raise ValueError('Vse sladice so že prodane!')
    print('katero sladico bi prodali?')
    sladica = izberi_neprodano_sladico(slascicar.neprodane_sladice())
    print('Na kaksen nacin ste prodali sladico?')
    nova_prodaja = izberi_prodajo(slascicar.prodaje)
    slascicar.prodaj_sladico(sladica, nova_prodaja)
    print('Uspešno ste prodali sladico!')

def vse_sladice():
    for sladica in slascicar.vse_sladice:
        if sladica.prodaja.vrsta == 'prazno':
            print(f'{rdece(sladica.ime)}: {sladica.cena}€, dne {sladica.datum}')
        else:
            print(f'{modro(sladica.ime)}: {sladica.cena}€, dne {sladica.datum}') 

def stanje():
    print(f'Skupni stroski so {slascicar.stroski_skupno()}€')
    print(f'Vas dobicek je {prikaz_skupnega_dobicka(slascicar.dobicek())}')
    print(f'Skupni prihodki so {slascicar.prihodki()}€')
    print(f'Najpogostejša prodaja je {slascicar.najpogostejsa_prodaja()}')
    print(f'Največji strošek je {slascicar.najvecji_stroski()}€')
    print(f'Najdrazja sladica je {prikaz_sladice(slascicar.najdrazja_sladica())}')


zacetna_stran()
osnovne_meni()
           