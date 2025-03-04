# Přidělené IP rozsahy

| Typ       | Název      | Nadřazený     | Rozsah         | Tagy            |
|-----------|------------|---------------|----------------|-----------------|
| Region | eastus | - | 10.0.0.0/14 | public, prod |
| Subscription | subscr01 | eastus | 10.0.0.0/14 | app1 |
| Vnet | area59 | subscr01 | 10.0.0.0/14 | internal |
| Subnet | project9 | area59 | 10.0.0.0/24 | dmz |
| Subnet | zaphodshome | area59 | 10.2.0.0/16 | backend |
| Region | westeu | - | 10.8.0.0/14 | private |
| Subscription | subscr02 | westeu | 10.8.0.0/14 | app2 |
| Vnet | galactichq | subscr02 | 10.8.0.0/14 | external |
| Subnet | vogonpoetry | galactichq | 10.8.0.0/15 | frontend |
| Subnet | improbabledrive | galactichq | 10.10.0.0/16 | database |
