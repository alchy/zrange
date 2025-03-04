"""
output.py - Generování výstupu do Markdownu a na konzoli.
"""

import ipaddress

def generate_markdown_table(allocations, output_path):
    """
    Vygeneruje Markdown soubor s hierarchicky odsazenými IP rozsahy ve formátu tabulky s tagy a rozsahem (od-do).
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("# Přidělené IP rozsahy\n\n")
        file.write("| Typ       | Název             | Nadřazený     | Rozsah (CIDR)      | Rozsah (od-do)         | Tagy            |\n")
        file.write("|-----------|-------------------|---------------|--------------------|------------------------|-----------------|\n")
        for allocation in allocations:
            write_allocation_table(file, allocation, parent_name=None, level=0)

def write_allocation_table(file, allocation, parent_name, level):
    """
    Rekurzivně zapisuje alokaci do tabulky s hierarchickým odsazením, tagy a rozsahem (od-do).
    
    Args:
        file: Otevřený soubor pro zápis.
        allocation: Slovník s informacemi o alokaci.
        parent_name: Jméno nadřazeného prvku (nebo None).
        level: Úroveň hierarchie (pro odsazení).
    """
    indent = "  " * level  # Odsazení dvěma mezerami na úroveň
    parent_display = parent_name if parent_name else "-"
    tags_display = ", ".join(allocation['tags']) if allocation['tags'] else "-"
    net = ipaddress.ip_network(allocation['range'], strict=False)
    ip_start = str(net.network_address)
    ip_end = str(net.broadcast_address)
    file.write(f"| {allocation['type'].capitalize()} | {indent}{allocation['name']} | {parent_display} | {allocation['range']} | {ip_start} - {ip_end} | {tags_display} |\n")
    if 'subscriptions' in allocation:
        for sub in allocation['subscriptions']:
            write_allocation_table(file, sub, allocation['name'], level + 1)
    if 'vnets' in allocation:
        for vnet in allocation['vnets']:
            write_allocation_table(file, vnet, allocation['name'], level + 1)
    if 'subnets' in allocation:
        for subnet in allocation['subnets']:
            write_allocation_table(file, subnet, allocation['name'], level + 1)

def print_to_console(allocations):
    """
    Vypíše přidělené IP rozsahy na konzoli s rozsahem (od-do), bez tagů.
    """
    print("Přidělené IP rozsahy:")
    for allocation in allocations:
        print_allocation(allocation, level=0)

def print_allocation(allocation, level):
    """
    Rekurzivně vypíše alokaci na konzoli s správným odsazením a rozsahem (od-do), bez tagů.
    """
    indent = "  " * level
    net = ipaddress.ip_network(allocation['range'], strict=False)
    ip_start = str(net.network_address)
    ip_end = str(net.broadcast_address)
    print(f"{indent}{allocation['type'].capitalize()} {allocation['name']}: {allocation['range']} ({ip_start} - {ip_end})")
    if 'subscriptions' in allocation:
        for sub in allocation['subscriptions']:
            print_allocation(sub, level + 1)
    if 'vnets' in allocation:
        for vnet in allocation['vnets']:
            print_allocation(vnet, level + 1)
    if 'subnets' in allocation:
        for subnet in allocation['subnets']:
            print_allocation(subnet, level + 1)
