# Přidělené IP rozsahy

| Typ       | Název             | Nadřazený     | Rozsah (CIDR)      | Rozsah (od-do)         | Tagy            |
|-----------|-------------------|---------------|--------------------|------------------------|-----------------|
| Region | eastus | - | 10.0.0.0/14 | 10.0.0.0 - 10.3.255.255 | public, prod |
| Subscription |   subscr01 | eastus | 10.0.0.0/14 | 10.0.0.0 - 10.3.255.255 | app1 |
| Vnet |     area59 | subscr01 | 10.0.0.0/14 | 10.0.0.0 - 10.3.255.255 | internal |
| Subnet |       project9 | area59 | 10.0.0.0/24 | 10.0.0.0 - 10.0.0.255 | dmz |
| Subnet |       zaphodshome | area59 | 10.2.0.0/16 | 10.2.0.0 - 10.2.255.255 | backend |
| Region | westeu | - | 10.8.0.0/14 | 10.8.0.0 - 10.11.255.255 | private |
| Subscription |   subscr02 | westeu | 10.8.0.0/14 | 10.8.0.0 - 10.11.255.255 | app2 |
| Vnet |     galactichq | subscr02 | 10.8.0.0/14 | 10.8.0.0 - 10.11.255.255 | external |
| Subnet |       vogonpoetry | galactichq | 10.8.0.0/15 | 10.8.0.0 - 10.9.255.255 | frontend |
| Subnet |       improbabledrive | galactichq | 10.10.0.0/16 | 10.10.0.0 - 10.10.255.255 | database |
