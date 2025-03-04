"""
output.py - Generování výstupu do Markdownu a na konzoli.
"""

import ipaddress

def generate_markdown(allocations, output_path):
    """
    Vygeneruje Markdown soubor s přidělenými IP rozsahy ve formátu seznamu (bez tagů).
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("# Přidělené IP rozsahy\n\n")
        for allocation in allocations:
            write_allocation(file, allocation, level=0)

def write_allocation(file, allocation, level):
    """
    Rekurzivně zapisuje alokaci do souboru s správným odsazením (bez tagů), včetně rozsahu IP.
    """
    indent = "  " * level
    net = ipaddress.ip_network(allocation['range'], strict=False)
    ip_start = str(net.network_address)
    ip_end = str(net.broadcast_address)
    file.write(f"{indent}## {allocation['type'].capitalize()}: {allocation['name']}\n")
    file.write(f"{indent}- Rozsah: {allocation['range']} ({ip_start} - {ip_end})\n")
    if 'subscriptions' in allocation:
        for sub in allocation['subscriptions']:
            write_allocation(file, sub, level + 1)
    if 'vnets' in allocation:
        for vnet in allocation['vnets']:
            write_allocation(file, vnet, level + 1)
    if 'subnets' in allocation:
        for subnet in allocation['subnets']:
            write_allocation(file, subnet, level + 1)

def generate_markdown_table(allocations, output_path):
    """
    Vygeneruje Markdown soubor s přidělenými IP rozsahy ve formátu hierarchické tabulky s tagy.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("# Přidělené IP rozsahy\n\n")
        file.write("| Typ       | Název      | Nadřazený     | Rozsah         | Tagy            |\n")
        file.write("|-----------|------------|---------------|----------------|-----------------|\n")
        for allocation in allocations:
            write_allocation_table(file, allocation, parent_name=None)

def write_allocation_table(file, allocation, parent_name):
    """
    Rekurzivně zapisuje alokaci do tabulky s informací o nadřazeném prvku a tagy.
    """
    parent_display = parent_name if parent_name else "-"
    tags_display = ", ".join(allocation['tags']) if allocation['tags'] else "-"
    file.write(f"| {allocation['type'].capitalize()} | {allocation['name']} | {parent_display} | {allocation['range']} | {tags_display} |\n")
    if 'subscriptions' in allocation:
        for sub in allocation['subscriptions']:
            write_allocation_table(file, sub, allocation['name'])
    if 'vnets' in allocation:
        for vnet in allocation['vnets']:
            write_allocation_table(file, vnet, allocation['name'])
    if 'subnets' in allocation:
        for subnet in allocation['subnets']:
            write_allocation_table(file, subnet, allocation['name'])

def print_to_console(allocations):
    """
    Vypíše přidělené IP rozsahy na konzoli (bez tagů).
    """
    print("Přidělené IP rozsahy:")
    for allocation in allocations:
        print_allocation(allocation, level=0)

def print_allocation(allocation, level):
    """
    Rekurzivně vypíše alokaci na konzoli s správným odsazením (bez tagů).
    """
    indent = "  " * level
    print(f"{indent}{allocation['type'].capitalize()} {allocation['name']}: {allocation['range']}")
    if 'subscriptions' in allocation:
        for sub in allocation['subscriptions']:
            print_allocation(sub, level + 1)
    if 'vnets' in allocation:
        for vnet in allocation['vnets']:
            print_allocation(vnet, level + 1)
    if 'subnets' in allocation:
        for subnet in allocation['subnets']:
            print_allocation(subnet, level + 1)
            