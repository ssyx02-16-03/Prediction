# -*- coding: utf-8 -*-
# denna kommentar måste va med för åäö

from OngoingsLoader import OngoingsLoader

# baseklass till alla klasser nedan
class ColorLoader(OngoingsLoader):

    def set_color(self, color):
        self.set_match({"match": {"Priority": color}})

class GreensLoader(ColorLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_color(u"Grön")
        super(GreensLoader, self).__init__(start_time, end_time, interval_minutes)

class BluesLoader(ColorLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_color(u"Blå")
        super(BluesLoader, self).__init__(start_time, end_time, interval_minutes)

class YellowsLoader(ColorLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_color(u"Gul")
        super(YellowsLoader, self).__init__(start_time, end_time, interval_minutes)

class OrangesLoader(ColorLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_color(u"Orange")
        super(OrangesLoader, self).__init__(start_time, end_time, interval_minutes)

class RedsLoader(ColorLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_color(u"Röd")
        super(RedsLoader, self).__init__(start_time, end_time, interval_minutes)
