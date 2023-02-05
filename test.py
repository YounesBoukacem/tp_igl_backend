import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import os

address = "http://localhost:3000"

driver = uc.Firefox()

driver.get(address)

time.sleep(1)

login_button = driver.find_element(By.ID,'Google')
login_button.click()

driver.switch_to.window(driver.window_handles[-1])
time.sleep(3)

email_field = driver.find_element(By.XPATH,"//input[@type='email']")
email_field.send_keys("esiswitch@gmail.com")
email_field.send_keys(Keys.RETURN)

time.sleep(5)

password_field = driver.find_element(By.XPATH,"//input[@type='password']")
password_field.send_keys("esiswitch2cp")
password_field.send_keys(Keys.RETURN)

driver.switch_to.window(driver.window_handles[0])
time.sleep(3)

add_listing_button = driver.find_element(By.ID,'sell')
add_listing_button.click()
time.sleep(3)

title_field = driver.find_element(By.ID,"title")
title_field.send_keys("My Listing")

description_field = driver.find_element(By.ID,"description")
description_field.send_keys("This is a great listing!")

type_field = driver.find_element(By.ID,"type")
type_field.send_keys("Appartement")

surface_field = driver.find_element(By.ID,"surface")
surface_field.send_keys("100")

price_field = driver.find_element(By.ID,"price")
price_field.send_keys("100000")

localisation_field = driver.find_element(By.ID,"localisation")
localisation_field.send_keys("Oued Smar Algeria")

wilaya_field = driver.find_element(By.ID,"wilaya")
wilaya_field.send_keys("Alger")

uploaded_photos = driver.find_element(By.ID,"uploaded_photos")
uploaded_photos.send_keys(os.path.abspath("test.jpg")+" \n "+os.path.abspath("test2.jpg")+" \n "+os.path.abspath("test3.jpg"))

commune_field = driver.find_element(By.ID,"commune")
commune_field.send_keys("El Harrach")

time.sleep(3)

submit_button = driver.find_element(By.ID,'create')
submit_button.submit()

time.sleep(20)

driver.quit()
