import json

from random import choice

from locust import HttpUser, SequentialTaskSet, TaskSet, task, between, events

import itertools


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
        print(str(self.user))

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


class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3, 5)


class Voters(HttpUser):
    host = HOST
    tasks = [DefVoters]
    wait_time = between(3, 5)


class Users(HttpUser):
    host = HOST
    tasks = [DefUsers]
    wait_time = between(3, 5)
