from selenium import webdriver
from time import sleep
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome("D:\ChromDriver\chromedriver_win32\chromedriver.exe")
driver.get('https://www.thingiverse.com/')
sleep(3)
categorySort__dropdown = driver.find_element_by_xpath(
    "//button[contains(@class,'CategorySort__dropdownButton--gpHIi Dropdown__dropdownButton--1iEp1')]").click()
categorySort__dropdown_select_3d_Printing = driver.find_element_by_xpath("//span[text()='3D Printing']").click()

result= driver.find_elements_by_xpath("//div[@class='SearchResult__searchResultItems--2XMQB undefined']")
print(result)
for i in range(len(result)):
    try:
        row_text = result[i].text
        print(row_text)
        print("\n")
    except:
        print("continue")
sleep(5)
list_product = driver.find_elements_by_class_name("SearchResult__searchResultItem--c4VZk")
# for product in range(1,len(list_product)):
#     driver.find_element_by_xpath(
#         "//a[@href='https://www.thingiverse.com/thing:4813609']//img[{product}]".format(product=product)).click()
#     sleep(5)
#     driver.execute_script("window.history.go(-1)")
#     sleep(7)
all_products=[]


test=[]

#
# for i in range(1,10):
#     try:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         sleep(5)
#         driver.find_element_by_link_text(str(i)).click()
#         list_product = driver.find_elements_by_class_name("ThingCard__thingCard--1IcHY")
#         print(len(list_product))
#         for i in range(len(list_product)):
#             try:
#                 row_text = list_product[i].click()
#                 sleep(5)
#                 driver.execute_script("window.history.go(-1)")
#                 sleep(3)
#                 driver.find_element_by_xpath(
#                     "//span[text()='3D Printing']").click()
#                 sleep(7)
#             except Exception as e :
#                 print(e)
#
#
#
#
#         all_products+=list_product
#         sleep(7)
#     except:
#         pass
#
# print(len(list_product))
# for i in range(len(list_product)):
#     try:
#         row_text = list_product[i].text
#         print(row_text)
#         print("\n")
#     except:
#         print("continue")