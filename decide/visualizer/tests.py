from django.test import TestCase, Client
from base import mods

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Testswitchlanguage:
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def tearDown(self):
        self.driver.quit()

    def test_testswitchlanguage(self):
        self.driver.get("http://localhost:8000/visualizer/2/")
        self.driver.set_window_size(945, 1016)
        dropdown = self.driver.find_element(By.NAME, "language")
        dropdown.find_element(By.XPATH, "//option[. = 'Inglés']").click()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
