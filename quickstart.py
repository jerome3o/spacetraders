import os
import json
import requests
from typing import Tuple

_token = os.environ["TOKEN"]
_url = "https://api.spacetraders.io"


def pprint(data: dict):
    print(json.dumps(data, indent=4))


def get_waypoint_components(waypoint: str) -> Tuple[str, str]:
    sector, system, _ = waypoint.split("-")
    system = f"{sector}-{system}"
    return sector, system


def get_agent_info() -> dict:
    response = requests.get(
        f"{_url}/v2/my/agent",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def get_waypoint_info(waypoint: str) -> dict:
    sector, system, _ = waypoint.split("-")
    system = f"{sector}-{system}"

    response = requests.get(
        f"{_url}/v2/systems/{system}/waypoints/{waypoint}",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def get_waypoints(system: str) -> dict:
    response = requests.get(
        f"{_url}/v2/systems/{system}/waypoints",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def get_contracts() -> dict:
    response = requests.get(
        f"{_url}/v2/my/contracts",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def accept_contract(contract_id: str) -> dict:
    response = requests.post(
        f"{_url}/v2/my/contracts/{contract_id}/accept",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def main():
    agent_info = get_agent_info()
    headquarters = agent_info["data"]["headquarters"]

    sector, system = get_waypoint_components(headquarters)
    waypoints = get_waypoints(system)
    pprint(waypoints)

    contracts = get_contracts()
    contract = contracts["data"][0]
    pprint(contract)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
