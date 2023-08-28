import requests
from bs4 import BeautifulSoup
from httpx import AsyncClient
import asyncio


# Определение количества страниц с ноутбуками
url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

response = requests.get(url)

pages_dict = {}
soup = BeautifulSoup(response.text, "html.parser")
pagination = soup.find("ul", class_="pagination").find_all("li")[-2].text


async def main():
    # Сохранение всех ноутбуков на каждой странице
    for page in range(1, int(pagination) + 1):
        url = f"https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page={page}"
        laptops_dict = {}
        async with AsyncClient() as client:
            response = await client.get(url)

            soup = BeautifulSoup(response.text, "html.parser")

            all_laptop_names = soup.find_all("a", class_="title")
            all_laptop_price = soup.find_all("h4", class_="pull-right price")
            all_laptop_description = soup.find_all("p", class_="description")
            all_laptop_rating = soup.find_all("p", attrs={"data-rating": True})

            for i in range(len(all_laptop_names)):
                if all_laptop_names[i]["title"] in laptops_dict:
                    laptops_dict[all_laptop_names[i]["title"] + " (2)"] = [all_laptop_price[i].text,
                                                                           all_laptop_description[i].text,
                                                                           all_laptop_rating[i]["data-rating"]
                                                                           ]
                    continue
                laptops_dict[all_laptop_names[i]["title"]] = [all_laptop_price[i].text,
                                                              all_laptop_description[i].text,
                                                              all_laptop_rating[i]["data-rating"]
                                                              ]
            pages_dict[f"Page {page}"] = laptops_dict

            # Отформатированный вывод всех ноутбуков на странице
            for name, value in laptops_dict.items():
                print(f"Laptop: {name}")
                print(f"Price: {value[0]}")
                print(f"Description: {value[1]}")
                print(f"Rating: {value[2]}")
                print("-------------------")


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
