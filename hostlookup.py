import requests, psutil, os, json
from colorama import init, Fore
from censys.search import CensysHosts
init()

#clearing cmd prompt/terminal to not make it cramped thing yes
os.system('cls;clear')

#cfdc_flag
cfdc = "false"

#"Welcome Screen"
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

#Lookup stuff thing yes
domain = str(input("Domain/IPv4 to look up: "))

#Cloudflare check by checking ISP
#A
h = CensysHosts()
cfcheck = requests.get(f"http://ip-api.com/json/{domain}?fields=512").json()
cfhostname = "Cloudflare, Inc."
try:
    cfcheck = str(cfcheck["isp"])
    if cfcheck == cfhostname:
        print("Cloudflare Detected")
        cfdc = "true"
except Exception:
    print("Invalid domain or a misc. error has occured (A)")
    print(Exception)
    exit()

#Censys Dump Thing #1
if cfdc == "true":
    print("Would you like to search&dump Censys JSON data to 'dump.json'? [Y/N]")
    answer = str(input())
    if answer == "y" or "Y":
        csquery_a = h.search(f"{domain}", per_page=1)
        with open('dump.json', 'w') as f:
            json.dump(csquery_a(), f, indent=4)
            f.close()
            print("Dumped data to 'dump.json'")
            exit()

#If Cloudflare not detected, continuing
#B
r = requests.get(f"http://ip-api.com/json/{domain}?fields=66846719").json()
try:
    continent = str(r["continent"])
    country = str(r["country"])
    countryCode = str(r["countryCode"])
    region = str(r["region"])
    regionName = str(r["regionName"])
    city = str(r["city"])
    zipCode = str(r["zip"])
    lat = str(r["lat"])
    lon = str(r["lon"])
    timezone = str(r["timezone"])
    isp = str(r["isp"])
    organization = str(r["org"])
    asn = str(r["as"])
    reverseDNS = str(r["reverse"])
    cellularNetwork = str(r["mobile"])
    proxy = str(r["proxy"])
    hostname = str(r["hosting"])
    ipquery = str(r["query"])
    print(f"\nContinent: {continent}")
    print(f"Country: {country} (Country Code: {countryCode})")
    print(f"Region: {region} (Region Name: {regionName})")
    print(f"City: {city}")
    print(f"Zip Code: {zipCode}")
    print(f"Latitude/Longitude: {lat}/{lon}")
    print(f"Timezone: {timezone}")
    print(f"ISP: {isp}")
    print(f"Organization: {organization}")
    print(f"ASN: {asn}")
    print(f"Reverse DNS: {reverseDNS}")
    print(f"Cellular Network? {cellularNetwork}")
    print(f"Proxy? {proxy}")
    print(f"Hosted? {hostname}")
    print(f"IP Queried: {ipquery}")
except Exception:
    print("An error has occured (B)")
    print(Exception)
    exit()

#Censys Dump Thing #2
print("")
print("Would you like to dump JSON data using Censys? [Y/N]")
answer = str(input())
if answer == "y" or "Y":
    csquery_b = h.search(f"{domain}", per_page=1)
    with open('dump.json', 'w') as f:
        json.dump(csquery_b(), f, indent=4)
        f.close()
        print("Dumped data to 'dump.json'")
        exit()

