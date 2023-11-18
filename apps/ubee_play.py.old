import appdaemon.plugins.hass.hassapi as hass
import requests
import json
from pydantic import BaseModel
from requests.exceptions import RequestException

class LoginInfo(BaseModel):
    username: str
    password: str
    url: str

class UbeePlayApp(hass.Hass):

    def initialize(self):
        """
        Initializes the Ubee System Info Reader App.
        """
        self.log("Initializing Ubee System Info Reader App")
        self.listen_state(self.run_system_info_reader, "input_boolean.run_ubee_system_info_reader", new="on")

        username = self.get_state("input_text.ubee_username")
        password = self.get_state("input_text.ubee_password")
        url = self.get_state("input_text.ubee_evw32c_url")

        if username is None or password is None or url is None:
            self.log("One or more values are missing")
            return

        login_info = LoginInfo(username=username, password=password, url=url)

        self.log(f"Received username: {username}")
        self.log(f"Received password: {password}")
        self.log(f"Received URL: {url}")

        response = requests.post("http://192.168.160.2:5000/run_system_info_reader/", json=login_info.dict())

        if response.status_code == 200:
            self.log("Request was successful")
            self.log(response.json())
        else:
            self.log(f"Request failed with status code {response.status_code}")
            self.log(response.text)

    def run_system_info_reader(self, entity: str, attribute: str, old: str, new: str, kwargs: dict) -> None:
        """
        Retrieves the username, password, and URL from input_text entities in Home Assistant.
        Creates a LoginInfo object with the retrieved values.
        Sends a POST request to a specified URL with the JSON representation of the LoginInfo object.
        Logs the response if the request is successful, otherwise logs the status code and response text.

        Args:
            entity (str): The entity that triggered the method.
            attribute (str): The attribute of the entity that triggered the method.
            old (str): The old value of the entity.
            new (str): The new value of the entity.
            kwargs (dict): Additional keyword arguments.

        Returns:
            None: Logs information about the request and response.
        """
        if new != "on":
            return

        try:
            username = self.get_state("input_text.ubee_username")
            password = self.get_state("input_text.ubee_password")
            url = kwargs.get("url")
            if url is None:
                self.log("URL is missing")
                return

            if not self.validate_url(url):
                self.log("Invalid URL")
                return

            login_info = LoginInfo(username=username, password=password, url=url)

            self.log(f"Received username: {username}")
            self.log(f"Received password: {password}")
            self.log(f"Received URL: {url}")

            response = requests.post("http://192.168.160.2:5000/run_system_info_reader/", json=login_info.dict())

            if response.status_code == 200:
                self.log("Request was successful")
                self.log(response.json())
            else:
                self.log(f"Request failed with status code {response.status_code}")
                self.log(response.text)

        except RequestException as e:
            self.error(f"Error in run_system_info_reader: {e}")
        except Exception as e:
            self.error(f"Unexpected error in run_system_info_reader: {e}")

    def validate_url(self, url: str) -> bool:
        """
        Validates the given URL.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        # Add URL validation logic here
        return True

    class LoginInfo(BaseModel):
        """
        Represents the login information.
        """
        username: str
        password: str
        url: str

    def run_system_info_reader(self, entity: str, attribute: str, old: str, new: str, kwargs: dict) -> None:
        """
        Retrieves the username, password, and URL from input_text entities in Home Assistant.
        Creates a LoginInfo object with the retrieved values.
        Sends a POST request to a specified URL with the JSON representation of the LoginInfo object.
        Logs the response if the request is successful, otherwise logs the status code and response text.

        Args:
            entity (str): The entity that triggered the method.
            attribute (str): The attribute of the entity that triggered the method.
            old (str): The old value of the entity.
            new (str): The new value of the entity.
            kwargs (dict): Additional keyword arguments.

        Returns:
            None: Logs information about the request and response.
        """
        try:
            username = self.get_state("input_text.ubee_username")
            password = self.get_state("input_text.ubee_password")
            url = self.get_state("input_text.ubee_evw32c_url")
            login_info = LoginInfo(username=username, password=password, url=url)

            self.log(f"Received username: {username}")
            self.log(f"Received password: {password}")
            self.log(f"Received URL: {url}")

            response = requests.post("http://192.168.160.2:5000/run_system_info_reader/", json=login_info.dict())

            if response.status_code == 200:
                self.log("Request was successful")
                self.log(response.json())
            else:
                self.log(f"Request failed with status code {response.status_code}")
                self.log(response.text)

        except RequestException as e:
            self.error(f"Error in run_system_info_reader: {e}")
        except Exception as e:
            self.error(f"Unexpected error in run_system_info_reader: {e}")

    def update_home_assistant_entities(self, data):
        if "error" in data:
            self.log("Error received from FastAPI app: " + data["error"])
            return

        # Assuming data is a dictionary with the keys matching the entity_id suffixes
        for key, value in data.items():
            entity_id = f"input_text.station1_{key}"
            self.call_service("input_text/set_value", entity_id=entity_id, value=value)
            self.log(f"{key.replace('_', ' ').title()} updated: {value}")
