import re
from abc import ABC, abstractmethod

# ==========================================================
# 1. Abstraktní třída PDU (Protocol Data Unit)
# ==========================================================
class PDU(ABC):
    def __init__(self, payload: str):
        # Bezpečnostní pojistka: Zamezí vytvoření "holého" PDU
        if type(self) is PDU:
            raise TypeError("Nelze instancovat abstraktní třídu PDU nezávisle (bez obalu).")
        
        # Protected (chráněná) proměnná s daty
        self._payload = payload

    @property
    def payload(self) -> str:
        """ Getter (vrací aktuální datový náklad) """
        return self._payload

    @payload.setter
    def payload(self, val: str):
        """ Setter (bezpečnostní zápis nových dat do PDU) """
        self._payload = val

    # Pro případ, že chcete používat i klasický notový zápis (typické pro JS/PHP)
    def getPayload(self) -> str:
        return self.payload

    def setPayload(self, val: str):
        self.payload = val

    @abstractmethod
    def isValid(self) -> bool:
        """ 
        Abstraktní kontrakt: Každý potomek, který dědí (obaluje PDU),
        musí implementovat svou vlastní rutinu pro ověření datové neporušenosti.
        """
        pass


# ==========================================================
# 2. Třída EthFrame (Ethernetový rámec)
# ==========================================================
class EthFrame(PDU):
    def __init__(self, dmac: str, smac: str, type_id: int, payload: str, fcs: int = None):
        # Okamžitě volá chráněný konstruktor svého rodiče PDU
        super().__init__(payload)
        
        # Detainí validace MAC adres přes statickou metodu pře samotným inicializováním
        if not EthFrame.isValidMac(dmac):
            raise ValueError(f"Kritická chyba: Nesmyslný formát cílové MAC (DMAC): '{dmac}'")
        if not EthFrame.isValidMac(smac):
            raise ValueError(f"Kritická chyba: Nesmyslný formát zdrojové MAC (SMAC): '{smac}'")
            
        # Atributy chráněné zvenčí
        self._dmac = dmac
        self._smac = smac
        self._type = type_id
        
        # FCS je buď vygenerováno validně, nebo dosazeno uměle jako poškozené ručně
        if fcs is None:
            self._recalculateFcs() # Vypočítáme hashový součet dat
        else:
            self._fcs = fcs

    @staticmethod
    def isValidMac(mac: str) -> bool:
        """ Statická utilita pro regexovou validaci vzhledu MAC adresy. """
        pattern = r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"
        return bool(re.match(pattern, mac))

    # ---- Vlastní Gettery & Settery s chytrou Auto-Hash logikou ----

    @property
    def dmac(self) -> str:
        return self._dmac

    @dmac.setter
    def dmac(self, val: str):
        if not EthFrame.isValidMac(val):
            raise ValueError("Neplatný formát MAC adresy.")
        self._dmac = val
        self._recalculateFcs() # Ihned po přepsání provést re-hash hlavičky!

    @property
    def smac(self) -> str:
        return self._smac

    @smac.setter
    def smac(self, val: str):
        if not EthFrame.isValidMac(val):
            raise ValueError("Neplatný formát MAC adresy.")
        self._smac = val
        self._recalculateFcs() # Ihned zvalidovat updatovaný rámec!

    @property
    def type(self) -> int:
        return self._type

    @type.setter
    def type(self, val: int):
        self._type = val
        self._recalculateFcs() # Ihned zvalidovat updatovaný rámec!

    @property
    def fcs(self) -> int:
        """ Getter vrací uložený patičkový součet; úmyslně nemá definovaný zvenčí setter """
        return self._fcs

    # ---- PŘETÍŽENÍ POTOMKA: Overriding Payload z Parent PDU ----
    @property
    def payload(self) -> str:
        # Použití rodičovského chování 
        return super().payload

    @payload.setter
    def payload(self, val: str):
        # 1. Použijeme rodičovský Setter z PDU pro bezpečné zpracovaní změny
        PDU.payload.fset(self, val)
        # 2. V dceři okamžitě přepálíme Hash (chytrá modifikace vlastnosti rodiče)
        self._recalculateFcs()

    # ---- Třídní Instanční Metody ----

    def calculateFcs(self) -> int:
        """ Algoritmus složitějšího ASCII Hashe datového obsahu hlavičky i potomka """
        data_to_hash = f"{self._dmac}{self._smac}{self._type}{self.payload}"
        hash_val = 0
        for char in data_to_hash:
            # Shift-and-add ASCII hash algoritmus a & 0xFFFFFFFF pro simulaci limitu na 32bit datový typ
            hash_val = ((hash_val << 5) - hash_val + ord(char)) & 0xFFFFFFFF
        return hash_val

    def _recalculateFcs(self):
        """ Privátní protected obálka zkracující generaci nového hashe (vyhneme se psaní dlouhé stěny v seterech) """
        self._fcs = self.calculateFcs()

    def isValid(self) -> bool:
        """
        Závěrečná overriding kontrolní validace z parenta.
        Během vyvolání si fyzicky přepočte teď právě obsah na hash a porovnává s uloženými daty v patičce.
        """
        return self._fcs == self.calculateFcs()

    def __str__(self) -> str:
        """ Magická metoda renderující text do konzole. """
        return f"[EthFrame] SRC: {self._smac} DST: {self._dmac} DATA: {self.payload}"

    # ---- Výukové Simulace Chyb (Škodící metoda) ----

    def corruptData(self):
        """ 
        Demoliční zbraň stavěná čistě pro demonstrační použití destrukce transportní architektury paketu. 
        """
        # 1. Zničí uvnitř rodičovské platformy data a úmyslně ZAKÁŽE logiku dceřiného chytrého property setteru (nebude re-hash)!
        PDU.payload.fset(self, "!!_[CORRUPTED_CRASH_DATA_PAYLOAD]_!!")
        
        # 2. Natvrdo přepálí v dceři patičkový Frame Check vlastním vymyšleným číslem
        self._fcs = 9999999999  


if __name__ == "__main__":
    # Korektní stavba
    frame = EthFrame(dmac="00:1A:2B:3C:4D:5E", smac="5E:4D:3C:2B:1A:00", type_id=0x0800, payload="AHOJ_SVETE")
    
    print(frame) 
    print(f"Rámec vycestoval - Je validní při letu?: {frame.isValid()}") # Očekáváme True

    # Smart modifikace obsahu uživatelem vyvolá korektní Re-hash a přežije kontrolu
    print("\n[Změna hodnot]")
    frame.payload = "JINY_TEXT_OD_UZIVATELE"
    frame.dmac = "FF:FF:FF:FF:FF:FF"
    print(f"Rámec modifikován (re-hash) - Je validní?: {frame.isValid()}") # Očekáváme True
    print(frame)

    # Nasilný výbuch a přepsání paketových dat zákeřníkem:
    print("\n[Vniknutí hackera na uzel a Error přenosu]")
    frame.corruptData()
    print(frame)
    print(f"Rámec zasažen - Je pak validní na routeru?: {frame.isValid()}") # Očekáváme obranu a False
