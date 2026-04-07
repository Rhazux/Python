# Dokumentace tříd `PDU` a `EthFrame`

Tento projekt ukazuje objektový návrh dvou tříd používaných pro jednoduchou simulaci síťové komunikace v Pythonu.  
Řešení je zaměřeno na abstraktní třídu, dědičnost, zapouzdření, přepis metod a kontrolu integrity dat.

---

## Obsah projektu

Projekt obsahuje dvě hlavní třídy:

- `PDU` – abstraktní základní třída pro obecnou datovou jednotku
- `EthFrame` – konkrétní třída reprezentující Ethernetový rámec

---

## 1. Třída `PDU`

### Popis
`PDU` (Protocol Data Unit) představuje obecnou datovou jednotku.  
Tato třída je abstraktní, takže z ní nelze vytvářet přímé instance.

Slouží jako základ pro další síťové objekty, které budou rozšiřovat její vlastnosti.

### Vlastnosti
- uchovává datový obsah `payload`
- poskytuje getter a setter pro bezpečnou práci s daty
- definuje abstraktní metodu `isValid()`

### Atributy
- `_payload` – chráněný atribut pro uložený datový náklad

### Metody

#### `__init__(payload: str)`
Inicializuje objekt a uloží datový náklad.  
Zároveň kontroluje, aby nebyla přímo vytvořena instance třídy `PDU`.

#### `payload`
Vlastnost pro čtení a zápis datového nákladu.

#### `getPayload()`
Vrací aktuální hodnotu `payload`.

#### `setPayload(val)`
Nastaví novou hodnotu `payload`.

#### `isValid()`
Abstraktní metoda, kterou musí implementovat každá děděná třída.

---

## 2. Třída `EthFrame`

### Popis
`EthFrame` reprezentuje Ethernetový rámec.  
Dědí z abstraktní třídy `PDU` a rozšiřuje ji o informace typické pro druhou vrstvu síťového modelu.

Rámec obsahuje:
- cílovou MAC adresu
- zdrojovou MAC adresu
- EtherType
- kontrolní součet `FCS`

### Atributy
- `_dmac` – cílová MAC adresa
- `_smac` – zdrojová MAC adresa
- `_type` – typ zapouzdřeného protokolu
- `_fcs` – kontrolní součet rámce
- `_payload` – zděděný datový obsah z třídy `PDU`

---

## Konstruktor

### `__init__(dmac: str, smac: str, type_id: int, payload: str, fcs: int = None)`

Při vytvoření objektu:

1. zavolá konstruktor rodičovské třídy `PDU`
2. zkontroluje validitu MAC adres
3. uloží hodnoty atributů
4. pokud není `fcs` zadáno, automaticky se vypočítá
5. pokud je `fcs` zadáno ručně, uloží se přímo

---

## Statická metoda

### `isValidMac(mac: str) -> bool`
Kontroluje, zda je MAC adresa ve správném formátu.

Použitý regulární výraz:

```python
^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$