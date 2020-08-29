from datetime import date
from model import Slascicar, Prodaja, Strosek, Sladica

slascicar = Slascicar()

posta = slascicar.dodaj_prodajo('po posti')
osebno = slascicar.dodaj_prodajo('osebno')
niprodano = slascicar.dodaj_prodajo('neprodano')

sestavine = slascicar.dodaj_strosek('sestavine', 20)
dodatni_delavec = slascicar.dodaj_strosek('dodatni_delavec', 50)

torta = slascicar.dodaj_sladico('torta', date.today(), 50, sestavine, niprodano, 5)
mafini = slascicar.dodaj_sladico('mafini', date.today(), 10, sestavine, osebno, 10)
makroni = slascicar.dodaj_sladico('makroni', date.today(), 10, sestavine, osebno, 20)

slascicar.prodaj_sladico(torta, osebno, 3)

slascicar.prodaj_sladico(torta, osebno, 2)

print(slascicar.prodane_sladice())
print(slascicar.neprodane_sladice())

