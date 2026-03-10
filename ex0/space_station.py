#!/usr/bin/env python3
# ########################################################################### #
#                                                                             #
#                                                          :::      ::::::::  #
#   space_station.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/08 16:27:07 by bbeaurai            #+#    #+#            #
#   Updated: 2026/03/10 11:49:39 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import sys
from typing import Optional, List, Dict
from datetime import datetime


green = "\033[32m\033[1m\033[1m"
red = "\033[31m\033[5m\033[1m"
redp = "\033[31m"
brown = "\033[0;33m"
blue = "\033[38;5;67m"
reset = "\033[0m"

# =============================================================================
# ================================ TEST =======================================
# =============================================================================

try:
    if (sys.prefix == sys.base_prefix):
        raise AttributeError(
            "Must be execute in Virtual Environment" + "\n\n"
            f"{blue}# Create your Virtual Environment" + "\n"
            f"{brown}$ python3 -m venv env_space" + "\n"
            "$ source env_space/bin/activate" + "\n"
            f"{blue}# And install pydentic" + "\n"
            f"{brown}$ pip install -U pydantic{reset}" + "\n"
                )

except AttributeError as e:
    print("\n" + f"{red}[ERROR]{reset}", e)
    exit()

try:
    from pydantic import BaseModel, Field, ValidationError
except ModuleNotFoundError:
    print(
        "\n" + f"{red}[ERROR]{reset} pydantic is not installed, "
        "install it as follows" + "\n\n"
        f"{blue}# Install pydentic" + "\n"
        f"{brown}$ pip install -U pydantic" + "\n"
            )
    exit()

# =============================================================================
# ============================ Base Model =====================================
# =============================================================================


# 'ge' is GREATER-THAN and 'le' is LESS-THAN
class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


# =============================================================================
# ================================ MAIN =======================================
# =============================================================================


# pip install -U pydantic desinstall lancienne et install la nouvelle
def main(data_stations: List[Dict[str, str]]) -> None:

    print("\n" + "Space Station Data Validation" + "\n")
    print("".center(79, "="))

    for data in data_stations:
        try:
            station = SpaceStation(**data)
            print("Valid station created:")
            print("ID:", station.station_id)
            print("Name:", station.name)
            print("Crew:", station.crew_size, "people")
            print(f"Power {station.power_level}%")
            print(f"Oxygen {station.oxygen_level}%")

            if (station.is_operational is True):
                print("Status: Operational")

            else:
                print("Status: Not Operational")
            print("\n" + "".center(79, "="))

        except ValidationError as e:
            print(f"{red}[ERROR]{reset} "
                  "Expected validation error:")
            print(e.errors()[0]["msg"])
            print("\n" + "".center(79, "="))
        except (ValueError, TypeError) as e:
            print(f"{red}[ERROR]{reset} "
                  "Expected validation error:")
            print(e)


if __name__ == "__main__":

    data_stations = [
            {
                "station_id": "ISS001",
                "name": "International Space Station",
                "crew_size": 6,
                "power_level": 85.5,
                "oxygen_level": 92.3,
                "last_maintenance": datetime.now(),
                "is_operational": True,
                "notes": ""
            },
            {
                "station_id": "ISS001",
                "name": "International Space Station",
                "crew_size": 42,
                "power_level": 85.5,
                "oxygen_level": 92.3,
                "last_maintenance": datetime.now(),
                "is_operational": True,
                "notes": ""
            },
                    ]

    main(data_stations)
