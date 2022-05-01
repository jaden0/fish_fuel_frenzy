from math import pi


def deg_to_rad(degrees):
    return degrees * pi / 180


def rad_to_deg(radians):
    return (radians * 180 / pi) % 360