from bs4 import BeautifulSoup
from requests import get
import re
import locale

#CYAN HELPERS
def parseRent(rentstring):
    rentLow = rentstring[0].get_text().split('-', 1)[0]
    print(rentLow)
    if(rentLow == 'Call'):
        return 0;
    rent = int(re.sub(r'[^0-9'+decimal+r']+','',rentLow))
    return rent;

def parseRent1(rentstring):
    rentLow = rentstring[0].get_text().split('-', 1)[0]
    rent = re.sub(r'[^0-9'+decimal+r']+','',rentLow)
    if (rent == ''):
        return 0;
    return int(rent);

def parseSqft(aptUnit):
    return int(aptUnit.find_all('td', attrs={"data-label": "Sq. Ft."})[0].get_text());

def parseAptNum(aptUnit):
    return aptUnit.find_all('td', attrs={"data-label": "Apartment"})[0].get_text();

def parseSqft1(aptUnit):
    sqftstring = aptUnit.find_all('td', attrs={"data-label": "SQ. FT."})[0].get_text()
    sqft = re.sub(r'[^0-9'+decimal+r']+','',sqftstring)
    return sqft;
#CYAN
with get('https://www.cyanpdx.com/apartmentsearchresult.aspx?Bed=-1&rent=&MoveInDate=&myOlePropertyId=207912&UnitCode=&control=1') as response:
    webpage = response.text
    decimal=locale.localeconv()['decimal_point']
    soup = BeautifulSoup(webpage,'html.parser')
    print("In CYANPDX we have the following apartments under $2.19/sqft")
    for aptunit in soup.find_all('tr'):
        rentstring = aptunit.find_all('td', attrs={"data-label": "Rent"})
        if(rentstring == []):
            continue;
        rent = parseRent(rentstring)
        if(rent == 0):
            continue;
        aptUnitNum = parseAptNum(aptunit)
        sqft = parseSqft(aptunit)
        apartment = "Apartment: " + str(aptUnitNum) + " for: $" + str(rent) + " with: " + str(sqft) + "sqft"
        if(rent/sqft < 2.19):
            print(apartment)
#LADD
with get('https://www.hollandresidential.com/ladd/floor-plans/') as response:
    webpage = response.text
    decimal=locale.localeconv()['decimal_point']
    soup = BeautifulSoup(webpage,'html.parser')
    # print(soup)
    scripts = soup.find_all("script")
    dataset = scripts[len(scripts)-2].get_text()
    dataarraystring = dataset.rsplit('= ')[1].rsplit(';')[0].rsplit('{')
    print("In The Ladd Apartments we have the following apartments under $2.19/sqft")
    for item in dataarraystring:
        if (len(item) < 4):
            continue;
        unitindex = item.find("Unit")
        unitstring = item[unitindex + 7]+item[unitindex + 8]+item[unitindex + 9]+item[unitindex + 10]
        unit= int(unitstring.replace('"', ''))
        sqftindex = item.find("SqFt")
        sqftstring = item[sqftindex + 7]+item[sqftindex + 8]+item[sqftindex + 9]+item[sqftindex + 10]
        sqft= int(sqftstring.replace('"', ''))
        rentindex = item.find("Rent")
        rentstring = item[rentindex + 7]+item[rentindex + 8]+item[rentindex + 9]+item[rentindex + 10]
        rent= int(rentstring.replace('"', ''))
        apartment = "Apartment: " + str(unit) + " for: $" + str(rent) + " with: " + str(sqft) + "sqft"
        if(rent/sqft < 2.19):
            print(apartment)

with get('https://parkavewestpdx.securecafe.com/onlineleasing/park-avenue-west/floorplans.aspx') as response:
    webpage = response.text
    decimal=locale.localeconv()['decimal_point']
    soup = BeautifulSoup(webpage,'html.parser')
    print("In Park Ave West we have the following apartments under $2.19/sqft")
    for aptunit in soup.find_all('tr'):
        rentstring = aptunit.find_all('td', attrs={"data-label": "Rent"})
        if(rentstring == []):
            continue;
        rent = parseRent1(rentstring)
        if(rent == 0):
            continue;
        sqft = parseSqft1(aptunit)
        apartment = "Apartment: CHECKONLINE for: $" + str(rent) + " with: " + str(sqft) + "sqft"
        if(rent/sqft < 2.19):
            print(apartment)
