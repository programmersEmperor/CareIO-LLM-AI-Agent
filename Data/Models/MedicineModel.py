from typing import Dict


class MedicineModel:
    id: int
    name: str
    description: str

    def __init__(self, medicine_id: int, name: str, description: str):
        self.id = medicine_id
        self.name = name
        self.description = description

    @staticmethod
    def from_json(json: Dict):
        return MedicineModel(
            medicine_id=json['id'],
            name=json['name'],
            description=json['description'],
        )