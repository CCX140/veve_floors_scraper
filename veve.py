from selenium import webdriver
import time
import colorama
from os import system
from colorama import Fore, Style
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import random
import json


#name must be comic_name+ratiry
def nametoid(name):
	with open("nametoid.txt") as nametoid:
		line = nametoid.readline()
		while line:
			if name in line :
				line = nametoid.readline()
				break
			line = nametoid.readline()

		return int(line)

def insertintoid(id,element):
	with open("./comics/"+id,'a') as file:
		file.write(element)

def quit():
	print(Fore.GREEN +"\n### VEVE SCRAPER QUIT ###"+Fore.WHITE)
	time.sleep(3)
	driver.quit()


headless = True

system("cls")

options = Options()
if headless :
	options.headless = True

driver = webdriver.Firefox(options=options)

driver.get("https://www.google.com/")
try:
	element = WebDriverWait(driver, 5).until(
	EC.presence_of_element_located((By.NAME, "q"))
	)
finally:
	if (element):
		print(Fore.GREEN +"### VEVE SCRAPER ###\n"+Fore.WHITE)
	else:
		print("Error : no connection")
		driver.quit()


while 1:
	driver.get("https://ecomiwiki.com/marketplace/floors")
	try:
		comicsbutton = WebDriverWait(driver, 5).until(
		EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div/nav/ul/li[2]/button'))
		)
	finally:
		comicsbutton.click()



	#INFINITE SCROLL DOWN
	try:
		WebDriverWait(driver, 5).until(
		EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div/div[2]/div/div/div/table/tbody/tr[3]/td[1]/div/div[2]/span[1]'))
		)
	except:
		print("marche po")


	SCROLL_PAUSE_TIME = 1

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
	    # Scroll down to bottom
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	    # Wait to load page
	    time.sleep(SCROLL_PAUSE_TIME)

	    # Calculate new scroll height and compare with last scroll height
	    new_height = driver.execute_script("return document.body.scrollHeight")
	    if new_height == last_height:
	        break
	    last_height = new_height


	nbcomics = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div/div[2]/div/div/div/table/tbody/tr')

	date = str(int(time.time()))

	for i in range(1,len(nbcomics)) :
		name = driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div[2]/div/div/div/table/tbody/tr['+str(i)+']/td[1]/div/div[2]/span[1]')
		rarity = driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div[2]/div/div/div/table/tbody/tr['+str(i)+']/td[1]/div/div[2]/span[2]')
		price = driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div[2]/div/div/div/table/tbody/tr['+str(i)+']/td[2]/span[2]')
		colorratity = Fore.WHITE
		if (rarity.text == "UNCOMMON"):
			colorratity = Fore.GREEN
		if (rarity.text == "RARE"):
			colorratity = Fore.YELLOW
		if (rarity.text == "ULTRA_RARE"):
			colorratity = Fore.RED
		if (rarity.text == "SECRET_RARE"):
			colorratity = Fore.MAGENTA

		#print(name.text+'\t',colorratity+rarity.text+'\t'+Fore.WHITE,price.text,nametoid(name.text+rarity.text))
		pricetext = price.text[1:]
		pricetext = "".join(pricetext.split())
		obj = '{time:'+date+',value:'+pricetext+'}\n'
		insertintoid(str(nametoid(name.text+rarity.text)),obj)

	print("got prices ",date)
	time.sleep(300)	

quit()
