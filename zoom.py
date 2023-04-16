import time
import obsws_python as obs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)
#create list of tuples
#each tuple is a (link, time) pair
#link is the link to the video
#time is the time in seconds to wait before switching to the next video
links = ["https://fhnw.zoom.us/rec/share/TAdBMvOUwUeBPSL8AO2_nmR81Qu4rF17tYJsvVPYHtW350K089Lb57Tlcp9sTTKm.OX_uEh4SHFrJXCB6?startTime=1678968540000",
         "https://fhnw.zoom.us/rec/share/UH9HJbYaex91CDgCB0cwYwpv2slIS2cXVAtO-ep_EdVS7_KCZgcFdwXYmCqfbNHU.G-6McAHp8mSFFCyf?startTime=1679573448000",
         "https://fhnw.zoom.us/rec/share/KkjPu9Hd8VyJNtx2qZfsXGrT0azWqpFmFlsPdIwB9UKd0rmzXx8V4e03QwLWZhlZ.11pkhOVi8WCps9jB?startTime=1680174673000"]

# OBS websocket settings
host = "ip adress"
port = 4455
password = "password"

cl = obs.ReqClient(host=host, port=port, password=password)
print(f'client created at {time.ctime()}')

driver = webdriver.Firefox(executable_path='./geckodriver/geckodriver.exe')


print(f'driver created at {time.ctime()}')



for link in links:
    driver.get(link)
    driver.maximize_window()
    duration=WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".vjs-time-range-duration"))).text
    duration_seconds = get_sec(duration)

    
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "zm-icon-fullscreen")))
    driver.find_element(By.CLASS_NAME, "zm-icon-fullscreen").click()
    time.sleep(2)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "vjs-play-control")))
    driver.find_element(By.CLASS_NAME, "vjs-play-control").click()
    cl.start_record()
    print(f'starting recording {link} at {time.ctime()}')
    #print current system time

    time.sleep(duration_seconds)
    cl.stop_record()
    print(f'recorded video {link} at {time.ctime()}')