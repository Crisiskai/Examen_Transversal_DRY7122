from netmiko import ConnectHandler
from getpass import getpass

usuario = input("Usuario SSH: ")
contrasena = getpass("Contraseña SSH: ")

router = {
    "device_type": "cisco_ios",
    "host": "192.168.56.103",
    "username": usuario,
    "password": contrasena,
    "secret": contrasena
}

comandos_configuracion = [
    "ipv6 unicast-routing",
    "router eigrp DRY7122",
    "address-family ipv4 unicast autonomous-system 100",
    "network 192.168.56.0 0.0.0.255",
    "af-interface default",
    "passive-interface",
    "exit-af-interface",
    "af-interface GigabitEthernet1",
    "no passive-interface",
    "exit-af-interface",
    "exit-address-family",
    "address-family ipv6 unicast autonomous-system 100",
    "af-interface default",
    "passive-interface",
    "exit-af-interface",
    "af-interface GigabitEthernet1",
    "no passive-interface",
    "exit-af-interface",
    "exit-address-family"
]

comandos_verificacion = [
    "show running-config | section router eigrp",
    "show ip interface brief",
    "show ipv6 interface brief",
    "show version"
]

conexion = None

try:
    conexion = ConnectHandler(**router)
    conexion.enable()

    print("\nConexion SSH mediante Netmiko establecida correctamente.")

    salida_configuracion = conexion.send_config_set(
        comandos_configuracion
    )

    print("\n=== CONFIGURACION APLICADA ===")
    print(salida_configuracion)

    salida_guardado = conexion.save_config()

    print("\n=== CONFIGURACION GUARDADA ===")
    print(salida_guardado)

    resultados = ""

    for comando in comandos_verificacion:
        salida = conexion.send_command(comando)

        bloque = (
            "\n"
            + "=" * 70
            + "\nCOMANDO: "
            + comando
            + "\n"
            + "=" * 70
            + "\n"
            + salida
            + "\n"
        )

        print(bloque)
        resultados += bloque

    with open(
        "resultados_item7.txt",
        "w",
        encoding="utf-8"
    ) as archivo:
        archivo.write(resultados)

    print("\nResultados guardados en resultados_item7.txt.")

except Exception as error:
    print("\nError durante la ejecucion:")
    print(error)

finally:
    if conexion is not None:
        conexion.disconnect()
        print("\nConexion SSH cerrada.")

