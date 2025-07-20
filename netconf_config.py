from ncclient import manager

# --- Datos de conexión al router ---
ROUTER_IP = '192.168.56.101' # IP del CSR1000v
PORT = 830
USER = 'devasc'
PASS = 'cisco'

# --- Filtro XML para cambiar el hostname ---
# Apellidos: Lobos, Farias, Prado, Gonzalez
hostname_filter = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>Lobos-Farias-Prado-Gonzalez</hostname>
  </native>
</config>
"""

# --- Filtro XML para crear la interfaz Loopback 11 ---
loopback_filter = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>11</name>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

# --- Bloque principal de ejecución ---
if __name__ == '__main__':
    print("Iniciando conexión NETCONF con el router...")
    with manager.connect(host=ROUTER_IP, port=PORT, username=USER, password=PASS, hostkey_verify=False) as m:
        # 1. Aplicar el cambio de hostname
        print("Enviando configuración de hostname...")
        response_hostname = m.edit_config(target='running', config=hostname_filter)
        print(response_hostname)

        # 2. Aplicar la creación de la interfaz Loopback
        print("\nEnviando configuración de Loopback11...")
        response_loopback = m.edit_config(target='running', config=loopback_filter)
        print(response_loopback)
        
    print("\nConfiguración completada y sesión cerrada.")
