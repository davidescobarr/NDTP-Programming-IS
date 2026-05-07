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

class AnalyzeHumanitiesLevelTestAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_analyze_humanities_level_test_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = (result == ScResult.OK)
        finish_action_with_status(action_element, is_successful)
        self.logger.info("AnalyzeHumanitiesLevelTestAgent finished %s", "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("AnalyzeHumanitiesLevelTestAgent started")

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

        # Подсчитываем количество ответов "Да" (answer = 0)
        yes_answers_count = 0
        total_questions = 0
        
        for idx, question in enumerate(questions, start=1):
            answer_val = question.get("answer")
            
            if answer_val is None:
                self.logger.warning("Question %d missing answer field, skipping", idx)
                continue
            
            if answer_val == 0:  # Ответ "Да"
                yes_answers_count += 1
                self.logger.debug("Question %d: Да", idx)
            else:  # Ответ "Нет"
                self.logger.debug("Question %d: Нет", idx)
            
            total_questions += 1
        
        self.logger.info("Yes answers count: %d out of %d", yes_answers_count, total_questions)
        
        if yes_answers_count <= 6:
            level = "низкий"
            result_text = f"""Низкая склонность к гуманитарным профессиям
Вам может быть ближе работа с точными науками, технологиями или структурированными задачами. Гуманитарная сфера не является вашим естественным направлением, но отдельные гуманитарные навыки могут развиваться при необходимости."""
            
        elif 7 <= yes_answers_count <= 12:
            level = "средний"
            result_text = f"""Умеренная склонность к гуманитарным профессиям
КУ вас есть отдельные гуманитарные способности, но они не доминируют. Вы можете успешно работать в смешанных областях: коммуникации в IT, аналитика, менеджмент, маркетинг."""
            
        elif 13 <= yes_answers_count <= 16:
            level = "высокий"
            result_text = f"""Выраженная склонность к гуманитарным профессиям
Гуманитарные профессии вам подходят. Вы сильны в коммуникации, работе с текстами, идеями, людьми. Подойдут направления: журналистика, образование, HR, PR, контент, творчество."""
        
        else:
            level = "очень высокий"
            result_text = f"""Ярко выраженная гуманитарная направленность
Гуманитарная сфера — ваша естественная среда. Вы обладаете развитым языковым, коммуникативным и творческим мышлением. Вам подойдут профессии, связанные с текстами, искусством, культурой, коммуникациями, психологией."""
        
        self.logger.info("Humanities level determined: %s (yes answers: %d)", level, yes_answers_count)

        result_data = {
            "text": result_text,
            "level": level,
            "yes_answers_count": yes_answers_count,
            "total_questions": total_questions
        }
        
        result_text_json = json.dumps(result_data, ensure_ascii=False)
        self.logger.info("Result JSON: %s", result_text_json)

        text_link = create_link(result_text_json, ScLinkContentType.STRING)
        create_action_answer(action_node, text_link)

        self.logger.info("AnalyzeHumanitiesLevelTestAgent test analysis completed, result sent")
        return ScResult.OK