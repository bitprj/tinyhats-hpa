import random
from locust import HttpUser, TaskSet, between

hats = [
  'cat-ears'
]

def index(l):
    l.client.get("/")


def browseProduct(l):
    l.client.get("/" + random.choice(hats))

class UserBehavior(TaskSet):

    def on_start(self):
        index(self)

    tasks = {index: 1,
        browseProduct: 20,
    }

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)