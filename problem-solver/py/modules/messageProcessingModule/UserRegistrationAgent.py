import logging

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

class UserRegistrationAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_user_registration_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("UserRegistrationAgent finished %s", "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("UserRegistrationAgent started")

        # Resolve required keynodes
        nrel_nickname = ScKeynodes.resolve("nrel_nickname", sc_types.NODE_NOROLE)
        nrel_firstname = ScKeynodes.resolve("nrel_firstname", sc_types.NODE_NOROLE)
        nrel_surname = ScKeynodes.resolve("nrel_surname", sc_types.NODE_NOROLE)
        nrel_patronymic = ScKeynodes.resolve("nrel_patronymic", sc_types.NODE_NOROLE)
        nrel_password = ScKeynodes.resolve("nrel_password", sc_types.NODE_NOROLE)
        concept_user = ScKeynodes.resolve("concept_user", sc_types.NODE_CONST_CLASS)

        if not all([nrel_nickname, nrel_firstname, nrel_surname, nrel_patronymic, nrel_password, concept_user]):
            self.logger.error("Required keynodes not found")
            return ScResult.ERROR

        # Get action arguments (nickname, firstname, surname, patronymic, password)
        arguments = get_action_arguments(action_node)
        if len(arguments) != 5:
            self.logger.error("Invalid number of arguments provided")
            return ScResult.ERROR_INVALID_PARAMS

        nickname, firstname, surname, patronymic, password = arguments

        # Create a new user node
        user_node = ScAddr()
        try:
            user_node = ScAddr.create_node(sc_types.NODE_CONST)
            create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, concept_user, user_node)

            # Add attributes to the user node
            self._create_user_attribute(user_node, nickname, nrel_nickname)
            self._create_user_attribute(user_node, firstname, nrel_firstname)
            self._create_user_attribute(user_node, surname, nrel_surname)
            self._create_user_attribute(user_node, patronymic, nrel_patronymic)
            self._create_user_attribute(user_node, password, nrel_password)
        except Exception as e:
            self.logger.error(f"Failed to create user: {e}")
            return ScResult.ERROR

        # Return the created user as an answer
        create_action_answer(action_node, user_node)
        self.logger.info("User successfully registered")
        return ScResult.OK

    def _create_user_attribute(self, user_node: ScAddr, value: ScAddr, relation: ScAddr):
        """Helper method to create an attribute for the user node"""
        link = create_link(value)
        create_edge(sc_types.EDGE_D_COMMON_CONST, user_node, link)
        create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, relation, link)