"""
allocator.py - Logika pro rekurzivní přidělování IP rozsahů.
"""

import ipaddress
from ip_manager import IPManager

def calculate_equal_size(ip_range, num_items):
    """
    Vypočítá velikost masky pro rovnoměrné rozdělení IP adres.
    """
    if num_items <= 0:
        return ip_range.prefixlen
    total_hosts = ip_range.num_addresses
    hosts_per_item = total_hosts // num_items
    if hosts_per_item <= 1:
        raise ValueError("Not enough IP addresses to split equally")
    mask_length = 32 - (hosts_per_item - 1).bit_length()
    return max(ip_range.prefixlen, min(mask_length, 30))

def allocate_resources(ip_manager, resources, addressing, level=0):
    """
    Rekurzivně přiděluje IP adresy podle hierarchie prostředků.
    """
    allocations = []
    num_items = len(resources)

    if not resources or not ip_manager.available:
        return allocations

    for resource in resources:
        obj_type = resource['type']
        obj_name = resource['name']
        print(f"Processing {obj_type} {obj_name} at level {level}")
        
        # Determine size: specific mask or default 'equal'
        spec = next((s['size'] for s in addressing['specific'] if s['type'] == obj_type and s['name'] == obj_name), 
                    addressing['default'].get(obj_type, 'equal'))
        
        if spec == 'equal':
            # Calculate size based on the number of siblings at this level
            if not ip_manager.available:
                raise ValueError(f"No available IP space for {obj_type} {obj_name}")
            size = calculate_equal_size(ip_manager.available[0], num_items)
        else:
            size = int(spec.lstrip('/'))
        
        if not ip_manager.available:
            raise ValueError(f"No available IP space for {obj_type} {obj_name}")
        if ip_manager.available[0].prefixlen > size:
            raise ValueError(f"Requested size /{size} is larger than available range {ip_manager.available[0]} for {obj_type} {obj_name}")
        
        print(f"Allocating for {obj_type} {obj_name} with size /{size}")
        try:
            ip_range = ip_manager.allocate(size)
        except ValueError as e:
            raise ValueError(f"Failed to allocate /{size} for {obj_type} {obj_name}: {str(e)}")
        print(f"Allocated {ip_range} for {obj_type} {obj_name}")
        
        allocation = {
            'type': obj_type,
            'name': obj_name,
            'range': str(ip_range),
            'tags': resource.get('tags', [])
        }
        
        if 'subscriptions' in resource:
            sub_ip_manager = IPManager([str(ip_range)])
            allocation['subscriptions'] = allocate_resources(sub_ip_manager, resource['subscriptions'], addressing, level + 1)
        elif 'vnets' in resource:
            vnet_ip_manager = IPManager([str(ip_range)])
            allocation['vnets'] = allocate_resources(vnet_ip_manager, resource['vnets'], addressing, level + 1)
        elif 'subnets' in resource:
            subnet_ip_manager = IPManager([str(ip_range)])
            allocation['subnets'] = allocate_resources(subnet_ip_manager, resource['subnets'], addressing, level + 1)
        
        allocations.append(allocation)
    return allocations
