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


def purchase_ship(ship_type: str, waypoint: str) -> dict:
    response = requests.post(
        f"{_url}/v2/my/ships",
        headers={"Authorization": f"Bearer {_token}"},
        json={
            "shipType": ship_type,
            "waypointSymbol": waypoint,
        },
    )
    return response.json()


def get_ship_info(ship_id: str) -> dict:
    response = requests.get(
        f"{_url}/v2/my/ships/{ship_id}",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def ship_dock(ship_id: str) -> dict:
    response = requests.post(
        f"{_url}/v2/my/ships/{ship_id}/dock",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def ship_orbit(ship_id: str) -> dict:
    response = requests.post(
        f"{_url}/v2/my/ships/{ship_id}/orbit",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def ship_extract(ship_id: str) -> dict:
    response = requests.post(
        f"{_url}/v2/my/ships/{ship_id}/extract",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def main():
    output = purchase_ship("SHIP_MINING_DRONE", "X1-ZT91-25027X")
    pprint(output)
    # agent_info = get_agent_info()
    # headquarters = agent_info["data"]["headquarters"]

    # sector, system = get_waypoint_components(headquarters)
    # waypoints = get_waypoints(system)
    # pprint(waypoints)
    # waypoints_with_shipyards = [
    #     w
    #     for w in waypoints["data"]
    #     if any([trait["symbol"] == "SHIPYARD" for trait in w["traits"]])
    # ]
    # print(waypoints_with_shipyards)

    # contracts = get_contracts()
    # contract = contracts["data"][0]
    # pprint(contract)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
