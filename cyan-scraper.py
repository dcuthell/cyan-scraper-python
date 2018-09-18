from bs4 import BeautifulSoup
from requests import get
import re
import locale

with get('https://www.cyanpdx.com/apartmentsearchresult.aspx?Bed=-1&rent=&MoveInDate=&myOlePropertyId=207912&UnitCode=&control=1') as response:
    listings = [{}]
    webpage = response.text
    decimal=locale.localeconv()['decimal_point']
    soup = BeautifulSoup(webpage,'html.parser')
    for aptUnit in soup.find_all('tr'):
        rentOutput = aptUnit.find_all('td', attrs={"data-label": "Rent"})
        if(rentOutput == []):
            continue;
        rentset = rentOutput[0].get_text().split('-', 1)[0]
        if(rentset == 'Call'):
            continue;
        rent = int(re.sub(r'[^0-9'+decimal+r']+','',rentset))
        aptUnitNum = aptUnit.find_all('td', attrs={"data-label": "Apartment"})[0].get_text()
        sqft = int(aptUnit.find_all('td', attrs={"data-label": "Sq. Ft."})[0].get_text())
        apartment = "Apartment: " + str(aptUnitNum) + " for: $" + str(rent) + " with: " + str(sqft) + "sqft"
        if(rent/sqft < 2.19):
            print(apartment)
