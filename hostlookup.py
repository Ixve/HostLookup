#i heart pep8
import requests
import psutil
import os
import json
import dns
import dns.resolver
from censys.search import CensysHosts

os.system('cls;clear')
print("""
  /$$   /$$                       /$$           /$$                           /$$                          
| $$  | $$                      | $$          | $$                          | $$                          
| $$  | $$  /$$$$$$   /$$$$$$$ /$$$$$$        | $$        /$$$$$$   /$$$$$$ | $$   /$$ /$$   /$$  /$$$$$$ 
| $$$$$$$$ /$$__  $$ /$$_____/|_  $$_/        | $$       /$$__  $$ /$$__  $$| $$  /$$/| $$  | $$ /$$__  $$
| $$__  $$| $$  \ $$|  $$$$$$   | $$          | $$      | $$  \ $$| $$  \ $$| $$$$$$/ | $$  | $$| $$  \ $$
| $$  | $$| $$  | $$ \____  $$  | $$ /$$      | $$      | $$  | $$| $$  | $$| $$_  $$ | $$  | $$| $$  | $$
| $$  | $$|  $$$$$$/ /$$$$$$$/  |  $$$$/      | $$$$$$$$|  $$$$$$/|  $$$$$$/| $$ \  $$|  $$$$$$/| $$$$$$$/
|__/  |__/ \______/ |_______/    \___/        |________/ \______/  \______/ |__/  \__/ \______/ | $$____/ 
                                                                                                | $$      
                                                                                                | $$      
                                                                                                |__/      """)
#psychopath detector 9000
ppid = os.getppid()
if psutil.Process(ppid).name() == "pythonw.exe":
    print("Why are you running this in Python IDLE you psychopath")
    exit()

domain = str(input("Domain/IPv4 to look up: "))

nameserver = dns.resolver.resolve(f'{domain}', 'NS')
mx = dns.resolver.resolve(f'{domain}', 'MX')

h = CensysHosts()
cfcheck = requests.get(f"http://ip-api.com/json/{domain}?fields=512").json()
cfhostname = "Cloudflare, Inc."
try:
    cfcheck = str(cfcheck["isp"])
    if cfcheck == cfhostname:
        print("Cloudflare Detected")
        cfdc = "true"
except Exception:
    print("Invalid domain or a misc. error has occured")
    print(Exception)
    exit()

r = requests.get(f"http://ip-api.com/json/{domain}?fields=66846719").json()
try:
    lat = str(r["lat"])
    lon = str(r["lon"])
    print(f"IP Queried: ", r["query"])
    print(f"\nContinent: ", r["continent"])
    print(f"Country: ", r["country"], " (Country Code: ", r["countryCode"])
    print(f"Region: ", r["region"], " (Region Name: ", r["regionName"])
    print(f"City: ", r["city"])
    print(f"Zip Code: ", r["zip"])
    print(f"Latitude/Longitude: {lat} / {lon}")
    print(f"Timezone: ", r["timezone"])
    print(f"ISP: ", r["isp"])
    print(f"Organization: ", r["org"])
    print(f"ASN: ", r["as"])
    print(f"Reverse DNS: ", r["reverse"])
    for val in nameserver:
        print("Nameserver: ", val.to_text())
    for val in mx:
        print("MX Record: ", val.to_text())
    print(f"Cellular Network? ", r["mobile"])
    print(f"Proxy? ", r["proxy"])
    print(f"Hosted? ", r["hosting"])

except Exception:
    print("An error has occured")
    print(Exception)
    exit()

print("")
print("Would you like to dump JSON data using Censys? [Y/N]")
answer = str(input())
if answer == "n" or "N":
    exit()
elif answer == "y" or "Y":
    csquery_b = h.search(f"{domain}", per_page=1)
    with open('dump.json', 'w') as f:
        json.dump(csquery_b(), f, indent=4)
        f.close()
        print("Dumped data to 'dump.json'")
        exit()
