class Slaščičar:

    def __init__(self):
        self.prodaje = []
        self.vsi_stroški = []
        self.vse_sladice = []
        self._imena_prodajanih_sladic = []
        self._vrste_prodaj = {}
        self._sladice_prodaje = {}
        self._imena_stroskov = {}
        self._sladice_stroski = {}
        
    def dodaj_prodajo(self, vrsta):
        nova_prodaja = Prodaja(vrsta, self)
        self.prodaje.append(nova_prodaja)
        self._vrste_prodaj[vrsta] = nova_prodaja
        self._sladice_prodaje[nova_prodaja] = []
        return nova_prodaja

    def dodaj_strošek(self, ime, strošek):
        if ime in self._imena_stroskov:
            raise ValueError('Strošek s tem imenom že obstaja!')
        nov_strošek = Strošek(ime, strošek, self)
        self.vsi_stroški.append(nov_strošek)
        self._imena_stroskov[ime] = nov_strošek
        self._sladice_stroski[nov_strošek] = []
        return nov_strošek

    def dodaj_sladico(self, ime, datum, cena, strošek, prodaja=None):
        self._preveri_prodajo(prodaja)
        self._preveri_strošek(strošek)
        nova_sladica = Sladica(ime, datum, cena, strošek, prodaja)
        self.vse_sladice.append(nova_sladica)
        self._sladice_stroski[strošek].append(nova_sladica)
        #self._vrste_prodaj[prodaja].append(nova_sladica)
        return nova_sladica

    def _preveri_prodajo(self, prodaja):
        if prodaja is not None and prodaja.slaščičar != self:
            raise ValueError(f'Prodaja {prodaja} ne spada v to slaščičarno!')

    def _preveri_strošek(self, strošek):
        if strošek.slaščičar != self:
            raise ValueError(f'Strošek {strošek} ne spada v to slaščičarno!')
            
    def odstrani_sladico(self, sladica):
        return self.vse_sladice.remove(sladica)

    def poisci_prodajo(self, vrsta):
        return self._vrste_prodaj[vrsta]

    def poisci_strošek(self, ime):
        return self._imena_stroskov[ime]

    def sladice_po_prodajah(self, prodaja):
        yield from self._vrste_prodaj[prodaja]

    def sladice_po_stroskih(self, strošek):
        yield from self._imena_stroskov[strošek]

    def prodane_sladice(self):
        prodane_sladice = []
        for sladica in self.vse_sladice:
            if sladica.prodaja != None:
                prodane_sladice.append(sladica)
                self._imena_prodajanih_sladic.append(sladica.ime)  
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

    def najbolj_prodajana_sladica(self):
        s = {}
        for sladica in self.prodane_sladice():
            if sladica not in s.values():
                s[sladica] = 1
            else:
                s[sladica] = s.get(sladica) + 1
        return max(s.values())
  
    def slovar_sladic(self):
        pass
class Prodaja:

    def __init__(self, vrsta, slaščičar):
        self.vrsta = vrsta #po pošti, osebno, ...
        self.slaščičar = slaščičar
        
    def __str__(self):
        return f'{self.vrsta}'

    def __repr__(self):
        return f'{self.vrsta}'

class Strošek:

    def __init__(self, ime, strošek, slaščičar):
        self.ime = ime # npr. cena sestavin, poštnina(prodaja po pošti), dodatni delavec, ...
        self.strošek = int(strošek)
        self.slaščičar = slaščičar

    def __str__(self):
        return f'{self.ime}'

    def __repr__(self):
        return f'{self.ime}'


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
