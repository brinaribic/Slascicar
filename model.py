import json

class Uporabnik:

    def __init__(self, uporabnisko_ime, zasifrirano_geslo, slaščičar):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.slaščičar = slaščičar
    
    def preveri_geslo(self, zasifrirano_geslo):
        if self.zasifrirano_geslo != zasifrirano_geslo:
            raise ValueError('Geslo je napačno!')
    
    def shrani_stanje(self, ime_datoteke):
        slovar_sladic = {
            'uporabnisko_ime': self.uporabnisko_ime,
            'zasifrirano_geslo': self.zasifrirano_geslo,
            'slaščičar': self.slaščičar.slovar_sladic(),
        }
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(slovar_sladic, datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_sladic = json.load(datoteka)
        uporabnisko_ime = slovar_sladic['uporabnisko_ime']
        zasifrirano_geslo = slovar_sladic['zasifrirano_geslo']
        slaščičar = Slaščičar.nalozi_iz_slovarja(slovar_sladic['slaščičar'])
        return cls(uporabnisko_ime, zasifrirano_geslo, slaščičar)

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
        if vrsta in self._vrste_prodaj:
            raise ValueError('Vrsta te prodaje že obstaja!')
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
        return self.prihodki() - sum([strošek.znesek for strošek in self.vsi_stroški])

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
            'stroški': [{
                'ime': strošek.ime,
                'znesek': strošek.znesek,
            } for strošek in self.vsi_stroški],
            'sladice': [{
                'ime': sladica.ime,
                'datum': str(sladica.datum),
                'cena': sladica.cena,
                'strošek': sladica.storšek.ime,
                'prodaja': None if sladica.prodaja == None else sladica.prodaja.vrsta,
            } for sladica in self.vse_sladice],
        }

    @classmethod
    def nalozi_iz_slovarja(cls, slovar_sladic):
        slaščičar = cls()
        for prodaja in slovar_sladic['prodaje']:
            dodaj_prodajo = slaščičar.dodaj_prodajo(prodaja['vrsta'])
        for strošek in slovar_sladic['stroški']:
            dodaj_strošek = slaščičar.dodaj_strošek(strošek['ime'], strošek['razporeditev'])
        for sladica in slovar_sladic['sladice']:
            slaščičar.dodaj_sladico(
                sladica['znesek'],
                sladica['datum'],
                sladica['opis'],
                slaščičar._imena_stroskov[sladica['strošek']],
                slaščičar._vrste_prodaj[sladica['prodaja']],
            )
        return slaščičar
    
    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.slovar_sladic(), datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_sladic = json.load(datoteka)
        return cls.nalozi_iz_slovarja(slovar_sladic)
class Prodaja:

    def __init__(self, vrsta, slaščičar):
        self.vrsta = vrsta #po pošti, osebno, ...
        self.slaščičar = slaščičar
        
    def __str__(self):
        return f'{self.vrsta}'

    def __repr__(self):
        return f'{self.vrsta}'

class Strošek:

    def __init__(self, ime, znesek, slaščičar):
        self.ime = ime # npr. cena sestavin, poštnina(prodaja po pošti), dodatni delavec, ...
        self.znesek = int(znesek)
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
