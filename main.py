from selenium import webdriver
from time import sleep
import pandas as pd
import csv
import json

# Chrom  Driver

driver = webdriver.Chrome("D:\ChromDriver\chromedriver_win32\chromedriver.exe")

#
# # Home Page
# driver.get('https://www.thingiverse.com/')
# sleep(3)
# # chose the 3d printing
# categorySort__dropdown = driver.find_element_by_xpath(
#     "//button[contains(@class,'CategorySort__dropdownButton--gpHIi Dropdown__dropdownButton--1iEp1')]").click()
# categorySort__dropdown_select_3d_Printing = driver.find_element_by_xpath("//span[text()='3D Printing']").click()
# sleep(3)
#
#
# url_list=[]
# condition = True
# testTemp = 0
# temp=1
# while condition:
#
#     result = driver.find_elements_by_class_name('ThingCardBody__cardBodyWrapper--ba5pu')
#     temp += 1
#     print(temp)
#     for i in range(len(result)):
#         try:
#             # print(i)
#             url_list.append(result[i].get_property('href'))
#
#
#         except Exception as  e:
#             print(e)
#     try:
#         driver.find_element_by_xpath("//div[@class='Pagination__button--2X-2z Pagination__more--24exV']").click()
#
#         # testTemp+=1
#         # if testTemp >=1 :
#         #     break
#         sleep(5)
#     except Exception as e:
#         condition = False
#         print(e)

url_list = []
# save all products urls from 3d printing in csv file
with open('Products_urls.csv','rt')as f:
  data = csv.reader(f)
  for row in data:
       url_list+=row
print(len(url_list))
#

# df2=pd.DataFrame(url_list)
# df2.to_csv('Products_urls.csv', index=False, header=False)

driver.get('https://www.thingiverse.com/')
users_url_who_writes_comments = []
list_of_products = []
followers_list=[]
for i in list(url_list[:3]) :
    try:
        print(i)
        driver.get(i)
        sleep(5)
        # name
        name = driver.find_element_by_class_name('ThingPage__modelName--3CMsV').text
        # owner
        owner = driver.find_element_by_xpath(
            '//*[@id="react-app"]/div/div/div/div[5]/div[1]/div/div[1]/div/div[2]/a').get_attribute('href')
        # Summary
        summary = driver.find_element_by_xpath("//div[@class='ThingPage__description--14TtH']//p[1]").text

        driver.find_element_by_xpath("(//div[@class='MetricButton__tabButton--2rvo1'])[2]").click()

        sleep(4)
        list_of_comments = driver.find_elements_by_class_name('ThingComment__modelName--Vqvbz')


        # create list of comments from a product
        for i in list_of_comments:
            users_url_who_writes_comments.append(i.get_property('href'))
        sleep(3)

        owner_profile = driver.find_element_by_xpath(
            "//div[@class='ThingPage__gallery--SnBAG']//div[2]/a").get_attribute('href')
        sleep(1)

        #  get into the owner Profile
        driver.get(owner_profile)


        sleep(3)
        # get list of urls of followers
        get_followers_url = driver.find_element_by_xpath(
            '//*[@id="react-app"]/div/div/div/div[4]/div[1]/div[1]/div[3]/a[1]').get_attribute('href')
        sleep(1)
        driver.get(get_followers_url)
        get_all_followers = driver.find_elements_by_class_name('user-header')
        for i in get_all_followers :
            followers_list.append(i.get_attribute('href'))

        list_of_products.append((name, owner, summary,users_url_who_writes_comments,followers_list))
    except:
        pass


df = pd.DataFrame(data=list_of_products,columns=['Product_name','owner','summary','users_Profile_who_writes_comments','followers'])


# storing data in JSON format
df.to_json('file1.json', orient='index')

# reading the JSON file
df = pd.read_json('file1.json', orient='index')
# Pretty Printing JSON string back


# pd.set_option('display.max_columns',5)
# pd.set_option("display.max_colwidth", None)
# print(df)
