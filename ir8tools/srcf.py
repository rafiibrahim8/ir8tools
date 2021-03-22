#!/usr/bin/python3
import argparse

VERSION = 1.0

MODE_DEFAULT = 0
MODE_URL_ONLY = 1
MODE_FULL_TEXT = 2

def get_mirrors():
    mirrors = [
        {
            "id": "altushost-swe",
            "name": "AltusHost",
            "location": "Stockholm, Sweden, SE"
        },
        {
            "id": "deac-ams",
            "name": "DEAC",
            "location": "Amsterdam, Netherlands, NL"
        },
        {
            "id": "deac-riga",
            "name": "DEAC",
            "location": "Latvia, LV"
        },
        {
            "id": "vorboss",
            "name": "Vorboss",
            "location": "London, United Kingdom, GB"
        },
        {
            "id": "netix",
            "name": "NetIX",
            "location": "Bulgaria, BG"
        },
        {
            "id": "deac-fra",
            "name": "DEAC",
            "location": "Frankfurt Am Main, Germany, DE"
        },
        {
            "id": "jztkft",
            "name": "JZT KFT",
            "location": "Mezotur, Hungary, HU"
        },
        {
            "id": "kumisystems",
            "name": "kumi systems",
            "location": "Austria, AT"
        },
        {
            "id": "nav",
            "name": "NAV Communications",
            "location": "Bucharest, Romania, RO"
        },
        {
            "id": "liquidtelecom",
            "name": "Liquid Telecom",
            "location": "Kenya, KE"
        },
        {
            "id": "iweb",
            "name": "iWeb Technologies",
            "location": "Montreal, QC, CA"
        },
        {
            "id": "pilotfiber",
            "name": "Pilot",
            "location": "New York, NY, US"
        },
        {
            "id": "managedway",
            "name": "ManagedWay",
            "location": "Detroit, MI, US"
        },
        {
            "id": "netactuate",
            "name": "NetActuate",
            "location": "Durham, NC, US"
        },
        {
            "id": "newcontinuum",
            "name": "SBA Edge",
            "location": "West Chicago, IL, US"
        },
        {
            "id": "tenet",
            "name": "TENET: The Tertiary Education and Research Network",
            "location": "Wynberg, South Africa, ZA"
        },
        {
            "id": "megalink",
            "name": "MegaLink",
            "location": "Linhares, Brazil, BR"
        },
        {
            "id": "cfhcable",
            "name": "CFH Cable",
            "location": "United States, US"
        },
        {
            "id": "nchc",
            "name": "National Center for High-Peformance Computing",
            "location": "Taipei, Taiwan, TW"
        },
        {
            "id": "jaist",
            "name": "Japan Advanced Institute of Science and Technology",
            "location": "Nomi, Japan, JP"
        },
        {
            "id": "ufpr",
            "name": "Centro de Computacao Cientifica e Software Livre",
            "location": "Curitiba, Brazil, BR"
        },
        {
            "id": "versaweb",
            "name": "Versaweb",
            "location": "Las Vegas, NV, US"
        },
        {
            "id": "phoenixnap",
            "name": "PhoenixNAP",
            "location": "Tempe, AZ, US"
        },
        {
            "id": "freefr",
            "name": "Free France",
            "location": "Paris, France, FR"
        },
        {
            "id": "netcologne",
            "name": "NetCologne GmbH",
            "location": "Cologne, Germany, DE"
        },
        {
            "id": "excellmedia",
            "name": "Excell Media",
            "location": "Hyderabad, India, IN"
        },
        {
            "id": "ixpeering",
            "name": "IX Australia",
            "location": "Brisbane, Australia, AU"
        }
    ]

    return mirrors

def list_mirrors(url:str, mode):
    if('.dl.sourceforge.net/project/' not in url):
        print('Please supply a valid direct url.')
        return
    if(not mode):
        mode = MODE_DEFAULT
    
    p_url = url[url.index('.'):]

    mode_str = {
        MODE_DEFAULT : '{sl: <2}  {loc: <30}    https://{mid}{p_url}',
        MODE_URL_ONLY : 'https://{mid}{p_url}',
        MODE_FULL_TEXT : '{sl: <2}  {m_name: <25}    {loc: <30}    https://{mid}{p_url}'
    }

    for i, mirror in enumerate(get_mirrors(), 1):
        print(mode_str[mode].format(sl=i, m_name=mirror['name'], loc=mirror['location'], mid=mirror['id'], p_url=p_url))

def main():
    parser = argparse.ArgumentParser(description='Show alternative mirrors for SourceForge.net')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u','--url-only', dest='mode', help='Show url only.', action='store_const', const=MODE_URL_ONLY)
    group.add_argument('-a','--full', dest='mode', help='Show full details including mirror name.', action='store_const', const=MODE_FULL_TEXT)
    parser.add_argument('url', metavar='URL', help='Direct url of SourceForge download.')
    parser.add_argument('-v','--version',help='Prints version information.',action='version',version= 'v'+str(VERSION))
    args = parser.parse_args()
    
    list_mirrors(args.url, args.mode)

if __name__ == "__main__":
    main()
