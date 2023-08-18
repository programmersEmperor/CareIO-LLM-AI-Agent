from typing import Dict


class HospitalModel:
    id: int
    name: str
    specialism: str
    latitude: float
    longitude: float

    def __init__(self, hospital_id: int, name: str, specialism: str, latitude: float, longitude: float):
        self.id = hospital_id
        self.name = name
        self.specialism = specialism
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_json(json: Dict):
        return HospitalModel(
            hospital_id=json['id'],
            name=json['name'],
            specialism=json['specialism'],
            latitude=json['latitude'],
            longitude=json['longitude'],
        )