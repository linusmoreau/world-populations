import selenium.webdriver
from msedge.selenium_tools.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

from webdriver_manager.microsoft import EdgeChromiumDriverManager


def wait():
    time.sleep(0.5)


def pixel_shift(value, mini, maxi, width):
    return (value - mini) / (maxi - mini) * width


def get_map(year, data, driver: WebDriver):
    wait()
    save_button = driver.find_element(By.ID, "downup")
    driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
    save_button.click()

    file_input = driver.find_element(By.ID, "upload-txt-inp")
    file_input.send_keys(data)

    wait()
    upload_button = driver.find_element(By.ID, "upload-config")
    driver.execute_script("arguments[0].scrollIntoView(true);", upload_button)
    upload_button.click()

    wait()
    slider = driver.find_element(By.CLASS_NAME, "slider.slider-horizontal")
    slider_button = slider.find_element(By.CLASS_NAME, "slider-handle.min-slider-handle.round")
    driver.execute_script("arguments[0].scrollIntoView(true);", slider_button)
    a = selenium.webdriver.ActionChains(driver)
    a.click_and_hold(slider_button).move_by_offset(
        -pixel_shift(int(slider_button.get_attribute("aria-valuenow")),
                     int(slider_button.get_attribute("aria-valuemin")),
                     int(slider_button.get_attribute("aria-valuemax")),
                     slider.size["width"]), 0).release().perform()
    a.click_and_hold(slider_button).move_by_offset(
        pixel_shift(min(year, int(slider_button.get_attribute("aria-valuemax"))),
                    int(slider_button.get_attribute("aria-valuemin")),
                    int(slider_button.get_attribute("aria-valuemax")),
                    slider.size["width"]), 0).release().perform()

    wait()
    preview_button = driver.find_element(By.ID, "convert")
    driver.execute_script("arguments[0].scrollIntoView(true);", preview_button)
    preview_button.click()

    wait()
    wait()
    download_button = driver.find_element(By.ID, "download")
    driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
    download_button.click()

    wait()
    edit_button = driver.find_element(By.ID, "edit")
    driver.execute_script("arguments[0].scrollIntoView(true);", edit_button)
    edit_button.click()


def get_maps(dataset):
    options = Options()
    service = Service(executable_path=EdgeChromiumDriverManager().install())
    with webdriver.Edge(service=service, options=options) as driver:
        driver.get("https://historicalmapchart.net/world-cold-war.html")
        driver.maximize_window()
        time.sleep(3)
        for year, data in dataset.items():
            while True:
                try:
                    print("Getting year", year)
                    get_map(year, data, driver)
                    break
                except:
                    pass
        wait()



