from Data.DataSourceHandlers.DBHandler import DBHandler
from Data.Repository.DoctorsHandler.IDoctorsHandler import IDoctorsHandler


class DBDoctorsHandler(IDoctorsHandler, DBHandler):

    def get_doctors(self):
        query: ""
        try:
            response = self.select(query)
            return []

        except:
            return []
