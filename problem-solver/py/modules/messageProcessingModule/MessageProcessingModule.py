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
from .UserInfoAgent import UserInfoAgent
from .GetProfessionsWIthDescriptions import GetProfessionsWithDescriptions
from .GetTestsWithDescriptionsAgent import GetTestsWithDescriptionsAgent
from .GetHolandTestAgent import GetHolandTestAgent
from .AnalyzeHolandTestAgent import AnalyzeHolandTestAgent
from .GetIovaishiTestAgent import GetIovaishiTestAgent
from .AnalyzeIovaishiTestAgent import AnalyzeIovaishiTestAgent
from .GetMotivationalTestAgent import GetMotivationalTestAgent
from .AnalyzeMotivationalTestAgent import AnalyzeMotivationalTestAgent
from .GetPersonalityToSuccessAgent import GetPersonalityToSuccessAgent
from .AnalyzePersonalityToSuccessTestAgent import AnalyzePersonalityToSuccessTestAgent
from .GetNeedInAchievementTestAgent import GetNeedInAchievementTestAgent
from .AnalyzeNeedInAchievementTestAgent import AnalyzeNeedInAchievementTestAgent
from. GetNeedInApprovalTestAgent import GetNeedInApprovalTestAgent
from .AnalyzeNeedInApprovalTestAgent import AnalyzeNeedInApprovalTestAgent
from .GetAbilityInSympathyTestAgent import GetAbilityInSympathyTestAgent
from .AnalyzeAbilityInSympathyTestAgent import AnalyzeAbilityInSympathyTestAgent
from .GetAdvancedTestAgent import GetAdvancedTestAgent
from .AnalyzeAdvancedTestAgent import AnalyzeAdvancedTestAgent


class MessageProcessingModule(ScModule):
    def __init__(self):
        super().__init__(WeatherAgent(),
                         SearchProfessionAgent(),
                         GetEstablishmentsWithDescriptionsAgent(),
                         GetProfessionsWithDescriptions(),
                         AddFeedbackToEstablishmentAgent(),
                         CreateQuestionAboutEstablishmentAgent(),
                         CreateAnswerToQuestionAgent(),
                         GetEstablishmentsByProfessionAgent(),
                         UserRegistrationAgent(),
                         UserAuthorizationAgent(),
                         UserInfoAgent(),
                         GetTestsWithDescriptionsAgent(),
                         GetHolandTestAgent(),
                         AnalyzeHolandTestAgent(),
                         GetIovaishiTestAgent(),
                         AnalyzeIovaishiTestAgent(),
                         GetMotivationalTestAgent(),
                         AnalyzeMotivationalTestAgent(),
                         GetPersonalityToSuccessAgent(),
                         AnalyzePersonalityToSuccessTestAgent(),
                         GetNeedInAchievementTestAgent(),
                         AnalyzeNeedInAchievementTestAgent(),
                         GetNeedInApprovalTestAgent(),
                         AnalyzeNeedInApprovalTestAgent(),
                         GetAbilityInSympathyTestAgent(),
                         AnalyzeAbilityInSympathyTestAgent(),
                         GetAdvancedTestAgent(),
                         AnalyzeAdvancedTestAgent()
                         )
