class Slaščičar:

    def __init__(self):
        self.prodaje = []
        self.vsi_stroški = []
        self.vse_sladice = []
        
    def dodaj_prodajo(self, ime):
        nova_prodaja = Prodaja(ime, self)
        self.prodaje.append(nova_prodaja)
        return nova_prodaja

    def dodaj_strošek(self, ime, strošek):
        nov_strošek = Strošek(ime, strošek, self)
        self.vsi_stroški.append(nov_strošek)
        return nov_strošek

    def dodaj_sladico(self, ime, datum, cena, strošek, prodaja=None):
        nova_sladica = Sladica(ime, datum, cena, strošek, prodaja)
        self.vse_sladice.append(nova_sladica)
        return nova_sladica

    def prodane_sladice(self):
        prodane_sladice = []
        for sladica in self.vse_sladice:
            if sladica.prodaja != None:
                prodane_sladice.append(sladica)
        return prodane_sladice

    def neprodane_sladice(self):
        neprodane = []
        for sladica in self.vse_sladice:
            if sladica not in self.prodane_sladice():
                neprodane.append(sladica)
        return neprodane

    def neprodane_sladice_cena(self):
        s = {}
        for sladica in self.neprodane_sladice():
            s[sladica] = sladica.cena
        return s

    def prihodki(self):
        z = 0
        for sladica in self.vse_sladice:
            if sladica.ime in self.prodane_sladice():
                z += sladica.cena
        return z
    
    def dobiček(self):
        return self.prihodki() - sum([strošek.strošek for strošek in self.vsi_stroški])
  
    
class Prodaja:

    def __init__(self, ime, slašččar):
        self.ime = ime #po pošti, osebno, ...
        self.slašččar = slašččar
        
    def __str__(self):
        return f'{self.ime}'

    def __repr__(self):
        return f'{self.ime}'

class Strošek:

    def __init__(self, ime, strošek, slaščičar):
        self.ime = ime # npr. cena sestavin, poštnina(prodaja po pošti), dodatni delavec, ...
        self.strošek = int(strošek)
        self.slaščičar = slaščičar

class Sladica:

    def __init__(self, ime, datum, cena, strošek, prodaja):
        self.ime = ime
        self.datum = datum
        self.cena = cena
        self.strošek = strošek
        self.prodaja = prodaja

    def __str__(self):
        return f'{self.ime}'

    def __repr__(self):
        return f'{self.ime}'
