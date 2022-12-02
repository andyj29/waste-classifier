import enum


class Label(enum.Enum):
    battery = 'battery'
    biological = 'biological'
    brown_glass = 'brown glass'
    cardboard = 'cardboard'
    clothes = 'clothes'
    green_glass = 'green glass'
    metal = 'metal'
    paper = 'paper'
    plastic = 'plastic'
    shoes = 'shoes'
    trash = 'trash'
    white_glass = 'white glass'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def to_list(cls):
        return list(i.value for i in cls)


class Area(enum.Enum):
    Ajax = 'Ajax'
    Aurora = 'Aurora'
    Brampton = 'Brampton'
    Brock = 'Brock'
    Burlington = 'Burlington'
    Caledon = 'Caledon'
    Clarington = 'Clarington'
    EastGwillimbury = 'East Gwillimbury'
    Georgina = 'Georgina'
    HaltonHills = 'Halton Hills'
    King = 'King'
    Markham = 'Markham'
    Milton = 'Milton'
    Mississauga = 'Mississauga'
    Newmarket = 'Newmarket'
    Oakville = 'Oakville'
    Oshawa = 'Oshawa'
    Pickering = 'Pickering'
    RichmondHill = 'Richmond Hill'
    Scugog = 'Scugog'
    Toronto = 'Toronto'
    Uxbridge = 'Uxbridge'
    Vaughan = 'Vaughan'
    Whitby = 'Whitby'
    WhitchurchStouffville = 'Whitchurch Stouffville'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def to_list(cls):
        return list(i.value for i in cls)

