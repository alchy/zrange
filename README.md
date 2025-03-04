# Some IP Address Segmentation Tool

## Popis
Tento nástroj slouží k segmentaci IP adresního prostoru v Azure prostředí. Na základě vstupní YAML konfigurace přiděluje IP adresy datacentrům, subskripcím, virtuálním sítím (VNet) a podsítím (subnet). Výstup je generován jak do Markdown souboru, tak na konzoli.

## Struktura projektu
- `config.py`: Načítání a validace YAML konfigurace.
- `ip_manager.py`: Správa IP adres a přidělování podsítí.
- `allocator.py`: Logika pro rekurzivní přidělování IP rozsahů.
- `output.py`: Generování výstupu do Markdownu a na konzoli.
- `main.py`: Hlavní skript, který propojuje všechny moduly.

## Použití
1. **Připravte konfiguraci**: Vytvořte YAML soubor (např. `config.yaml`) s definicí dostupných IP adres, hierarchie prostředků a požadavků na adresaci.
   
   Příklad:
   ```yaml
   address_spaces:
     - 10.64.0.0/16
   resources:
     - type: region
       name: we
       subscriptions:
         - type: subscription
           name: subscr01
           vnets:
             - type: vnet
               name: vnet1
               subnets:
                 - type: subnet
                   name: subn1
   addressing:
     default:
       region: equal
       subscription: equal
       vnet: equal
       subnet: equal
     specific:
       - type: region
         name: we
         size: /16
    ```

odkazy: [IP Calculator](https://www.calculator.net/ip-subnet-calculator.html)
