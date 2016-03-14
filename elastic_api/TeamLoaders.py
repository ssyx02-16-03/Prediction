# -*- coding: utf-8 -*-
# denna kommentar måste va med för åäö

from OngoingsLoader import OngoingsLoader

# baseklass till alla klasser nedan
class TeamLoader(OngoingsLoader):

    def set_team(self, team):
        self.set_match({"match": {"Team": team}})

class NakmeLoader(TeamLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_team("NAKME")
        super(NakmeLoader, self).__init__(start_time, end_time, interval_minutes)

class NakorLoader(TeamLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_team("NAKOR")
        super(NakorLoader, self).__init__(start_time, end_time, interval_minutes)

class NakkiLoader(TeamLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_team("NAKKI")
        super(NakkiLoader, self).__init__(start_time, end_time, interval_minutes)

class NakonLoader(TeamLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_team("NAKÖN")
        super(NakonLoader, self).__init__(start_time, end_time, interval_minutes)

class NakonLoader(TeamLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_team("NAKÖN")
        super(NakonLoader, self).__init__(start_time, end_time, interval_minutes)

class NakbaLoader(TeamLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_team("NAKBA")
        super(NakbaLoader, self).__init__(start_time, end_time, interval_minutes)

class NakkkLoader(TeamLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_team("NAKKK")
        super(NakkkLoader, self).__init__(start_time, end_time, interval_minutes)

class NakmLoader(TeamLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_team("NAKM")
        super(NakmLoader, self).__init__(start_time, end_time, interval_minutes)

