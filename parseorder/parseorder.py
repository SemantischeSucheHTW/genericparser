import datetime as dt_pkg

class ParseOrder:
    def __init__(self, url, datetime):
        #downloaded URL: String
        self.url=url

        #date & time at which the download was performed: import datetime -> datetime.datetime.now()
        assert isinstance(datetime, dt_pkg.datetime)
        self.datetime=datetime
