import numpy as np
from PIL import Image

class OnePieceSaga:
    def __init__(self):
        # Mapping volumes to sagas
        self.saga_mapper = {
            "East_Blue": range(1, 12),
            "Alabasta": range(12, 25),
            "Skypiea": range(25, 32),            
            "Water_7": range(32, 39),
            "Enies_Lobby": range(39, 46),
            "Thriller_Bark": range(46, 50),
            "Sabaody": range(50, 54),
            "Amazon_Lily": range(54,55),
            "Impel_Down": range(55, 57),
            "Marineford": range(56, 60),
            "Post-War": range(60, 61),
            "Fish-Man_Island": range(61, 67),
            "Punk_Hazard": range(67, 71),
            "Dressrosa": range(71, 81),
            "Whole_Cake_Island": range(81, 91),
            "Wano": range(91, 101),
        }

        # Mapping volumes to sagas
        self.saga_mapper_extended = {
            "Romance_Dawn": range(1, 2),
            "Orange_Town": range(2, 4),
            "Syrup_Village": range(4, 5),
            "Baratie": range(5, 8),
            "Arlong_Park": range(8, 12),
            "Loguetown_&_Reverse_Mountain": range(12, 13),
            "Little_Garden": range(13, 15),
            "Drum": range(15, 17),
            "Alabasta": range(17, 25),
            "Jaya": range(25, 26),
            "Skypiea": range(26, 32),
            "Long_Ring_Long_Land": range(32, 34),
            "Water_7": range(34, 39),
            "Enies_Lobby": range(39, 46),
            "Thriller_Bark": range(46, 50),
            "Sabaody": range(50, 54),
            "Amazon_Lily": range(54,55),
            "Impel_Down": range(55, 56),
            "Marineford": range(56, 60),
            "Post-War": range(60, 61),
            "Fish-Man_Island": range(61, 67),
            "Punk_Hazard": range(67, 70),
            "Dressrosa": range(70, 81),
            "Zou": range(81, 83),
            "Whole_Cake_Island": range(83, 91),
            "Wano": range(91, 105),
            "Egghead": range(105, 112),
        }

    def get_saga_by_volume(self, volume: int) -> str:
        """Return the saga name for a given volume."""
        for saga, vol_range in self.saga_mapper.items():
            if volume in vol_range:
                return saga
        return "Unknown Saga"

def read_image(path_to_image):
    with open(path_to_image, "rb") as file:
        image = Image.open(file).convert("L").convert("RGB")
        image = np.array(image)
    return image