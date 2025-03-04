"""
ip_manager.py - Správa IP adres a přidělování podsítí.

Tento modul obsahuje třídu IPManager pro správu dostupných IP adresních prostorů
a přidělování podsítí požadované velikosti.
"""

import ipaddress

class IPManager:
    """Třída pro správu IP adresního prostoru a přidělování podsítí."""
    
    def __init__(self, address_spaces):
        """
        Inicializuje IPManager s dostupnými adresními prostory.
        
        Args:
            address_spaces (list): Seznam IP rozsahů (např. ['10.64.0.0/16']).
        """
        self.available = [ipaddress.ip_network(space) for space in address_spaces]
        self.allocated = []
        self.current_offset = 0  # Sleduje aktuální posun v prvním dostupném bloku

    def allocate(self, size):
        """
        Přidělí podsíť požadované velikosti z dostupného prostoru spojitě.
        
        Args:
            size (int): Požadovaná velikost masky (např. 24 pro /24).
        
        Returns:
            ipaddress.IPv4Network: Přidělená podsíť.
        
        Raises:
            ValueError: Pokud není dostatek IP adres.
        """
        if not self.available:
            raise ValueError("No available IP ranges")
        net = self.available[0]
        total_addresses = net.num_addresses
        addresses_needed = 2 ** (32 - size)

        if self.current_offset + addresses_needed > total_addresses:
            raise ValueError(f"Not enough space in current block {net} for /{size}")
        
        start_ip = int(net.network_address) + self.current_offset
        subnet = ipaddress.ip_network(f"{ipaddress.ip_address(start_ip)}/{size}", strict=False)
        self.allocated.append(subnet)
        self.current_offset += addresses_needed

        # Pokud je blok vyčerpán, přesuneme se na další
        if self.current_offset >= total_addresses:
            self.available.pop(0)
            self.current_offset = 0
        
        return subnet
