from sc_kpm import ScModule
from .WeatherAgent import WeatherAgent
from .SearchProfessionAgent import SearchProfessionAgent
from .GetEstablishmentsWithDescriptionsAgent import GetEstablishmentsWithDescriptionsAgent
from .AddFeedbackToEstablishmentAgent import AddFeedbackToEstablishmentAgent
from .CreateQuestionAboutEstablishmentAgent import CreateQuestionAboutEstablishmentAgent
from .CreateAnswerToQuestionAgent import CreateAnswerToQuestionAgent
from .GetEstablishmentsByProfessionAgent import GetEstablishmentsByProfessionAgent
from .UserRegistrationAgent import UserRegistrationAgent
from .UserAuthorizationAgent import UserAuthorizationAgent


class MessageProcessingModule(ScModule):
    def __init__(self):
        super().__init__(WeatherAgent(),
                         SearchProfessionAgent(),
                         GetEstablishmentsWithDescriptionsAgent(),
                         AddFeedbackToEstablishmentAgent(),
                         CreateQuestionAboutEstablishmentAgent(),
                         CreateAnswerToQuestionAgent(),
                         GetEstablishmentsByProfessionAgent(),
                         UserRegistrationAgent(),
                         UserAuthorizationAgent()
                         )
