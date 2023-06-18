import os
import json
import requests
from typing import Tuple
from datetime import datetime, timezone
import time

_token = os.environ["TOKEN"]
_url = "https://api.spacetraders.io"


def pprint(data: dict):
    print(json.dumps(data, indent=4))


def is_past(timestamp: str) -> bool:
    datetime_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    datetime_obj = datetime_obj.replace(tzinfo=timezone.utc)
    current_time = datetime.now(timezone.utc)
    return current_time > datetime_obj

def wait_until(timestamp: str):
    while not is_past(timestamp):
        time.sleep(10)



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


def ship_navigate(ship_id: str, destination: str) -> dict:
    response = requests.post(
        f"{_url}/v2/my/ships/{ship_id}/navigate",
        headers={"Authorization": f"Bearer {_token}"},
        json={"waypointSymbol": destination},
    )
    return response.json()


def ship_refuel(ship_id: str) -> dict:
    response = requests.post(
        f"{_url}/v2/my/ships/{ship_id}/refuel",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def contract_deliver(
    contract_id: str,
    ship_id: str,
    trade_symbol: str,
    units: int,
) -> dict:
    response = requests.post(
        f"{_url}/v2/my/contracts/{contract_id}/deliver",
        headers={"Authorization": f"Bearer {_token}"},
        json={
            "shipSymbol": ship_id,
            "tradeSymbol": trade_symbol,
            "units": units,
        },
    )
    return response.json()


def contract_deliver_all_available(
    contract_id: str,
    ship_id: str,
):
    contract_info = get_contract_info(contract_id)
    ship_info = get_ship_info(ship_id)
    cargo_info = ship_info["data"]["cargo"]

    relevant_cargo_symbol = contract_info["data"]["terms"]["deliver"][0]["tradeSymbol"]

    relevant_cargo_units = 0
    for cargo in cargo_info["inventory"]:
        if cargo["symbol"] == relevant_cargo_symbol:
            relevant_cargo_units += cargo["units"]

    contract_deliver(
        contract_id=contract_id,
        ship_id=ship_id,
        trade_symbol=relevant_cargo_symbol,
        units=relevant_cargo_units,
    )


def get_contract_info(contract_id: str) -> dict:
    response = requests.get(
        f"{_url}/v2/my/contracts/{contract_id}",
        headers={"Authorization": f"Bearer {_token}"},
    )
    return response.json()


def contract_is_complete(contract_id: str) -> bool:
    contract = get_contract_info(contract_id)

    deliver_details = contract["data"][0]["terms"]["deliver"][0]
    return deliver_details["unitsRequired"] <= deliver_details["unitsFulfilled"]


def ready_to_deliver(contract_id: str, ship_id: str) -> bool:
    contract_info = get_contract_info(contract_id)
    ship_info = get_ship_info(ship_id)
    cargo_info = ship_info["data"]["cargo"]

    capacity = cargo_info["capacity"]
    relevant_cargo_symbol = contract_info["data"]["terms"]["deliver"][0]["tradeSymbol"]

    relevant_cargo_units = 0
    for cargo in cargo_info["inventory"]:
        if cargo["symbol"] == relevant_cargo_symbol:
            relevant_cargo_units += cargo["units"]

    return relevant_cargo_units >= capacity * 0.9


def ship_is_full(ship_id: str) -> bool:
    ship_info = get_ship_info(ship_id)
    cargo = ship_info["data"]["cargo"]
    return cargo["units"] == cargo["capacity"]


def sell_non_contract_goods(ship_id: str, contract_id: str) -> dict:
    contract_info = get_contract_info(contract_id)
    ship_info = get_ship_info(ship_id)
    cargo_info = ship_info["data"]["cargo"]

    relevant_cargo_symbol = contract_info["data"]["terms"]["deliver"][0]["tradeSymbol"]

    for cargo in cargo_info["inventory"]:
        if cargo["symbol"] != relevant_cargo_symbol:
            sell_goods(ship_id, cargo["symbol"], cargo["units"])


def sell_goods(ship_id: str, symbol: str, units: str) -> dict:
    response = requests.post(
        f"{_url}/v2/my/ships/{ship_id}/sell",
        headers={"Authorization": f"Bearer {_token}"},
        json={
            "symbol": symbol,
            "unit": units,
        },
    )
    return response.json()


def contract_automation(
    contract_id: str,
    ship_id: str,
    asteroid_field: str,
) -> dict:
    # assumption: all contracts require extraction from an asteroid field

    # for each ship
    contract_info = get_contract_info(contract_id)
    contract_location = contract_info["data"][0]["terms"]["deliver"][0][
        "destinationSymbol"
    ]

    # do this loop until contract is fulfilled
    while not contract_is_complete(contract_id):
        # navigate to asteroid field
        navigation = ship_navigate(ship_id, asteroid_field)
        # dock, refuel, orbit
        ship_dock(ship_id)
        ship_refuel(ship_id)
        ship_orbit(ship_id)

        # do this loop until 90% cargo full of contract goods
        while ready_to_deliver(contract_id, ship_id):
            while not ship_is_full(ship_id):
                # extract from the asteroid field untill cargo full
                ship_extract(ship_id)

            # dock
            ship_dock(ship_id)

            # sell non-contract goods
            sell_non_contract_goods(ship_id, contract_id)

            # orbit
            ship_orbit(ship_id)

        # navigate to contract destination
        ship_navigate(ship_id, contract_location)

        # dock, deliver, refuel, orbit
        ship_dock(ship_id)

        contract_deliver_all_available(
            contract_id=contract_id,
            ship_id=ship_id,
        )
    # fulfill contract


def main():
    output = purchase_ship("SHIP_MINING_DRONE", "X1-ZT91-25027X")
    pprint(output)

    contract_automation(
        contract_id="",
        ship_id="JERMO-3",
        asteroid_field="X1-ZT91-18205B",
    )

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
