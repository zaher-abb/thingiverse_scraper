from selenium import webdriver
from time import sleep
import pandas as pd


class Product:

    # TODO : persons who write comments and the comments
    def __init__(self, name, owner, summary):
        self.owner = owner
        self.name = name
        self.summary = summary


driver = webdriver.Chrome("D:\ChromDriver\chromedriver_win32\chromedriver.exe")

driver.get('https://www.thingiverse.com/')
sleep(3)

categorySort__dropdown = driver.find_element_by_xpath(
    "//button[contains(@class,'CategorySort__dropdownButton--gpHIi Dropdown__dropdownButton--1iEp1')]").click()
categorySort__dropdown_select_3d_Printing = driver.find_element_by_xpath("//span[text()='3D Printing']").click()
sleep(3)

url_list = []

condition = True
testTemp = 0
while condition:

    result = driver.find_elements_by_class_name('ThingCardBody__cardBodyWrapper--ba5pu')

    for i in range(len(result)):
        try:
            url_list.append(result[i].get_property('href'))
        except Exception as  e:
            print(e)
    try:
        driver.find_element_by_xpath("//div[@class='Pagination__button--2X-2z Pagination__more--24exV']").click()

        # testTemp+=1
        # if testTemp >=1 :
        #     break
        sleep(5)
    except Exception as e:
        condition = False
        print(e)

print(len(url_list))
users_url_who_writes_comments = []
list_of_products = []
for i in url_list:
    try:
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

        for i in list_of_comments:
            users_url_who_writes_comments.append(i.get_property('href'))

        list_of_products.append([name, owner, summary,users_url_who_writes_comments])
    except:
        pass



df = pd.DataFrame(list_of_products)
df.to_csv('3d_printer_Data.csv', index=False, header=False)

