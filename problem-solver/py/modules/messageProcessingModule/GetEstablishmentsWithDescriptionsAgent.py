import logging
import json

from sc_client.models import ScAddr, ScTemplate
from sc_client.constants import sc_types
from sc_client.client import template_search

from sc_kpm import ScAgentClassic, ScResult
from sc_kpm.utils import (
    create_link,
    get_link_content_data,
    get_system_idtf
)
from sc_kpm.utils.action_utils import (
    create_action_answer,
    finish_action_with_status
)
from sc_kpm import ScKeynodes

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s | %(name)s | %(message)s", 
    datefmt="[%d-%b-%y %H:%M:%S]"
)

class GetEstablishmentsWithDescriptionsAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_get_establishments_with_descriptions_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("GetEstablishmentsWithDescriptionsAgent finished %s",
                         "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("GetEstablishmentsWithDescriptionsAgent started")

        # Разрешение ключевых узлов
        nrel_full_info = ScKeynodes.resolve("nrel_full_info", sc_types.NODE_NOROLE)
        concept_establishment = ScKeynodes.resolve("concept_establishment", sc_types.NODE_CONST_CLASS)
        nrel_main_idtf = ScKeynodes.resolve("nrel_main_idtf", sc_types.NODE_NOROLE)

        if not nrel_full_info or not concept_establishment or not nrel_main_idtf:
            self.logger.error("Required keynodes not found")
            return ScResult.ERROR

        # Поиск всех учебных заведений
        template = ScTemplate()
        template.triple(
            concept_establishment,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.NODE_VAR >> "_establishment"
        )

        search_result = template_search(template)
        if not search_result:
            self.logger.warning("No establishments found")
            return ScResult.ERROR_NOT_FOUND

        establishments = {}

        for item in search_result:
            establishment_node = item.get("_establishment")

            # Поиск информации (описания) через nrel_full_info
            info_template = ScTemplate()
            info_template.triple_with_relation(
                establishment_node,
                sc_types.EDGE_D_COMMON_VAR,
                sc_types.LINK_VAR >> "_info_link",
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                nrel_full_info
            )

            info_result = template_search(info_template)
            if not info_result:
                self.logger.warning(f"No description found for {get_system_idtf(establishment_node)}")
                continue

            info_content = None
            for info_item in info_result:
                info_link = info_item.get("_info_link")
                info_content = get_link_content_data(info_link)
                if info_content:
                    break  # Берём первый найденный результат

            if not info_content:
                continue  # Пропускаем заведение без описания

            # Поиск названия через nrel_main_idtf
            name_template = ScTemplate()
            name_template.triple_with_relation(
                establishment_node,
                sc_types.EDGE_D_COMMON_VAR,
                sc_types.LINK_VAR >> "_name_link",
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                nrel_main_idtf
            )

            name_result = template_search(name_template)
            if not name_result:
                self.logger.warning(f"No name found for {get_system_idtf(establishment_node)}")
                continue

            name_content = None
            for name_item in name_result:
                name_link = name_item.get("_name_link")
                name_content = get_link_content_data(name_link)
                if name_content:
                    break

            if not name_content:
                continue  # Пропускаем заведение без названия

            establishment_idtf = get_system_idtf(establishment_node)
            if establishment_idtf.strip().lower() == "info":
                establishment_idtf = str(establishment_node)

            establishments[establishment_idtf] = {
                "name": name_content,
                "info": info_content
            }

        if not establishments:
            self.logger.warning("No establishments with descriptions found.")
            return ScResult.ERROR_NOT_FOUND

        json_answer = json.dumps(establishments, ensure_ascii=False)
        self.logger.info("JSON answer: %s", json_answer)

        json_link = create_link(json_answer)
        create_action_answer(action_node, json_link)

        self.logger.info("Establishments found and answer created")
        return ScResult.OK
