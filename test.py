from datetime import date
from model import Slascicar, Prodaja, Strosek, Sladica

slascicar = Slascicar()

posta = slascicar.dodaj_prodajo('po posti')
osebno = slascicar.dodaj_prodajo('osebno')

sestavine = slascicar.dodaj_strosek('sestavine', 20)
dodatni_delavec = slascicar.dodaj_strosek('dodatni_delavec', 50)

torta = slascicar.dodaj_sladico('visnjeva_torta', date(2020, 6, 12), 50, sestavine, posta)
torta = slascicar.dodaj_sladico('visnjeva_torta', date(2020, 6, 12), 50, sestavine, posta)
torta = slascicar.dodaj_sladico('visnjeva_torta', date(2020, 6, 12), 50, sestavine, posta)
makroni = slascicar.dodaj_sladico('makroni', date(2020, 7, 19), 10, dodatni_delavec, osebno)
mafini = slascicar.dodaj_sladico('mafini', date(2020, 7, 19), 20, sestavine, osebno)
torta = slascicar.dodaj_sladico('cokoladna_torta', date(2020, 6, 12), 100, sestavine, osebno)

print(slascicar._vrste_prodaj)

print(slascicar.prihodki())

print(slascicar.dobicek())

print(slascicar.slovar_sladic()["stroski"])

for strosek in slascicar.slovar_sladic()['stroski']:
    #dodaj_strosek = slascicar.dodaj_strosek(strosek['ime'], strosek['znesek'])
    print(strosek['ime'])