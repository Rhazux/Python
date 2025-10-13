import math

def je_prvocislo(x: int) -> bool:
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    r = int(math.isqrt(x))
    for d in range(3, r + 1, 2):
        if x % d == 0:
            return False
    return True

# Načtení vstupu (n > 0)
while True:
    try:
        n = int(input("Zadej celé číslo n (> 0): "))
        if n > 0:
            break
        print("n musí být větší než 0.")
    except ValueError:
        print("Zadej prosím platné celé číslo.")

pocet_sudych = 0
pocet_lichych = 0
pocet_prvocisel = 0

# Výpis 1..n s vlastnostmi
for i in range(1, n + 1):
    sude = (i % 2 == 0)
    del3 = (i % 3 == 0)
    prv = je_prvocislo(i)

    if sude:
        pocet_sudych += 1
    else:
        pocet_lichych += 1
    if prv:
        pocet_prvocisel += 1

    print(
        f"{i}: "
        f"{'sudé' if sude else 'liché'}, "
        f"{'dělitelné 3' if del3 else 'nedělitelné 3'}, "
        f"{'prvočíslo' if prv else 'není prvočíslo'}"
    )

# Souhrn
print("\nSouhrn:")
print(f"Počet sudých čísel:   {pocet_sudych}")
print(f"Počet lichých čísel:  {pocet_lichych}")
print(f"Počet prvočísel:      {pocet_prvocisel}")