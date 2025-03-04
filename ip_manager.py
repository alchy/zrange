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

    def allocate(self, size):
        """
        Přidělí podsíť požadované velikosti z dostupného prostoru.
        
        Args:
            size (int): Požadovaná velikost masky (např. 24 pro /24).
        
        Returns:
            ipaddress.IPv4Network: Přidělená podsíť.
        
        Raises:
            ValueError: Pokud není dostatek IP adres.
        """
        print(f"Allocating /{size} from available: {self.available}")
        if not self.available:
            print("No available space - raising ValueError")
            raise ValueError("No available IP ranges")
        net = self.available[0]
        try:
            subnet = next(net.subnets(new_prefix=size))
            self.allocated.append(subnet)
            self.available = list(net.address_exclude(subnet))
            print(f"Allocated {subnet}, remaining available: {self.available}")
            return subnet
        except StopIteration:
            print("StopIteration: Could not allocate subnet of requested size")
            raise ValueError("Could not allocate subnet of requested size")