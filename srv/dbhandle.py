import datetime


def unimplemented():
    raise Exception("ssvp: error: db module tried to use an unimplemented function")
    

class DBAbstract:
    def __init__(self, config: dict) -> None:
        pass
    
    def get_uptime_stats(self, srv: str) -> dict:
        unimplemented()
        return {}
    
    def get_daily_data(self, srv: str) -> list:
        base = self._fetch_daily_data(srv)
        res = []
        for z in [datetime.date.today() - datetime.timedelta(days=n) for n in range(89, -1, -1)]:
            if z in base:
                res.append(base[z])
            else:
                res.append(-1)
        return res
    
    def _fetch_daily_data(self, srv: str) -> dict:
        unimplemented()
        return {}
    
    def handle_daily_record(self, srv: str, st: int) -> int:
        unimplemented()
        return 0
        
    def insert_interval_log(self, srv: str, status: int) -> None:
        unimplemented()
        
    def update_cached_stats(self, srv: str, st: int) -> None:
        unimplemented()
