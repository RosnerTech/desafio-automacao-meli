import requests

#Configuracao API
# Substitur por sua API Key
IP_FIREWALL = "172.16.16.246"
API_KEY = "SUA_API_KEY"  

url = f"https://{IP_FIREWALL}/api/?type=config&action=set&key={API_KEY}"

xml_payload = """
<config>
  <devices>
    <entry name="lab.rosnertech">
      <network>
        <ike>
          <gateway>
            <entry name="VPN_FORTIGATE">
              <authentication>
                <pre-shared-key>
                  <key>S3nh4F0rt3!</key>
                </pre-shared-key>
              </authentication>
              <protocol>
                <ikev2>
                  <dpd>
                    <enable>yes</enable>
                  </dpd>
                </ikev2>
              </protocol>
              <peer-address>203.0.113.1</peer-address>
              <local-address>
                <interface>ethernet1/1</interface>
              </local-address>
              <ikev2-crypto-profile>VPN_PROFILE</ikev2-crypto-profile>
            </entry>
          </gateway>
        </ike>
      </network>
    </entry>
  </devices>
</config>
"""

response = requests.post(url, data=xml_payload, verify=False)

print("Status Code:", response.status_code)
print("Resposta XML:\n", response.text)
