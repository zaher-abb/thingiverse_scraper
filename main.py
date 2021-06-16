from selenium import webdriver
from time import sleep
import pandas as pd
import csv
from selenium.webdriver.common.keys import Keys
import json


from itertools import zip_longest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC, wait

# Chrom  Driver
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome("D:\ChromDriver\chromedriver_win32\chromedriver.exe")

url_list = []



# collect proudcts urls
# # # Home Page
# driver.get('https://www.thingiverse.com/')
# sleep(3)
# # chose the 3d printing
# categorySort__dropdown = driver.find_element_by_xpath(
#     "//button[contains(@class,'CategorySort__dropdownButton--gpHIi Dropdown__dropdownButton--1iEp1')]").click()
# categorySort__dropdown_select_3d_Printing = driver.find_element_by_xpath("//span[text()='3D Printing']").click()
#
# sleep(9)
# driver.find_element_by_xpath("//button[contains(@class,'Sort__dropdownButton--1myG8 Dropdown__dropdownButton--1iEp1')]").click()
#
#
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
#     # temp += 1
#     # print(temp)
#     for i in range(len(result)):
#         try:
#             # print(i)
#             url_list.append(result[i].get_property('href'))
#             print(result[i].get_property('href'))
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
#
# def scroll_down(driver):
#     global count
#     iter = 0
#     while 1:
#         scroll_top_num = str(iter * 1000)
#         iter += 1
#         driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#         try:
#             sleep(3)
#             WebDriverWait(driver, 30).until(check_difference_in_count)
#         except Exception as e:
#             print(e)
#             count = 0
#             break
#
# def check_difference_in_count(driver):
#     global count
#
#     new_count = len(driver.find_elements_by_class_name('ThingCardBody__cardBodyWrapper--ba5pu'))
#
#     if count != new_count:
#         count = new_count
#         return True
#     else:
#         return False

# save all products urls from 3d printing in csv file
with open('3d_Designs2.csv','rt')as f:
  data = csv.reader(f)
  for row in data:
       url_list+=row
print(len(url_list))

