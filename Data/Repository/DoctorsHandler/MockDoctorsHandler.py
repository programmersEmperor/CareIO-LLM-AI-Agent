from Data.Repository.DoctorsHandler.IDoctorsHandler import IDoctorsHandler
from Data.Models.DoctorModel import DoctorModel


class MockDoctorsHandler(IDoctorsHandler):

    def get_doctors(self):
        mockData = [
            {
                'id': 1,
                'name': 'Ali Muhammed',
                'specialism': 'Bones',
                'longitude': 12.3,
                'latitude': 12.3,
            },
            {
                'id': 2,
                'name': 'Hussain Salah',
                'specialism': 'Eyes',
                'longitude': 10.3,
                'latitude': 27.3,
            },
            {
                'id': 3,
                'name': 'Khalid Waleed',
                'specialism': 'Dentist',
                'longitude': 29.3,
                'latitude': 12.3,
            },
            {
                'id': 4,
                'name': 'Mutasim Salim',
                'specialism': 'Brains',
                'longitude': 35.3,
                'latitude': 89.3,
            }
        ]
        mock_doctors = []
        for doctor in mockData:
            mock_doctors.append(DoctorModel.from_json(doctor))

        return mock_doctors