# Tutorial: https://www.youtube.com/watch?v=dRcvJRmqFHQ&lc=UgyUDvoIA0A37EWWoC54AaABAg.9Aem3mXGQzz9Aep5dNrAY6
import requests
from bs4 import BeautifulSoup
import json
import time
import csv
import pandas as pd
import os
import random


USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.79 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
     'Gecko/20100101 '
     'Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.91 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/62.0.3202.89 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/63.0.3239.108 '
     'Safari/537.36'),  # chrome
]

proxies=["https://193.200.211.19:8080",
        "https://103.216.51.210:8191",
        "https://195.154.42.163:7777",
        "https://188.165.141.114:3129"]


class ZillowScraper():
    results = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'zguid=23|%2403435e76-0699-4a32-b86d-77d033c907ef; _ga=GA1.2.1271511001.1575011821; zjs_user_id=null; zjs_anonymous_id=%2203435e76-0699-4a32-b86d-77d033c907ef%22; _gcl_au=1.1.1333357279.1575011822; _pxvid=3cfcc163-1278-11ea-bff8-0242ac12000b; ki_r=; __gads=ID=84d8013cfac6df96:T=1575012041:S=ALNI_MaSvVNZsir2JXJ17pv54bjsPuyfcw; ki_s=199442%3A0.0.0.0.0%3B199444%3A0.0.0.0.2; zgsession=1|c0999376-b167-4a47-a1cd-0e456d882d4e; _gid=GA1.2.55965867.1578668946; JSESSIONID=87D0662A6BC141A73F0D12620788519C; KruxPixel=true; DoubleClickSession=true; KruxAddition=true; ki_t=1575011869563%3B1578669044158%3B1578669044158%3B2%3B10; _pxff_tm=1; _px3=2e6809e35ce7e076934ff998c2bdb8140e8b793b53e08a27c5da11f1b4760755:DFItCmrETuS2OQcztcFmt0FYPUn00ihAAue2ynQgbfSq6H+p2yP3Rl3aeyls3Unr1VRJSgcNue8Rr1SUq4P1jA==:1000:9ueZvAJ6v5y4ny7psGF25dK+d3GlytY2Bh+Xj9UUhC4DaioIZ+FMXPU0mOX+Qnghqut0jIT61gLecN4fyu6qXaPDlBX6YsZVbIry1YyBN/37l0Ri3JP+E0h+m+QEBB+bqb6MbE2HtgGBJRJAry8dgOKGM5JtBGdX+X/nuQX1xaw=; AWSALB=E6JYC43gXQRlE2jPT9e2vAQOYPvdHnccBlqi0mcXevYExTaHro0M+uo/Qxahi6JyLz9LpotY9eLtEbYrAOeQXcCm6UhjWnTopQHernmjlR/ibE6JmE8F6tReiBn4; search=6|1581261153229%7Crect%3D40.96202658306895%252C-73.55498286718745%252C40.4487909557045%252C-74.40093013281245%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D3%26z%3D0%26lt%3Dfsbo%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%09%01%096181%09%09%09%090%09US_%09',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.142 Chrome/75.0.3770.142 Safari/537.36'
    }

    def fetch(self, url, params):
        self.headers['user-agent'] = random.choice(USER_AGENTS)
        response = requests.get(url, headers=self.headers, params=params, proxies={'https': random.choice(proxies)})
        print(response.status_code)
        return response

    def parse(self, response):
        content = BeautifulSoup(response, 'lxml')
        deck = content.find('ul', {'class': 'photo-cards photo-cards_wow photo-cards_short'})
        for card in deck.contents:
            script = card.find('script', {'type': 'application/ld+json'})
            if script:
                script_json = json.loads(script.contents[0])
                self.headers['user-agent'] = random.choice(USER_AGENTS)
                loop_response = requests.get(script_json['url'], headers=self.headers, proxies={'https': random.choice(proxies)})
                loop_soup = BeautifulSoup(loop_response.text, 'html.parser')
                try:
                    loop_result2 = loop_soup.findAll('div', class_="ds-expandable-card-section-default-padding")[
                        1].findAll('li', class_="ds-home-fact-list-item")
                except IndexError:
                    loop_result2 = 'null'
                lot = 'null'; 
                house_type = 'null';
                year_build = 'null';
                parking = 'null';
                hoa = 'null';
                lot_conversion_to_sqft = 'null';
                zillow_price_per_sqft = 'null';

                if loop_result2:
                    for contents in loop_result2:
                        print(contents.text)
                        if "Lot" in contents.text.split(":")[0]:
                            lot = contents.text.split(":")[1];
                        if "Type" in contents.text.split(":")[0]:
                            house_type = contents.text.split(":")[1];
                        if "Year built" in contents.text.split(":")[0]:
                            year_build = contents.text.split(":")[1];
                        if "Parking" in contents.text.split(":")[0]:
                            parking = contents.text.split(":")[1];
                        if "HOA" in contents.text.split(":")[0]:
                            hoa = contents.text.split(":")[1];
                        if "Price/sqft" in contents.text.split(":")[0]:
                            zillow_price_per_sqft = contents.text.split(":")[1];

                    try:
                        zestimate = loop_soup.findAll('div', class_="ds-expandable-card-section-default-padding")[
                            2].find('p', class_="Text-aiai24-0 sc-cMljjf sc-cTjmhe eXGbuO").text
                        rent_zestimate = loop_soup.findAll('div', class_="ds-expandable-card-section-default-padding")[
                            3].find('p', class_="Text-aiai24-0 sc-cMljjf sc-cTjmhe eXGbuO").text
                    except AttributeError:
                        zestimate = 'null'
                        rent_zestimate = 'null'
                    try:
                        if (str(lot.split(" ")[1]) == "sqft"):
                            lot_conversion_to_sqft = float(lot.split(" ")[0].replace(',', ""));
                        elif ((str(lot.split(" ")[1]) == "acres") or (str(lot.split(" ")[1]) == "acre")):
                            lot_conversion_to_sqft = round(float(lot.split(" ")[0].replace(',', "")) * 43560, 2);
                        elif (lot == "No Data"):
                            lot_conversion_to_sqft = 'null'
                        else:
                            lot_conversion_to_sqft = 'null'
                    except IndexError:
                        lot_conversion_to_sqft = 'null'

                    self.results.append({
                        'Listing_type': card.find('div', {'class': 'list-card-type'}).text,
                        'Price': card.find('div', {'class': 'list-card-price'}).text,
                        'Full_address': script_json['name'],
                        'Street': script_json['address']['streetAddress'],
                        'City': script_json['address']['addressLocality'],
                        'State': script_json['address']['addressRegion'],
                        'Zip_code': script_json['address']['postalCode'],
                        'Latitude': script_json['geo']['latitude'],
                        'Longitude': script_json['geo']['longitude'],
                        'Square_Feet': script_json['floorSize']['value'],
                        'Lot': lot,
                        'Lot_conversion_to_sqft': lot_conversion_to_sqft,
                        'House_type': house_type,
                        'Year_build': year_build,
                        'Parking': parking,
                        'Hoa': hoa,
                        'Zillow_price_per_sqft': zillow_price_per_sqft,
                        'Zestimate': zestimate,
                        'Rent_zestimate': rent_zestimate,
                        'House_website': script_json['url']
                    })
                    time.sleep(3)

    def to_csv(self):
        dirName = 'Output/Zillow/'
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory ", dirName, " Folder created ")
        else:
            print("Directory ", dirName, " Folder already exists")

        with open('./' + dirName + 'Q2-2020_Single_Family_Data_page17-20.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def to_dftable(self):
        house_data = pd.DataFrame(self.results)
        print(house_data)

    #     Filter Out Coming Soon, Auction, Home Type: Houses, Days On Zillow: 90 Days
    def run(self):
        url = 'https://www.zillow.com/ca/houses/'
        for page in range(17, 21):
            params = {
                'searchQueryState': '{"pagination":{"currentPage":%s},"usersSearchTerm":"ca","mapBounds":"mapBounds":{"west":-116.73594918758027,"east":-115.8364435723459,"south":33.43613945636894,"north":34.202829290316075},"regionSelection":[{"regionId":9,"regionType":2}],"isMapVisible":true,"mapZoom":5,"filterState":{"sortSelection":{"value":"globalrelevanceex"},"isCondo":{"value":false},"isMultiFamily":{"value":false},"isManufactured":{"value":false},"isLotLand":{"value":false},"isTownhouse":{"value":false},"isApartment":{"value":false},"isComingSoon":{"value":false},"isAuction":{"value":false},"doz":{"value":"90"}},"isListVisible":true}' % page
            }
            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        self.to_dftable()
        self.to_csv()


if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run();