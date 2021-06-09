from selenium import webdriver
from time import sleep
import pandas as pd
import csv
import json

# Chrom  Driver
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome("D:\ChromDriver\chromedriver_win32\chromedriver.exe")
users_url_who_writes_comments = []

list_of_products = []

followers_urls_list=[]
users_likes=[]
designs_Data=[]
user_Data=[]
url_list = []
all_makes=[]
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

# driver.get('https://www.thingiverse.com/')



# temp=0
for i in list(url_list[40:60]) :
    try:
        # temp+=1
        # print(temp)
        driver.get(i)
        sleep(5)
        # name
        product_name = driver.find_element_by_class_name('ThingPage__modelName--3CMsV').text
        print(product_name)
        # Summary
        summary_of_product = driver.find_element_by_xpath("//div[@class='ThingPage__description--14TtH']//p[1]").text
        created_at = driver.find_element_by_xpath(
            '//*[@id="react-app"]/div/div/div/div[5]/div[1]/div/div[1]/div/div[2]').text
        created_at = created_at.split(" ", 2)[2:][0]


        # TODO : fix String print_setting
        print_Settings=x=driver.find_elements_by_class_name('ThingPage__preHistory--312bi')




        words = [i.text for i in print_Settings]
        # print Settings
        print_Settings_string = ''.join(words)


        # owner
        owner_profile_url = driver.find_element_by_xpath(
            '//*[@id="react-app"]/div/div/div/div[5]/div[1]/div/div[1]/div/div[2]/a').get_attribute('href')



        owner_name= driver.find_element_by_xpath(
            '//*[@id="react-app"]/div/div/div/div[5]/div[1]/div/div[1]/div/div[2]/a').text


        # click comments button
        driver.find_element_by_xpath("(//div[@class='MetricButton__tabButton--2rvo1'])[2]").click()

        comments = []
        temp = 0
        sleep(4)
        condition = True

        # get throw all comments  [View More Comments]
        while condition:
            try:
                driver.find_element_by_xpath("//button[text()='View More Comments']").click()
                sleep(5)
            except Exception as e:
                condition = False

        sleep(4)

        # get the whole list of comments
        list_of_comments = driver.find_elements_by_class_name('ThingCommentsList__commentContainer--EjmOU')

        for i in list_of_comments:
            try:
                comment = i.find_element_by_class_name('ThingComment__commentBody--2xT45').text
                temp += 1
                user  = i.find_element_by_xpath(
                    "(//div[@class='ThingComment__headerWrapper--3KNll'])[{}]".format(temp)).text.split("\n", 2)
                user_name = user[0]
                wrote_at  = user[1]
                comments.append((comment, user_name, wrote_at))
            except Exception as e:
                pass

        sleep(3)

        # create list of users url who wrote a comments on a product
        for i in driver.find_elements_by_class_name('ThingComment__modelName--Vqvbz'):
                users_url_who_writes_comments.append(i.get_property('href'))
        sleep(2)

        # makes
        makes_button=driver.find_element_by_xpath("(//div[@class='MetricButton__tabButton--2rvo1'])[3]")
        makes_button.click()
        number_of_makes=makes_button.text
        sleep(4)
        # scroll down

        temp = 1

        # TODO : fix error execute_script
        while temp==1:
            try:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                pageHeight = driver.execute_script("return document.body.scrollHeight")
                print(pageHeight)
                totalScrolledHeight = driver.execute_script("return window.pageYOffset + window.innerHeight")
                # driver.find_element_by_class_name('ScrollUpButton__scrollUpContainer--9n07w').click()
                sleep(5)

                # -1 is to make sure the rounding issues
                if ((pageHeight - 1) <= totalScrolledHeight):
                    print('pass')
                else:
                    temp = 0
            except Exception as e:
                temp = 0

                pass

        # makes
        all_makes_url = driver.find_elements_by_class_name("ThingCardBody__cardBodyWrapper--ba5pu")
        print(len(all_makes_url))
        all_makes_user=driver.find_elements_by_class_name("ThingCardHeader__avatarWrapper--1Jliv")
        all_makes_created_at=driver.find_elements_by_class_name("ThingCardHeader__cardCreatedAfter--3xS2o")
        sleep(2)
        for i ,y,z  in zip(all_makes_user,all_makes_url,all_makes_created_at) :
            mixed_by_url=i.get_attribute('href')
            mixed_by = str(mixed_by_url).rsplit('/',1)[1]

            make_created_at=z.text
            make_product_url = y.get_attribute('href')

            all_makes.append((owner_name, mixed_by,make_product_url,make_created_at))



        sleep(2)
        #  get into the owner Profile
        driver.get(owner_profile_url)
        sleep(2)
        number_of_created_products=driver.find_element_by_xpath("//div[@id='react-app']/div[1]/div[1]/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[1]").text

        sleep(2)

        # get list of urls of followers
        get_followers_url = driver.find_element_by_xpath(
            '//*[@id="react-app"]/div/div/div/div[4]/div[1]/div[1]/div[3]/a[1]').get_attribute('href')
        sleep(1)
        driver.get(get_followers_url)

        get_all_followers_urls = driver.find_elements_by_class_name('user-header')

        for i in get_all_followers_urls :
            followers_urls_list.append(i.get_attribute('href'))

        # TODO : get user likes (products) from his Profile
        # users_likes=driver.find_elements_by_class_name('ThingCardBody__cardBodyWrapper--ba5pu')

        # for i in users_likes :
        #     users_likes.append(i.get_attribute('href'))

        list_of_products.append((product_name,created_at,summary_of_product,print_Settings_string,owner_name,owner_profile_url,number_of_created_products,users_url_who_writes_comments,followers_urls_list,len(followers_urls_list),number_of_makes,all_makes))


        user_Data.append((owner_name,owner_profile_url,number_of_created_products,users_url_who_writes_comments,followers_urls_list,len(followers_urls_list)))

        designs_Data.append((product_name,created_at,summary_of_product,print_Settings_string,comments,number_of_makes,all_makes))
    except Exception as e :
        print(e)
        pass



df = pd.DataFrame(data=list_of_products,columns=['Product_name','created_at','summary','print_Settings','owner_name','owner_profile_url',
                                                 'number_of_created_products','users_Profile_who_writes_comments','followers','followers_count','makes'])



users_data_frame=pd.DataFrame(data=user_Data,columns=['owner_name','owner_profile_url',
                                                 'number_of_created_products','users_Profile_who_writes_comments','followers','followers_count'])

designs_Data_frame=pd.DataFrame(data=designs_Data,columns=['Product_name','created_at','summary','print_Settings','comments','number_of_makes','makes'])

# how much product has the user created
# product_counted = df['owner_name'].value_counts()[:10]











# sorted_lead_User_by_followersNumber = df.sort_values(by=['followers_count'], ascending=False)
#
# df.set_option('display.max_columns',8)
# df.set_option("display.max_colwidth", None)
# print(sorted_lead_User_by_followersNumber)
# storing data in JSON format

designs_Data_frame.to_json('designs_Data.json', orient='index',default_handler=str)
users_data_frame.to_json('users_Data.json', orient='index',default_handler=str)

# reading the JSON file
# designs_Data_frame = pd.read_json('a.json', orient='index')
# Pretty Printing JSON string back


# pd.set_option('display.max_columns',5)
# pd.set_option("display.max_colwidth", None)
# print(df)
