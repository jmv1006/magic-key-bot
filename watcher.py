import imp
from response_handler import ResponseHandler

response_handler = ResponseHandler('inspire')

class Watcher:
    def __init__(self):
        self.dates_being_watched = []
    
    def add_date(self, date):
        self.dates_being_watched.append(date)
        self.check_if_available()
    
    def check_if_available(self):
        if not self.dates_being_watched: return
        available = response_handler.get_all_available()
        for date in self.dates_being_watched:
            if date in available:
                print("date is available")
                self.dates_being_watched.remove(date)
            else: 
                print("date is still not available")