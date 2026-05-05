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

class AnalyzeNeedInApprovalTestAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_analyze_need_in_approval_test_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = (result == ScResult.OK)
        finish_action_with_status(action_element, is_successful)
        self.logger.info("AnalyzeNeedInApprovalTestAgent finished %s", "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("AnalyzeNeedInApprovalTestAgent started")

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
        yes_score_questions = {1, 2, 3, 4, 5, 8, 13, 14, 15, 19}
        
        # Ответы "Нет" (answer = 1) дают 1 балл
        no_score_questions = {6, 7, 9, 11, 12, 16, 17, 18}

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
        if total_score <= 7:
            level = "низкая"
            result_text = f"""Тебе не так важно производить впечатление или подстраиваться под ожидания других.
Ты чаще опираешься на собственные решения и внутренние ориентиры."""
        elif 8 <= total_score <= 14:
            level = "средняя"
            result_text = f"""Ты стремишься выглядеть хорошо в глазах окружающих, но без чрезмерной зависимости от их мнения.
Умеешь сохранять баланс между самовыражением и социальными ожиданиями."""
        else:
            level = "высокая"   
            result_text = f"""Тебе важно получать одобрение, поддерживать позитивный образ и избегать негативной оценки.
Это помогает легко находить общий язык с людьми, но иногда может мешать отстаивать свои интересы."""
        
        self.logger.info("Motivation level determined: %s (score: %d)", level, total_score)

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

        self.logger.info("AnalyzeNeedInApprovalTestAgent test analysis completed, result sent")
        return ScResult.OK