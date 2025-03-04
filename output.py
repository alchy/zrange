"""
output.py - Generování výstupu do Markdownu a na konzoli.
"""

import ipaddress

def generate_markdown_table(allocations, output_path):
    """
    Vygeneruje Markdown soubor s hierarchicky oddělenými IP rozsahy ve formátu tabulky s tagy.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("# Přidělené IP rozsahy\n\n")
        file.write("| Region | Subscription | Vnet      | Subnet         | Rozsah             | Tagy            |\n")
        file.write("|--------|--------------|-----------|----------------|--------------------|-----------------|\n")
        for allocation in allocations:
            write_allocation_table(file, allocation, level=0)

def write_allocation_table(file, allocation, level):
    """
    Rekurzivně zapisuje alokaci do tabulky s hierarchickým oddělením pomocí prázdných buněk.
    
    Args:
        file: Otevřený soubor pro zápis.
        allocation: Slovník s informacemi o alokaci.
        level: Úroveň hierarchie (0=region, 1=subscription, 2=vnet, 3=subnet).
    """
    net = ipaddress.ip_network(allocation['range'], strict=False)
    ip_start = str(net.network_address)
    ip_end = str(net.broadcast_address)
    tags_display = ", ".join(allocation['tags']) if allocation['tags'] else "-"
    range_display = f"{allocation['range']} ({ip_start} - {ip_end})"

    # Podle úrovně hierarchie vyplníme jen relevantní sloupce
    if level == 0:  # Region
        file.write(f"| {allocation['name']} |              |           |                | {range_display} | {tags_display} |\n")
    elif level == 1:  # Subscription
        file.write(f"|        | {allocation['name']} |           |                | {range_display} | {tags_display} |\n")
    elif level == 2:  # Vnet
        file.write(f"|        |              | {allocation['name']} |                | {range_display} | {tags_display} |\n")
    elif level == 3:  # Subnet
        file.write(f"|        |              |           | {allocation['name']} | {range_display} | {tags_display} |\n")

    # Rekurzivní volání pro podřízené položky
    if 'subscriptions' in allocation:
        for sub in allocation['subscriptions']:
            write_allocation_table(file, sub, level + 1)
    if 'vnets' in allocation:
        for vnet in allocation['vnets']:
            write_allocation_table(file, vnet, level + 1)
    if 'subnets' in allocation:
        for subnet in allocation['subnets']:
            write_allocation_table(file, subnet, level + 1)

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
    