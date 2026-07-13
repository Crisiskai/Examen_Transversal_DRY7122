from ncclient import manager
from getpass import getpass

HOST = "192.168.56.103"
PUERTO = 830

usuario = input("Usuario SSH: ")
password = getpass("Contraseña SSH: ")

configuracion = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>Cornejo-Munoz-Munoz</hostname>

    <interface>
      <Loopback>
        <name>11</name>
        <description>Configurada mediante NETCONF</description>

        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>

        <shutdown operation="remove"/>
      </Loopback>
    </interface>
  </native>
</config>
"""

try:
    with manager.connect(
        host=HOST,
        port=PUERTO,
        username=usuario,
        password=password,
        hostkey_verify=False,
        device_params={"name": "csr"}
    ) as conexion:

        print("\nConexión NETCONF establecida correctamente.")
        print(f"Session ID: {conexion.session_id}")

        respuesta = conexion.edit_config(
            target="running",
            config=configuracion
        )

        print("\nConfiguración enviada correctamente.")
        print(respuesta)

except Exception as error:
    print(f"\nError durante la operación NETCONF: {error}")
