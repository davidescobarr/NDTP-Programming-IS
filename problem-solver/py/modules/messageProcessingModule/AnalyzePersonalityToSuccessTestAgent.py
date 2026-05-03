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

class AnalyzePersonalityToSuccessTestAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_analyze_personality_to_success_test_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = (result == ScResult.OK)
        finish_action_with_status(action_element, is_successful)
        self.logger.info("AnalyzePersonalityToSuccessTestAgent finished %s", "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("AnalyzePersonalityToSuccessTestAgent started")

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
        yes_score_questions = {2, 3, 4, 5, 7, 8, 9, 10, 14, 15, 16, 17, 21, 22, 25, 26, 27, 28, 29, 30, 32, 37, 41}
        
        # Ответы "Нет" (answer = 1) дают 1 балл
        no_score_questions = {6, 18, 19, 20, 24, 31, 36, 38, 39}
        
        # Вопросы, которые не учитываются
        ignored_questions = {1, 11, 12, 19, 28, 33, 34, 35, 40}

        total_score = 0
        processed_questions = 0
        
        # ВАЖНО: перебираем вопросы по индексу (начиная с 1 для номера вопроса)
        for idx, question in enumerate(questions, start=1):
            answer_val = question.get("answer")
            
            if answer_val is None:
                self.logger.warning("Question %d missing answer field, skipping", idx)
                continue
            
            # Пропускаем игнорируемые вопросы
            if idx in ignored_questions:
                self.logger.debug("Question %d ignored", idx)
                continue
            
            # Подсчет баллов
            if idx in yes_score_questions and answer_val == 0:  # Ответ "Да"
                total_score += 1
                self.logger.debug("Question %d: Yes (answer=0) -> +1 point", idx)
            elif idx in no_score_questions and answer_val == 1:  # Ответ "Нет"
                total_score += 1
                self.logger.debug("Question %d: No (answer=1) -> +1 point", idx)
            else:
                self.logger.debug("Question %d: no point added (answer=%d)", idx, answer_val)
            
            processed_questions += 1

        self.logger.info("Total score: %d out of %d processed questions", total_score, processed_questions)

        # Определяем уровень мотивации на основе суммы баллов
        if 1 <= total_score <= 10:
            level = "низкая"
            result_text = f"""Низкая мотивация к успеху (от 1 до 10 баллов)

Сумма набранных баллов: {total_score}

У вас наблюдается низкий уровень мотивации к успеху. 
Возможно, вы избегаете ситуаций, где нужно проявлять инициативу 
и брать на себя ответственность. Рекомендуется работать над 
повышением уверенности в себе и постановкой достижимых целей."""
        
        elif 11 <= total_score <= 16:
            level = "средняя"
            result_text = f"""Средний уровень мотивации к успеху (от 11 до 16 баллов)

Сумма набранных баллов: {total_score}

У вас средний уровень мотивации к успеху. Вы стремитесь к 
достижениям, но при этом сохраняете разумный подход к риску. 
Это оптимальный уровень для большинства видов деятельности."""
        
        elif 17 <= total_score <= 20:
            level = "умеренно высокая"
            result_text = f"""Умеренно высокий уровень мотивации к успеху (от 17 до 20 баллов)

Сумма набранных баллов: {total_score}

У вас высокий уровень мотивации к успеху. Вы активно стремитесь 
к достижениям, готовы прилагать значительные усилия для 
получения результата. Важно следить за балансом между работой и отдыхом."""
        
        elif total_score >= 21:
            level = "слишком высокая"
            result_text = f"""Слишком высокий уровень мотивации к успеху (свыше 21 балла)

Сумма набранных баллов: {total_score}

У вас чрезмерно высокий уровень мотивации к успеху. Это может 
приводить к излишнему стрессу, выгоранию и неспособности 
адекватно оценивать риски. Рекомендуется научиться принимать 
неудачи и снизить требования к себе."""
        
        else:  # total_score < 1
            level = "неопределена"
            result_text = f"""Результат не может быть определён однозначно

Сумма набранных баллов: {total_score}

Возможно, вы ответили не на все вопросы или допустили ошибку 
при заполнении теста. Пожалуйста, пройдите тест заново."""
        
        self.logger.info("Motivation level determined: %s (score: %d)", level, total_score)

        # Формируем результат в виде JSON
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

        self.logger.info("PersonalityToSuccess test analysis completed, result sent")
        return ScResult.OK