#!/usr/bin/env python3
# ########################################################################### #
#                                                                             #
#                                                          :::      ::::::::  #
#   alien_contact.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/08 19:24:40 by bbeaurai            #+#    #+#            #
#   Updated: 2026/03/10 13:10:53 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


from typing import Optional, List, Dict

import sys

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


class ContactType(Enum):
    PHYSICAL = "physical"
    TELEPATIC = "telepathic"
    RADIO = "radio"


# =============================================================================
# ============================== BaseModel ====================================
# =============================================================================


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(max_length=500)
    is_verified: bool = Field(default=False)

    # Contact ID must start with "AC" (Alien Contact)
    @model_validator(mode="after")
    def check_id(self) -> Self:
        if (not self.contact_id.startswith("AC")):
            raise ValueError("The Contact ID does not begin with “AC”.")
        return (self)

    # Physical contact reports must be verified
    @model_validator(mode="after")
    def check_contact_physical(self) -> Self:
        if (self.contact_type.value == "physical"):
            if (self.is_verified is False):
                raise ValueError("Physical contact must be verified.")
        return (self)

    # Telepathic contact requires at least 3 witnesses
    @model_validator(mode="after")
    def check_contact_telepathic(self) -> Self:
        if (self.contact_type.value == "telepathic"):
            if (self.witness_count < 3):
                raise ValueError("Telepathic contact requires "
                                 "at least 3 witnesses")
        return (self)

    # Strong signals (> 7.0) should include received messages
    @model_validator(mode="after")
    def check_signal(self) -> Self:
        if (self.signal_strength > 7):
            if (len(self.message_received) == 0):
                raise ValueError("Signal greater than 7 waiting for a message")
        return (self)


# =============================================================================
# ================================ MAIN =======================================
# =============================================================================


def main(data_alien: List[Dict[str, str]]) -> bool:
    print("\n" + "Alien Contact Log Validation" + "\n")

    print("".center(79, "="))
    for data in data_alien:
        try:
            station = AlienContact(**data)
            print("Valid station created:")
            print("ID:", station.contact_id)
            print("Type:", station.contact_type.value)
            print(f"Location: {station.location} people")
            print(f"Signal: {station.signal_strength}/10")
            print(f"Duration: {station.duration_minutes} minutes")
            print(f"Witnesses: {station.witness_count}")
            print(f"Message: \"{station.message_received}\"")

        except (ValueError, ValidationError) as e:
            print(f"{red}[ERROR]{reset} Expected validation error:")
            print(e.errors()[0]["msg"][13:])

        finally:
            print("\n" + "".center(79, "="))


if __name__ == "__main__":
    data_alien = [
            {
                "contact_id": "AC_2026_001",
                "contact_type": ContactType.RADIO,
                "location": "Area 51, Nevada",
                "signal_strength": 8.5,
                "duration_minutes": 45,
                "witness_count": 5,
                "message_received": "Greetings from Zeta Reticuli",
                "is_verified": False,
                "timestamp": datetime.now(),
            },
            {
                "contact_id": "AC_2026_042",
                "contact_type": ContactType.TELEPATIC,
                "location": "Area 42, Le Havre",
                "signal_strength": 8.5,
                "duration_minutes": 45,
                "witness_count": 2,
                "message_received": "Greetings from Zeta Reticuli",
                "is_verified": False,
                "timestamp": datetime.now(),
            },
                    ]

    main(data_alien)
