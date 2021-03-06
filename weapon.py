import configparser

from abc import ABCMeta, abstractmethod

from utils import Point, Surface, create_logger


log = create_logger(__name__, "weapon.log")
config_file = "weapons.cfg"
config = configparser.SafeConfigParser(allow_no_value=True,
        interpolation=configparser.ExtendedInterpolation())
config.read(config_file)


class IWeapon(object, metaclass=ABCMeta):
    @abstractmethod
    def make_shot(self):
        """Make shot, if can't - raise Value Error"""
        pass


    @abstractmethod
    def update(self):
        """update coords list"""
        pass


def _load_from_config(weapon, config):
    section = weapon.__name__
    params = ("ammo", "max_ammo", "cooldown", "damage", "radius", "dy")
    return {var : config.get(section, var) for var in params}


class Weapon(IWeapon):
    def __init__(self, ammo, max_ammo, cooldown, damage, radius, dy):
        self._type     = "__basic__"
        self._image    = None
        self._ammo     = int(ammo) if ammo.isdigit() else ammo
        self._max_ammo = int(max_ammo) if max_ammo.isdigit() else max_ammo
        self._cooldown = float(cooldown)
        self._damage   = int(damage)
        self._radius   = int(radius)
        self._dy       = int(dy)
        self._current_cooldown = 0

        #Experimental
        self.ready = True

        self._coords = []

    def _prepare_weapon(self):
        #play sound
        self.ready = True


    def make_shot(self, pos):
        if not self.ready:
            return

        if self._ammo == "infinite":
            self._coords.append(Point(x=pos.x, y=pos.y-1))
        elif self._ammo > 0:
            self._coords.append(Point(x=pos.x, y=pos.y-1))
            self._ammo -= 1
        if self._ammo == 0: raise ValueError("No ammo!")

        self.ready = False
        self._current_cooldown = self._cooldown


    def get_render_data(self):
        return (self._coords, self._image.get_image())

    get_data = get_render_data


    @property
    def ammo(self):
        return 999 if self._ammo == "infinite" else self._ammo


    @property
    def max_ammo(self):
        return 999 if self._max_ammo == "infinite" else self._max_ammo


    @property
    def type(self):
        return self.__class__.__name__


    def update(self):
        new_coords = []
        for i in self._coords:
            if i.y - self._dy > 0:
                new_coords.append(Point(x=i.x, y=i.y - self._dy))
        self._coords = new_coords[:]
        self._current_cooldown -= 1
        if self._current_cooldown <= 0:
            self.ready = True


import curses
class Blaster(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, config))
        self._image = Surface([["^"]], style=[[curses.A_BOLD]])


class Laser(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, config))
        self._image = Surface([["|"]])


class UM(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, config))
        self._image = Surface([["^"],
                               ["|"],
                               ["*"]], style = [[curses.A_BOLD] for _ in range(3)])


if __name__ == "__main__":
    from pprint import pprint
   # pprint(vars(_load_from_config(Blaster, config)))
   # _load_from_config(Blaster, config).make_shoot()
   # _load_from_config(Laser, config)
   # _load_from_config(UM, config)
    Blaster()
