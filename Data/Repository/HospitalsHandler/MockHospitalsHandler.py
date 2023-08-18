from Data.Models.DoctorModel import DoctorModel
from Data.Models.HospitalModel import HospitalModel
from Data.Repository.HospitalsHandler.IHospitalsHandler import IHospitalsHandler


class MockHospitalsHandler(IHospitalsHandler):

    def get_hospitals(self):
        mockData = [
            {
                'id': 1,
                'name': 'Hospital 1',
                'specialism': 'Bones',
                'longitude': 12.3,
                'latitude': 12.3,
            },
            {
                'id': 2,
                'name': 'Hospital 2',
                'specialism': 'Eyes',
                'longitude': 10.3,
                'latitude': 27.3,
            },
            {
                'id': 3,
                'name': 'Hospital 3',
                'specialism': 'Dentist',
                'longitude': 29.3,
                'latitude': 12.3,
            },
            {
                'id': 4,
                'name': 'Hospital 4',
                'specialism': 'Brains',
                'longitude': 35.3,
                'latitude': 89.3,
            }
        ]
        mock_hospitals = []
        for hospital in mockData:
            mock_hospitals.append(HospitalModel.from_json(hospital))

        return mock_hospitals
