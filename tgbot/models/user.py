from dataclasses import dataclass
from typing import Optional

from aiogram.types import Location

from tgbot.misc.base import Base


@dataclass
class UserLocation(Base):

    def __init__(self, location: Location):
        self.longitude = location.longitude
        self.latitude = location.latitude
        self.horizontal_accuracy = location.horizontal_accuracy
        self.live_period = location.live_period
        self.heading = location.heading
        self.proximity_alert_radius = location.proximity_alert_radius
        dict.__init__(self, longitude=self.longitude, latitude=self.latitude,
                      horizontal_accuracy=self.horizontal_accuracy, live_period=self.live_period, heading=self.heading,
                      proximity_alert_radius=self.proximity_alert_radius)


@dataclass
class User(Base):

    def __init__(self, dict_: dict):
        super().__init__()

        user_id: int = dict_.get("id")
        username: str = dict_.get("username")
        first_name: str = dict_.get("first_name")
        last_name: str = dict_.get("last_name")
        location: Optional[Location] = dict_.get("location") or None
        user_mode_enabled: bool = dict_.get("user_mode_enabled", False)

        self.id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.user_mode_enabled = user_mode_enabled

        if location:
            self.location = UserLocation(location)
        else:
            self.location = None

        dict.__init__(
            self,
            id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            location=location,
        )


# def user(value: dict) -> User:
#     return User(**value)
# def user(value: dict) -> User:
#     return User(value)
def user(**kwargs) -> User:
    return User(kwargs)
