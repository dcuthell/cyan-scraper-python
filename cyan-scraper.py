from bs4 import BeautifulSoup
from requests import get
import re
import locale

def parseRent(aptunit):
    rentstring = aptunit.find_all('td', attrs={"data-label": "Rent"})
    rentLow = rentstring[0].get_text().split('-', 1)[0]
    if(rentLow == 'Call'):
        return 0;
    rent = int(re.sub(r'[^0-9'+decimal+r']+','',rentLow))
    return rent;

def parseSqft(aptUnit):
    return int(aptUnit.find_all('td', attrs={"data-label": "Sq. Ft."})[0].get_text());

def parseAptNum(aptUnit):
    return aptUnit.find_all('td', attrs={"data-label": "Apartment"})[0].get_text();



with get('https://www.cyanpdx.com/apartmentsearchresult.aspx?Bed=-1&rent=&MoveInDate=&myOlePropertyId=207912&UnitCode=&control=1') as response:
    webpage = response.text
    decimal=locale.localeconv()['decimal_point']
    soup = BeautifulSoup(webpage,'html.parser')
    table = soup.find_all('tr', class_='AvailUnitRow')
    for aptunit in table:
        rent = parseRent(aptunit)
        if(rent == 0):
            continue;
        aptUnitNum = parseAptNum(aptunit)
        sqft = parseSqft(aptunit)
        apartment = "Apartment: " + str(aptUnitNum) + " for: $" + str(rent) + " with: " + str(sqft) + "sqft"
        if(rent/sqft < 2.19):
            print(apartment)
