import logging
import json

from sc_client.models import ScAddr, ScLinkContentType, ScTemplate
from sc_client.constants import sc_types
from sc_client.client import template_search, create_elements

from sc_kpm import ScAgentClassic, ScModule, ScResult, ScServer
from sc_kpm.utils import (
    create_link,
    get_link_content_data,
    check_edge, create_edge,
    delete_edges,
    get_system_idtf,
    get_edge
)
from sc_kpm.utils.action_utils import (
    create_action_answer,
    finish_action_with_status,
    get_action_arguments
)
from sc_kpm import ScKeynodes

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(name)s | %(message)s", datefmt="[%d-%b-%y %H:%M:%S]"
)


class AnalyzeHolandTestAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_analyze_holand_test_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("AnalyzeHolandTestAgent finished %s",
                         "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("AnalyzeHolandTestAgent started")

        json_link = get_action_arguments(action_node, 1)[0]
        json_data = get_link_content_data(json_link)

        if not json_data:
            self.logger.error("No JSON data found")
            return ScResult.ERROR

        try:
            user_answers = json.loads(json_data)
            self.logger.info("Received JSON data: %s", user_answers)
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse JSON: %s", str(e))
            return ScResult.ERROR
        
        # TODO Анализирование результатов теста

        result_text = "Спасибо за прохождение теста! Ваши ответы учтены."

        text_link = create_link(result_text, ScLinkContentType.STRING)

        create_action_answer(action_node, text_link)

        self.logger.info("Test analysis completed, result sent")
        return ScResult.OK
