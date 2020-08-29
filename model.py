import json

class Slascicar:

    def __init__(self):
        self.prodaje = []
        self.vsi_stroski = []
        self.vse_sladice = []
        self._vrste_prodaj = {}
        self._imena_stroskov = {}
        self._imena_sladic = {}
        
    def dodaj_prodajo(self, vrsta):
        if vrsta in self._vrste_prodaj:
            raise ValueError('Vrsta te prodaje že obstaja!')
        nova_prodaja = Prodaja(vrsta, self)
        self.prodaje.append(nova_prodaja)
        self._vrste_prodaj[vrsta] = nova_prodaja
        return nova_prodaja

    def dodaj_strosek(self, ime, strosek):
        if ime in self._imena_stroskov:
            raise ValueError('Strošek s tem imenom že obstaja!')
        nov_strosek = Strosek(ime, strosek, self)
        self.vsi_stroski.append(nov_strosek)
        self._imena_stroskov[ime] = nov_strosek
        return nov_strosek

    def dodaj_sladico(self, ime, datum, cena, strosek, prodaja, kolicina):
        self._preveri_prodajo(prodaja)
        self._preveri_strosek(strosek)         
        nova_sladica = Sladica(ime, datum, cena, strosek, prodaja, kolicina)
        self.vse_sladice.append(nova_sladica)
        self._imena_sladic[ime] = nova_sladica
        return nova_sladica

    def _preveri_prodajo(self, prodaja):
        if prodaja.slascicar != self:
            raise ValueError(f'Prodaja {prodaja} ne spada v to slaščičarno!')

    def _preveri_strosek(self, strosek):
        if strosek.slascicar != self:
            raise ValueError(f'Strosek {strosek} ne spada v to slaščičarno!')

    def poisci_prodajo(self, vrsta):
        return self._vrste_prodaj[vrsta]

    def poisci_strosek(self, ime):
        return self._imena_stroskov[ime]

    def poisci_sladico(self, ime):
        return self._imena_sladic[ime]

    def sladice_po_prodajah(self, prodaja):
        yield from self._vrste_prodaj[prodaja]

    def sladice_po_stroskih(self, strosek):
        yield from self._imena_stroskov[strosek]

    def prodane_sladice(self):
        prodane_sladice = []
        for sladica in self.vse_sladice:
            if sladica.prodaja.vrsta != 'neprodano':
                prodane_sladice.append(sladica) 
        return prodane_sladice

    def neprodane_sladice(self):
        neprodane = []
        for sladica in self.vse_sladice:
            if sladica.prodaja.vrsta == 'neprodano':
                neprodane.append(sladica)
        return neprodane
          
    def prodaj_sladico(self, sladica, nova_prodaja, kolicina):
        self._preveri_prodajo(nova_prodaja)
        if kolicina > sladica.kolicina or kolicina < 1:
            raise ValueError('Toliko sladice ne morete prodati!')
        elif sladica in self.neprodane_sladice():
            self.vse_sladice.remove(sladica)
            neprodana_kolicina = sladica.kolicina - kolicina
            if neprodana_kolicina != 0:
                neprodana_sladica = Sladica(
                    sladica.ime, sladica.datum, 
                    sladica.cena, 
                    sladica.strosek, 
                    sladica.prodaja, 
                    neprodana_kolicina)
                self.vse_sladice.append(neprodana_sladica)
                self.neprodane_sladice().append(neprodana_sladica)
                prodana_sladica = Sladica(sladica.ime, 
                    sladica.datum, 
                    sladica.cena, 
                    sladica.strosek, 
                    nova_prodaja, 
                    kolicina)
                self.vse_sladice.append(prodana_sladica)
                self.prodane_sladice().append(prodana_sladica)
            else:
                self.prodane_sladice().append(sladica)
                sladica.prodaja = nova_prodaja
        else:
            raise ValueError('Ta sladica je ze prodana!') 

    def prihodki(self):
        z = 0
        for sladica in self.vse_sladice:
            if sladica in self.prodane_sladice():
                z += int(sladica.cena * sladica.kolicina)
        return z

    def stroski_skupno(self):
        z = 0
        for sladica in self.prodane_sladice():
            z += int(sladica.strosek.znesek * sladica.kolicina)
        return z
    
    def dobicek(self):
        return int(self.prihodki() - self.stroski_skupno())

    def najpogostejsa_prodaja(self):
        s = [sladica.prodaja.vrsta for sladica in self.vse_sladice]
        if s == []:
            pass
        else:
            return max(set(s), key = s.count)

    def najvecji_stroski(self):
        if set(strosek.znesek for strosek in self.vsi_stroski) == set():
            pass
        else:
            m = max(set(strosek.znesek for strosek in self.vsi_stroski))
            for strosek in self.vsi_stroski:
                if m == strosek.znesek:
                    return  strosek.ime

    def najdrazja_sladica(self):
        if len(self.vse_sladice) == 0:
            pass
        else:
            m = max(set(sladica.cena for sladica in self.vse_sladice))
            for sladica in self.vse_sladice:
                if m == sladica.cena:
                    return sladica.ime
        
    def slovar_sladic(self):
        return {
            'prodaje': [{
                'vrsta': prodaja.vrsta,
            } for prodaja in self.prodaje],
            'stroski': [{
                'ime': strosek.ime,
                'znesek': strosek.znesek,
            } for strosek in self.vsi_stroski],
            'sladice': [{
                'ime': sladica.ime,
                'datum': str(sladica.datum),
                'cena': sladica.cena,
                'strosek': sladica.strosek.ime,
                'prodaja': sladica.prodaja.vrsta,
                'kolicina': sladica.kolicina,
            } for sladica in self.vse_sladice],
        }

    @classmethod
    def nalozi_iz_slovarja(cls, slovar_sladic):
        slascicar = cls()
        for prodaja in slovar_sladic['prodaje']:
            slascicar.dodaj_prodajo(prodaja['vrsta'])
        for strosek in slovar_sladic['stroski']:
            slascicar.dodaj_strosek(strosek['ime'], strosek['znesek'])
        for sladica in slovar_sladic['sladice']:
            slascicar.dodaj_sladico(
                sladica['ime'],
                sladica['datum'],
                sladica['cena'],
                slascicar._imena_stroskov[sladica['strosek']],
                slascicar._vrste_prodaj[sladica['prodaja']],
                sladica['kolicina'],
            )
        return slascicar
    
    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.slovar_sladic(), datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_sladic = json.load(datoteka)
        return cls.nalozi_iz_slovarja(slovar_sladic)

class Prodaja:

    def __init__(self, vrsta, slascicar):
        self.vrsta = vrsta 
        self.slascicar = slascicar
        
    def __str__(self):
        return f'{self.vrsta}'

    def __repr__(self):
        return f'{self.vrsta}'

class Strosek:

    def __init__(self, ime, znesek, slascicar):
        self.ime = ime
        self.znesek = int(znesek)
        self.slascicar = slascicar

    def __str__(self):
        return f'{self.ime}'

    def __repr__(self):
        return f'{self.ime}'

class Sladica:

    def __init__(self, ime, datum, cena, strosek, prodaja, kolicina):
        self.ime = ime
        self.datum = datum
        self.cena = cena 
        self.strosek = strosek
        self.prodaja = prodaja
        self.kolicina = int(kolicina)

    def __str__(self):
        return f'{self.ime}: {self.kolicina}'

    def __repr__(self):
        return f'{self.ime}: {self.kolicina}'

    def __lt__(self, other):
        return self.datum < other.datum