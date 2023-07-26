import logging
import time
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(filename="scraper.log", level=logging.ERROR)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")


def scrape_coinmarketcap():
    base_url = "https://coinmarketcap.com/"
    number_of_pages_to_be_scraped = 1

    data = []
    driver = webdriver.Chrome(options=chrome_options)

    for i in range(1, number_of_pages_to_be_scraped + 1):
        params = {"page": i}
        url = base_url + "?" + urlencode(params)

        driver.get(url)
        time.sleep(3)

        # scrolloing to load dynamic data
        scroll_speed = 0.1

        initial_height = driver.execute_script("return document.body.scrollHeight")
        scroll_distance = 2500

        scroll_iterations = int(initial_height / scroll_distance)

        # Scroll through the page in increments with the desired speed
        for _ in range(scroll_iterations):
            driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
            time.sleep(scroll_speed)

        response = driver.page_source
        soup = BeautifulSoup(response, "html.parser")

        table = soup.find("table", class_="cmc-table")
        rows = table.tbody.find_all("tr")

        for row in rows:
            try:
                columns = row.find_all("td")

                # extracting data from columns
                name_without_symbol = columns[2].find_all("p")[0].text.strip()
                symbol = columns[2].find_all("p")[1].text.strip()
                name = name_without_symbol + " " + symbol
                price = columns[3].text.strip()
                percent_1h = columns[4].text.strip()
                percent_24h = columns[5].text.strip()
                percent_7d = columns[6].text.strip()
                market_cap_raw = columns[7].text.strip()

                market_cap_parts = market_cap_raw.split("$")
                if len(market_cap_parts) >= 2:
                    market_cap = "$" + market_cap_parts[2]
                else:
                    market_cap = market_cap_raw

                volume_24h = columns[8].find("p").text.strip().split(" ")[0]
                circulating_supply = columns[9].text.strip().split(" ")[0]

                # Append the extracted data to the list
                data.append(
                    {
                        "Name": name,
                        "Price": price,
                        "1h%": percent_1h,
                        "24h%": percent_24h,
                        "7d%": percent_7d,
                        "Market Cap": market_cap,
                        "Volume(24h)": volume_24h,
                        "Circulating Supply": circulating_supply,
                    }
                )

            except Exception as e:
                logging.error(f"Error occurred during row processing : {str(e)}")

    driver.quit()
    return data


def send_data_to_django(data):
    try:
        url = "http://localhost:8000/api/update_data/"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        logging.info("Data sent to Django successfully")
    except Exception as e:
        logging.error(f"Error occurred during sending data to Django: {str(e)}")


if __name__ == "__main__":
    while True:
        try:
            data = scrape_coinmarketcap()
            print(data[1])
            send_data_to_django(data)
        except Exception as e:
            logging.error(f"Error occurred during scraping and sending data: {str(e)}")

        time.sleep(5)
