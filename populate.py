# scraping the dat afrom BITS swd website.
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','blackswdsearch.settings')
import django
django.setup()
from mainapp.models import Student

# now "just" build a scrapper and save the data into db
# use get_or_create method to avoid duplicates, if feel necessary
from selenium import webdriver
import time
browser = webdriver.Firefox()
browser.get('http://universe.bits-pilani.ac.in:12349/StudentSearch.aspx')
id_elem=browser.find_element_by_id('idnoTxt')
id_elem.send_keys('2012')  # change this accordingly
submit_elem=browser.find_element_by_id('searchBtn')
submit_elem.click()

n=2
while(n<58): # change this accordingly

    meow = browser.find_elements_by_css_selector('#searchResultGridView tr td')[0:100]
    x=0
    test = Student()
    for i in meow:
        if x%5==0:
            print('idno: '+i.text)
            test.idno=i.text
        if x%5==1:
            print('name: '+i.text)
            test.name = i.text
        if x%5==2:
            print('hostel: '+i.text)
            test.hostel=i.text
        if x%5==3:
            print('room: '+i.text)
            # is it integer?
            test.room=int(i.text)
        if x%5==4:
            print('sex: '+i.text)
            if i.text=='M':
                test.sex=True
            else:
                test.sex=False
            print()
            test.save()
            print('new banda')
            test=Student()
            print()
        x+=1

    if (n%10)==1:
        bhow= browser.find_elements_by_link_text('...')[-1]
        bhow.click()
        n+=1
    else:
        bhow= browser.find_element_by_link_text(str(n))
        bhow.click()
        n+=1
