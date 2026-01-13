import os
import django
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_comparison.settings')
django.setup()

from products.models import Product, Category 

def scrape_and_save_data():
    section_urls = [
        ('https://chaldal.com/rices', 'Rice'), 
        ('https://chaldal.com/oil', 'Oil'), 
        ('https://chaldal.com/eggs', 'Eggs'), 
        ('https://chaldal.com/meat-new', 'Meat'), 
        ('https://chaldal.com/frozen-fish', 'Fish'), 
        ('https://chaldal.com/spices', 'Spices'), 
        ('https://chaldal.com/fresh-vegetable', 'Vegetable'),
        ('https://chaldal.com/fresh-fruit', 'Fruit'),  
        ('https://chaldal.com/juice', 'Juice'), 
        ('https://chaldal.com/beverages-tea', 'Tea'),
    ]

    for url, category_name in section_urls:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        products = soup.find_all('div', class_='product')

        category, created = Category.objects.get_or_create(name=category_name)

        for product in products:
            name_element = product.find('div', class_='name')
            if name_element:
                name = name_element.text.strip()
                if name.startswith("Loading more..."):
                    continue
            else:
                continue

            price_element = product.find('div', class_='price')
            if price_element:
                price = price_element.text.strip()
                price = re.sub(r'[^\d.]', '', price)
            else:
                price = "Not Available"

            sub_text = product.find('div', class_='subText')
            if sub_text:
                quantity_text = sub_text.text.strip()
                
                quantity_match = re.search(r'(\d+(\.\d+)?\s*(?:kg|g|gm|PC|pcs|p))', quantity_text, re.IGNORECASE)
                
                if quantity_match:
                    quantity = quantity_match.group(1)
                else:
                    quantity_match = re.search(r'(\d+(\.\d+)?)\s+(.*)', quantity_text)
                    if quantity_match:
                        quantity = f"{quantity_match.group(1)} {quantity_match.group(3)}"
                    else:
                        quantity = None
            else:
                quantity = None


            link_element = product.find('a', class_='btnShowDetails')
            if link_element and link_element.get('href'):
                website = 'https://chaldal.com' + link_element['href']
            else:
                website = "Not Available"

            try:
                product_obj, created = Product.objects.update_or_create(
                    name=name,
                    defaults={'price': price, 'quantity': quantity, 'website': website, 'category': category}
                )
                print(f"Product '{product_obj.name}' saved to database.")
            except Exception as e:
                print(f"Error occurred while saving product '{name}': {e}")

def scrape_and_save_data2():      
    section_urls = [
        ('https://sobjibazaar.com/meat', 'Meat'),
        ('https://sobjibazaar.com/fish', 'Fish'),  
        ('https://sobjibazaar.com/vegetables', 'Vegetable'),
        ('https://sobjibazaar.com/fruits-2', 'Fruit'),    
    ]

    for url, category_name in section_urls:
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')
        products = soup.find_all('div', class_='product-item')

        category, created = Category.objects.get_or_create(name=category_name)

        for product in products:
            product_name_element = product.find('h2', class_='product-title').a
            product_name = product_name_element.text.strip()

            price_element = product.find('span', class_='price actual-price')
            if price_element:
                raw_price = price_element.text.strip()
                cleaned_price = re.sub(r'[^\d.]', '', raw_price)
                if cleaned_price:
                    product_price = cleaned_price
                else:
                    print(f"Error: Invalid price format for product '{product_name}': {raw_price}")
                    continue  
            else:
                product_price = "Price not found"

            quantity_temp = product_name

            quantity_match = re.search(r'(\d+(\.\d+)?\s*\S+)$', quantity_temp)
            if quantity_match:
                quantity = quantity_match.group(1)
            else:
                quantity = None

            product_url = "https://sobjibazaar.com" + product_name_element.get('href')

            try:
                product_obj, created = Product.objects.update_or_create(
                    name=product_name,
                    defaults={'price': product_price, 'quantity': quantity, 'website': product_url, 'category': category}
                )
                print(f"Product '{product_obj.name}' saved to database.")
            except Exception as e: 
                print(f"Error occurred while saving product '{product_name}': {e}")


def scrape_and_save_data3():      
    section_urls = [
        ('https://www.othoba.com/rice?orderby=0&pagesize=80', 'Rice'),
        ('https://www.othoba.com/eggs?orderby=0&pagesize=80', 'Eggs'),
        ('https://www.othoba.com/oil?orderby=0&pagesize=80', 'Oil'),
        ('https://www.othoba.com/meat?orderby=0&pagesize=80', 'Meat'), 
        ('https://www.othoba.com/fish?orderby=0&pagesize=80', 'Fish'), 
        ('https://www.othoba.com/spice?orderby=0&pagesize=80', 'Spices'),
        ('https://www.othoba.com/fresh-vegetables?orderby=0&pagesize=80', 'Vegetable'),
        ('https://www.othoba.com/fresh-fruits?orderby=0&pagesize=80', 'Fruit'),
        ('https://www.othoba.com/tea-coffee?orderby=0&pagesize=80', 'Tea'),
        ('https://www.othoba.com/juice?orderby=0&pagesize=80', 'Juice'),
    ]

    unit_mapping = {
        'pcs': 'pcs',
        'pieces': 'pcs',
        'each': '1 pc',
        'piece': '1 pc',
        'pc': '1 pc',
        'per kg': '1 kg',
    }

    for url, category_name in section_urls:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        product_elements = soup.find_all('h4', class_='product-name')

        category, created = Category.objects.get_or_create(name=category_name)

        driver = webdriver.Chrome()
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        prices = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'new-price')))

        for product, price in zip(product_elements, prices):
            name_text = product.text.strip()
            price_text = price.text.strip()
            price_numeric = re.sub(r'[^\d.]', '', price_text)
            
            product_link = product.find('a')['href']
            full_product_link = f"https://www.othoba.com{product_link}"

            match = re.search(r'(\d+(\.\d+)?\s*(kg|g|gm|pc|pcs|pieces|piece|each|Pc|per kg))', name_text, re.IGNORECASE)
            if match:
                quantity = match.group(1)
                unit = match.group(3).lower()

                if unit in unit_mapping:
                    if unit_mapping[unit] == 'pcs':
                        quantity = f"{match.group(1)} pcs"
                    else:
                        quantity = unit_mapping[unit]
            else:
                quantity = None

            try:
                product_obj, created = Product.objects.update_or_create(
                    name=name_text,
                    defaults={'price': price_numeric, 'quantity': quantity, 'website': full_product_link, 'category': category}
                )
                print(f"Product '{product_obj.name}' saved to database.")
            except Exception as e:
                print(f"Error occurred while saving product '{name_text}': {e}")

        driver.quit()



if __name__ == "__main__":
    scrape_and_save_data()
    scrape_and_save_data2()
    scrape_and_save_data3()