from locust import HttpUser, task, between

class LoginTestUser(HttpUser):
    wait_time = between(1, 5)  

    @task
    def login(self):
        response = self.client.post("/signin", data={
            "email": "test@mail.com",
            "password": "password"
        })
        if response.status_code == 200:
            print("Login successful")
        else:
            print(f"Login failed")
