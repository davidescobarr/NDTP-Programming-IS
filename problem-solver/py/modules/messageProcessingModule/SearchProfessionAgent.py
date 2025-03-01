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

class SearchProfessionAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_search_profession")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = result == ScResult.OK
        finish_action_with_status(action_element, is_successful)
        self.logger.info("GetHolandTestAgent finished %s",
                         "successfully" if is_successful else "unsuccessfully")
        return result


    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("SearchProfessionAgent started")

        # Получаем необходимые ключевые узлы
        concept_profession = ScKeynodes.resolve("concept_profession", sc_types.NODE_CONST_CLASS)
        nrel_skills = ScKeynodes.resolve("nrel_skills", sc_types.NODE_NOROLE)

        # Получаем навыки человека из базы знаний
        human_skills = self.get_human_skills()
        if not human_skills:
            self.logger.info("SearchProfessionAgent: human skills not found")
            return ScResult.ERROR_NOT_FOUND

        # Ищем все профессии
        template = ScTemplate()
        template.triple(
            concept_profession,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.NODE_VAR >> "_profession"
        )
        professions_result = template_search(template)
        if not professions_result:
            self.logger.info("SearchProfessionAgent: no professions found")
            return ScResult.ERROR_NOT_FOUND

        # Подсчитываем для каждой профессии количество совпадающих навыков
        dict_professions = {}
        for res in professions_result:
            profession_node = res.get("_profession")
            dict_professions[profession_node] = 0

            # Получаем навыки конкретной профессии
            template = ScTemplate()
            template.triple_with_relation(
                profession_node,
                sc_types.EDGE_D_COMMON_VAR,
                sc_types.NODE_VAR >> "_skill",
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                nrel_skills
            )
            skills_result = template_search(template)
            if not skills_result:
                continue

            for skill_res in skills_result:
                skill_node = skill_res.get("_skill")
                if skill_node and skill_node in human_skills:
                    dict_professions[profession_node] += 1

        if not dict_professions:
            self.logger.info("SearchProfessionAgent: no matching professions found")
            return ScResult.ERROR_NOT_FOUND

        self.logger.info("Professions scores: %s", dict_professions)

        # Выбираем профессию с максимальным числом совпадений
        sorted_professions = sorted(dict_professions, key=dict_professions.get)
        for i in sorted_professions:
            self.logger.info(get_system_idtf(i))
        best_profession = sorted_professions[-1]

        # Получаем название выбранной профессии (например, системный идентификатор)
        profession_name = get_system_idtf(best_profession)
        self.logger.info("Selected profession: %s", profession_name)

        # Формируем JSON-объект с названием профессии
        result_data = {
            "profession": profession_name
        }
        result_json = json.dumps(result_data)
        self.logger.info(result_json)

        # Создаём Sc-ссылку с JSON-текстом и отправляем её как ответ
        result_link = create_link(result_json)
        self.logger.info(create_link)
        create_action_answer(action_node, result_link)

        return ScResult.OK

    def get_human_skills(self) -> List[ScAddr]:
        # Разрешаем узел "concept_human"
        concept_human = ScKeynodes.resolve("concept_human", sc_types.NODE_CONST_CLASS)
        nrel_skills = ScKeynodes.resolve("nrel_skills", sc_types.NODE_NOROLE)

        # Находим узел, представляющий человека
        template = ScTemplate()
        template.triple(
            concept_human,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.NODE_VAR >> "_human"
        )
        human_result = template_search(template)
        if not human_result:
            self.logger.info("SearchProfessionAgent: human node not found")
            return []

        human_node = human_result[0].get("_human")

        # Извлекаем навыки человека
        template = ScTemplate()
        template.triple_with_relation(
            human_node,
            sc_types.EDGE_D_COMMON_VAR,
            sc_types.NODE_VAR >> "_skill",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            nrel_skills
        )
        skills_result = template_search(template)
        if not skills_result:
            self.logger.info("SearchProfessionAgent: no human skills found")
            return []

        return [res.get("_skill") for res in skills_result if res.get("_skill")]
