import requests
from bs4 import BeautifulSoup

# Определение количества страниц с ноутбуками
url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

response = requests.get(url)

laptops_dict = {}
soup = BeautifulSoup(response.text, "html.parser")
pagination = soup.find("ul", class_="pagination").find_all("li")[-2].text

# Сохранение всех ноутбуков на каждой странице
for page in range(1, int(pagination) + 1):
    url = f"https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page={page}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    all_laptop_names = soup.find_all("a", class_="title")
    all_laptop_price = soup.find_all("h4", class_="pull-right price")
    all_laptop_description = soup.find_all("p", class_="description")
    all_laptop_rating = soup.find_all("p", attrs={"data-rating": True})

    for i in range(len(all_laptop_names)):
        laptops_dict[all_laptop_names[i]["title"]] = [all_laptop_price[i].text,
                                                      all_laptop_description[i].text,
                                                      all_laptop_rating[i]["data-rating"]
                                                      ]

# Отформатированный вывод всех ноутбуков
for name, value in laptops_dict.items():
    print(f"Laptop: {name}")
    print(f"Price: {value[0]}")
    print(f"Description: {value[1]}")
    print(f"Rating: {value[2]}")
    print("-------------------")
