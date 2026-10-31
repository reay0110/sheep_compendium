from typing import Dict

from models.models import Sheep


class FakeDB:
    def __init__(self):
        self.data: Dict[int, Sheep] = {}

    def get_sheep(self, id: int) -> Sheep:
        return self.data.get(id)

    def add_sheep(self, sheep: Sheep) -> Sheep:
        # Check if the sheep ID already exists
        if sheep.id in self.data:
            raise ValueError("Sheep with this ID already exists")
        # Add the new sheep to the database
        self.data[sheep.id] = sheep
        return sheep

    def update_sheep(self, id: int, sheep: Sheep) -> Sheep:
        # update_sheep takes the id separately from the Sheep record.
        # add_sheep only takes a Sheep, and uses sheep.id as the key.
        if id not in self.data:
            raise ValueError("Sheep not found")
        updated = sheep.model_copy(update={"id": id})
        self.data[id] = updated
        return updated

    def delete_sheep(self, id: int) -> Sheep:
        if id not in self.data:
            raise ValueError("Sheep not found")
        return self.data.pop(id)

    def get_all_sheep(self) -> list[Sheep]:
        return list(self.data.values())


db = FakeDB()
db.data = {
    1: Sheep(id=1, name="Spice", breed="Gotland", sex="ewe"),
    2: Sheep(id=2, name="Blondie", breed="Polypay", sex="ram"),
    3: Sheep(id=3, name="Deedee", breed="Jacobs Four Horns", sex="ram"),
    4: Sheep(id=4, name="Rommy", breed="Romney", sex="ewe"),
    5: Sheep(id=5, name="Vala", breed="Valais Blacknose", sex="ewe"),
    6: Sheep(id=6, name="Esther", breed="Border Leicester", sex="ewe"),
}
