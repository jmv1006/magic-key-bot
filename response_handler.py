from api import DataGetter

class AvailableDate:
    def __init__(self, date):
        self.date = date
        self.parks = []
    
    def add_park(self, park):
        self.parks.append(park)


class ResponseHandler:
    def __init__(self, key):
        self.key = key
        self.getter = DataGetter(self.key)
        self.available_dates = self.get_all_available()
    
    def get_all_available(self):
        response = self.getter.fetchData()
        dates = response['calendar-availabilities']

        available = []
        for date in dates:
            if(date['availability'] == 'cms-key-all-availability' or date['availability'] == 'cms-key-at-least-one-availability'):
                new_date = AvailableDate(date['date'])
                for park in date['facilities']:
                    if park['facilityName'] == "DLR_DP" and park['available']:
                        new_date.add_park("Disneyland Park")
                    elif park['facilityName'] == "DLR_CA" and park['available']:
                        new_date.add_park("Disney California Adventure")
                available.append(new_date)

        result = {} 
        for date in available:
            result[date.date] = date.parks
            if len(result) >= 90: return result
        
        self.available_dates = result
        return result

    def get_specific_date(self, date):
        month = date[0]
        day = date[1]
        year = date[2]

        formatted_date = year + '-' + month + '-' + day

        if formatted_date in self.available_dates:
            return self.available_dates[formatted_date]
        else: return False



handler = ResponseHandler('inspire')

handler.get_specific_date(['10', '01', '2022'])
