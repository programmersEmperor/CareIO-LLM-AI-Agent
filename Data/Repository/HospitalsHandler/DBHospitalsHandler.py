from Data.DataSourceHandlers.DBHandler import DBHandler
from Data.Repository.HospitalsHandler.IHospitalsHandler import IHospitalsHandler


class DBHospitalsHandler(IHospitalsHandler, DBHandler):

    def get_hospitals(self):
        query: ""
        try:
            response = self.select(query)
            return []

        except:
            return []
