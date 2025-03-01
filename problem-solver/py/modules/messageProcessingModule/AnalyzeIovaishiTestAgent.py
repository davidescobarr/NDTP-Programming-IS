import logging
import json

from sc_client.models import ScAddr, ScLinkContentType, ScTemplate
from sc_client.constants import sc_types
from sc_client.client import template_search, create_elements

from sc_kpm import ScAgentClassic, ScModule, ScResult, ScServer
from sc_kpm.utils import (
    create_link,
    get_link_content_data,
    check_edge, create_edge,
    delete_edges,
    get_system_idtf,
    get_edge
)
from sc_kpm.utils.action_utils import (
    create_action_answer,
    finish_action_with_status,
    get_action_arguments
)
from sc_kpm import ScKeynodes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(message)s",
    datefmt="[%d-%b-%y %H:%M:%S]"
)

class AnalyzeIovaishiTestAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_analyze_iovaishi_test_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = (result == ScResult.OK)
        finish_action_with_status(action_element, is_successful)
        self.logger.info("AnalyzeIovaishiTestAgent finished %s", "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("AnalyzeIovaishiTestAgent started")

        json_link = get_action_arguments(action_node, 1)[0]
        json_data = get_link_content_data(json_link)
        self.logger.info(json_data)
        if not json_data:
            self.logger.error("No JSON data found")
            return ScResult.ERROR

        try:
            questions = json.loads(json_data)
            self.logger.info("Received JSON data: %s", questions)
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse JSON: %s", str(e))
            return ScResult.ERROR

        if not isinstance(questions, list):
            self.logger.error("JSON data is not a list")
            return ScResult.ERROR

        category_definitions = {
            "category1": ["1a", "3a", "5a", "6a", "8a", "11a", "13a", "15a", "16a", "18a", "20a", "24a"],
            "category2": ["2a", "2b", "5b", "6b", "7a", "9a", "11b", "14a", "18b", "21a", "22b", "23a"],
            "category3": ["4a", "5c", "7b", "11c", "12a", "15b", "16b", "18c", "19a", "20b", "21b", "22b"],
            "category4": ["1b", "2b", "3c", "7c", "9b", "10a", "12b", "14b", "17a", "21c", "22c", "23b"],
            "category5": ["2c", "4b", "8b", "9c", "10b", "12c", "13b", "14c", "15c", "17b", "19b", "24b"],
            "category6": ["1c", "4c", "6c", "8c", "10c", "13c", "16c", "17c", "19c", "20c", "23c", "24c"],
        }

        category_scores = {cat: 0 for cat in category_definitions}

        for i, question in enumerate(questions):
            answer_val = question.get("answer")
            question_number = i + 1
            
            if answer_val == 0:
                effective_id = f"{question_number}a"
            elif answer_val == 1:
                effective_id = f"{question_number}b"
            elif answer_val == 2:
                effective_id = f"{question_number}c"
            else:
                continue
            
            self.logger.info("Question %s: effective id %s", question_number, effective_id)

            for cat, id_list in category_definitions.items():
                if effective_id in id_list:
                    category_scores[cat] += 1

        winning_category = max(category_scores, key=category_scores.get)
        self.logger.info("Winning category: %s", winning_category)

        result_text = ''

        if winning_category == "category1":
            result_text = '''Склонность к работе с людьми. Профессии, связанные с управлением, обучением, воспитанием,
                            обслуживанием (бытовым, медицинским, справочно-информационным). Людей, успешных в
                            профессиях этой группы, отличает общительность, способность находить общий язык с разными
                            людьми, понимать их настроение, намерения.
                            '''
        elif winning_category == "category2":
            result_text = '''Склонность к исследовательской (интеллектуальной) работе. Профессии, связанные с научной
                            деятельностью. Кроме специальных знаний такие люди обычно отличаются рациональностью,
                            независимостью суждений, аналитическим складом ума.
                            '''
        elif winning_category == "category3":
            result_text = '''Ваш результат преобладает в категории 3.
                            Склонность к практической деятельности. Круг этих профессий очень широк: производство
                            и обработка металла; сборка, монтаж приборов и механизмов; ремонт, наладка, обслуживание
                            электронного и механического оборудования; монтаж, ремонт зданий, конструкций; управление
                            транспортом; изготовление изделий
                            '''
        elif winning_category == "category4":
            result_text = '''Склонность к эстетическим видам деятельности. Профессии творческого характера,
                            связанные с изобразительной, музыкальной, литературно-художественной, актерско-сценической
                            деятельностью. Людей творческих профессий кроме специальных способностей (музыкальных,
                            литературных, актерских) отличает оригинальность и независимость.
                            '''
        elif winning_category == "category5":
            result_text = '''Склонность к экстремальным видам деятельности. Профессии, связанные с занятиями
                            спортом, путешествиями, экспедиционной работой, охранной и оперативно-розыскной деятельности,
                            службой в армии. Все они предъявляют особые требования к физической подготовке, здоровью,
                            волевым качествам.
                            '''
        elif winning_category == "category6":
            result_text = '''Склонность к планово-экономическим видам деятельности. Профессии, связанные с
                            расчетами и планированием (бухгалтер, экономист); делопроизводством, анализом текстов и их
                            преобразованием (редактор, переводчик, лингвист); схематическим изображением объектов
                            (чертежник, топограф). Эти профессии требуют от человека собранности и аккуратности.
                            '''
        else:
            result_text = "Спасибо за прохождение теста! Ваши ответы учтены."
        
        threshold = 7
        recommendations = {cat: (f"Для {cat} рекомендуем обратить внимание на соответствующие направления." if score >= threshold else f"Для {cat} рекомендаций пока нет.") for cat, score in category_scores.items()}

        result_data = {
            "text": result_text,
            "scores": category_scores,
            "recommendations": recommendations
        }
        result_text_json = json.dumps(result_data)

        text_link = create_link(result_text_json, ScLinkContentType.STRING)
        create_action_answer(action_node, text_link)

        self.logger.info("Test analysis completed, result sent")
        return ScResult.OK
