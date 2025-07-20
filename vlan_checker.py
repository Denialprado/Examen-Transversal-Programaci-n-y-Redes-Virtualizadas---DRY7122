# Script para verificar el rango de una VLAN
try:
    vlan_id = int(input("Ingrese el número de VLAN: "))

    if 1 <= vlan_id <= 1005:
        print(f"La VLAN {vlan_id} corresponde al rango NORMAL.")
    elif 1006 <= vlan_id <= 4094:
        print(f"La VLAN {vlan_id} corresponde al rango EXTENDIDO.")
    else:
        print("El número ingresado está fuera del rango válido para VLANs (1-4094).")

except ValueError:
    print("Error: Por favor, ingrese solo un número entero.")
