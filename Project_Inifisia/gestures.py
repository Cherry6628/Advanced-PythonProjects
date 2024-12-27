import math
fingers = {"thumb": [1, 2, 3, 4], "index": [5, 6, 7, 8], "middle": [9, 10, 11, 12], "ring": [13, 14, 15, 16], "small": [17, 18, 19, 20]}


def gesture1(point_data: list[list[int, int, int]]) -> bool:
    """Pointing Upwards with Index Finger"""
    optimum_values = {
        "Degree": 22.5,
        "Error in Finger Height": 50,
        "Minimum Height per Phalanges": 30
    }

    point_data = point_data[:, [0, 1]]
    """Pointing Upwards"""
    if all(point_data[[5, 9, 13, 17]][:, 1] < point_data[0][1]):
        mean = sum(point_data[[5, 9, 13, 17]]) / 4
        O = point_data[0]
        degree = (math.asin(abs((mean[0] - O[0]) / (((mean[0] - O[0]) ** 2 + (mean[1] - O[1]) ** 2) ** (1 / 2))))) * 180 / math.pi
        if degree < optimum_values['degree']:
            fingers_to_be_closed = [fingers['middle'], fingers['ring'], fingers['small']]
            for finger in fingers_to_be_closed:
                if point_data[finger[1]][1]-point_data[finger[3]][1] > optimum_values['Error in Finger Height']:
                    return False

            if ((point_data[5][1] - point_data[6][1] > optimum_values['Minimum Height per Phalanges']) and
                    (point_data[6][1] - point_data[7][1] > optimum_values['Minimum Height per Phalanges']) and
                    (point_data[7][1] - point_data[8][1] > optimum_values['Minimum Height per Phalanges'])):
                return True
    return False
