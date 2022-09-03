# coding=gbk
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

from gensim import utils
import re
import gensim
from gensim.parsing.preprocessing import preprocess_string
gensim.parsing.preprocessing.STOPWORDS = set()
import time
import sys

def strip_short2(s, minsize=2):
    s = utils.to_unicode(s)
    def remove_short_tokens(tokens, minsize):
        return [token for token in tokens if len(token) >= minsize]
    return " ".join(remove_short_tokens(s.split(), minsize))
gensim.parsing.preprocessing.DEFAULT_FILTERS[6]=strip_short2
del gensim.parsing.preprocessing.DEFAULT_FILTERS[-1]

def is_same_author(first,second):
    first=set(preprocess_string(first))
    second=set(preprocess_string(second))
    x = first.intersection(second)
    if(len(x)>=2 or (len(x)==1 and len(first)==1 and len(second)==1)):
        return True
    else:
        return False

def print_to_file(filename, string_info, mode="a"):
	with open(filename, mode) as f:
		f.write(str(string_info) + "\n")

def init_option():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--hide-scrollbars')
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-javascript")
    ua = UserAgent()
    options.add_argument('user-agent="%s"' % ua.random)
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    return options

driver = webdriver.Chrome(options=init_option())

if len(sys.argv) < 2:
    print("Not enough parameters: ", len(sys.argv))
    sys.exit

topauthor = sys.argv[1]

print_to_file("Advisor-student.txt",topauthor)
driver.get('https://openreview.net/search?term='+topauthor+'&group=all&content=all&source=all')
driver.implicitly_wait(5)
driver.find_element_by_xpath("/html/body/div/div[3]/div/div/main/div/form/div[1]/div/div/div[1]/div[2]/input").send_keys('author',Keys.ENTER)
driver.implicitly_wait(5)

Student=[]
def is_advisor(author):
    Advisor=[]
    driver.implicitly_wait(10)
    author.click()
    driver.implicitly_wait(3)
    try:
        advisor=driver.find_elements_by_xpath("/html/body/div/div[3]/div/div/main/div/div/div/section[5]/div/div")
        student=driver.find_element_by_xpath("//*[@id=\"content\"]/div/header/div/h1").text
    except:
        driver.back()
        return
    for i in advisor:
        try:
            Advisor.append(i.find_element_by_xpath('./div[2]').text)
            print(i.find_element_by_xpath('./div[2]').text)
        except:
            print("No")
    for name in Advisor:
        if(is_same_author(topauthor,name)):
            if(student not in Student):
                Student.append(student)
                print_to_file("Advisor-student.txt",student)
            print(student+" is student of "+topauthor)
            break
    print(student)
    driver.back()

while(1):
    count=0
    for i in range(25):
        driver.implicitly_wait(5)
        paper=driver.find_elements_by_xpath("/html/body/div/div[3]/div/div/main/div/div/ul/li["+str(i+1)+"]/div/div/a")
        for idx,val in enumerate(paper):
            driver.implicitly_wait(20)
            j=driver.find_element_by_xpath("/html/body/div/div[3]/div/div/main/div/div/ul/li["+str(i+1)+"]/div/div/a["+str(idx+1)+"]")
            author=j.get_attribute("href")
            if("dblp.org" in author):
                continue
            print(author)
            try:
                is_advisor(j)
            except:
                print("skip")
            count+=1
    print(count)
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div/div[3]/div/div/main/div/div/nav/ul/li[13]/a").click()
