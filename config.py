"""
config.py - Načítání a validace YAML konfigurace.

Tento modul obsahuje funkci pro načtení YAML konfigurace ze souboru
a její převod na Python slovník.
"""

import yaml

def load_config(config_path):
    """
    Načte YAML konfiguraci ze souboru a vrátí ji jako Python slovník.
    
    Args:
        config_path (str): Cesta k souboru s konfigurací.
    
    Returns:
        dict: Načtená konfigurace.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    # Zde by mohla být přidána validace (např. kontrola formátu IP adres)
    return config
