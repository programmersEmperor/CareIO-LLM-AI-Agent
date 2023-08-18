from Data.DataSourceHandlers.APIHandler import APIHandler
from Data.Repository.DoctorsHandler.IDoctorsHandler import IDoctorsHandler


class APIDoctorsHandler(IDoctorsHandler, APIHandler):

    def get_doctors(self):
        url: ""
        try:
            response = self.get(url)
            return []

        except:
            return []
