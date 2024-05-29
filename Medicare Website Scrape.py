import redshift_connector
import pandas
from redshift_connector import cursor
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import pandas as pd
import numpy as nm

#Redshift connector
conn=redshift_connector.connect(
    host='',
    database='',
    user='',
    password='' )
#query
cursor: redshift_connector.cursor=conn.cursor()
cursor.execute("select cpt_code from cpt_codes")
#dataframe
result: pandas.DataFrame = cursor.fetch_dataframe()
r=result['cpt_code'].unique().tolist()
#lst = r.values.tolist()
lst_scrape = r[18:20]
print('lst_scrape ', lst_scrape)

#driver path
# DRIVER_PATH = 'C:/Users/poorn/OneDrive/Desktop/chromedriver_win32/chromedriver.exe'
DRIVER_PATH = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
#open page
driver.get('https://www.medicare.gov/procedure-price-lookup/')
#driver.maximize_window()
import time
time.sleep(2)

#click and open the page you want to scrape
driver.find_element_by_xpath('//*[@id="prefix-overlay-header"]/button').click()
r=1
table=[]
for i in lst_scrape:
    time.sleep(2)
    input_txt = driver.find_element_by_xpath('//*[@id="autocomplete_1"]')
    input_txt.clear()
    input_txt.send_keys(i)
    time.sleep(2)
    try:
        driver.find_element_by_xpath('//*[@id="autocomplete_1"]').send_keys(Keys.ENTER)
        time.sleep(2)
        driver.find_element_by_id('downshift-0-item-0').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/span').click()
        driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[2]/div/div[3]/div[1]/div[2]/span').click()
        time.sleep(2)
        #scrapping part
        codes = driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[1]/div[2]/div/div[2]/h2')
        ##Ambulatory surgical centers
        totalcost_ASC = driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/strong')
        doctorfee_ASC= driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[1]/div/div[3]/div[2]/div[3]/div[1]/div[2]')
        facilityfee_ASC = driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[1]/div/div[3]/div[2]/div[3]/div[2]/div[2]')
        medicarepay_ASC = driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[1]/div/div[3]/div[2]/div[4]/strong')
        patientpay_ASC= driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[1]/div/div[3]/div[2]/div[5]/div[2]')
        ##Hospitals
        totalcost_H = driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[2]/div/div[3]/div[2]/div[2]/strong')
        doctorfee_H = driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[2]/div/div[3]/div[2]/div[3]/div[1]/div[2]')
        facilityfee_H = driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[2]/div/div[3]/div[2]/div[3]/div[2]/div[2]')
        medicarepay_H = driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[2]/div/div[3]/div[2]/div[4]/strong')
        patientpay_H = driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/section[1]/div[1]/div[2]/div/div[3]/div[2]/div[5]/div[2]')
        #write into a table
        Table_data = {
                    'CPT Code': codes.text.split("Code:",1)[1].strip(),
                     'Total Cost - ASC': totalcost_ASC.text.replace('$',''),
            'Doctor Fee - ASC' : doctorfee_ASC.text.replace('$',''),
            'Facility Fee - ASC': facilityfee_ASC.text.replace('$',''),
            'Medicare Payment - ASC': medicarepay_ASC.text.replace('$',''),
            'Patient Pay - ASC': patientpay_ASC.text.replace('$',''),
            'Total Cost - Hosp': totalcost_H.text.replace('$',''),
            'Doctor Fee - Hosp': doctorfee_H.text.replace('$',''),
            'Facility Fee - Hosp': facilityfee_H.text.replace('$',''),
            'Medicare Payment - Hosp': medicarepay_H.text.replace('$',''),
            'Patient Pay - Hosp': patientpay_H.text.replace('$',''),
                }
        table.append(Table_data)
        df = pd.DataFrame(table)
        r+=1
        #loopbacktomainpage
        driver.get('https://www.medicare.gov/procedure-price-lookup/')
    except Exception as ex:
        pass

driver.close()
#write to excel file
# print(df)
# df.to_csv('CPT_Scrapped_DB.csv')
for dataobj in table:
    # updateQuery = f"update cpt_codes set total_cost_asc='{dataobj['CPT Code']}'  where cpt_code='{dataobj['CPT Code']}'"
    updateQuery = f"update cpt_codes set total_cost_asc={dataobj['Total Cost - ASC']}, doctor_fee_asc ={dataobj['Doctor Fee - ASC']}, facility_fee_asc ={dataobj['Facility Fee - ASC']}, medicare_payment_asc ={dataobj['Medicare Payment - ASC']}, patient_pay_asc ={dataobj['Patient Pay - ASC']}, total_cost_hosp ={dataobj['Total Cost - Hosp']}, doctor_fee_hosp ={dataobj['Doctor Fee - Hosp']}, facility_fee_hosp ={dataobj['Facility Fee - Hosp']}, medicare_payment_hosp ={dataobj['Medicare Payment - Hosp']}, patient_pay_hosp ={dataobj['Patient Pay - Hosp']}  where cpt_code='{dataobj['CPT Code']}'"
    print(updateQuery)
    cursor.execute(updateQuery)
conn.commit()
cursor.close()
conn.close()
#with conn.cursor() as cursor:
#    cursor.write_dataframe(df,"cpt_codes")

