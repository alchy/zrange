"""
main.py - Hlavní skript pro segmentaci IP adres v Azure prostředí.
"""

import os
import sys
from config import load_config
from ip_manager import IPManager
from allocator import allocate_resources
from output import generate_markdown, print_to_console  # Changed back to generate_markdown

def main(config_path):
    """
    Hlavní funkce programu pro segmentaci IP adres.
    """
    config = load_config(config_path)
    ip_manager = IPManager(config['address_spaces'])
    allocations = allocate_resources(ip_manager, config['resources'], config['addressing'])
    
    base, _ = os.path.splitext(config_path)
    output_path = f"{base}.out.md"
    
    generate_markdown(allocations, output_path)  # Using regular list output with IP ranges
    print_to_console(allocations)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = 'config.yaml'
        print("Nebyl zadán vstupní soubor, používám výchozí 'config.yaml'")
    
    main(config_path)
    