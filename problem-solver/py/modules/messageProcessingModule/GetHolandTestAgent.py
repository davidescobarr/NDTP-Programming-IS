"""
This code creates some test agent and registers until the user stops the process.
For this we wait for SIGINT.
"""
import logging
from re import template
from typing import List, Optional
import json

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

class GetHolandTestAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_get_holand_test_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("GetHolandTestAgent finished %s",
                         "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("GetHolandTestAgent started")

        # Resolve required keynodes
        nrel_name = ScKeynodes.resolve("nrel_name", sc_types.NODE_NOROLE)
        concept_test = ScKeynodes.resolve("concept_test", sc_types.NODE_CONST_CLASS)

        if not nrel_name or not concept_test:
            self.logger.error("Required keynodes not found")
            return ScResult.ERROR

        # Search for all tests
        template = ScTemplate()
        template.triple(
            concept_test,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.NODE_VAR >> "_test"
        )

        search_result = template_search(template)
        if not search_result:
            self.logger.warning("No tests found")
            return ScResult.ERROR_NOT_FOUND

        # Iterate over found tests and check their name
        for item in search_result:
            test_node = item.get("_test")

            # Search for the name of the test
            name_template = ScTemplate()
            name_template.triple_with_relation(
                test_node,
                sc_types.EDGE_D_COMMON_VAR,
                sc_types.LINK_VAR >> "_name_link",
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                nrel_name
            )

            name_result = template_search(name_template)
            if not name_result:
                continue

            for name_item in name_result:
                name_link = name_item.get("_name_link")
                test_name = get_link_content_data(name_link)

                if test_name == "test_holand":
                    self.logger.info("Found Holland Test: %s", test_name)

                    
                    return ScResult.OK

        self.logger.warning("Holland Test not found")
        return ScResult.ERROR_NOT_FOUND
