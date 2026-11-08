"""Every place a student can report from. Both apps read this file.
To add a place, add ONE line below. Nothing else needs to change."""

MAP_CENTER = (53.5222, -113.5310)

# ---- Residence towers: building -> number of floors and map position ----
TOWERS = {
    "Henday Hall": {"floors": 10, "coords": (53.52119827024105, -113.53060577851979)},
    "Mackenzie Hall": {"floors": 11, "coords": (53.521327840257364, -113.53172497898909)},
    "Kelsey Hall": {"floors": 10, "coords": (53.522029186520335, -113.5317608351634)},
    "Shaffer Hall": {"floors": 12, "coords": (53.52248095835739, -113.53156635838)},
    "Chalifoux Hall": {"floors": 5, "coords": (53.520643630132334, -113.5313884780551)},
}

# Wings and areas inside a tower
ZONES = ["North Wing", "South Wing", "Main Lounge", "West Stairwell", "Exterior/Grounds"]

# ---- Shared spaces: no floor to choose. ----
# TODO: replace each pair with the real position. In Google Maps (satellite view),
# right-click the spot and click the two numbers at the top of the menu to copy them.
SHARED_SPACES = {
    "Main entrance and front desk": (53.5222, -113.5310),
    "Main corridors": (53.5223, -113.5308),
    "Dining hall": (53.5221, -113.5306),
    "Conference rooms": (53.5224, -113.5306),
    "Gym": (53.5220, -113.5309),
    "Outdoor grounds and paths": (53.5222, -113.5314),
}

SHARED_FLOOR = "N/A"
SHARED_ZONE = "Shared space"


def place_coords(name):
    """Map position for a tower or a shared space."""
    if name in TOWERS:
        return TOWERS[name]["coords"]
    return SHARED_SPACES.get(name, MAP_CENTER)


def all_places():
    return list(TOWERS) + list(SHARED_SPACES)


def place_label(building, floor, zone):
    """Short readable location for cards and popups."""
    if building in SHARED_SPACES:
        return f"{building}"
    return f"{building} · {floor} · {zone}"