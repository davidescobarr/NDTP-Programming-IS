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

class UserAuthorizationAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_user_authorization_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("UserAuthorizationAgent finished %s", "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("UserAuthorizationAgent started")

        # Resolve required keynodes
        nrel_login = ScKeynodes.resolve("nrel_nickname", sc_types.NODE_NOROLE)
        nrel_password = ScKeynodes.resolve("nrel_password", sc_types.NODE_NOROLE)
        concept_user = ScKeynodes.resolve("concept_user", sc_types.NODE_CONST_CLASS)

        if not all([nrel_login, nrel_password, concept_user]):
            self.logger.error("Required keynodes not found")
            return ScResult.ERROR

        # Get action arguments (login and password)
        arguments = get_action_arguments(action_node, 2)
        if len(arguments) != 2:
            self.logger.error("Invalid number of arguments provided")
            return ScResult.ERROR_INVALID_PARAMS

        login, password = arguments
        login = get_link_content_data(login)
        password = get_link_content_data(password)
        self.logger.info(login)
        self.logger.info(password)


        # Search for a user with matching login and password
        template = ScTemplate()
        template.triple(
            concept_user,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.NODE_VAR >> "_user",
        )
        # template.triple_with_relation(
        #     "_user",
        #     sc_types.EDGE_D_COMMON_VAR,
        #     sc_types.LINK_VAR >> "_login_link",
        #     sc_types.EDGE_ACCESS_VAR_POS_PERM,
        #     nrel_login
        # )
        template.triple_with_relation(
            "_user",
            sc_types.EDGE_D_COMMON_VAR,
            sc_types.LINK_VAR >> "_password_link",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            nrel_password
        )

        # template.triple_with_relation(
        #     entity_profession,
        #     sc_types.EDGE_D_COMMON_VAR,
        #     sc_types.NODE_VAR >> "_node",
        #     sc_types.EDGE_ACCESS_VAR_POS_PERM,
        #     nrel_skills
        # )

        search_result = template_search(template)
        self.logger.warning(search_result)
        if not search_result:
            self.logger.warning("No users found with the provided password")
            return ScResult.ERROR_NOT_FOUND

        for item in search_result:
            user_node = item.get("_user")
            # login_link = item.get("_login_link")
            password_link = item.get("_password_link")

            template = ScTemplate()
            template.triple_with_relation(
                user_node,
                sc_types.EDGE_D_COMMON_VAR,
                sc_types.LINK_VAR >> "_login_link",
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                nrel_login
            )

            search_result2 = template_search(template)

            if not search_result2:
                self.logger.warning("No users found with the provided login")
                return ScResult.ERROR_NOT_FOUND

            login_link = search_result2[0].get("_login_link")

            login_value = get_link_content_data(login_link)
            password_value = get_link_content_data(password_link)
                        
            if login_value == login and password_value == password:
                create_action_answer(action_node, user_node)
                self.logger.info("User successfully authorized")
                return ScResult.OK

        self.logger.warning("Authorization failed: invalid login or password")
        return ScResult.ERROR_INVALID_PARAMS
