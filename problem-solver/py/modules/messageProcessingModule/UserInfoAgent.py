import json

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

class UserInfoAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_get_information_about_user")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info(
            "UserInfoAgent finished %s",
            "successfully" if is_successful else "unsuccessfully",
        )
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("UserInfoAgent started")

        # Проверить аргументы
        arguments = get_action_arguments(action_node)
        if not arguments or len(arguments) != 1:
            self.logger.error("Invalid arguments. Expected 1 argument: user identifier.")
            return ScResult.ERROR_INVALID_PARAMS

        user_node = arguments[0]
        if not is_node_of_class(user_node, "concept_user"):
            self.logger.error("Invalid user identifier: %s", user_node)
            return ScResult.ERROR_NOT_FOUND

        # Извлечь информацию о пользователе
        user_info = self.get_user_info(user_node)
        if not user_info:
            self.logger.error("Failed to retrieve information for user: %s", user_node)
            return ScResult.ERROR

        # Формировать JSON-ответ
        self.create_json_response(action_node, user_info)
        return ScResult.OK

    def get_user_info(self, user_node: ScAddr) -> dict:
        # Инициализировать ключевые узлы
        nrel_firstname = ScKeynodes.resolve("nrel_firstname", sc_types.NODE_NOROLE)
        nrel_surname = ScKeynodes.resolve("nrel_surname", sc_types.NODE_NOROLE)
        nrel_patronymic = ScKeynodes.resolve("nrel_patronymic", sc_types.NODE_NOROLE)
        nrel_nickname = ScKeynodes.resolve("nrel_nickname", sc_types.NODE_NOROLE)
        nrel_hobbies = ScKeynodes.resolve("nrel_hobbies", sc_types.NODE_NOROLE)
        nrel_traits = ScKeynodes.resolve("nrel_traits", sc_types.NODE_NOROLE)
        nrel_history_test_user = ScKeynodes.resolve("nrel_history_test_user", sc_types.NODE_NOROLE)

        # Извлечь данные
        firstname = get_link_content(find_target(user_node, nrel_firstname))
        surname = get_link_content(find_target(user_node, nrel_surname))
        patronymic = get_link_content(find_target(user_node, nrel_patronymic))
        nickname = get_link_content(find_target(user_node, nrel_nickname))
        hobbies = find_targets(user_node, nrel_hobbies)
        traits = find_targets(user_node, nrel_traits)
        test_history = find_targets(user_node, nrel_history_test_user)

        # Формировать структуру
        return {
            "fullname": {
                "firstname": firstname,
                "surname": surname,
                "patronymic": patronymic,
            },
            "nickname": nickname,
            "hobbies": [get_link_content(hobby) for hobby in hobbies],
            "traits": [get_link_content(trait) for trait in traits],
            "test_history": [get_link_content(test) for test in test_history],
        }

    def create_json_response(self, action_node: ScAddr, user_info: dict):
        nrel_answer = ScKeynodes.resolve("nrel_answer", sc_types.NODE_NOROLE)

        # Формировать JSON
        response_json = json.dumps(user_info, ensure_ascii=False, indent=4)

        # Сохранить JSON как содержимое узла
        answer_node = create_elements({
            "type": sc_types.LINK_CONST,
            "content": response_json,
        })
        create_elements({
            "type": sc_types.EDGE_D_COMMON,
            "source": action_node,
            "target": answer_node,
        })
        create_elements({
            "type": sc_types.EDGE_ACCESS,
            "source": nrel_answer,
            "target": answer_node,
        })