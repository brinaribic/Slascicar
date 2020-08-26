from datetime import date
from model import Slascicar, Prodaja, Strosek, Sladica

slascicar = Slascicar()

posta = slascicar.dodaj_prodajo('po posti')
osebno = slascicar.dodaj_prodajo('osebno')
niprodano = slascicar.dodaj_prodajo('prazno')

sestavine = slascicar.dodaj_strosek('sestavine', 20)
dodatni_delavec = slascicar.dodaj_strosek('dodatni_delavec', 50)

torta = slascicar.dodaj_sladico('visnjeva_torta', date(2020, 6, 12), 50, sestavine, posta)
mafini = slascicar.dodaj_sladico('mafini', date(2020, 7, 19), 20, sestavine, niprodano)

torta = slascicar.dodaj_sladico('visnjeva_torta', date(2020, 6, 12), 50, sestavine, posta)
torta = slascicar.dodaj_sladico('visnjeva_torta', date(2020, 6, 12), 50, sestavine, posta)
makroni = slascicar.dodaj_sladico('makroni', date(2020, 7, 19), 10, dodatni_delavec, osebno)

torta = slascicar.dodaj_sladico('cokoladna_torta', date(2020, 6, 12), 100, sestavine, niprodano)

print(slascicar.poisci_sladico('makroni'))
