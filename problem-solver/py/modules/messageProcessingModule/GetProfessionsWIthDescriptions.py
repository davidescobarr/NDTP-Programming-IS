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

class GetProfessionsWithDescriptions(ScAgentClassic):
    def __init__(self):
        super().__init__("action_get_professions_with_descriptions_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("GetProfessionsWithDescriptionsAgent finished %s",
                         "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("GetProfessionsWithDescriptionsAgent started")

        # Resolve required keynodes
        nrel_full_info = ScKeynodes.resolve(
            "nrel_full_info", sc_types.NODE_NOROLE)
        concept_profession = ScKeynodes.resolve(
            "concept_profession", sc_types.NODE_CONST_CLASS)
        nrel_main_idtf = ScKeynodes.resolve(
            "nrel_main_idtf", sc_types.NODE_NOROLE)

        if not nrel_full_info or not concept_profession:
            self.logger.error("Required keynodes not found")
            return ScResult.ERROR

        # Search for professions
        template = ScTemplate()
        template.triple(
            concept_profession,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.NODE_VAR >> "_profession"
        )

        search_result = template_search(template)
        if not search_result:
            self.logger.warning("No professions found")
            return ScResult.ERROR_NOT_FOUND

        professions = {}

        temp = []

        for item in search_result:
            profession_node = item.get("_profession")

            # Search for full info related to the profession
            info_template = ScTemplate()
            info_template.triple_with_relation(
                profession_node,
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
                        profession_node,
                        sc_types.EDGE_D_COMMON_VAR,
                        sc_types.LINK_VAR >> "_name_link",
                        sc_types.EDGE_ACCESS_VAR_POS_PERM,
                        nrel_main_idtf
                    )

                    name_result = template_search(name_template)
                    if not name_result:
                        continue

                    for name_item in name_result:
                        name_link = name_item.get("_name_link")
                        name_content = get_link_content_data(name_link)

                        if name_content:
                            profession_idtf = get_system_idtf(profession_node)
                            profession_desc = {}
                            profession_desc["name"] = name_content
                            profession_desc["info"] = info_content
                            professions[profession_idtf] = profession_desc
                    

        json_answer = json.dumps(professions)



        self.logger.info(json_answer)

        json_link = create_link(json_answer)

        create_action_answer(action_node, json_link)

        self.logger.info("Professions found and answer created")
        return ScResult.OK