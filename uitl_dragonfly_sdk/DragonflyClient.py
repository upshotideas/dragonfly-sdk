from typing import Dict, Any

import requests
import json

from uitl_dragonfly_sdk.common.DragonflyException import DragonflyException
from uitl_dragonfly_sdk.common.util import verify_mandatory_param, DRAGONFLY_API_HEALTH_REPORT_URL, DEFAULT_MIN_DCR


class DragonflyClient:
    def __init__(self: "DragonflyClient",
                 client_id: str,
                 client_secret: str,
                 auth_server_realm_baseurl: str,
                 api_server_baseurl: str) -> None:
        self.access_token = None

        verify_mandatory_param(client_id, "client_id")
        verify_mandatory_param(client_secret, "client_secret")
        verify_mandatory_param(auth_server_realm_baseurl, "auth_server_realm_baseurl")
        verify_mandatory_param(api_server_baseurl, "api_server_baseurl")

        self.auth_server_url = f"{auth_server_realm_baseurl}/protocol/openid-connect/token"
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_server_baseurl = api_server_baseurl
        self._minimum_dcr = DEFAULT_MIN_DCR

        self.get_new_access_token()

    # @property
    # def minimum_dcr(self) -> float:
    #     return self._minimum_dcr
    #
    # @minimum_dcr.setter
    # def minimum_dcr(self, dcr: float) -> None:
    #     self._minimum_dcr = dcr

    def get_new_access_token(self):
        self.access_token = self.get_token()

    def get_token(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", self.auth_server_url, headers=headers, data=payload, verify=False)

        if response.status_code != 200:
            raise DragonflyException("Failed to get access token. Reason: {}", response.text)

        response_data = json.loads(response.text)
        return response_data["access_token"]

    def run_health_report(self, pipeline_id: int = 0, component_id: int = 0, run_id: str = "", pipeline_name: str = "",
                          component_name: str = "") -> Any:
        # , log_result: bool = False, fail_on_low_dcr: bool = False
        if not pipeline_id and not pipeline_name:
            raise DragonflyException("Either pipeline_id or pipeline_name must be provided.")

        health_report_url = self.api_server_baseurl + DRAGONFLY_API_HEALTH_REPORT_URL
        headers = self.build_auth_headers()

        payload: Dict[str, int | str] = {}
        if pipeline_id != 0:
            payload["pipelineId"] = pipeline_id
        if component_id != 0:
            payload["componentId"] = component_id
        if pipeline_name != "":
            payload["pipelineName"] = pipeline_name
        if component_name != "":
            payload["componentName"] = component_name
        if run_id != "":
            payload["runId"] = run_id

        response = requests.request("POST", health_report_url, headers=headers, json=payload, verify=False)

        if response.status_code != 200:
            raise DragonflyException("Failed to execute health report. Reason: {}", response.text)

        health_log = response.json()
        return health_log

    def build_auth_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_token}"
        }

    # def print_component_health(self, health_log: Any):
    #     print("============================== Dragonfly Log: Start ==============================")
    #     print(f"Task Id: {health_log['name']}")
    #     print(f"Task Health: {health_log['health']['value']}")
    #     print(f"Task Dependencies Health: {health_log['health']['dependenciesHealth']}")
    #     print("Executed Checks:")
    #     for ch in (health_log['health']["executedChecks"] or []):
    #         print("----- Dragonfly Check Result -----")
    #         print(f"\tCheck Name: {ch['healthCheckName']}")
    #         print(f"\tCheck Result Health: {ch['value']}")
    #         print(f"\tCheck Additional Information: {ch['meta']}")
    #         print("----------------------------------")
    #
    #     print("=============================== Dragonfly Log: End ===============================")
    #
