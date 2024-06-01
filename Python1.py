import csv
from bs4 import BeautifulSoup
import requests
import sqlite3
import time
from random import randint


path = "information.txt"
path2 = "C:\\Users\\lukee\\OneDrive\\Desktop\\Python masalebi\\Databases\\Info.sqlite"
path3 = "information.csv"


#Parses ultra.ge's laptop section using "While True" loop to avoid problems with paging. Also, it avoids
#getting detected from anti-DDOS plugin by randomizing its iterating time and whole information gets
#simultaneously saved into ".csv",".txt" and ".sqlite" files.

#Code brings 3 kinds of information : Laptop's title, price and link to its image.
#Also, code is optimized to handle some advanced occasions, for instance some products
#on "Ultra.ge" are currently on sale, so it checks if product is on sale inside HTML, and brings
#most recent, (current) price.

def scrape_info():
    scraped_info = []
    page = 1

    while True:
        url = f"https://ultra.ge/index.php?route=product/category&path=20&page={page}"
        info = requests.get(url)
        soup = BeautifulSoup(info.text, 'html.parser')
        notebooks = soup.find("div", class_="row category-row")

        if not notebooks:
            break

        all_notebooks = notebooks.find_all("div", class_="product-thumb transition")

        if not all_notebooks:
            break

        for notebook in all_notebooks:
            title = notebook.find("div", class_="thumb-description clearfix").div.h4.text.strip().replace("ნოუთბუქი: ", "")
            price_container = notebook.find("div", class_="thumb-description clearfix").div.div
            picture_container = notebook.find("div", class_="image").a.img.get("src")
            new_price_tag = price_container.find("span", class_="price-new")
            if new_price_tag:
                price = new_price_tag.text.strip()
            else:
                price = price_container.find("p", class_="price").text.strip()

            scraped_info.append((title, price, picture_container))

        page += 1
        time.sleep(randint(15, 20))

    return scraped_info

def save_into_csv(path_3, information):
    with open(path_3, 'w', encoding="utf-8_sig", newline='\n') as csvfile:
        f = csv.writer(csvfile, delimiter=',')
        for info in information:
            f.writerow([info[0], info[1], info[2]])

def save_into_file(path_1, information):
    with open(path_1, "w", encoding="utf-8") as file:
        for info in information:
            file.write(info[0] + " | " + info[1] + ' | ' + info[2] + "\n")

    file.close()

def save_into_database(path_2, information):
    conn = sqlite3.connect(path_2)
    curr = conn.cursor()
    curr.execute('''create table if not exists Main 
    (id integer primary key autoincrement,
    title text,
    price text,
    image text)''')
    for info in information:
        curr.execute('''insert into Main(title, price, image) values (?,?,?)''', (info[0], info[1], info[2]))

    conn.commit()
    conn.close()


def main():
    information = scrape_info()
    save_into_file(path, information)
    save_into_database(path2, information)
    save_into_csv(path3, information)


if __name__ == '__main__':
    main()
