"""
PROIECT DE SEMESTRU: ANALIZOR TEXT (OPTIUNEA C)
Autor: Student
Data: Ianuarie 2026
Versiune: Cu Jurnalizare DETALIATA (Rezultate complete in raport)
"""

import datetime

# ==========================================
# VARIABILE GLOBALE
# ==========================================
text_curent = ""
istoric = []


# ==========================================
# FUNCTII UTILITARE
# ==========================================

def log_actiune(titlu, detalii=""):
    """
    Adauga o actiune si rezultatul ei in istoric.
    """
    global istoric
    timp = datetime.datetime.now().strftime("%H:%M:%S")

    # Formatam frumos intrarea in log
    linie_log = f"[{timp}] --- {titlu} ---\n"
    if len(detalii) > 0:
        linie_log += detalii + "\n"

    istoric.append(linie_log)


def extrage_cuvinte(text):
    cuvinte = []
    cuvant_temp = ""
    i = 0
    while i < len(text):
        caracter = text[i]
        if caracter.isalnum():
            cuvant_temp = cuvant_temp + caracter.lower()
        else:
            if len(cuvant_temp) > 0:
                cuvinte.append(cuvant_temp)
                cuvant_temp = ""
        i = i + 1
    if len(cuvant_temp) > 0:
        cuvinte.append(cuvant_temp)
    return cuvinte


def numar_propozitii(text):
    nr = 0
    i = 0
    while i < len(text):
        if text[i] in ".!?":
            nr = nr + 1
        i = i + 1
    if nr == 0 and len(text) > 0:
        nr = 1
    return nr


# ==========================================
# FUNCTIONALITATI PRINCIPALE
# ==========================================

def incarca_text():
    global text_curent
    print("\n=== INCARCARE TEXT ===")
    print("1. Introducere manuala (tastatura)")
    print("2. Incarca text demonstrativ")
    print("3. Incarca din fisier")

    optiune = input("Alege optiunea: ")
    mesaj_log = ""

    if optiune == "1":
        print("Scrie textul (scrie 'GATA' pe o linie noua pentru a termina):")
        linii = []
        while True:
            linie = input()
            if linie == "GATA":
                break
            linii.append(linie)
        text_nou = ""
        index = 0
        while index < len(linii):
            text_nou = text_nou + linii[index] + "\n"
            index = index + 1
        text_curent = text_nou
        print("Text incarcat!")
        mesaj_log = "Utilizatorul a introdus text manual."

    elif optiune == "2":
        text_curent = "Python este un limbaj puternic. Avem un radar performant si un cojoc gros. Ana are mere."
        print("Text demonstrativ incarcat!")
        mesaj_log = "S-a incarcat textul demonstrativ (radar/cojoc)."

    elif optiune == "3":
        nume_fisier = input("Nume fisier: ")
        try:
            f = open(nume_fisier, "r")
            text_curent = f.read()
            f.close()
            print("Text incarcat din fisier!")
            mesaj_log = f"S-a incarcat fisierul: {nume_fisier}"
        except:
            print("Eroare la citirea fisierului.")
            mesaj_log = f"Eroare la incarcarea fisierului: {nume_fisier}"
    else:
        print("Optiune invalida.")
        mesaj_log = "Incercare incarcare text esuata (optiune gresita)."

    log_actiune("INCARCARE TEXT", mesaj_log)


def statistici_de_baza():
    global text_curent
    if len(text_curent) == 0:
        print("\n[!] Nu exista text incarcat!")
        return

    nr_caractere = len(text_curent)
    nr_fara_spatii = 0
    i = 0
    while i < len(text_curent):
        if text_curent[i] not in " \n":
            nr_fara_spatii = nr_fara_spatii + 1
        i = i + 1

    lista_cuvinte = extrage_cuvinte(text_curent)

    # Construim rezultatul intr-un string
    rezultat = f"Caractere (total): {nr_caractere}\n"
    rezultat += f"Caractere (fara spatii): {nr_fara_spatii}\n"
    rezultat += f"Cuvinte: {len(lista_cuvinte)}\n"
    rezultat += f"Propozitii: {numar_propozitii(text_curent)}"

    print(f"\n=== STATISTICI ===\n{rezultat}")

    # Salvam exact acest rezultat in istoric
    log_actiune("STATISTICI GENERATE", rezultat)


