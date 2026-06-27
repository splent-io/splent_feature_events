from locust import HttpUser, TaskSet, task
from splent_framework.environment.host import get_host_for_locust_testing


class SplentFeatureEventsBehavior(TaskSet):
    def on_start(self):
        self.index()

    @task
    def index(self):
        response = self.client.get("/splent_feature_events")

        if response.status_code != 200:
            print(f"SplentFeatureEvents index failed: {response.status_code}")


class SplentFeatureEventsUser(HttpUser):
    tasks = [SplentFeatureEventsBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
