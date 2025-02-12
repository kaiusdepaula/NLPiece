class OnePieceSaga:
    def __init__(self):
        # Mapping volumes to sagas
        self.saga_mapper = {
            "East_Blue": range(1, 11),
            "Alabasta": range(11, 25),
            "Skypiea": range(25, 32),
            "Water_7_&_Enies_Lobby": range(32, 45),
            "Thriller_Bark": range(45, 50),
            "Summit_War": range(50, 61),
            "Fish-Man_Island": range(61, 67),
            "Punk_Hazard": range(67, 71),
            "Dressrosa": range(71, 81),
            "Whole_Cake_Island": range(81, 91),
            "Wano": range(91, 101),
        }

        # Defining the relevant characters per saga
        self.character_mapper = {
            "East_Blue": [
                "Shanks", "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji", "Buggy",
                "Koby", "Monkey D. Luffy (child)", "Roronoa Zoro (child)", "Kuina"
            ],
            "Alabasta": [
                "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji", "Mr. 2 Bon Clay",
                "Tony Tony Chopper", "Vivi", "Crocodile", "Nico Robin", "Portgas D. Ace"
            ],
            "Skypiea": [
                "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji",
                "Tony Tony Chopper", "Nico Robin", "Enel", "Gan Fall", "Wyper",
            ],
            "Water_7_&_Enies_Lobby": [
                "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji",
                "Tony Tony Chopper", "Nico Robin", "Franky", "Spandam", "Rob Lucci",
            ],
            "Thriller_Bark": [
                "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji",
                "Tony Tony Chopper", "Nico Robin", "Franky", "Brook", "Gecko Moria",
            ],
            "Summit_War": [
                "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji",
                "Tony Tony Chopper", "Nico Robin", "Franky", "Brook", "Portgas D. Ace",
                "Whitebeard", "Sengoku", "Akainu", "Aokiji", "Kizaru", "Boa Hancock",
                "Jinbe", "Buggy", "Crocodile", "Dracule Mihawk", "Donquixote Doflamingo",
                "Silvers Rayleigh", "Mr. 2 Bon Clay", "Shanks",
            ],
            "Fish-Man_Island": [
                "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji",
                "Tony Tony Chopper", "Nico Robin", "Franky", "Brook", "Jinbe",
                "Hody Jones", "Fukaboshi", "Shirahoshi",
            ],
            "Punk_Hazard": [
                "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji",
                "Tony Tony Chopper", "Nico Robin", "Franky", "Brook", "Trafalgar D. Water Law",
                "Caesar Clown", "Vergo", "Monet",
            ],
            "Dressrosa": [
                "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji",
                "Tony Tony Chopper", "Nico Robin", "Franky", "Brook", "Trafalgar D. Water Law",
                "Donquixote Doflamingo", "Sabo", "Rebecca", "Kyros", "Bartolomeo",
            ],
            "Whole_Cake_Island": [
                "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji",
                "Tony Tony Chopper", "Nico Robin", "Franky", "Brook", "Jinbe",
                "Charlotte Linlin (Big Mom)", "Charlotte Katakuri", "Charlotte Pudding",
                "Pedro", "Carrot",
            ],
            "Wano": [
                "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji",
                "Tony Tony Chopper", "Nico Robin", "Franky", "Brook", "Jinbe",
                "Trafalgar D. Water Law", "Eustass Kid", "Kaido", "Yamato", "Kozuki Oden",
                "Kin'emon", "Momonosuke", "Kozuki Hiyori", "Denjiro", "Kanjuro", "Raizo",
            ],
        }

    def get_saga_by_volume(self, volume: int) -> str:
        """Return the saga name for a given volume."""
        for saga, vol_range in self.saga_mapper.items():
            if volume in vol_range:
                return saga
        return "Unknown Saga"

    def get_characters_by_volume(self, volume: int) -> list[str]:
        """Return a list of most relevant characters for a given volume."""
        saga = self.get_saga_by_volume(volume)
        return self.character_mapper.get(saga, [])