def frecventa_cuvinte():
    global text_curent
    if len(text_curent) == 0:
        print("\n[!] Nu exista text incarcat!")
        return

    lista_cuvinte = extrage_cuvinte(text_curent)
    frecvente = {}
    i = 0
    while i < len(lista_cuvinte):
        c = lista_cuvinte[i]
        if c in frecvente:
            frecvente[c] = frecvente[c] + 1
        else:
            frecvente[c] = 1
        i = i + 1

    lista_perechi = []
    for k in frecvente:
        lista_perechi.append((k, frecvente[k]))

    # Bubble sort descrescator
    n = len(lista_perechi)
    i = 0
    while i < n - 1:
        j = 0
        while j < n - i - 1:
            if lista_perechi[j][1] < lista_perechi[j + 1][1]:
                temp = lista_perechi[j]
                lista_perechi[j] = lista_perechi[j + 1]
                lista_perechi[j + 1] = temp
            j = j + 1
        i = i + 1

    # Construim string-ul cu top 5
    rezultat = ""
    limit = 0
    while limit < len(lista_perechi) and limit < 5:
        rezultat += f"{lista_perechi[limit][0]}: {lista_perechi[limit][1]} aparitii\n"
        limit = limit + 1

    print(f"\n=== TOP CUVINTE ===\n{rezultat}")
    log_actiune("FRECVENTA CUVINTE (TOP 5)", rezultat)


def histograma_lungimi():
    global text_curent
    if len(text_curent) == 0:
        print("\n[!] Lipsa text!")
        return
    lista = extrage_cuvinte(text_curent)
    lungimi = {}
    i = 0
    while i < len(lista):
        l = len(lista[i])
        if l in lungimi:
            lungimi[l] = lungimi[l] + 1
        else:
            lungimi[l] = 1
        i = i + 1

    # Construim histograma intr-un string
    rezultat = ""
    l = 1
    while l <= 15:
        if l in lungimi:
            bara = '#' * lungimi[l]
            rezultat += f"Lungime {l}: {bara} ({lungimi[l]})\n"
        l = l + 1

    print(f"\n=== HISTOGRAMA ===\n{rezultat}")
    log_actiune("HISTOGRAMA LUNGIMI", rezultat)


def cauta_in_text():
    global text_curent
    if len(text_curent) == 0:
        print("\n[!] Lipsa text!")
        return
    termen = input("Cauta: ").lower()
    lista = extrage_cuvinte(text_curent)
    nr = 0
    i = 0
    while i < len(lista):
        if lista[i] == termen:
            nr = nr + 1
        i = i + 1

    mesaj = f"Termenul '{termen}' a fost gasit de {nr} ori."
    print(mesaj)
    log_actiune("CAUTARE CUVANT", mesaj)


# ==========================================
# FUNCTIONALITATI SUPLIMENTARE
# ==========================================

def raport_vocale():
    global text_curent
    if len(text_curent) == 0:
        print("\n[!] Lipsa text!")
        return
    voc = 0
    cons = 0
    v = "aeiouAEIOU"
    i = 0
    while i < len(text_curent):
        c = text_curent[i]
        if c.isalpha():
            if c in v:
                voc = voc + 1
            else:
                cons = cons + 1
        i = i + 1

    rezultat = f"Numar Vocale: {voc}\nNumar Consoane: {cons}"
    print(f"\n=== RAPORT VOCALE ===\n{rezultat}")
    log_actiune("RAPORT VOCALE/CONSOANE", rezultat)


