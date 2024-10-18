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


class SearchProfessionAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_search_profession")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("SearchProfessionAgent finished %s",
                         "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("SearchProfessionAgent started")

        try:
            message_addr = get_action_arguments(action_node, 1)[0]
            concept = ScKeynodes.resolve(
                "concept_profession", sc_types.NODE_CONST_CLASS)
            nrel_profession = ScKeynodes.resolve(
                "nrel_profession", sc_types.NODE_NOROLE)
            nrel_skills = ScKeynodes.resolve(
                "nrel_skills", sc_types.NODE_NOROLE)
            message_type = ScKeynodes.resolve('concept_message_ask_about_personaly_profession', sc_types.NODE_CONST_CLASS)

            if not check_edge(sc_types.EDGE_ACCESS_VAR_POS_PERM, message_type, message_addr):
                self.logger.info(
                    f"SearchProfessionAgent: the message isn’t about profession")
                return ScResult.OK

        except:
            self.logger.info(f"SearchProfessionAgent: finished with an error")
            return ScResult.ERROR

        human_skills = []
        human_skills = self.get_human_skills()

        if human_skills is None:
            self.logger.info(f"SearchProfessionAgent: human skills is none")
            return ScResult.ERROR_NOT_FOUND

        if not len(human_skills) > 0:
            self.logger.info(f"SearchProfessionAgent: human skills not found")
            return ScResult.OK

        concept_profession = ScKeynodes.resolve(
            "concept_profession", sc_types.NODE_CONST_CLASS)
        template = ScTemplate()
        # entity node or link

        template.triple(
            concept_profession,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.NODE_VAR >> "_node"
        )

        result = template_search(template)

        if not len(result) > 0:
            self.logger.info(
                f"SearchProfessionAgent: the professions not found")
            return ScResult.ERROR_NOT_FOUND

        dict_professions = {}

        for addr in result:
            entity_profession = addr.get("_node")
            dict_professions[entity_profession] = 0

            template = ScTemplate()
            # entity node or link

            template.triple_with_relation(
                entity_profession,
                sc_types.EDGE_D_COMMON_VAR,
                sc_types.NODE_VAR >> "_node",
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                nrel_skills
            )

            result_skills = template_search(template)

            if not len(result_skills) > 0:
                continue

            for addr_skill in result_skills:
                skill = addr_skill.get("_node")
                if not skill:
                    continue
                if skill in human_skills:
                    dict_professions[entity_profession] += 1

        if not len(dict_professions) > 0:
            self.logger.info(
                f"SearchProfessionAgent: the professions not found with generals skills")
            return ScResult.ERROR_NOT_FOUND

        self.logger.info(dict_professions)

        sorted_dict_professions = sorted(dict_professions, key=dict_professions.__getitem__)
        profession = sorted_dict_professions[-1]

        fireman = ScKeynodes.resolve(
            "Architector", sc_types.NODE_CONST)
        profession_edge = create_edge(
            sc_types.EDGE_ACCESS_CONST_POS_PERM, message_addr, profession)
        create_action_answer(action_node, profession_edge)

        return ScResult.OK

    def get_human_skills(self):
        concept_human = ScKeynodes.resolve("concept_human", sc_types.NODE_CONST_CLASS)

        nrel_skills = ScKeynodes.resolve(
            "nrel_skills", sc_types.NODE_NOROLE)

        template = ScTemplate()

        template.triple(
            concept_human,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.NODE_VAR >> "_node"
        )

        result = template_search(template)

        if not len(result) > 0:
            self.logger.info(
                f"SearchProfessionAgent: the human not found")
            return None

        human = result[0].get("_node")

        template = ScTemplate()
        # entity node or link

        template.triple_with_relation(
            human,
            sc_types.EDGE_D_COMMON_VAR,
            sc_types.NODE_VAR >> "_node",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            nrel_skills
        )

        result_human_skills = template_search(template)

        if not len(result_human_skills) > 0:
            self.logger.info(
                f"SearchProfessionAgent: the skills human not found")
            return None

        human_skills = []

        for human_skill_addr in result_human_skills:
            human_skills.append(human_skill_addr.get("_node"))

        return human_skills

    def get_ru_idtf(self, entity_addr: ScAddr) -> ScAddr:
        main_idtf = ScKeynodes.resolve(
            "nrel_main_idtf", sc_types.NODE_CONST_NOROLE)
        lang_ru = ScKeynodes.resolve("lang_ru", sc_types.NODE_CONST_CLASS)

        template = ScTemplate()
        template.triple_with_relation(
            entity_addr,
            sc_types.EDGE_D_COMMON_VAR,
            sc_types.LINK,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            main_idtf,
        )
        search_results = template_search(template)
        for result in search_results:
            idtf = result[2]
            lang_edge = get_edge(
                lang_ru, idtf, sc_types.EDGE_ACCESS_VAR_POS_PERM)
            if lang_edge:
                return idtf
        return get_element_by_norole_relation(
            src=entity_addr, nrel_node=main_idtf)

    def get_entity_addr(self, message_addr: ScAddr, rrel_entity: ScAddr):
        rrel_entity = ScKeynodes.resolve("rrel_entity", sc_types.NODE_ROLE)
        concept_country = ScKeynodes.resolve(
            "concept_country", sc_types.NODE_CONST_CLASS)
        template = ScTemplate()
        # entity node or link

        template.triple_with_relation(
            message_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.VAR,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rrel_entity,
        )
        search_results = template_search(template)
        if len(search_results) == 0:
            return ScAddr(0), None
        entity = search_results[0][2]
        if len(search_results) == 1:
            return entity, None
        # check country position in search_results
        country_edge = get_edge(
            concept_country, entity, sc_types.EDGE_ACCESS_VAR_POS_PERM)
        if country_edge:
            return search_results[1][2], entity
        else:
            return entity, search_results[1][2]

    def clear_previous_answer(self, entity, nrel_temperature, answer_phrase):
        message_answer_set = ScSet(set_node=answer_phrase)
        message_answer_set.clear()
        if not entity.is_valid():
            return

        template = ScTemplate()
        template.triple_with_relation(
            entity,
            sc_types.EDGE_D_COMMON_VAR,
            sc_types.LINK,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            nrel_temperature
        )
        search_results = template_search(template)
        for result in search_results:
            delete_edges(result[0], result[2], sc_types.EDGE_D_COMMON_VAR)
