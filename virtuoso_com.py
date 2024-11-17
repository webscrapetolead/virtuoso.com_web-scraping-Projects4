from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd

#initial driver
driver = webdriver.Chrome()
driver.maximize_window()

#visit main url
driver.get("https://www.virtuoso.com/travel/advisors/search")
time.sleep(3)

#scrolling height
scroll_down = driver.execute_script("return document.body.scrollHeight")
scroll_position= scroll_down * 0.7
driver.execute_script(f"window.scrollTo(0, {scroll_position});")
time.sleep(3)

all_profiles = []
all_data_urls = []

#close popUp button
try:
    close_popup_btn = driver.find_element(By.XPATH, "//button[@class='leadinModal-close']").click()
except:
    pass

# count = 0
try:
    while True:
        try:
            #click showmore button
            driver.find_element(By.XPATH, "(//button[@class='btn btn-sm btn-tertiary mx-auto'])[2]").click()
            
            #vertically scroll
            current_position = driver.execute_script("return window.scrollY;")
            new_position = current_position + 2400
            driver.execute_script(f"window.scrollTo(0, {new_position});")
            time.sleep(3)
            
            # count += 1
            # if count == 2: break
        except:
            break
        
        all_urls = driver.find_elements(By.XPATH, "//h3/a")
        
        for urls in all_urls:
            single_profile = urls.get_attribute("href")
            all_profiles.append(single_profile)
            
        
except Exception as error:
    pass

for single_data in all_profiles:
    driver.get(single_data)
    time.sleep(3)
    
    try:
        name = driver.find_element(By.XPATH, "//h1").text
        name = name.replace("\n"," ")
    except:
        name = ""
    
    try:
        company_name = driver.find_element(By.XPATH, "//div[@class='-agency']/a").text
    except:
        company_name = ""
    
    try:
        address = driver.find_element(By.XPATH, "//div[@class='-location']").text
    except:
        address =""
    
    try:
        facebook = driver.find_element(By.XPATH, "(//div[@class='-links pt-2 pt-md-1']//li/a)[1]").get_attribute("href")
    except:
        facebook = ""
       
    try:
        insta = driver.find_element(By.XPATH, "(//div[@class='-links pt-2 pt-md-1']//li/a)[2]").get_attribute("href")
    except:
        insta = ""
    
    try:
        linkedin = driver.find_element(By.XPATH, "(//div[@class='-links pt-2 pt-md-1']//li/a)[3]").get_attribute("href")
    except:
        linkedin = ""  
       
    #Click contact info
    try:
        driver.find_element(By.XPATH, "//button[@class='btn btn-sm btn-primary-regular']").click()
        # time.sleep(5)
    except:
        pass
    
    try:
        phone = driver.find_element(By.XPATH, "(//div[@class='d-md-none mb-1']/a)[1]").get_attribute("href")
        phone = re.sub(r"\D", "", phone)
    except:
        phone = ""

    try:
        email = driver.find_element(By.XPATH, "(//div[@class='d-md-none mb-1']/a)[2]").get_attribute("href")
        email = email.replace("mailto:", "")
    except:
        email = ""   
    
    try:
        about_me = driver.find_element(By.XPATH, "(//div[@class='-description mt-3']/p)[1]").text
    except:
        about_me = ""      
    
    try:
        profile_image = driver.find_element(By.XPATH, "//div[@class='-photo']/img").get_attribute("src")
    except:
        profile_image= ""
    
    #Lisit of all requirments 
    all_profile_url = {
        "Name": name,
        "Company_name": company_name,
        "Address": address,
        "Facebook": facebook,
        "Instagram": insta,
        "Linkedin": linkedin,
        "Phone": phone,
        "Email": email,
        "About_me": about_me,
        "Profile Image": profile_image,  
    }
    
    all_data_urls.append(all_profile_url)
    print(f"Scrape done", len(all_data_urls))
    # if len(all_data_urls) == 3:
    #     break

#Export to CSV
df = pd.DataFrame(all_data_urls)
df.to_csv(f"virtuoso.csv", index= False)

#Close driver
driver.quit()
    
    
    
    
    
    
    
    
    
    


