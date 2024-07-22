from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import re
import random



def space_search_and_scrape(driver):
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.SPACE)
    time.sleep(random.uniform(2, 4))  
    
    elements = driver.find_elements(By.CSS_SELECTOR, '[style*="background-image"][style*="gotinder.com/u/"]')

    scraped_urls = []
    for element in elements:
        
        style_attribute = element.get_attribute("style")
        url_start_index = style_attribute.find('url("') + len('url("')
        url_end_index = style_attribute.find('")', url_start_index)
        
        if url_start_index != -1 and url_end_index != -1:
            url = style_attribute[url_start_index:url_end_index]
            scraped_urls.append(url)
        else:
            print("URL not found for element:", element.get_attribute("outerHTML"))
            
    return scraped_urls



# Chromedriver - Patch to your own path
PATH = r"C:\Users\lucas\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Chrome options - Patch to your own path
opts = webdriver.ChromeOptions()
opts.add_argument("--user-data-dir=C:\\Users\\lucas\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
opts.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=opts)
driver.get("https://tinder.com/app/recs")


for j in range(9999):
    time.sleep(random.uniform(12, 14))
    buttons = driver.find_elements(By.CSS_SELECTOR, 'button.bullet[aria-label*="1 af"][aria-label*="tilgængelige billeder"]')
    #body = driver.find_element(By.TAG_NAME, 'body')
    #body.send_keys(Keys.ARROW_RIGHT)
    total_images = 0

    if buttons and len(buttons) > 1:
        
        button = buttons[1]
        
        aria_label = button.get_attribute("aria-label")
        attempt_count = 0
        max_attempts = 10  
        
        while attempt_count < max_attempts:
            if aria_label:
                parts = aria_label.split(" ")
                if "af" in parts and "tilgængelige" in parts:
                    x_index = parts.index("tilgængelige") - 1
                    if x_index >= 0:
                        total_images = parts[x_index]
                        print("Total available images:", total_images)
                        try:
                            total_images = int(total_images)
                            break  
                        except ValueError:
                            print(f"Error converting total_images to int: {total_images}")
                    else:
                        print("Could not determine the total number of available images.")
                else:
                    print("Could not find the relevant parts in the aria-label attribute.")
            else:
                print("aria-label attribute not found for the button.")
            
            attempt_count += 1
            if total_images is None or total_images == 0:
                print(f"Attempt {attempt_count} failed to find total_images. Retrying...")
                time.sleep(random.uniform(1, 2))
        



        
        
    total_images = int(total_images)
    
    space_search_count = [0] * total_images

    unique_urls = set()
    
    unique_base_urls = set()

    unique_original_urls = set()


    for i in range(total_images):
        scraped_urls = space_search_and_scrape(driver)
    
        base_urls = [url.split('?')[0] for url in scraped_urls[1:]]
    
        unique_base_urls.update(base_urls)
    
        unique_original_urls.update(scraped_urls[1:])
    
        if i < total_images - 1:
            space_search_count[i+1] += 1
            

    elements = driver.find_elements(By.TAG_NAME, 'div')

    elements = driver.find_elements(By.CSS_SELECTOR, '[style*="background-image"][style*="gotinder.com/u/"]')

    separator = "\n----------------\n"

    print("Unique URLs:", separator.join(unique_urls))

    with open('urls.txt', 'r') as f:
        existing_base_urls = set(line.split('?')[0].strip() for line in f)

    unique_base_urls -= existing_base_urls
    
    new_urls = [url for url in unique_original_urls if url.split('?')[0] in unique_base_urls]


    if new_urls:
        url_string = separator.join(new_urls)
        url_string += "\n----------------\n"
        with open('urls.txt', 'a') as f:
            f.write(url_string)
        
    driver.refresh()

