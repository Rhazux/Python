def bmi(vyska, hmotnost):
    return hmotnost / (vyska ** 2)

def kategorie_bmi(hodnota_bmi):
    if hodnota_bmi < 18.5:
        return "Podváha"
    elif 18.5 <= hodnota_bmi < 25:
        return "Normální váha"
    elif 25 <= hodnota_bmi < 30:
        return "Nadváha"
    else:
        return "Obezita"

# Načtení dat od uživatele
try:
    vyska = float(input("Zadej výšku v metrech (např. 1.75): "))
    hmotnost = float(input("Zadej hmotnost v kilogramech: "))
    
    if vyska <= 0 or hmotnost <= 0:
        print("Výška i hmotnost musí být kladná čísla!")
    else:
        vysledek_bmi = bmi(vyska, hmotnost)
        kategorie = kategorie_bmi(vysledek_bmi)

        print("\n--- Výsledek BMI ---")
        print(f"BMI: {vysledek_bmi:.2f}")
        print(f"Kategorie: {kategorie}")

except ValueError:
    print("Prosím, zadej platná čísla pro výšku a hmotnost.")