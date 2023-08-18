from typing import Dict


class PharmacyModel:
    id: int
    name: str
    specialism: str
    latitude: float
    longitude: float

    def __init__(self, pharmacy_id: int, name: str, specialism: str, latitude: float, longitude: float):
        self.id = pharmacy_id
        self.name = name
        self.specialism = specialism
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_json(json: Dict):
        return PharmacyModel(
            pharmacy_id=json['id'],
            name=json['name'],
            specialism=json['specialism'],
            latitude=json['latitude'],
            longitude=json['longitude'],
        )