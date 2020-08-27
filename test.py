from datetime import date
from model import Slascicar, Prodaja, Strosek, Sladica

slascicar = Slascicar()

posta = slascicar.dodaj_prodajo('po posti')
osebno = slascicar.dodaj_prodajo('osebno')
niprodano = slascicar.dodaj_prodajo('prazno')

sestavine = slascicar.dodaj_strosek('sestavine', 20)
dodatni_delavec = slascicar.dodaj_strosek('dodatni_delavec', 50)

torta = slascicar.dodaj_sladico('torta', date.today(), 50, sestavine, niprodano)
mafini = slascicar.dodaj_sladico('mafini', date.today(), 10, sestavine, osebno)
makroni = slascicar.dodaj_sladico('makroni', date.today(), 10, sestavine, osebno)

print(slascicar.najpogostejsa_prodaja())
print(slascicar.najpogostejsi_stroski())
print(slascicar.najvecji_stroski())