df2=pd.DataFrame(url_list)
df2.to_csv('Products_urls.csv', index=False, header=False)
users_url_who_writes_comments = []
list_of_products = []
followers_urls_list = []
user_Data = []
designs_Data = []
count=0
for url in list(url_list[500:1000]) :

    try:

        count+=1
        print('count in ')
        print(count)
        driver.get(url)
        sleep(5)
        # name
        product_name = driver.find_element_by_class_name('ThingPage__modelName--3CMsV').text
        print(product_name)
        # Summary
        summary_of_product = driver.find_element_by_xpath("//div[@class='ThingPage__description--14TtH']//p[1]").text
        created_at = driver.find_element_by_xpath(
            '//*[@id="react-app"]/div/div/div/div[5]/div[1]/div/div[1]/div/div[2]').text
        created_at = created_at.split(" ", 2)[2:][0]



        print_Settings=x=driver.find_elements_by_class_name('ThingPage__preHistory--312bi')

        words = [i.text for i in print_Settings]

        # print Settings
        print_Settings_string = ''.join(words)

        print_Settings_string=print_Settings_string.replace('\n',' ')

        # owner
        owner_profile_url = driver.find_element_by_xpath(
            '//*[@id="react-app"]/div/div/div/div[5]/div[1]/div/div[1]/div/div[2]/a').get_attribute('href')
        print('commenst')
        # get owner name
        owner_name= driver.find_element_by_xpath(
            '//*[@id="react-app"]/div/div/div/div[5]/div[1]/div/div[1]/div/div[2]/a').text
        comment_url= str(url) + '/comments'
        print(comment_url)
        driver.get(comment_url)




        comments = []
        temp2 = 0
        sleep(4)
        condition = True

        # get throw all comments  [View More Comments]
        while condition:
            try:
                driver.find_element_by_xpath("//button[text()='View More Comments']").click()
                sleep(6)
            except Exception as e:
                condition = False
        sleep(4)
        # get the whole list of comments
        list_of_comments = driver.find_elements_by_class_name('ThingCommentsList__commentContainer--EjmOU')

        for c in list_of_comments:
            try:
                comment = c.find_element_by_class_name('ThingComment__commentBody--2xT45').text
                temp2 += 1
                user  = c.find_element_by_xpath(
                    "(//div[@class='ThingComment__headerWrapper--3KNll'])[{}]".format(temp2)).text.split("\n", 2)
                user_name = user[0]
                wrote_at  = user[1]
                comments.append((comment, user_name, wrote_at))
            except Exception as e:
                pass
        print(' out of comments ')
        sleep(3)

        # create list of users url who wrote a comments on a product
        for user_comments in driver.find_elements_by_class_name('ThingComment__modelName--Vqvbz'):
                users_url_who_writes_comments.append(user_comments.get_property('href'))
        print(' out of comments 2')
        sleep(2)
        temp_url = str(str(url) + '/makes')
        print(temp_url)
        driver.get(temp_url)
        sleep(4)


        # makes_Number
        makes_num = int(driver.find_element_by_xpath("(//div[@class='MetricButton__tabButton--2rvo1 MetricButton__selected--BGAr0'])/div[1]").text)
        print('makes')


        print(makes_num)

        sleep(4)

        # scroll down

        #makes
        while True:
            try:
                htmlelement = driver.find_element_by_tag_name('html')
                htmlelement.send_keys(Keys.END)
                sleep(4)
                htmlelement.send_keys(Keys.END)
                print(makes_num/10)
                if makes_num < 20 :
                    makes_num= 100
                for num in range(int(makes_num / 10)):
                    htmlelement.send_keys(Keys.END)
                    sleep(2)
                    htmlelement.send_keys(Keys.END)
                    sleep(2)
                    htmlelement.send_keys(Keys.END)
                    sleep(1)
                    all_makes_temp = driver.find_elements_by_class_name("ThingCardBody__cardBodyWrapper--ba5pu")
                    if(len(all_makes_temp) < 18 ):
                        break
                    if(len(all_makes_temp)==makes_num):
                        break
                    sleep(5)
                break


            except TimeoutException:
                print('Exception makes ')
                break  # not more posts were loaded - exit the loop

        # makes
        all_makes_url = driver.find_elements_by_class_name("ThingCardBody__cardBodyWrapper--ba5pu")
        print("all makes ")
        print(len(all_makes_url))
        print('test1')
        all_makes_user=driver.find_elements_by_class_name("ThingCardHeader__avatarWrapper--1Jliv")
        print('test2')
        all_makes_created_at=driver.find_elements_by_class_name("ThingCardHeader__cardCreatedAfter--3xS2o")
        print('test3')
        sleep(2)
        all_makes=[]
        for x , y, z  in list(zip_longest(all_makes_user, all_makes_url, all_makes_created_at)) :
          try:

            mixed_by_url=x.get_attribute('href')
            mixed_by = str(mixed_by_url).rsplit('/',1)[1]

            make_created_at=z.text
            make_product_url = y.get_attribute('href')

            all_makes.append((owner_name, mixed_by,make_product_url,make_created_at))
          except IndexError as e:
              print(e)
              pass

            # print(all_makes)
        print('test4')

        sleep(2)
        # Remix_Number
        remixes_url=str(str(url) + '/remixes')
        print(remixes_url)
        driver.get(remixes_url)
        sleep(4)
        print('remix')


        test_temp=str(driver.find_element_by_xpath("//div[@class='MetricButton__tabButton--2rvo1 MetricButton__selected--BGAr0']/div[1]").text)
        if(test_temp==''):
            print('remix number')
            remixes_num=int(driver.find_element_by_xpath("//div[@class='MetricButton__tabButton--2rvo1'][5]/div[1]").text)
            print(remixes_num)
        else:
            remixes_num = int(driver.find_element_by_xpath("//div[@class='MetricButton__tabButton--2rvo1 MetricButton__selected--BGAr0']/div[1]").text)

        print('remixes number')

        # remakes
        print(remixes_num)



        sleep(4)
        while True:
            try:
                htmlelement = driver.find_element_by_tag_name('html')
                htmlelement.send_keys(Keys.END)
                sleep(4)
                htmlelement.send_keys(Keys.END)
                print(remixes_num / 10)
                if remixes_num < 20:
                     remixes_num = 100
                for num in range(int(remixes_num / 10)):
                    htmlelement.send_keys(Keys.END)
                    all_remixes_temp = driver.find_elements_by_class_name("ThingCardBody__cardBodyWrapper--ba5pu")
                    if (len(all_remixes_temp) < 18):
                        break
                    if (len(all_remixes_temp) == remixes_num):
                        break
                    sleep(5)
                break

            except TimeoutException:
                print('Exception remixes ')
                pass  # not more posts were loaded - exit the loop

        # makes
        all_remixes_url = driver.find_elements_by_class_name("ThingCardBody__cardBodyWrapper--ba5pu")
        print("all remixes ")
        print(len(all_remixes_url))
        all_remixes_user = driver.find_elements_by_class_name("ThingCardHeader__avatarWrapper--1Jliv")
        all_remixes_created_at = driver.find_elements_by_class_name("ThingCardHeader__cardCreatedAfter--3xS2o")
        sleep(2)
        all_remixes = []

        for x1, y1, z1 in list(zip_longest(all_remixes_user, all_remixes_url, all_remixes_created_at)):
              try:

                remixes_by_url = x1.get_attribute('href')
                remixes_by = str(remixes_by_url).rsplit('/', 1)[1]
                remixes_created_at = z1.text
                remixes_product_url = y1.get_attribute('href')
                all_remixes.append((owner_name, remixes_by, remixes_product_url, remixes_created_at))
              except Exception as e:
                  print(e)
                  pass

        print(all_remixes)

        sleep(2)
        print('test5')
        #  get into the owner Profile
        driver.get(owner_profile_url)
        sleep(2)
        number_of_created_products=int(driver.find_element_by_xpath("//div[@id='react-app']/div[1]/div[1]/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[1]").text)
        print('test6')
        sleep(2)

        # get list of urls of followers
        get_followers_url = driver.find_element_by_xpath(
            '//*[@id="react-app"]/div/div/div/div[4]/div[1]/div[1]/div[3]/a[1]').get_attribute('href')
        sleep(1)
        print('test7')
        driver.get(get_followers_url)
        sleep(3)
        get_all_followers_urls = driver.find_elements_by_class_name('user-header')
        print('test8')
        for follower_url in get_all_followers_urls :
            followers_urls_list.append(follower_url.get_attribute('href'))


        # TODO : get user likes (products) from his Profile
        # # users_likes=driver.find_elements_by_class_name('ThingCardBody__cardBodyWrapper--ba5pu')
        #
        # for i in users_likes :
        #     users_likes.append(i.get_attribute('href'))

        list_of_products.append((product_name,created_at,summary_of_product,print_Settings_string,owner_name,
                                 owner_profile_url,number_of_created_products,users_url_who_writes_comments,
                                 followers_urls_list,len(followers_urls_list),len(all_makes),all_makes,len(all_remixes),all_remixes))

        user_Data.append((owner_name,owner_profile_url,number_of_created_products,users_url_who_writes_comments,followers_urls_list,len(followers_urls_list)))

        designs_Data.append((product_name,created_at,summary_of_product,print_Settings_string,comments,len(all_makes),all_makes,len(all_remixes),all_remixes))
    except Exception as e :
            print(e)
            pass

all_data_frame = pd.DataFrame(data=list_of_products,columns=['Product_name','created_at','summary','print_Settings','owner_name','owner_profile_url',
                                                 'number_of_created_products','users_Profile_who_writes_comments','followers_profile_urls','followers_count','number_of_makes','makes','number_of_remixes','remixes'])



users_data_frame=pd.DataFrame(data=user_Data,columns=['owner_name','owner_profile_url',
                                                 'number_of_created_products','users_Profile_who_writes_comments','followers','followers_count'])

designs_Data_frame=pd.DataFrame(data=designs_Data,columns=['Product_name','created_at','summary','print_Settings','comments','number_of_makes','makes','number_of_remixes','remixes'])


designs_Data_frame.to_json('designs_Data_500_1000.json', orient='index',default_handler=str)
users_data_frame.to_json('users_Data_500_1000.json', orient='index',default_handler=str)
all_data_frame.to_json('all_data_500_1000.json', orient='index',default_handler=str)
