"""
main.py - Hlavní skript pro segmentaci IP adres v Azure prostředí.
"""

import os
import sys
from config import load_config
from ip_manager import IPManager
from allocator import allocate_resources
from output import generate_markdown_table, print_to_console, generate_tags_file

def main(config_path, output_path=None):
    """
    Hlavní funkce programu pro segmentaci IP adres.
    """
    config = load_config(config_path)
    ip_manager = IPManager(config['address_spaces'])
    allocations = allocate_resources(ip_manager, config['resources'], config['addressing'])
    
    if output_path is None:
        base, _ = os.path.splitext(config_path)
        output_path = f"{base}.out.md"
    
    generate_markdown_table(allocations, output_path)
    tags_output_path = f"{os.path.splitext(output_path)[0]}.out.tags"  # Např. 'ztest2.out.tags'
    generate_tags_file(allocations, tags_output_path)
    print_to_console(allocations)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        config_path = sys.argv[1]
        output_path = sys.argv[2]
    elif len(sys.argv) > 1:
        config_path = sys.argv[1]
        output_path = None
    else:
        config_path = 'config.yaml'
        output_path = None
        print("Nebyl zadán vstupní soubor, používám výchozí 'config.yaml'")
    
    main(config_path, output_path)