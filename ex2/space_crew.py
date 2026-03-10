#!/usr/bin/env python3
# ########################################################################### #
#                                                                             #
#                                                          :::      ::::::::  #
#   space_crew.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/09 16:54:23 by bbeaurai            #+#    #+#            #
#   Updated: 2026/03/10 13:02:14 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import sys
from typing import List, Dict

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
    from typing_extensions import Self
    from pydantic import BaseModel, Field, ValidationError, model_validator
    from enum import Enum
    from datetime import datetime

except AttributeError as e:
    print("\n" + f"{red}[ERROR]{reset}", e)
    exit()

except ModuleNotFoundError:
    print(
        "\n" + f"{red}[ERROR]{reset} pydantic is not installed, "
        "install it as follows" + "\n\n"
        f"{blue}# Install pydentic" + "\n"
        f"{brown}$ pip install -U pydantic" + "\n"
            )
    exit()


# =============================================================================
# ================================ ENUM =======================================
# =============================================================================


class Rank(Enum):
    CADET = "cadet"
    OFFICIER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


# =============================================================================
# ============================= BASEMODEL =====================================
# ================================ #1 =========================================


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


# =============================================================================
# ============================= BASEMODEL =====================================
# ================================ #2 =========================================


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(strict=True, min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    # Mission ID must start with "M"
    @model_validator(mode="after")
    def check_id(self) -> Self:
        if (not self.mission_id.startswith("M")):
            raise ValueError("Mission ID must start with \"M\"")
        return (self)

    # Must have at least one Commander or Captain
    @model_validator(mode="after")
    def check_rank(self) -> Self:
        for crew in self.crew:
            if (crew.rank.value == "commander" or
                    crew.rank.value == "captain"):
                return (self)
        raise ValueError("Mission must have at least one Commander or Captain")

    # Long missions (> 365 days) need 50% experienced crew (5+ years)
    @model_validator(mode="after")
    def check_exp(self) -> Self:
        years = []
        count = 0
        if (self.duration_days > 365):
            for crew in self.crew:
                years.append(crew.years_experience)
        for year in years:
            if (year >= 5):
                count += 1
        if ((len(years) / 2) <= count):
            return (self)
        raise ValueError("The mission requires 50% experienced crew ""(5 years"
                         " or more) for a long-duration mission (> 365 days).")

    # All crew members must be active
    @model_validator(mode="after")
    def check_active(self) -> Self:
        for crew in self.crew:
            if (crew.is_active is False):
                raise ValueError("All crew members must be active")
        return (self)


# =============================================================================
# =============================== MAIN ========================================
# =============================================================================


def main(space_mission: List[Dict[str, str]]) -> None:

    try:
        for mission in space_mission:
            m = SpaceMission(**mission)
            print("Valid station created:")
            print(f"Mission: {m.mission_name}")
            print(f"ID: {m.mission_id}")
            print(f"Destination: {m.destination}")
            print(f"Duration: {m.duration_days} days")
            print(f"Budget: {m.budget_millions}M")
            print(f"Crew size: {len(m.crew)}")
            print("Crew members:")
            for member in m.crew:
                print(f"- {member.name} ({member.rank.value}) - "
                      f"{member.specialization}")
            print("\n" + "".center(79, "="))

    except (ValueError, ValidationError, TypeError) as e:
        print(f"{red}[ERROR]{reset} Expected validation error:")
        print(e.errors()[0]["msg"][13:])


if __name__ == "__main__":

    print("\n" + "Space Mission Crew Validation" + "\n")
    print("".center(79, "="))

# *****************************************************************************
# *                                 data 1                                    *
# *                                                                           *

    data_member = [
            {
                "member_id": "SC_2006",
                "name": "Sarah Connor",
                "rank": Rank.COMMANDER,
                "age": 36,
                "specialization": "Mission Command",
                "years_experience": 20,
                "is_active": True,
            },
            {
                "member_id": "JS_2014",
                "name": "John Smith",
                "rank": Rank.LIEUTENANT,
                "age": 31,
                "specialization": "Navigation",
                "years_experience": 12,
                "is_active": True,
            },
            {
                "member_id": "AJ_2018",
                "name": "Alice Johnson",
                "rank": Rank.OFFICIER,
                "age": 27,
                "specialization": "Navigation",
                "years_experience": 8,
                "is_active": True,
            },
                  ]

    total_member: List[CrewMember] = []
    for data in data_member:
        try:
            member = CrewMember(**data)
            total_member.append(member)
        except (ValueError, ValidationError, TypeError) as e:
            print(f"{red}[ERROR]{reset} Expected validation error:")
            print(e.errors()[0]["msg"][13:])

# *****************************************************************************
# *                                 data 2                                    *
# *                                                                           *

    data_member2 = [
            {
                "member_id": "SC_2006",
                "name": "Sarah Connor",
                "rank": Rank.CADET,
                "age": 36,
                "specialization": "Mission Command",
                "years_experience": 5,
                "is_active": True,
            },
            {
                "member_id": "JS_2014",
                "name": "John Smith",
                "rank": Rank.CADET,
                "age": 31,
                "specialization": "Navigation",
                "years_experience": 4,
                "is_active": True,
            },
            {
                "member_id": "AJ_2018",
                "name": "Alice Johnson",
                "rank": Rank.OFFICIER,
                "age": 27,
                "specialization": "Navigation",
                "years_experience": 1,
                "is_active": True,
            },
                  ]

    total_member2: List[CrewMember] = []
    for data in data_member2:
        try:
            member = CrewMember(**data)
            total_member2.append(member)
        except (ValueError, ValidationError, TypeError) as e:
            print(f"{red}[ERROR]{reset} Expected validation error:")
            print(e.errors()[0]["msg"][13:])

# *****************************************************************************
# *                                Mission                                    *
# *                                                                           *

    space_mission = [
        {
            "mission_id": "M2024_MARS",
            "mission_name": "Mars Colony Establishment",
            "destination": "Mars",
            "launch_date": datetime.now(),
            "duration_days": 900,
            "crew": total_member,
            "mission_status": "",
            "budget_millions": "2500.0"
        },
        {
            "mission_id": "M2024_MARS",
            "mission_name": "Mars Colony Establishment",
            "destination": "Mars",
            "launch_date": datetime.now(),
            "duration_days": 900,
            "crew": total_member2,
            "mission_status": "",
            "budget_millions": "2500.0"
        }
    ]

    main(space_mission)
