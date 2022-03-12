import selenium.webdriver
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
import time


def pixel_shift(value, mini, maxi, width):
    return (value - mini) / (maxi - mini) * width


def get_maps(dataset):
    service = Service(executable_path=EdgeChromiumDriverManager().install())
    for year, data in dataset.items():
        while True:
            try:
                get_map(year, data, service)
                break
            except:
                pass


def get_map(year, data, service):
    with webdriver.Edge(service=service) as driver:
        driver.implicitly_wait(10)
        driver.get("https://historicalmapchart.net/world-cold-war.html")
        time.sleep(1)
        save_button = driver.find_element(By.ID, "downup")
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        save_button.click()

        data_box = driver.find_element(By.ID, "upload-textarea")
        data_box.send_keys(data)

        time.sleep(1)
        upload_button = driver.find_element(By.ID, "upload-config")
        driver.execute_script("arguments[0].scrollIntoView(true);", upload_button)
        upload_button.click()

        time.sleep(1)
        slider = driver.find_element(By.CLASS_NAME, "slider.slider-horizontal")
        slider_button = slider.find_element(By.CLASS_NAME, "slider-handle.min-slider-handle.round")
        driver.execute_script("arguments[0].scrollIntoView(true);", slider_button)
        a = selenium.webdriver.ActionChains(driver)
        a.click_and_hold(slider_button).move_by_offset(
            pixel_shift(year, int(slider_button.get_attribute("aria-valuemin")),
                        int(slider_button.get_attribute("aria-valuemax")), slider.size["width"]), 0).release().perform()

        time.sleep(1)
        preview_button = driver.find_element(By.ID, "convert")
        driver.execute_script("arguments[0].scrollIntoView(true);", preview_button)
        preview_button.click()

        time.sleep(1)
        download_button = driver.find_element(By.ID, "download")
        driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
        download_button.click()
        time.sleep(1)


