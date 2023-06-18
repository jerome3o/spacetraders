import os
import requests
from pprint import pprint

_token = os.environ["TOKEN"]
_url = "https://api.spacetraders.io"


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
    pprint(response.json())




def main():
    agent_info = get_agent_info()
    pprint(agent_info)

    headquarters = agent_info["data"]["headquarters"]
    waypoint_info = get_waypoint_info(headquarters)



if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
