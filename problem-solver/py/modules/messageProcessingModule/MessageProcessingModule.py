from sc_kpm import ScModule
from .WeatherAgent import WeatherAgent
from .SearchProfessionAgent import SearchProfessionAgent


class MessageProcessingModule(ScModule):
    def __init__(self):
        super().__init__(WeatherAgent(), SearchProfessionAgent())
