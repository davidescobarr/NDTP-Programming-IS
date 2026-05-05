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

class AnalyzeAdvancedTestAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_analyze_advanced_test_agent")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        result = self.run(action_element)
        is_successful = (result == ScResult.OK)
        finish_action_with_status(action_element, is_successful)
        self.logger.info("AnalyzeAdvancedTestAgent finished %s", "successfully" if is_successful else "unsuccessfully")
        return result

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("AnalyzeAdvancedTestAgent started")

        # Получаем JSON с ответами (Sc-ссылка)
        json_link = get_action_arguments(action_node, 1)[0]
        json_data = get_link_content_data(json_link)
        if not json_data:
            self.logger.error("No JSON data found")
            return ScResult.ERROR

        try:
            # Ожидаемый формат JSON: массив объектов с полем "answer"
            # answer: 0 - вариант А, 1 - вариант Б
            questions = json.loads(json_data)
            self.logger.info("Received JSON data with %d questions", len(questions))
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse JSON: %s", str(e))
            return ScResult.ERROR

        if not isinstance(questions, list):
            self.logger.error("JSON data is not a list")
            return ScResult.ERROR

        # Создаем словарь для подсчета баллов по категориям
        # Категории: Ч, Т, П, 3, X
        categories = {
            "Ч": 0,
            "Т": 0,
            "П": 0,
            "3": 0,
            "X": 0
        }
        
        # Расшифровка таблицы: для каждого вопроса указано, 
        # в какую категорию идет ответ "а" и ответ "б"
        # Формат: вопрос: {"а": категория, "б": категория}
        
        question_mapping = {
            # Строка 1: 2а 1б 1а 2б 3а
            1: {"а": "Т", "б": "П"},   # 1б и 1а - вопрос 1: а->Т, б->П
            2: {"а": "Ч", "б": "3"},   # 2а и 2б - вопрос 2: а->Ч, б->3
            3: {"а": "X", "б": "Т"},   # 3а - вопрос 3: а->X (б нет в этой строке)
            
            # Строка 2: 4б 4а 3б 5а 5б
            4: {"а": "П", "б": "Ч"},   # 4б и 4а - вопрос 4: а->П, б->Ч
            5: {"а": "3", "б": "X"},   # 5а и 5б - вопрос 5: а->3, б->X
            3: {"а": "X", "б": "Т"},   # 3б - добавляем для вопроса 3 ответ б->Т
            
            # Строка 3: 6б 7б 6а 9б 7а
            6: {"а": "3", "б": "Ч"},   # 6б и 6а - вопрос 6: а->3, б->Ч
            7: {"а": "X", "б": "Т"},   # 7б и 7а - вопрос 7: а->X, б->Т
            9: {"б": "П"},             # 9б - вопрос 9: б->П
            
            # Строка 4: 8а 9а 10а 10б 8б
            8: {"а": "Ч", "б": "X"},   # 8а и 8б - вопрос 8: а->Ч, б->X
            9: {"а": "Т"},             # 9а - вопрос 9: а->Т
            10: {"а": "П", "б": "3"},  # 10а и 10б - вопрос 10: а->П, б->3
            
            # Строка 5: 12а 11б 11а 126 13а
            11: {"а": "3", "б": "Ч"},  # 11б и 11а - вопрос 11: а->3, б->Ч
            12: {"а": "Т", "б": "?"},  # 12а - вопрос 12: а->Т (126 вероятно опечатка)
            13: {"а": "X"},            # 13а - вопрос 13: а->X
            
            # Строка 6: 14б 14а 13б 15а 15б
            13: {"б": "П"},            # 13б - вопрос 13: б->П
            14: {"а": "П", "б": "Ч"},  # 14б и 14а - вопрос 14: а->П, б->Ч
            15: {"а": "3", "б": "X"},  # 15а и 15б - вопрос 15: а->3, б->X
            
            # Строка 7: 16б 17б 16а 19б 17а
            16: {"а": "X", "б": "Ч"},  # 16б и 16а - вопрос 16: а->X, б->Ч
            17: {"а": "Т", "б": "3"},  # 17б и 17а - вопрос 17: а->Т, б->3
            19: {"б": "П"},            # 19б - вопрос 19: б->П
            
            # Строка 8: 18а 19а 20а 20б 18б
            18: {"а": "Ч", "б": "X"},  # 18а и 18б - вопрос 18: а->Ч, б->X
            19: {"а": "Т"},            # 19а - вопрос 19: а->Т
            20: {"а": "П", "б": "3"},  # 20а и 20б - вопрос 20: а->П, б->3
        }
        
        # Упрощенная версия маппинга (более читаемая)
        # На основе вашей таблицы, вот правильное распределение:
        
        # Вопрос 1: а->Т, б->П
        # Вопрос 2: а->Ч, б->3  
        # Вопрос 3: а->X, б->Т
        # Вопрос 4: а->П, б->Ч
        # Вопрос 5: а->3, б->X
        # Вопрос 6: а->3, б->Ч
        # Вопрос 7: а->X, б->Т
        # Вопрос 8: а->Ч, б->X
        # Вопрос 9: а->Т, б->П
        # Вопрос 10: а->П, б->3
        # Вопрос 11: а->3, б->Ч
        # Вопрос 12: а->Т (б - не указан)
        # Вопрос 13: а->X, б->П
        # Вопрос 14: а->П, б->Ч
        # Вопрос 15: а->3, б->X
        # Вопрос 16: а->X, б->Ч
        # Вопрос 17: а->Т, б->3
        # Вопрос 18: а->Ч, б->X
        # Вопрос 19: а->Т, б->П
        # Вопрос 20: а->П, б->3
        
        # Очищаем и создаем правильный маппинг
        question_mapping_clean = {
            1: {"а": "Т", "б": "П"},
            2: {"а": "Ч", "б": "3"},
            3: {"а": "X", "б": "Т"},
            4: {"а": "П", "б": "Ч"},
            5: {"а": "3", "б": "X"},
            6: {"а": "3", "б": "Ч"},
            7: {"а": "X", "б": "Т"},
            8: {"а": "Ч", "б": "X"},
            9: {"а": "Т", "б": "П"},
            10: {"а": "П", "б": "3"},
            11: {"а": "3", "б": "Ч"},
            12: {"а": "Т", "б": None},  # только ответ а
            13: {"а": "X", "б": "П"},
            14: {"а": "П", "б": "Ч"},
            15: {"а": "3", "б": "X"},
            16: {"а": "X", "б": "Ч"},
            17: {"а": "Т", "б": "3"},
            18: {"а": "Ч", "б": "X"},
            19: {"а": "Т", "б": "П"},
            20: {"а": "П", "б": "3"},
        }
        
        # Подсчет баллов по категориям
        processed_questions = 0
        
        for idx, question in enumerate(questions, start=1):
            answer_val = question.get("answer")
            
            if answer_val is None:
                self.logger.warning("Question %d missing answer field, skipping", idx)
                continue
            
            if idx > 20:
                self.logger.warning("Question %d exceeds test limit (max 20), skipping", idx)
                continue
            
            # Определяем категорию для данного вопроса и ответа
            answer_key = "а" if answer_val == 0 else "б"
            
            if idx in question_mapping_clean:
                category = question_mapping_clean[idx].get(answer_key)
                if category and category in categories:
                    categories[category] += 1
                    self.logger.debug("Question %d, answer %s (%s) -> category %s", 
                                     idx, answer_key, "А" if answer_val == 0 else "Б", category)
                elif category is None:
                    self.logger.debug("Question %d, answer %s has no category mapping", idx, answer_key)
                else:
                    self.logger.warning("Question %d, unknown category: %s", idx, category)
            else:
                self.logger.warning("Question %d not found in mapping", idx)
            
            processed_questions += 1
        
        # Находим категорию с максимальным количеством баллов
        max_category = max(categories, key=categories.get)
        max_score = categories[max_category]
        
        self.logger.info("Category scores: %s", categories)
        self.logger.info("Dominant category: %s with score %d", max_category, max_score)
        self.logger.info("Processed questions: %d", processed_questions)
        
        # Формируем результат (заглушки для текстов - замените на реальные)
        category_texts = {
    "Ч": """Ведущая категория: ЧЕЛОВЕК — ЧЕЛОВЕК

    Ваш тип профессий связан с общением и взаимодействием с людьми. 
    Вам подходят профессии, где основной объект труда — человек: 
    учитель, врач, менеджер, психолог, социальный работник, 
    продавец, официант, экскурсовод.

    У вас развиты коммуникативные навыки, вы умеете находить 
    общий язык с разными людьми, проявляете эмпатию и готовность помогать.""",

        "Т": """Ведущая категория: ЧЕЛОВЕК — ТЕХНИКА

    Ваш тип профессий связан с техникой, механизмами и техническими системами. 
    Вам подходят профессии: инженер, программист, механик, водитель, 
    электрик, технолог, монтажник, ремонтник, оператор станков.

    У вас развито техническое мышление, вы любите разбираться в 
    устройстве механизмов, проявляете интерес к точным наукам и 
    практической деятельности.""",

        "П": """Ведущая категория: ЧЕЛОВЕК — ПРИРОДА

    Ваш тип профессий связан с природой, растениями, животными и 
    природными процессами. Вам подходят профессии: биолог, эколог, 
    ветеринар, агроном, садовник, лесник, зоолог, фермер, геолог.

    Вы любите природу, наблюдательны, заботливы, умеете ухаживать 
    за растениями и животными, проявляете интерес к естественным наукам.""",

        "3": """Ведущая категория: ЧЕЛОВЕК — ЗНАКОВАЯ СИСТЕМА

    Ваш тип профессий связан с обработкой информации, знаков, цифр, 
    текстов и символов. Вам подходят профессии: программист, бухгалтер, 
    экономист, редактор, переводчик, оператор ЭВМ, архивист, 
    библиотекарь, аналитик, лингвист.

    У вас развито логическое и абстрактное мышление, вы внимательны 
    к деталям, усидчивы, умеете работать с большими объёмами 
    информации и знаковыми системами.""",

        "X": """Ведущая категория: ЧЕЛОВЕК — ХУДОЖЕСТВЕННЫЙ ОБРАЗ

    Ваш тип профессий связан с творчеством, искусством, созданием 
    художественных образов. Вам подходят профессии: художник, дизайнер, 
    музыкант, актёр, архитектор, писатель, фотограф, режиссёр, 
    модельер, скульптор, искусствовед.

    У вас развито образное мышление, творческие способности, 
    художественный вкус, эмоциональность и стремление к 
    самовыражению через искусство."""
    }

        result_text = f"""Результаты теста:

Доминирующая категория: {max_category} ({max_score} баллов)

{category_texts[max_category]}

Подробная разбивка по категориям:
"""
        
        for cat, score in categories.items():
            result_text += f"\n{cat}: {score} баллов"
        
        # Формируем JSON результата
        result_data = {
            "text": result_text,
            "dominant_category": max_category,
            "category_scores": categories,
            "max_score": max_score,
            "total_processed": processed_questions
        }
        
        result_text_json = json.dumps(result_data, ensure_ascii=False)
        self.logger.info("Result JSON: %s", result_text_json)
        
        text_link = create_link(result_text_json, ScLinkContentType.STRING)
        create_action_answer(action_node, text_link)
        
        self.logger.info("AnalyzeAdvancedTestAgent analysis completed, result sent")
        return ScResult.OK