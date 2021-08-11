import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pytz import timezone
import datetime, json, pytz

import time

from opencalendar import Calendar

import smtplib, ssl

EMAIL_ADDRESS = "LWOD@venturerei.com"
EMAIL_PASSWORD = "LWOD1234!"

mins = 1

def bot(htmlstring, drvier):
    global mins
    time.sleep(5)
    
    email = "ruby@nomagroup.com"
    pwd   = "$Baxter12"
    
    email_input = driver.find_element_by_id("email-login-input")
    email_input.send_keys(email)
    time.sleep(0.3)
    
    next_button = driver.find_element_by_xpath("//button[contains(@class, 'cta-button')]")
    next_button.click()
    time.sleep(1)
    
    pwd_input = driver.find_element_by_name("password")
    pwd_input.send_keys(pwd)
    time.sleep(0.3)
    
    signin_button = driver.find_element_by_xpath("//button[contains(@class, 'cta-button')]")
    signin_button.click()
    time.sleep(20)
    
    flag = True
    while (flag):
        print(datetime.datetime.now())
        try:
            sch_unclaimed_lists = driver.find_elements_by_xpath("//ul[@id='unclaimed-list']//li/a")
            print("Scheduled Unclaimed Lists Counts---------------> : ", len(sch_unclaimed_lists))
            print(sch_unclaimed_lists)
            
            sch_url_array = []
            for sch_unclaimed_list in sch_unclaimed_lists:
                sch_unclaimed_list_url = sch_unclaimed_list.get_attribute("href")
                sch_url_array.append(sch_unclaimed_list_url)
            
            for sch_list_url in sch_url_array:
                print(sch_list_url)
                driver.get(sch_list_url)
                time.sleep(15)
                appt(driver.page_source, driver, sch_list_url, "scheduled")
        
        except IndexError as e:
            print(e)
            
        driver.get("https://listingagent.opendoor.com/appointments?filter=unclaimed")
            
        time.sleep(mins / 1.5 * 60)
        proactive_button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div[2]')
        proactive_button.click()
        time.sleep(5)
        
        # unclaimed_lists = []
        
        try:
            unclaimed_lists = driver.find_elements_by_xpath("//ul[@id='unclaimed-list']//li/a")
            print("Unclaimed Lists Counts------------------> : ", len(unclaimed_lists))
            print(unclaimed_lists)
            
            # for unclaimed_list in unclaimed_lists:
            #     unclaimed_list_url = unclaimed_list.get_attribute("href")
            #     driver.get(unclaimed_list_url)
            #     time.sleep(15)
            
            url_array = []
            for unclaimed_list in unclaimed_lists:
                unclaimed_list_url = unclaimed_list.get_attribute("href")
                url_array.append(unclaimed_list_url)
            
            for list_url in url_array:
                print(list_url)
                driver.get(list_url)
                time.sleep(15)
                appt(driver.page_source, driver, list_url, "proactive")
                
        except IndexError as e:
            print(e)
        
        # list_url = "https://listingagent.opendoor.com/appointments/499c0ee8-4653-4fc5-b605-72040aa0535d"
        # driver.get(list_url)
        # appt(driver.page_source, driver, list_url)
        time.sleep((mins / 3) * 60 * 2)
        driver.get("https://listingagent.opendoor.com/appointments?filter=unclaimed")
        print("Reload")
        
def appt(htmlstring, driver, url, opendoor_type):
    print(url)
    
    # driver.get(url)
    time.sleep(10)
    
    detail_info = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div/div/div/div/div[1]/div/div[1]').text
    appt_time_info   = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div/div/div/div/div[1]/div/div[2]').text

    print("Detail_Infos-------------------------> : ", detail_info)
    print("Appt Time----------------------------> : ", appt_time_info)
    
    
    if "th" in appt_time_info:
        appt_time_info = appt_time_info.replace("th", "")
    elif "nd" in appt_time_info:
        appt_time_info = appt_time_info.replace("nd", "")
    elif "rd" in appt_time_info:
        appt_time_info = appt_time_info.replace("rd", "")
        
    appt_time_array = appt_time_info.split(" ")
    appt_timezone_str = appt_time_array[len(appt_time_array) - 1]
    
    appt_time_str = ""
    for i in range(1, len(appt_time_array) - 1):
        if "am" in appt_time_array[i].lower() or "pm" in appt_time_array[i].lower():
            appt_time_str = appt_time_str[:-1] + appt_time_array[i]
        else:
            appt_time_str = appt_time_str + appt_time_array[i] + " "
    
    appt_time_obj = datetime.datetime.strptime(appt_time_str, '%b %d %Y %I:%M%p')
    
    print(appt_time_obj)
    
    calendarApi = Calendar()
    agent_details = calendarApi.calendar(appt_time_obj, appt_timezone_str)
    
    print(agent_details["name"], " is Aavailable at that time")
    
    if opendoor_type == "proactive":
        agent_details["name"] = "Frank Vazquez"
    
    if agent_details["name"] == "":
        return
    
    
    claim_button = driver.find_element_by_xpath("//button[@id='claim-appointment']")
    claim_button.click()
    time.sleep(3)
    
    agent_input = driver.find_element_by_xpath("//input[@placeholder='Select an Agent']")
    agent_input.send_keys(agent_details["name"])
    time.sleep(1)
    
    select_agent = driver.find_element_by_xpath("//div[@id='agent-dropdown-option']")
    select_agent.click()
    time.sleep(1)
    
    assign_button = driver.find_element_by_xpath('//*[@id="BasicDialog-content"]/div[3]/button')
    assign_button.click()
    time.sleep(10)
    print("Assigned", agent_details["name"])
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        subject = "Opendoor Event"
        body = "{0}\n{1}\n{2}".format(detail_info, appt_time_info, agent_details["name"])
        
        msg = f'Subject: {subject}\n\n{body}' 
        
        smtp.sendmail(EMAIL_ADDRESS, "jeremy@venturerei.com", msg)
        smtp.sendmail(EMAIL_ADDRESS, agent_details["email"], msg)
        
        
    
    
    
if __name__ == "__main__":
    
    options = Options()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    time.sleep(3)
    
    path = "driver\\chromedriver.exe"
    # driver = Chrome(executable_path=path, chrome_options = options)
    driver = Chrome(executable_path=path)
    
    driver.get("https://listingagent.opendoor.com/appointments?filter=unclaimed")
    
    
    driver.maximize_window()
    time.sleep(10)
    
    bot(driver.page_source, driver)