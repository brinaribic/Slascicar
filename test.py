from datetime import date
from model import Slaščičar, Prodaja, Strošek, Sladica

slaščičar = Slaščičar()

pošta = slaščičar.dodaj_prodajo('po pošti')
osebno = slaščičar.dodaj_prodajo('osebno')

sestavine = slaščičar.dodaj_strošek('sestavine', 20)
dodatni_delavec = slaščičar.dodaj_strošek('dodatni_delavec', 50)

torta = slaščičar.dodaj_sladico('višnjeva_torta', date(2020, 6, 12), 50, sestavine, pošta)
torta = slaščičar.dodaj_sladico('višnjeva_torta', date(2020, 6, 12), 50, sestavine, pošta)
torta = slaščičar.dodaj_sladico('višnjeva_torta', date(2020, 6, 12), 50, sestavine, pošta)
makroni = slaščičar.dodaj_sladico('makroni', date(2020, 7, 19), 10, dodatni_delavec, osebno)
mafini = slaščičar.dodaj_sladico('mafini', date(2020, 7, 19), 20, sestavine, osebno)
torta = slaščičar.dodaj_sladico('čokoladna_torta', date(2020, 6, 12), 100, sestavine)

print(slaščičar.neprodane_sladice_cena())

print(slaščičar.neprodane_sladice())

print(slaščičar.prodane_sladice())

print(slaščičar._sladice_stroski)

print(slaščičar.najbolj_prodajana_sladica())