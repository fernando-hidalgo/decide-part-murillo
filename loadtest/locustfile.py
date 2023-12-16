import json

from random import choice

from locust import HttpUser, SequentialTaskSet, TaskSet, task, between, events

import itertools

import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


HOST = "http://localhost:8000"
VOTING = 1


class DefVisualizer(TaskSet):
    @task
    def index(self):
        self.client.get("/visualizer/{0}/".format(VOTING))


class DefVoters(SequentialTaskSet):
    def on_start(self):
        with open("voters.json") as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post(
            "/authentication/login/",
            {
                "username": username,
                "password": pwd,
            },
        ).json()

    @task
    def getuser(self):
        self.usr = self.client.post("/authentication/getuser/", self.token).json()

    @task
    def voting(self):
        headers = {
            "Authorization": "Token " + self.token.get("token"),
            "content-type": "application/json",
        }
        self.client.post(
            "/store/",
            json.dumps(
                {
                    "token": self.token.get("token"),
                    "vote": {"a": "12", "b": "64"},
                    "voter": self.usr.get("id"),
                    "voting": VOTING,
                }
            ),
            headers=headers,
        )

    def on_quit(self):
        self.voter = None


class DefVotersYesNo(SequentialTaskSet):
    def on_start(self):
        with open("voters.json") as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post(
            "/authentication/login/",
            {
                "username": username,
                "password": pwd,
            },
        ).json()

    @task
    def getuser(self):
        self.usr = self.client.post("/authentication/getuser/", self.token).json()

    @task
    def voting(self):
        headers = {
            "Authorization": "Token " + self.token.get("token"),
            "content-type": "application/json",
        }
        self.client.post(
            "/store/yesno/",
            json.dumps(
                {
                    "token": self.token.get("token"),
                    "vote": {
                        "a": "64119368847335423641078646156828255749833202653731360808687267447782576175858",
                        "b": "52007631667441025563156436855670910748550693138302081971963757824364607817458",
                    },
                    "voter": self.usr.get("id"),
                    "voting": VOTING,
                }
            ),
            headers=headers,
        )

    def on_quit(self):
        self.voter = None


class DefVotersPreference(SequentialTaskSet):
    def on_start(self):
        with open("voters.json") as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post(
            "/authentication/login/",
            {
                "username": username,
                "password": pwd,
            },
        ).json()

    @task
    def getuser(self):
        self.usr = self.client.post("/authentication/getuser/", self.token).json()

    @task
    def voting(self):
        headers = {
            "Authorization": "Token " + self.token.get("token"),
            "content-type": "application/json",
        }
        self.client.post(
            "/store/preference/",
            json.dumps(
                {
                    "token": self.token.get("token"),
                    "vote": {
                        "a": "69529957725889040311609873320104549818830701945574049611265050537691555907406",
                        "b": "6543397338357564287800663518400903625081871529329623372835477067005646573025",
                    },
                    "voter": self.usr.get("id"),
                    "voting": VOTING,
                }
            ),
            headers=headers,
        )

    def on_quit(self):
        self.voter = None


class DefVotersMultichoice(SequentialTaskSet):
    def on_start(self):
        with open("voters.json") as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post(
            "/authentication/login/",
            {
                "username": username,
                "password": pwd,
            },
        ).json()

    @task
    def getuser(self):
        self.usr = self.client.post("/authentication/getuser/", self.token).json()

    @task
    def voting(self):
        headers = {
            "Authorization": "Token " + self.token.get("token"),
            "content-type": "application/json",
        }
        self.client.post(
            "/store/multichoice/",
            json.dumps(
                {
                    "token": self.token.get("token"),
                    "vote": {"a": "658373672383", "b": "573615163433"},
                    "voter": self.usr.get("id"),
                    "voting": VOTING,
                }
            ),
            headers=headers,
        )

    def on_quit(self):
        self.voter = None


class DefUsers(SequentialTaskSet):
    username_counter = itertools.count()

    def on_start(self):
        # Generate unique username
        base_username = "testuser"
        username = f"{base_username}_{next(self.username_counter)}"
        self.username = username
        self.password = "ThisIsATestPasswordThatIsSecure"

    @task
    def register_user(self):

        # Perform registration request
        response = self.client.post(
            "/authentication/registeruser/",
            {
                "username": self.username,
                "email": f"{self.username}@example.com",
                "email_conf": f"{self.username}@example.com",
                "password": "ThisIsATestPasswordThatIsSecure",
                "password_conf": "ThisIsATestPasswordThatIsSecure",
            },
        )

    @task
    def login(self):
        username = self.username
        pwd = self.password
        self.token = self.client.post(
            "/authentication/login/",
            {
                "username": username,
                "password": pwd,
            },
        ).json()

    @task
    def getuser(self):
        self.usr = self.client.post("/authentication/getuser/", self.token).json()
        print(str(self.user))

    def on_quit(self):
        self.username = None
        self.password = None


class DefCensus(SequentialTaskSet):
    def on_start(self):
        self.driver = webdriver.Firefox()
        self.vars = {}

    @task
    def test_cargaexportacion(self):
        self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
        self.driver.set_window_size(550, 662)
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        self.driver.find_element(By.LINK_TEXT, "Censuss").click()
        self.driver.find_element(By.ID, "action-toggle").click()
        self.driver.find_element(By.NAME, "action").click()
        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Exportar a Excel']").click()
        self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(4)").click()
        self.driver.find_element(By.NAME, "index").click()

    def on_quit(self):
        self.driver.quit()


class DefBooth(TaskSet):
    @task
    def index(self):
        self.client.get("/booth/{0}/".format(VOTING))


class DefBoothYesNo(TaskSet):
    @task
    def index(self):
        self.client.get("/booth/yesno/{0}/".format(VOTING))


class DefBoothPreference(TaskSet):
    @task
    def index(self):
        self.client.get("/booth/preference/{0}/".format(VOTING))


class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3, 5)


class Voters(HttpUser):
    host = HOST
    tasks = [DefVoters]
    wait_time = between(3, 5)


class VotersYesNo(HttpUser):
    host = HOST
    tasks = [DefVotersYesNo]
    wait_time = between(3, 5)


class VotersPreference(HttpUser):
    host = HOST
    tasks = [DefVotersPreference]
    wait_time = between(3, 5)


class VotersMultichoice(HttpUser):
    host = HOST
    tasks = [DefVotersMultichoice]
    wait_time = between(3, 5)


class Users(HttpUser):
    host = HOST
    tasks = [DefUsers]
    wait_time = between(3, 5)


class Census(HttpUser):
    host = HOST
    tasks = [DefCensus]
    wait_time = between(3, 5)


class Booth(HttpUser):
    host = HOST
    tasks = [DefBooth]
    wait_time = between(3, 5)


class BoothYesNo(HttpUser):
    host = HOST
    tasks = [DefBoothYesNo]
    wait_time = between(3, 5)


class BoothPreference(HttpUser):
    host = HOST
    tasks = [DefBoothPreference]
    wait_time = between(3, 5)
