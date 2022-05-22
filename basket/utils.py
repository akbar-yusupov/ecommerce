def get_center_coordinates(lat_a, long_a, lat_b, long_b):
    cord = (lat_a, long_a)
    if lat_b:
        cord = [(lat_a + lat_b) / 2, (long_a + long_b) / 2]
    return cord


def get_zoom(distance):
    if distance <= 100:
        return 8
    elif 100 < distance <= 5000:
        return 4
    else:
        return 2
