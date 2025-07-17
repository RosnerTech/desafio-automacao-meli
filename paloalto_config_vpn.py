import requests

# Configuração IKE Gateway no Palo Alto
url = "http:/172.16.16.246/api/?type=config&action=set&key=API_KEY"
xml_payload = """
<request>
    <set>
        <network>
            <ike>
                <gateway>
                    <entry name="VPN_FORTIGATE">
                        <protocol>
                            <ikev2>
                                <dpd>
                                    <enable>yes</enable>
                                </dpd>
                            </ikev2>
                        </protocol>
                        <peer-address>203.0.113.1</peer-address>
                        <pre-shared-key>S3nh4F0rt3!</pre-shared-key>
                        <local-interface>ethernet1/1</local-interface>
                        <ikev2-crypto-profile>VPN_PROFILE</ikev2-crypto-profile>
                    </entry>
                </gateway>
            </ike>
        </network>
    </set>
</request>
"""
response = requests.post(url, data=xml_payload, verify=False)
print(response.text)