def gaseste_palindroame():
    global text_curent
    if len(text_curent) == 0:
        print("\n[!] Nu exista text incarcat!")
        return

    lista_cuvinte = extrage_cuvinte(text_curent)
    palindroame = []

    idx = 0
    while idx < len(lista_cuvinte):
        cuv = lista_cuvinte[idx]
        if len(cuv) > 2:
            stanga = 0
            dreapta = len(cuv) - 1
            e_palindrom = True
            while stanga < dreapta:
                if cuv[stanga] != cuv[dreapta]:
                    e_palindrom = False
                    break
                stanga = stanga + 1
                dreapta = dreapta - 1
            if e_palindrom:
                if cuv not in palindroame:
                    palindroame.append(cuv)
        idx = idx + 1

    rezultat = ""
    if len(palindroame) > 0:
        i = 0
        while i < len(palindroame):
            rezultat += f"- {palindroame[i]}\n"
            i = i + 1
    else:
        rezultat = "Nu s-au gasit palindroame."

    print(f"\n=== PALINDROAME GASITE ===\n{rezultat}")
    log_actiune("CAUTARE PALINDROAME", rezultat)


def cripteaza_text():
    global text_curent
    if len(text_curent) == 0:
        print("\n[!] Lipsa text!")
        return

    secret = ""
    i = 0
    while i < len(text_curent):
        c = text_curent[i]
        if c.isalpha():
            cod = ord(c)
            if c == 'z':
                secret += 'a'
            elif c == 'Z':
                secret += 'A'
            else:
                secret += chr(cod + 1)
        else:
            secret += c
        i = i + 1

    print("\n=== TEXT CRIPTAT ===")
    print(secret)

    # Salvam tot textul criptat in log
    log_actiune("CRIPTARE TEXT (Caesar +1)", secret)


def salvare_raport():
    global text_curent
    global istoric

    if len(text_curent) == 0 and len(istoric) == 0:
        print("\n[!] Nimic de salvat!")
        return

    try:
        f = open("raport.txt", "w")

        f.write("=======================================\n")
        f.write("      RAPORT FINAL PROIECT           \n")
        f.write("=======================================\n")
        f.write(f"Data si ora generarii: {datetime.datetime.now()}\n\n")

        f.write("sectiunea 1: TEXTUL ORIGINAL\n")
        f.write("---------------------------------------\n")
        if len(text_curent) > 0:
            f.write(text_curent + "\n")
        else:
            f.write("(Niciun text nu a fost incarcat)\n")

        f.write("\n\n")
        f.write("sectiunea 2: JURNAL COMPLET DE ACTIVITATE\n")
        f.write("---------------------------------------\n")
        f.write("(Aici sunt incluse toate rezultatele obtinute in sesiune)\n\n")

        i = 0
        while i < len(istoric):
            f.write(istoric[i] + "\n")
            f.write("-" * 30 + "\n")  # Separator intre actiuni
            i = i + 1

        f.close()
        print("Raportul DETALIAT a fost salvat in 'raport.txt'!")
        log_actiune("SALVARE", "Utilizatorul a exportat raportul pe disc.")

    except:
        print("Eroare la scrierea fisierului raport.txt")


# ==========================================
# MENIU
# ==========================================

def meniu_principal():
    global text_curent
    log_actiune("START APLICATIE", "Sesiune noua pornita.")

    while True:
        print("\n=== MENIU PRINCIPAL ===")
        print("1. Incarca text")
        print("2. Incarca DEMO (Palindroame)")
        print("3. Statistici")
        print("4. Frecventa")
        print("5. Histograma")
        print("6. Cautare")
        print("7. Vocale/Consoane")
        print("8. Palindroame")
        print("9. Criptare")
        print("10. Salvare Raport (Text + Jurnal)")
        print("0. Iesire")

        o = input("Optiune: ")

        if o == "1":
            incarca_text()
        elif o == "2":
            text_curent = "un radar performant si un cojoc gros capac"
            print("Text demo incarcat!")
            log_actiune("INCARCARE DEMO RAPID", "Text: un radar performant si un cojoc gros capac")
        elif o == "3":
            statistici_de_baza()
        elif o == "4":
            frecventa_cuvinte()
        elif o == "5":
            histograma_lungimi()
        elif o == "6":
            cauta_in_text()
        elif o == "7":
            raport_vocale()
        elif o == "8":
            gaseste_palindroame()
        elif o == "9":
            cripteaza_text()
        elif o == "10":
            salvare_raport()
        elif o == "0":
            log_actiune("IESIRE", "Aplicatie oprita.")
            break
        else:
            print("Optiune gresita!")


if __name__ == "__main__":
    meniu_principal()