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

class GetTestsWithDescriptionsAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_get_tests_with_descriptions_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("GetTestsWithDescriptionsAgent finished %s",
                         "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("GetTestsWithDescriptionsAgent started")

        # Resolve required keynodes
        nrel_full_info = ScKeynodes.resolve(
            "nrel_full_info", sc_types.NODE_NOROLE)
        concept_test = ScKeynodes.resolve(
            "concept_test", sc_types.NODE_CONST_CLASS)
        nrel_name = ScKeynodes.resolve(
            "nrel_name", sc_types.NODE_NOROLE)

        if not nrel_full_info or not concept_test:
            self.logger.error("Required keynodes not found")
            return ScResult.ERROR

        # Search for tests
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

        tests = {}

        for item in search_result:
            test_node = item.get("_test")

            # Search for full info related to the test
            info_template = ScTemplate()
            info_template.triple_with_relation(
                test_node,
                sc_types.EDGE_D_COMMON_VAR,
                sc_types.LINK_VAR >> "_info_link",
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                nrel_full_info
            )

            info_result = template_search(info_template)
            if not info_result:
                continue



            for info_item in info_result:
                info_link = info_item.get("_info_link")
                info_content = get_link_content_data(info_link)

                if info_content:

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
                        name_content = get_link_content_data(name_link)

                        if name_content:
                            test_idtf = get_system_idtf(test_node)
                            test_desc = {}
                            test_desc["name"] = name_content
                            test_desc["info"] = info_content
                            tests[test_idtf] = test_desc
                    

        json_answer = json.dumps(tests)



        self.logger.info(json_answer)

        json_link = create_link(json_answer)

        create_action_answer(action_node, json_link)

        self.logger.info("Tests found and answer created")
        return ScResult.OK