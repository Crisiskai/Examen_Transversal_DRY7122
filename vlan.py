try:
    vlan = int(input("Ingrese el número de VLAN: "))

    if 1 <= vlan <= 1005:
        print("La VLAN pertenece al rango normal.")
    elif 1006 <= vlan <= 4094:
        print("La VLAN pertenece al rango extendido.")
    elif vlan == 0 or vlan == 4095:
        print("La VLAN está reservada.")
    else:
        print("Número de VLAN inválido.")

except ValueError:
    print("Debe ingresar un número entero.")
