# IP Address Segmentation Helper for Azure

## Popis
Tento nástroj slouží k segmentaci IP adresního prostoru a měl by zjednodušit práci při přidělování IP rozsahů na úrovni jednotlivých Azure prostředí. Na základě vstupní YAML konfigurace přiděluje IP adresy datacentrům, subskripcím, virtuálním sítím (VNet) a podsítím (subnet). Výstup je generován jak do Markdown souboru, tak na konzoli.

## Struktura projektu
- `config.py`: Načítání a validace YAML konfigurace.
- `ip_manager.py`: Správa IP adres a přidělování podsítí.
- `allocator.py`: Logika pro rekurzivní přidělování IP rozsahů.
- `output.py`: Generování výstupu do Markdownu a na konzoli.
- `main.py`: Hlavní skript, který propojuje všechny moduly.

## Použití
YAML soubor (např. `ztest1.yaml`) s definicí dostupných IP adres, hierarchie prostředků a požadavků na adresaci.

odkazy: [IP Calculator](https://www.calculator.net/ip-subnet-calculator.html)
