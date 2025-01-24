import logging
#from sc_client.models import ScAddr

# from sc_client.models import ScAddr, ScLinkContentType, ScTemplate, ScConstruction
# from sc_client.constants import sc_types
# from sc_client.client import template_search, create_elements

# from sc_client.constants import sc_types
# from sc_client.client import create_elements, find_by_template, set_content
# from sc_kpm import ScAgentClassic, ScResult
# from sc_kpm.utils import finish_action_with_status, get_action_arguments
# from sc_kpm import ScKeynodes

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

class GetEstablishmentsByProfessionAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_get_establishments_by_profession")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info(
            "GetEstablishmentsByProfessionAgent finished %s",
            "successfully" if is_successful else "unsuccessfully",
        )
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("GetEstablishmentsByProfessionAgent started")

        # Проверка аргумента
        arguments = get_action_arguments(action_node)
        if not arguments or len(arguments) != 1:
            self.logger.error("Invalid arguments. Expected 1 argument: profession name.")
            return ScResult.ERROR_INVALID_PARAMS

        profession_name_link = arguments[0]

        # Получение содержимого ссылки
        profession_name = set_content(profession_name_link)
        if not profession_name:
            self.logger.error("Failed to retrieve profession name from link.")
            return ScResult.ERROR_INVALID_STATE

        # Поиск профессии по названию
        concept_profession = ScKeynodes.resolve("concept_profession", sc_types.NODE_CONST_CLASS)
        profession_node = self.find_profession_by_name(profession_name, concept_profession)
        if not profession_node:
            self.logger.error("No profession found with the name: %s", profession_name)
            return ScResult.ERROR_NOT_FOUND

        # Поиск специальностей, связанных с профессией
        nrel_set_required_specialities = ScKeynodes.resolve("nrel_set_required_specialities", sc_types.NODE_NOROLE)
        specialities = self.find_related_nodes(profession_node, nrel_set_required_specialities)
        if not specialities:
            self.logger.error("No specialities found for profession: %s", profession_name)
            return ScResult.ERROR_NOT_FOUND

        # Поиск учебных заведений для каждой специальности
        concept_establishment = ScKeynodes.resolve("concept_establishment", sc_types.NODE_CONST_CLASS)
        establishments = self.find_establishments_for_specialities(specialities, concept_establishment)
        if not establishments:
            self.logger.error("No establishments found for the specialities of profession: %s", profession_name)
            return ScResult.ERROR_NOT_FOUND

        # Формирование результата
        self.logger.info("Found establishments for profession '%s': %s", profession_name, establishments)
        return ScResult.OK

    def find_profession_by_name(self, profession_name: str, concept_profession: ScAddr) -> ScAddr:
        results = find_by_template({
            "concept": concept_profession,
            "relation": sc_types.NODE_CONST,
            "link": profession_name,
        })
        return results[0].get("concept") if results else None

    def find_related_nodes(self, source_node: ScAddr, relation: ScAddr) -> list[ScAddr]:
        results = find_by_template({
            "source": source_node,
            "relation": relation,
            "target": sc_types.NODE_CONST,
        })
        return [result.get("target") for result in results]

    def find_establishments_for_specialities(self, specialities: list[ScAddr], concept_establishment: ScAddr) -> list[ScAddr]:
        establishments = []
        for speciality in specialities:
            results = find_by_template({
                "source": speciality,
                "relation": sc_types.NODE_CONST,
                "target": sc_types.NODE_CONST,
            })
            for result in results:
                establishment = result.get("target")
                if self.is_node_of_class(establishment, concept_establishment):
                    establishments.append(establishment)
        return establishments

    def is_node_of_class(self, node: ScAddr, concept_class: ScAddr) -> bool:
        results = find_by_template({
            "instance": node,
            "relation": sc_types.NODE_CONST,
            "class": concept_class,
        })
        return len(results) > 0