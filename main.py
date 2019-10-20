# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time

maxPage = 1


def getNumberOfPages():
    global maxPage
    site = "https://onlinecourses.ooo"
    reqheaders = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    req = urllib.request.Request(site, headers=reqheaders)
    try:
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')

        data = soup.findAll('a', attrs={'class': 'page-numbers'})
        print(data)
        for pageNum in data:
            currentPage = pageNum.getText().replace(',', '').encode('ascii', 'ignore')
            if(currentPage != b''):
                print(currentPage)
                currentPage = int(currentPage)
                if maxPage < currentPage:
                    maxPage = currentPage
        print(maxPage)
    except:
        maxPage = 1


def getLinks():
    global maxPage
    for index in range(1, maxPage + 1):

        site = "https://onlinecourses.ooo/page/" + str(index) + '/'
        reqheaders = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        req = urllib.request.Request(site, headers=reqheaders)
        try:
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, 'html.parser')

            data = soup.findAll('h3', attrs={'class': 'entry-title'})
            for div in data:
                links = div.findAll('a')
                for a in links:
                    with open('index.txt', 'a') as fileWithLinks:
                        fileWithLinks.write(a['href']+'\n')
                        # print(a['href'])
        except:
            print("An exception occurred")


def getCouponLink():
    with open('index.txt') as fileWithLinks:
        siteList = fileWithLinks.readlines()
        siteList = [x.strip() for x in siteList]
    print(siteList)
    i = 1
    for site in siteList:
        print(i)
        i = i + 1
        reqheaders = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        req = urllib.request.Request(site, headers=reqheaders)
        try:
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, 'html.parser')

            data = soup.findAll('div', attrs={'class': 'link-holder'})
            for div in data:
                links = div.findAll('a')
                for a in links:
                    with open('couponFile.txt', 'a') as fileWithLinks:
                        fileWithLinks.write(a['href']+'\n')
                        # print(a['href'])
        except:
            print("An exception occurred")

# code running ok, but after 40 links a capcha is triggered


def redeemCoupons():
    with open('couponFile.txt') as fileWithLinks:
        siteList = fileWithLinks.readlines()
        siteList = [x.strip() for x in siteList]
    currentLink = 0
    turn = 0

    options = webdriver.ChromeOptions()
    options.binary_location = "<opera webdriver path>"
    driver = webdriver.Opera(options=options)

    for site in siteList:
        if(currentLink >= 855):
            if(currentLink % 15 == 0):
                driver.quit()
                if(turn == 1):
                    driver = webdriver.Opera(options=options)
                    turn = 0
                else:
                    driver = webdriver.Firefox()
                    turn = 1

                driver.get("https://www.udemy.com/")

                getFormButton = driver.find_element_by_xpath(
                    '//*[@id="udemy"]/div[1]/div[2]/div[1]/div[4]/div[4]/div/button')
                getFormButton.click()
                time.sleep(random.randint(10, 40))

                username = driver.find_element_by_xpath(
                    '//*[@id="form-item-email"]/div/input')
                print(username)
                password = driver.find_element_by_xpath(
                    '//*[@id="id_password"]')

                username.clear()
                username.send_keys('<udemy username>')

                password.clear()
                password.send_keys('<udemy password>')

                login = driver.find_element_by_xpath(
                    '//*[@id="submit-id-submit"]')
                login.click()

        if(currentLink > 855):
            # used to open the link
            driver.execute_script('window.open("' + site + '","_blank");')
            time.sleep(random.randint(20, 60))  # wait for the website to load
            # switch the driver to the new page
            driver.switch_to_window(driver.window_handles[-1])
            try:
                redeemButton = driver.find_element_by_css_selector(
                    '#udemy > div.main-content-wrapper > div.main-content > div.full-width.full-width--streamer.streamer--complete > div > div:nth-child(2) > div.col-xxs-4.right-col.js-right-col > div > div.right-col__module > div.right-col__inner > div:nth-child(1) > div > div.buy-box__element.buy-box__element--row > div > div > div > button')
                print(redeemButton)
                redeemButton.click()
            except:
                print("already redeamed")
            time.sleep(random.randint(20, 30))
            driver.close()  # used to close the tab
            # used to switch back to the main tab
            driver.switch_to_window(driver.window_handles[0])
            time.sleep(random.randint(20, 40))
        currentLink = currentLink + 1

    driver.quit()


# getNumberOfPages()
# getLinks()
# getCouponLink()
redeemCoupons()
