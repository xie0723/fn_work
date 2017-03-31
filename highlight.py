# coding=utf-8
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from functools import wraps
import time
from datetime import datetime


# 获取当前时间
def get_now_time():
    return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


# 高亮元素and截图
def highlight(element, element_name=None, debug=True):
    """
    :param element:  定位到的元素
    :param element_name: 定位元素名
    :param debug: 开关截图功能
    :return:
    """
    # 执行js 高亮元素
    def apply_style():
        js = "arguments[0].style.border='4px solid red'"
        driver.execute_script(js, element)

    # 截图
    def screen_shot(screen_name):
        driver.save_screenshot(screen_name)

    if debug:
        try:
            screen_shot(str(element_name) + '_before.jpg')
            apply_style()
            screen_shot(str(element_name) + '_after.jpg')
        except Exception as e:
            return e

    apply_style()


# 高亮元素装饰器
def highlights(func):

    def apply_style(element):
        js = "arguments[0].style.border='4px solid red'"
        driver.execute_script(js, element)

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        element = func(self, *args, **kwargs)
        apply_style(element)
        return element

    return wrapper

# 截图装饰器
def screenshot(func):

    def screen_shot(screen_name):
        driver.save_screenshot(screen_name)

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        element = func(self, *args, **kwargs)

        screen_shot(str(args[-1]) + '.jpg')
        return element


    return wrapper

# 定位封装
class Action(object):
    def __init__(self, driver):
        self.driver = driver

    @screenshot
    @highlights
    def find_element(self, *loc):
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except Exception as e:
            return e


driver = webdriver.Chrome()

driver.get('http://www.baidu.com')

action = Action(driver)
element = driver.find_element(By.ID, 'kw')
highlight(element, 'kw')

time.sleep(3)
driver.quit()
