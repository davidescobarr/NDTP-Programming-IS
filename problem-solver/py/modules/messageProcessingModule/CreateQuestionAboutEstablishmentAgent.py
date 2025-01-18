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
    level=logging.INFO, format="%(asctime)s | %(name)s", datefmt="[%d-%b-%y %H:%M:%S]"
)

class CreateQuestionAboutEstablishmentAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_create_question_about_establishment")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("CreateQuestionAboutEstablishmentAgent finished %s",
                         "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("CreateQuestionAboutEstablishmentAgent started")

        # Шаг 1: Проверка аргументов действия
        arguments = get_action_arguments(action_node)
        if not arguments or len(arguments) != 3:
            self.logger.error("Invalid arguments for action. Expected 3 arguments: user node, establishment node, and question text link")
            return ScResult.ERROR_INVALID_PARAMS

        user_node, establishment_node, question_text_link = arguments
        question_text = get_link_content_data(question_text_link)

        if not question_text:
            self.logger.error("Failed to retrieve question text from argument")
            return ScResult.ERROR

        # Создание узла вопроса
        concept_question = ScKeynodes.resolve("concept_question", sc_types.NODE_CONST_CLASS)
        nrel_question = ScKeynodes.resolve("nrel_question", sc_types.NODE_NOROLE)
        nrel_text = ScKeynodes.resolve("nrel_text", sc_types.NODE_NOROLE)
        nrel_authors = ScKeynodes.resolve("nrel_authors", sc_types.NODE_NOROLE)

        question_node = create_elements({
            "type": sc_types.NODE_CONST,
        })[0]

        if not question_node:
            self.logger.error("Failed to create question node")
            return ScResult.ERROR

        # Связывание узла вопроса с концептом "question"
        create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, concept_question, question_node)

        # Связь вопроса с учебным заведением
        create_edge(sc_types.EDGE_D_COMMON_CONST, establishment_node, question_node, nrel_question)

        # Добавление текста вопроса
        create_edge(sc_types.EDGE_D_COMMON_CONST, question_node, question_text_link, nrel_text)

        # Указание автора вопроса
        create_edge(sc_types.EDGE_D_COMMON_CONST, question_node, user_node, nrel_authors)

        # Создание ответа для действия
        create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, action_node, question_node)

        self.logger.info("Question about establishment added successfully")
        return ScResult.OK