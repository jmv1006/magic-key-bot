import requests

passtypes = ["inspire", "believe", "imagine", "enchant"]

class DataGetter:
    def __init__(self, passtype):
        if(passtype not in passtypes): self.passtype = "inspire"
        self.passtype = passtype
        self.url = f"https://disneyland.disney.go.com/passes/blockout-dates/api/get-availability/?product-types={passtype}-key-pass&destinationId=DLR&numMonths=1"
 
    def fetchData(self):
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
        response = requests.get(self.url, headers=header)
        if(not response.ok): return ["Response not okay"]
        return response.json()