#!/usr/bin/env python3
# ########################################################################### #
#                                                                             #
#                                                          :::      ::::::::  #
#   space_crew.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/09 16:54:23 by bbeaurai            #+#    #+#            #
#   Updated: 2026/03/09 18:09:49 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import sys
from typing import List
from typing_extensions import Self

green = "\033[32m\033[1m\033[1m"
red = "\033[31m\033[5m\033[1m"
redp = "\033[31m"
brown = "\033[0;33m"
blue = "\033[38;5;67m"
reset = "\033[0m"


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
    from pydantic import BaseModel, Field, ValidationError, model_validator
    from enum import Enum
    from datetime import datetime
except ModuleNotFoundError:
    print(
        "\n" + f"{red}[ERROR]{reset} pydantic is not installed, "
        "install it as follows" + "\n\n"
        f"{blue}# Install pydentic" + "\n"
        f"{brown}$ pip install -U pydantic" + "\n"
            )
    exit()


class Rank(Enum):
    CADET = "cadet"
    OFFICIER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_validate(self) -> Self:
        # commander = captain = inactive = 0
        # years = []
        # Mission ID must start with "M"
        if (not self.mission_id.startswith("M")):
            raise ValueError("startwith M")
        # Must have at least one Commander or Captain
        if (self.crew):
            pass
        # Long missions (> 365 days) need 50% experienced crew (5+ years)
        # All crew members must be active


def main(total_member: List[CrewMember],
         space_mission: SpaceMission) -> None:
    print("\n" + "Space Mission Crew Validation" + "\n")

    print("".center(79, "="))
    try:
        mission = space_mission
        print("Valid station created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: {mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")

    except (ValueError, ValidationError, TypeError) as e:
        print(f"{red}[ERROR]{reset} Expected validation error:")
        print(e.errors()[0]["msg"][13:])

    print("Crew members:")
    for data in data_member:
        try:
            member = CrewMember(**data)
            print(f"- {member.name} ({member.rank.value}) - "
                  f"{member.specialization}")
        except (ValueError, ValidationError, TypeError) as e:
            print(f"{red}[ERROR]{reset} Expected validation error:")
            print(e.errors()[0]["msg"][13:])

    print("\n" + "".center(79, "="))


if __name__ == "__main__":

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

    total_member = []
    for data in data_member:
        try:
            member = CrewMember(**data)
            total_member.append(member)
        except (ValueError, ValidationError, TypeError) as e:
            print(f"{red}[ERROR]{reset} Expected validation error:")
            print(e.errors()[0]["msg"][13:])

    space_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.now(),
        duration_days=900,
        crew=total_member,
        mission_status="",
        budget_millions="2500.0",
    )
    main(total_member, space_mission)
