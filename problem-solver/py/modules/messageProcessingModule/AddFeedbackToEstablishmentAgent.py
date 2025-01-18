"""
This code creates some test agent and registers until the user stops the process.
For this we wait for SIGINT.
"""
import logging
from re import template
from typing import List, Optional

from sc_client.models import ScAddr, ScLinkContentType, ScTemplate, ScConstruction
from sc_client.constants import sc_types
from sc_client.client import template_search, create_elements

from sc_kpm import ScAgentClassic, ScModule, ScResult, ScServer
from sc_kpm.sc_sets import ScSet
from sc_kpm.utils import (
    create_link,
    get_link_content_data,
    check_edge, create_edge,
    delete_edges,
    get_element_by_role_relation,
    get_element_by_norole_relation,
    get_system_idtf,
    get_edge
)
from sc_kpm.utils.action_utils import (
    create_action_answer,
    finish_action_with_status,
    get_action_arguments,
    get_element_by_role_relation
)
from sc_kpm import ScKeynodes

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(name)s | %(message)s", datefmt="[%d-%b-%y %H:%M:%S]"
)

class AddFeedbackToEstablishmentAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_add_feedback_to_establishment")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("AddFeedbackToEstablishmentAgent finished %s",
                         "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("AddFeedbackToEstablishmentAgent started")

        # Проверка аргументов действия
        arguments = get_action_arguments(action_node)
        if not arguments or len(arguments) != 2:
            self.logger.error("Invalid arguments for action. Expected 2 arguments: establishment node and feedback text")
            return ScResult.ERROR_INVALID_PARAMS

        establishment_node, feedback_text_link = arguments
        feedback_text = get_link_content_data(feedback_text_link)

        if not feedback_text:
            self.logger.error("Failed to retrieve feedback text from argument")
            return ScResult.ERROR

        # Создание узла отзыва
        concept_feedback = ScKeynodes.resolve("concept_feedback", sc_types.NODE_CONST_CLASS)
        nrel_feedback = ScKeynodes.resolve("nrel_feedback", sc_types.NODE_NOROLE)
        nrel_text = ScKeynodes.resolve("nrel_text", sc_types.NODE_NOROLE)

        feedback_node = create_elements({
            "type": sc_types.NODE_CONST,
        })[0]

        if not feedback_node:
            self.logger.error("Failed to create feedback node")
            return ScResult.ERROR

        # Связывание узла отзыва с концептом "feedback"
        create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, concept_feedback, feedback_node)

        # Связь отзыва с учебным заведением
        create_edge(sc_types.EDGE_D_COMMON_CONST, establishment_node, feedback_node, nrel_feedback)

        # Добавление текста отзыва
        create_edge(sc_types.EDGE_D_COMMON_CONST, feedback_node, feedback_text_link, nrel_text)

        # Создание ответа для действия
        create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, action_node, feedback_node)

        self.logger.info("Feedback added successfully")
        return ScResult.OK