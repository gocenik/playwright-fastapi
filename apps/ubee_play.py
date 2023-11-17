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
        self.log("Initializing Ubee System Info Reader App")
        self.listen_state(self.run_system_info_reader, "input_boolean.run_ubee_system_info_reader", new="on")

    def run_system_info_reader(self, entity, attribute, old, new, kwargs):
        try:
            username = self.get_state("input_text.ubee_username")  
            password = self.get_state("input_text.ubee_password")
            url = self.get_state("input_text.ubee_evw32c_url")
            login_info = LoginInfo(username=username, password=password, url=url)

            response = requests.post("http://192.168.160.2:5000/run_system_info_reader/", json=login_info.dict())

            # Check the status code of the response
            if response.status_code == 200:
                # The request was successful
                self.log("Request was successful")
                self.log(response.json())
            else:
                # The request was not successful
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