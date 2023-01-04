import requests
from bs4 import BeautifulSoup
import csv
import time

#specify the runtime of the scrapper
TIME_TO_RUN = 5
header = ['Name', 'Link', 'Old Price', 'New Price', 'Discount %']

with open('output.csv', 'w', newline='') as file:
    # Create a CSV writer object
    writer = csv.writer(file)
    writer.writerow(header)

    # Start the timer
    count = 0
    start_time = time.time()
    elapsed_time = 0
    while(elapsed_time <= TIME_TO_RUN):
        elapsed_time = time.time() - start_time

        URL = f"https://m.jdsports.fr/promo/?from={count}&sort=price-low-high"
        headers = {'Content-Type': 'utf-16'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find all the elements with the class "itemPrice"
        price_elements = soup.find_all(class_='itemInformation itemSale')
        # Print the old and new price of each item
        for price_element in price_elements:
            # Find the link element and extract the link
            link_element = price_element.find('a')
            link = "https://m.jdsports.fr" + link_element['href']

            # Find the name element and extract the name
            name_element = price_element.find(class_='itemTitle')
            if name_element:
                name = name_element.text
            else:
                name = 'N/A'

            old_price_element = price_element.find(class_='was')
            new_price_element = price_element.find(class_='pri')

        # Extract the integer value from the old price text
            old_price = old_price_element.text.split()[1]

        # Extract the discount and new price from the new price text
            discount_text = new_price_element.text
            discount = discount_text[-4:-1]
            new_price = discount_text.split()[1]

            # print("NAME:", name[1:len(name)-1])
            # print("LINK:", link)
            # print("old price:", old_price)
            # print("DISCOUNT: ",discount)
            # print("NEW PRICE: ",new_price,"\n\n\n")
            writer.writerow([name[1:len(name)-1], link,
                            old_price, new_price, discount])
            count = count + 24
