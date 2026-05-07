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

class AnalyzeAbilityInSympathyTestAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_analyze_ability_in_sympathy_test_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = (result == ScResult.OK)
        finish_action_with_status(action_element, is_successful)
        self.logger.info("AnalyzeAbilityInSympathyTestAgent finished %s", "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("AnalyzeAbilityInSympathyTestAgent started")

        # Получаем JSON с ответами (Sc-ссылка)
        json_link = get_action_arguments(action_node, 1)[0]
        json_data = get_link_content_data(json_link)
        if not json_data:
            self.logger.error("No JSON data found")
            return ScResult.ERROR

        try:
            # Ожидаемый формат JSON: массив объектов с полем "answer"
            # answer: 0 - Да, 1 - Нет
            questions = json.loads(json_data)
            self.logger.info("Received JSON data with %d questions", len(questions))
            self.logger.info("First few questions: %s", str(questions[:3]) if len(questions) > 3 else str(questions))
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse JSON: %s", str(e))
            return ScResult.ERROR

        if not isinstance(questions, list):
            self.logger.error("JSON data is not a list")
            return ScResult.ERROR

        # Определяем множества вопросов для подсчета баллов
        # Номера вопросов (индексы в массиве, начиная с 1)
        # Ответы "Да" (answer = 0) дают 1 балл
        yes_score_questions = {1, 5, 7, 8, 9, 10, 12, 14, 16, 17, 18, 19, 25, 26, 27, 29, 31}
        
        # Ответы "Нет" (answer = 1) дают 1 балл
        no_score_questions = {2, 3, 4, 6, 11, 13, 15, 20, 21, 22, 23, 24, 28, 30, 32, 33}

        total_score = 0
        processed_questions = 0
        
        for idx, question in enumerate(questions, start=1):
            answer_val = question.get("answer")
            
            if answer_val is None:
                self.logger.warning("Question %d missing answer field, skipping", idx)
                continue
            
            if idx in yes_score_questions and answer_val == 0:
                total_score += 1
            elif idx in no_score_questions and answer_val == 1:
                total_score += 1
            else:
                self.logger.debug("Question %d: no point added (answer=%d)", idx, answer_val)
            
            processed_questions += 1

        # Определяем уровень мотивации на основе суммы баллов
        if total_score <= 16:
            level = "очень низкий"
            result_text = f"""Тебе трудно считывать эмоциональные сигналы и сопереживать.
Комфортнее работать там, где важны задачи, процессы и чёткие правила, а не взаимодействие с людьми."""
        elif 17 <= total_score <= 22:
            level = "низкий"
            result_text = f"""Тебе сложнее распознавать эмоции других людей, ты больше опираешься на факты, чем на чувства.
Подходят профессии, где важны логика, структура и минимальное эмоциональное вовлечение."""
        elif 23 <= total_score <= 29:
            level = "средний"
            result_text = f"""Ты достаточно хорошо понимаешь чувства окружающих, но сохраняешь баланс между эмпатией и рациональностью.
Подходит для большинства профессий, особенно где важно взаимодействие, но без постоянной эмоциональной нагрузки."""
        else:
            level = "высокий"   
            result_text = f"""Ты легко улавливаешь эмоции других людей, быстро понимаешь их состояние и умеешь сопереживать.
Подходит для профессий, где важны общение, поддержка и работа с людьми."""
        
        self.logger.info("Sympathy level determined: %s (score: %d)", level, total_score)

        result_data = {
            "text": result_text,
            "level": level,
            "total_score": total_score,
            "max_possible_score": len(yes_score_questions) + len(no_score_questions),
            "processed_questions": processed_questions
        }
        
        result_text_json = json.dumps(result_data, ensure_ascii=False)
        self.logger.info("Result JSON: %s", result_text_json)

        text_link = create_link(result_text_json, ScLinkContentType.STRING)
        create_action_answer(action_node, text_link)

        self.logger.info("AnalyzeAbilityInSympathyTestAgent test analysis completed, result sent")
        return ScResult.OK