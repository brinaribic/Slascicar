import json

class Uporabnik:

    def __init__(self, uporabnisko_ime, zasifrirano_geslo, slascicar):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.slascicar = slascicar
    
    def preveri_geslo(self, zasifrirano_geslo):
        if self.zasifrirano_geslo != zasifrirano_geslo:
            raise ValueError('Geslo je napacno!')
    
    def shrani_stanje(self, ime_datoteke):
        slovar_s_sladicami = {
            'uporabnisko_ime': self.uporabnisko_ime,
            'zasifrirano_geslo': self.zasifrirano_geslo,
            'slascicar': self.slascicar.slovar_sladic(),
        }
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(slovar_s_sladicami, datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_s_sladicami = json.load(datoteka)
        uporabnisko_ime = slovar_s_sladicami['uporabnisko_ime']
        zasifrirano_geslo = slovar_s_sladicami['zasifrirano_geslo']
        slascicar = Slascicar.nalozi_iz_slovarja(slovar_s_sladicami['slascicar'])
        return cls(uporabnisko_ime, zasifrirano_geslo, slascicar)

class Slascicar:

    def __init__(self):
        self.prodaje = []
        self.vsi_stroski = []
        self.vse_sladice = []
        self._imena_prodajanih_sladic = []
        self._vrste_prodaj = {}
        self._sladice_prodaje = {}
        self._imena_stroskov = {}
        self._sladice_stroski = {}
        
    def dodaj_prodajo(self, vrsta):
        if vrsta in self._vrste_prodaj:
            raise ValueError('Vrsta te prodaje ze obstaja!')
        nova_prodaja = Prodaja(vrsta, self)
        self.prodaje.append(nova_prodaja)
        self._vrste_prodaj[vrsta] = nova_prodaja
        self._sladice_prodaje[nova_prodaja] = []
        return nova_prodaja

    def dodaj_strosek(self, ime, strosek):
        if ime in self._imena_stroskov:
            raise ValueError('Strosek s tem imenom ze obstaja!')
        nov_strosek = Strosek(ime, strosek, self)
        self.vsi_stroski.append(nov_strosek)
        self._imena_stroskov[ime] = nov_strosek
        self._sladice_stroski[nov_strosek] = []
        return nov_strosek

    def dodaj_sladico(self, ime, datum, cena, strosek, prodaja):
        self._preveri_prodajo(prodaja)
        self._preveri_strosek(strosek)          
        nova_sladica = Sladica(ime, datum, cena, strosek, prodaja)
        self.vse_sladice.append(nova_sladica)
        self._sladice_stroski[strosek].append(nova_sladica)
        self._sladice_prodaje[prodaja].append(nova_sladica)
        return nova_sladica

    def _preveri_prodajo(self, prodaja):
        if prodaja is not None and prodaja.slascicar != self:
            raise ValueError(f'Prodaja {prodaja} ne spada v to slascicarno!')

    def _preveri_strosek(self, strosek):
        if strosek.slascicar != self:
            raise ValueError(f'Strosek {strosek} ne spada v to slascicarno!')

    def poisci_prodajo(self, vrsta):
        return self._vrste_prodaj[vrsta]

    def poisci_strosek(self, ime):
        return self._imena_stroskov[ime]

    def sladice_po_prodajah(self, prodaja):
        yield from self._vrste_prodaj[prodaja]

    def sladice_po_stroskih(self, strosek):
        yield from self._imena_stroskov[strosek]

    def prodane_sladice(self):
        prodane_sladice = []
        for sladica in self.vse_sladice:
            if sladica.prodaja.vrsta != 'prazno':
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

    def prodaj_sladico(self, sladica, nova_prodaja):
        self._preveri_prodajo(nova_prodaja)
        if sladica in self.neprodane_sladice():
            self.prodane_sladice().append(sladica)
            self.neprodane_sladice().remove(sladica)
            sladica.prodaja = nova_prodaja
        else:
            raise ValueError('Ta sladica je ze prodana!')  

    def prihodki(self):
        z = 0
        for sladica in self.vse_sladice:
            if sladica in self.prodane_sladice():
                z += int(sladica.cena)
        return z

    def stroski_skupno(self):
        z = 0
        for sladica in self.prodane_sladice():
            z += int(sladica.strosek.znesek)
        return z
    
    def dobicek(self):
        return int(self.prihodki() - self.stroski_skupno())

    def najbolj_prodajana_sladica(self):
        s = {}
        for sladica in self.prodane_sladice():
            if sladica not in s.values():
                s[sladica] = 1
            else:
                s[sladica] = s.get(sladica) + 1
        return max(s.values())
  
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
            } for sladica in self.vse_sladice],
        }

    @classmethod
    def nalozi_iz_slovarja(cls, slovar_sladic):
        slascicar = cls()
        for prodaja in slovar_sladic['prodaje']:
            dodaj_prodajo = slascicar.dodaj_prodajo(prodaja['vrsta'])
        for strosek in slovar_sladic['stroski']:
            dodaj_strosek = slascicar.dodaj_strosek(strosek['ime'], strosek['znesek'])
        for sladica in slovar_sladic['sladice']:
            slascicar.dodaj_sladico(
                sladica['ime'],
                sladica['datum'],
                sladica['cena'],
                slascicar._imena_stroskov[sladica['strosek']],
                slascicar._vrste_prodaj[sladica['prodaja']],
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
        self.vrsta = vrsta #po posti, osebno, ...
        self.slascicar = slascicar
        
    def __str__(self):
        return f'{self.vrsta}'

    def __repr__(self):
        return f'{self.vrsta}'

class Strosek:

    def __init__(self, ime, znesek, slascicar):
        self.ime = ime # npr. cena sestavin, postnina(prodaja po posti), dodatni delavec, ...
        self.znesek = int(znesek)
        self.slascicar = slascicar

    def __str__(self):
        return f'{self.ime}'

    def __repr__(self):
        return f'{self.ime}'

class Sladica:

    def __init__(self, ime, datum, cena, strosek, prodaja):
        self.ime = ime
        self.datum = datum
        self.cena = cena
        self.strosek = strosek
        self.prodaja = prodaja

    def __str__(self):
        return f'{self.ime}'

    def __repr__(self):
        return f'{self.ime}'

    def __lt__(self, other):
        return self.datum < other.datum

