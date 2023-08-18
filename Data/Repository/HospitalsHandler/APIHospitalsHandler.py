from Data.DataSourceHandlers.APIHandler import APIHandler
from Data.Repository.HospitalsHandler.IHospitalsHandler import IHospitalsHandler


class APIHospitalsHandler(IHospitalsHandler, APIHandler):

    def get_hospitals(self):
        url: ""
        try:
            response = self.get(url)
            return []

        except:
            return []
