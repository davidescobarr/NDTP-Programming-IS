import logging
import json

from sc_client.models import ScAddr, ScLinkContentType
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

class AnalyzeMotivationalTestAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_analyze_motivational_test_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = (result == ScResult.OK)
        finish_action_with_status(action_element, is_successful)
        self.logger.info("AnalyzeMotivationalTestAgent finished %s", "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("AnalyzeMotivationalTestAgent started")

        # Получаем JSON с ответами (Sc-ссылка)
        json_link = get_action_arguments(action_node, 1)[0]
        json_data = get_link_content_data(json_link)
        if not json_data:
            self.logger.error("No JSON data found")
            return ScResult.ERROR

        try:
            # Ожидаемый формат JSON: массив объектов-вопросов с полем "answer"
            questions = json.loads(json_data)
            self.logger.info("Received JSON data with %d questions", len(questions))
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse JSON: %s", str(e))
            return ScResult.ERROR

        if not isinstance(questions, list):
            self.logger.error("JSON data is not a list")
            return ScResult.ERROR

        # Подсчитываем количество ответов с id = 0
        zero_answers_count = 0
        total_answers = 0

        for question in questions:
            answer_val = question.get("answer")
            if answer_val is not None:
                total_answers += 1
                if answer_val == 0:
                    zero_answers_count += 1

        self.logger.info("Zero answers count: %d out of %d", zero_answers_count, total_answers)

        if total_answers == 0:
            self.logger.error("No answers found")
            return ScResult.ERROR

        # Таблица соответствия количества нулей категориям
        # Категория A: [3, 4, 7, 17, 18, 19, 21, 24]
        # Категория Б: [5, 8, 11, 14, 15, 16, 20, 23]
        # Категория В: [1, 2, 6, 9, 10, 12, 13, 22]
        
        category_a_counts = {3, 4, 7, 17, 18, 19, 21, 24}
        category_b_counts = {5, 8, 11, 14, 15, 16, 20, 23}
        category_c_counts = {1, 2, 6, 9, 10, 12, 13, 22}
        
        # Определяем категорию
        if zero_answers_count in category_a_counts:
            category = "A"
            result_text = """Категория А:\n
                            У вас преобладают мотивы выбора престижной профессии,
                            ярко выражено стремление занять видное положение в обществе,
                            реализовать свой высокий уровень притязаний.
                          """
        
        elif zero_answers_count in category_b_counts:
            category = "Б"
            result_text = """Категория Б:\n
                            Вас привлекают материальное благополучие, желание
                            заработать, а интересы, склонности, практическая подготовленность учитываются в меньшей
                            степени.
                          """
        
        elif zero_answers_count in category_c_counts:
            category = "C"
            result_text = """Категория C:\n
                            У вас есть стремление к творческой работе, интерес к новым
                            технологиям, приобретению необходимых умений и навыков,
                            которые требует избираемая профессия.
                          """
        
        else:
            # Если количество нулей не попадает ни в одну категорию
            self.logger.warning("Zero count %d not found in any category", zero_answers_count)
            category = "неопределена"
            result_text = f"""Результат не может быть определён однозначно

                              Количество ответов с выбором первого варианта: {zero_answers_count} из {total_answers}.
                           """
                                        
        self.logger.info("Category determined: %s (zero answers: %d)", category, zero_answers_count)

        # Формируем результат в виде JSON
        result_data = {
            "text": result_text,
            "category": category,
            "zero_answers_count": zero_answers_count,
            "total_answers": total_answers
        }
        
        result_text_json = json.dumps(result_data, ensure_ascii=False)

        text_link = create_link(result_text_json, ScLinkContentType.STRING)
        create_action_answer(action_node, text_link)

        self.logger.info("Motivational test analysis completed, result sent")
        return ScResult.OK