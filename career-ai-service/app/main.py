import math
import os
import random
from typing import Any, Dict, List, Optional, Set, Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


MIN_QUESTIONS = 10
MAX_QUESTIONS = 15

DIMENSIONS = [
    {"key": "practical", "label": "Практика"},
    {"key": "analytical", "label": "Аналитика"},
    {"key": "social", "label": "Люди"},
    {"key": "creative", "label": "Творчество"},
    {"key": "enterprising", "label": "Управление"},
    {"key": "conventional", "label": "Система"},
    {"key": "digital", "label": "Цифровые технологии"},
    {"key": "science", "label": "Исследования"},
    {"key": "care", "label": "Помощь"},
    {"key": "risk", "label": "Динамика"},
    {"key": "autonomy", "label": "Самостоятельность"},
    {"key": "learning", "label": "Развитие"},
]

DIMENSION_KEYS = [item["key"] for item in DIMENSIONS]
DIMENSION_LABELS = {item["key"]: item["label"] for item in DIMENSIONS}


PROFESSIONS = [
    {
        "id": "software_engineer",
        "name": "программист-разработчик",
        "description": "Подходит профиль, где важны логика, цифровая среда, самостоятельное решение задач и регулярное развитие.",
        "vector": {"practical": 52, "analytical": 86, "social": 36, "creative": 58, "enterprising": 42, "conventional": 62, "digital": 96, "science": 62, "care": 28, "risk": 28, "autonomy": 78, "learning": 88},
        "education": "информатика, программная инженерия, прикладная математика, системный анализ",
        "risk": "важно проверить терпимость к долгой отладке и работе с абстрактными задачами",
    },
    {
        "id": "data_analyst",
        "name": "data-аналитик",
        "description": "Сильная зона - числа, причинно-следственные связи, аккуратные выводы и объяснение данных бизнесу.",
        "vector": {"practical": 38, "analytical": 94, "social": 46, "creative": 42, "enterprising": 52, "conventional": 76, "digital": 88, "science": 76, "care": 26, "risk": 22, "autonomy": 66, "learning": 82},
        "education": "статистика, бизнес-информатика, экономика, прикладная математика",
        "risk": "профессия требует аккуратности и готовности перепроверять гипотезы",
    },
    {
        "id": "cybersecurity",
        "name": "специалист по кибербезопасности",
        "description": "Подходит сочетание аналитики, цифровых технологий, системности и спокойной работы с риском.",
        "vector": {"practical": 58, "analytical": 88, "social": 34, "creative": 48, "enterprising": 44, "conventional": 78, "digital": 96, "science": 62, "care": 32, "risk": 66, "autonomy": 72, "learning": 90},
        "education": "информационная безопасность, компьютерные сети, системное администрирование",
        "risk": "нужно быть готовым к постоянному обновлению угроз и инструментов",
    },
    {
        "id": "engineer",
        "name": "инженер-разработчик",
        "description": "Профиль тянется к технике, расчетам, прототипам и прикладному результату.",
        "vector": {"practical": 88, "analytical": 82, "social": 32, "creative": 56, "enterprising": 38, "conventional": 72, "digital": 62, "science": 76, "care": 22, "risk": 42, "autonomy": 64, "learning": 80},
        "education": "машиностроение, электроника, робототехника, промышленный дизайн",
        "risk": "стоит заранее понять, интересны ли расчеты и техническая документация",
    },
    {
        "id": "doctor",
        "name": "врач",
        "description": "Ведущие признаки - помощь людям, естественно-научное мышление, ответственность и устойчивость к нагрузке.",
        "vector": {"practical": 62, "analytical": 76, "social": 76, "creative": 26, "enterprising": 42, "conventional": 82, "digital": 36, "science": 88, "care": 96, "risk": 64, "autonomy": 48, "learning": 92},
        "education": "лечебное дело, педиатрия, стоматология, медико-биологические направления",
        "risk": "высокая цена ошибки и длинная образовательная траектория",
    },
    {
        "id": "psychologist",
        "name": "психолог-консультант",
        "description": "Подходит ориентация на людей, внимательное слушание, этичную помощь и работу с мотивацией.",
        "vector": {"practical": 28, "analytical": 64, "social": 94, "creative": 48, "enterprising": 40, "conventional": 54, "digital": 24, "science": 58, "care": 92, "risk": 28, "autonomy": 62, "learning": 84},
        "education": "психология, педагогика, социальная работа, консультирование",
        "risk": "важны личные границы и готовность к эмоционально сложным темам",
    },
    {
        "id": "teacher",
        "name": "преподаватель",
        "description": "Профиль показывает склонность объяснять, структурировать знания и поддерживать развитие других.",
        "vector": {"practical": 34, "analytical": 62, "social": 92, "creative": 56, "enterprising": 54, "conventional": 66, "digital": 40, "science": 56, "care": 82, "risk": 24, "autonomy": 58, "learning": 86},
        "education": "педагогика, предметное образование, методика преподавания, EdTech",
        "risk": "нужно принять регулярную коммуникацию и работу с разным уровнем мотивации учеников",
    },
    {
        "id": "ux_designer",
        "name": "UX/UI-дизайнер",
        "description": "Сильное сочетание творчества, цифровой среды, эмпатии к пользователю и прикладного результата.",
        "vector": {"practical": 44, "analytical": 64, "social": 66, "creative": 92, "enterprising": 48, "conventional": 48, "digital": 82, "science": 34, "care": 58, "risk": 28, "autonomy": 72, "learning": 78},
        "education": "дизайн, HCI, веб-разработка, продуктовый дизайн",
        "risk": "понадобится защищать решения аргументами, а не только вкусом",
    },
    {
        "id": "architect",
        "name": "архитектор",
        "description": "Подходит баланс эстетики, пространственного мышления, технических ограничений и проектной работы.",
        "vector": {"practical": 70, "analytical": 68, "social": 46, "creative": 94, "enterprising": 44, "conventional": 72, "digital": 56, "science": 44, "care": 32, "risk": 32, "autonomy": 66, "learning": 72},
        "education": "архитектура, градостроительство, дизайн среды, BIM-проектирование",
        "risk": "нужно выдерживать длительные проекты и много правок",
    },
    {
        "id": "marketer",
        "name": "маркетолог",
        "description": "Профиль указывает на интерес к людям, идеям, коммуникации, аналитике рынка и влиянию на выбор.",
        "vector": {"practical": 28, "analytical": 62, "social": 78, "creative": 76, "enterprising": 82, "conventional": 42, "digital": 68, "science": 28, "care": 36, "risk": 48, "autonomy": 64, "learning": 72},
        "education": "маркетинг, реклама, коммуникации, бизнес-аналитика",
        "risk": "результаты часто зависят от рынка, гипотез и быстрых изменений",
    },
    {
        "id": "product_manager",
        "name": "продуктовый менеджер",
        "description": "Подходит роль на стыке пользователей, бизнеса, команды разработки и принятия решений.",
        "vector": {"practical": 42, "analytical": 76, "social": 78, "creative": 64, "enterprising": 92, "conventional": 58, "digital": 78, "science": 34, "care": 42, "risk": 58, "autonomy": 76, "learning": 84},
        "education": "бизнес-информатика, менеджмент, системный анализ, предпринимательство",
        "risk": "много неопределенности, переговоров и ответственности без прямого контроля над всеми деталями",
    },
    {
        "id": "project_manager",
        "name": "менеджер проекта",
        "description": "Профиль показывает склонность организовывать людей, сроки, ресурсы и доводить результат до конца.",
        "vector": {"practical": 46, "analytical": 62, "social": 78, "creative": 38, "enterprising": 90, "conventional": 78, "digital": 48, "science": 22, "care": 42, "risk": 52, "autonomy": 66, "learning": 70},
        "education": "менеджмент, управление проектами, экономика, IT-менеджмент",
        "risk": "часто придется решать конфликты и держать несколько потоков задач одновременно",
    },
    {
        "id": "entrepreneur",
        "name": "предприниматель",
        "description": "Выражены инициативность, самостоятельность, готовность к риску и интерес к созданию ценности.",
        "vector": {"practical": 52, "analytical": 58, "social": 72, "creative": 70, "enterprising": 98, "conventional": 36, "digital": 56, "science": 24, "care": 34, "risk": 86, "autonomy": 94, "learning": 82},
        "education": "предпринимательство, экономика, продуктовый менеджмент, маркетинг",
        "risk": "высокая неопределенность дохода и необходимость быстро учиться на ошибках",
    },
    {
        "id": "financial_analyst",
        "name": "финансовый аналитик",
        "description": "Подходит системная работа с числами, прогнозами, рисками и экономической логикой.",
        "vector": {"practical": 28, "analytical": 88, "social": 38, "creative": 24, "enterprising": 60, "conventional": 92, "digital": 66, "science": 52, "care": 18, "risk": 42, "autonomy": 58, "learning": 76},
        "education": "финансы, экономика, прикладная математика, бизнес-аналитика",
        "risk": "работа требует внимательности к деталям и устойчивости к монотонным проверкам",
    },
    {
        "id": "lawyer",
        "name": "юрист",
        "description": "Профиль близок к нормам, аргументации, защите позиции, документам и точности формулировок.",
        "vector": {"practical": 26, "analytical": 76, "social": 68, "creative": 34, "enterprising": 66, "conventional": 94, "digital": 26, "science": 28, "care": 46, "risk": 42, "autonomy": 60, "learning": 72},
        "education": "юриспруденция, международное право, правовое обеспечение бизнеса",
        "risk": "много текста, процедур и ответственности за точность позиции",
    },
    {
        "id": "journalist",
        "name": "журналист или медиаредактор",
        "description": "Сильны коммуникация, интерес к событиям, текстам, людям и быстрой упаковке смыслов.",
        "vector": {"practical": 24, "analytical": 58, "social": 82, "creative": 86, "enterprising": 58, "conventional": 36, "digital": 58, "science": 24, "care": 42, "risk": 62, "autonomy": 78, "learning": 76},
        "education": "журналистика, филология, медиакоммуникации, редактура",
        "risk": "нужно выдерживать дедлайны, публичность и большой поток информации",
    },
    {
        "id": "researcher",
        "name": "исследователь",
        "description": "Профиль тяготеет к гипотезам, глубокой аналитике, экспериментам и поиску новых знаний.",
        "vector": {"practical": 42, "analytical": 96, "social": 30, "creative": 56, "enterprising": 28, "conventional": 68, "digital": 58, "science": 98, "care": 26, "risk": 28, "autonomy": 82, "learning": 96},
        "education": "естественные науки, математика, инженерные науки, академическая магистратура",
        "risk": "результат может быть небыстрым, а путь требует терпения к неопределенности",
    },
    {
        "id": "hr_specialist",
        "name": "HR-специалист",
        "description": "Подходит работа с людьми, оценкой, развитием команды, переговорами и организацией процессов.",
        "vector": {"practical": 24, "analytical": 54, "social": 92, "creative": 46, "enterprising": 70, "conventional": 66, "digital": 38, "science": 24, "care": 72, "risk": 34, "autonomy": 58, "learning": 72},
        "education": "управление персоналом, психология, менеджмент, организационное развитие",
        "risk": "много эмоциональных ситуаций и несовпадения интересов людей",
    },
    {
        "id": "logistics",
        "name": "логист",
        "description": "Сильна ориентация на системы, маршруты, ресурсы, сроки и практическую оптимизацию.",
        "vector": {"practical": 66, "analytical": 72, "social": 46, "creative": 24, "enterprising": 60, "conventional": 86, "digital": 48, "science": 32, "care": 22, "risk": 44, "autonomy": 52, "learning": 58},
        "education": "логистика, транспортные системы, экономика, управление цепями поставок",
        "risk": "часто придется быстро реагировать на сбои и ограничения",
    },
    {
        "id": "industrial_designer",
        "name": "промышленный дизайнер",
        "description": "Подходит создание предметов на стыке эстетики, технологии, удобства и производства.",
        "vector": {"practical": 72, "analytical": 58, "social": 44, "creative": 94, "enterprising": 38, "conventional": 54, "digital": 62, "science": 36, "care": 36, "risk": 28, "autonomy": 70, "learning": 72},
        "education": "промышленный дизайн, инженерный дизайн, CAD, материаловедение",
        "risk": "идеи нужно регулярно проверять ограничениями производства и стоимости",
    },
    {
        "id": "robotics_engineer",
        "name": "инженер-робототехник",
        "description": "Профиль соединяет практику, код, механику, электронику, исследование и любовь к сложным системам.",
        "vector": {"practical": 88, "analytical": 86, "social": 28, "creative": 58, "enterprising": 36, "conventional": 68, "digital": 88, "science": 82, "care": 22, "risk": 36, "autonomy": 72, "learning": 92},
        "education": "робототехника, мехатроника, электроника, программирование встроенных систем",
        "risk": "порог входа выше среднего: понадобится математика, физика и терпение к прототипам",
    },
    {
        "id": "biotechnologist",
        "name": "биотехнолог",
        "description": "Подходит интерес к естественным наукам, лабораторной работе, точности и прикладным исследованиям.",
        "vector": {"practical": 62, "analytical": 82, "social": 28, "creative": 42, "enterprising": 28, "conventional": 78, "digital": 38, "science": 96, "care": 44, "risk": 32, "autonomy": 58, "learning": 88},
        "education": "биотехнология, биология, химия, фармацевтика, лабораторная диагностика",
        "risk": "много регламентов, лабораторной дисциплины и постепенного накопления результата",
    },
    {
        "id": "rescue_specialist",
        "name": "специалист службы спасения",
        "description": "Выражены практичность, готовность к динамике, помощь людям и способность действовать под давлением.",
        "vector": {"practical": 86, "analytical": 50, "social": 68, "creative": 20, "enterprising": 54, "conventional": 66, "digital": 24, "science": 34, "care": 84, "risk": 96, "autonomy": 48, "learning": 68},
        "education": "безопасность жизнедеятельности, медицина катастроф, пожарная безопасность, физическая подготовка",
        "risk": "высокие физические и эмоциональные нагрузки",
    },
    {
        "id": "accountant",
        "name": "бухгалтер",
        "description": "Подходит аккуратная, регламентированная работа с документами, цифрами и стабильными процедурами.",
        "vector": {"practical": 24, "analytical": 68, "social": 26, "creative": 12, "enterprising": 34, "conventional": 98, "digital": 48, "science": 24, "care": 16, "risk": 12, "autonomy": 42, "learning": 54},
        "education": "бухгалтерский учет, экономика, финансы, налоговое администрирование",
        "risk": "важно нормально относиться к повторяемости, отчетности и жестким срокам",
    },
    {
        "id": "qa_engineer",
        "name": "QA-инженер",
        "description": "Подходит внимательность к деталям, системность, цифровая среда и желание находить слабые места продукта.",
        "vector": {"practical": 50, "analytical": 78, "social": 38, "creative": 34, "enterprising": 34, "conventional": 86, "digital": 88, "science": 42, "care": 24, "risk": 28, "autonomy": 62, "learning": 78},
        "education": "тестирование ПО, информатика, системный анализ, автоматизация тестирования",
        "risk": "часть работы может быть повторяемой, зато требует точности и терпения",
    },
    {
        "id": "devops_engineer",
        "name": "DevOps-инженер",
        "description": "Сильное совпадение с инфраструктурой, автоматизацией, надежностью систем и практическим решением инцидентов.",
        "vector": {"practical": 70, "analytical": 82, "social": 38, "creative": 42, "enterprising": 46, "conventional": 82, "digital": 96, "science": 48, "care": 24, "risk": 62, "autonomy": 72, "learning": 88},
        "education": "системное администрирование, облачные технологии, сети, программирование",
        "risk": "возможны срочные инциденты и ответственность за стабильность сервисов",
    },
    {
        "id": "game_designer",
        "name": "геймдизайнер",
        "description": "Подходит сочетание творчества, логики систем, понимания людей и цифровых продуктов.",
        "vector": {"practical": 36, "analytical": 68, "social": 58, "creative": 94, "enterprising": 54, "conventional": 36, "digital": 82, "science": 28, "care": 34, "risk": 48, "autonomy": 78, "learning": 80},
        "education": "геймдизайн, интерактивные медиа, программирование, сценарное мастерство",
        "risk": "идеи нужно постоянно проверять балансом, аналитикой и обратной связью игроков",
    },
    {
        "id": "system_administrator",
        "name": "системный администратор",
        "description": "Профиль близок к практической цифровой инфраструктуре, стабильности, настройке и поддержке систем.",
        "vector": {"practical": 76, "analytical": 70, "social": 42, "creative": 24, "enterprising": 34, "conventional": 84, "digital": 92, "science": 32, "care": 40, "risk": 44, "autonomy": 58, "learning": 74},
        "education": "компьютерные сети, администрирование ОС, информационные системы",
        "risk": "часто нужно быстро помогать пользователям и реагировать на технические сбои",
    },
    {
        "id": "civil_engineer",
        "name": "инженер-строитель",
        "description": "Подходит практическое мышление, расчеты, нормативы, работа с объектами и материальным результатом.",
        "vector": {"practical": 90, "analytical": 74, "social": 42, "creative": 42, "enterprising": 46, "conventional": 88, "digital": 42, "science": 54, "care": 24, "risk": 46, "autonomy": 52, "learning": 66},
        "education": "строительство, проектирование зданий, геодезия, строительные материалы",
        "risk": "высокая ответственность за безопасность, сроки и соблюдение норм",
    },
    {
        "id": "ecologist",
        "name": "эколог",
        "description": "Подходит интерес к природе, исследованиям, общественной пользе и работе с данными о среде.",
        "vector": {"practical": 56, "analytical": 72, "social": 50, "creative": 32, "enterprising": 32, "conventional": 68, "digital": 38, "science": 92, "care": 66, "risk": 34, "autonomy": 58, "learning": 82},
        "education": "экология, природопользование, биология, география, экологический мониторинг",
        "risk": "часть работы связана с отчетностью, полевыми выездами и долгими наблюдениями",
    },
    {
        "id": "pharmacist",
        "name": "фармацевт",
        "description": "Профиль соединяет естественные науки, помощь людям, точность и регламентированную ответственность.",
        "vector": {"practical": 54, "analytical": 70, "social": 64, "creative": 18, "enterprising": 36, "conventional": 90, "digital": 30, "science": 86, "care": 82, "risk": 34, "autonomy": 42, "learning": 78},
        "education": "фармация, химия, биология, фармакология",
        "risk": "нужна высокая точность и готовность работать с регламентами и ответственностью",
    },
    {
        "id": "translator",
        "name": "переводчик",
        "description": "Подходит внимательность к смыслу, языку, текстам, культурам и самостоятельной интеллектуальной работе.",
        "vector": {"practical": 18, "analytical": 66, "social": 56, "creative": 74, "enterprising": 28, "conventional": 70, "digital": 36, "science": 24, "care": 34, "risk": 18, "autonomy": 76, "learning": 86},
        "education": "лингвистика, переводоведение, филология, межкультурная коммуникация",
        "risk": "рынок требует специализации, высокой грамотности и постоянного развития словаря",
    },
    {
        "id": "sales_manager",
        "name": "менеджер по продажам",
        "description": "Подходит активная коммуникация, переговоры, влияние, ориентация на результат и динамичный темп.",
        "vector": {"practical": 28, "analytical": 44, "social": 88, "creative": 48, "enterprising": 94, "conventional": 38, "digital": 36, "science": 12, "care": 32, "risk": 66, "autonomy": 64, "learning": 58},
        "education": "маркетинг, менеджмент, продажи, коммуникации, экономика",
        "risk": "доход и результат часто зависят от отказов, переговоров и рыночной ситуации",
    },
    {
        "id": "smm_specialist",
        "name": "SMM-специалист",
        "description": "Подходит работа на стыке контента, аналитики аудитории, визуальной подачи и быстрых цифровых каналов.",
        "vector": {"practical": 24, "analytical": 54, "social": 76, "creative": 88, "enterprising": 68, "conventional": 34, "digital": 78, "science": 18, "care": 32, "risk": 54, "autonomy": 72, "learning": 72},
        "education": "медиакоммуникации, маркетинг, контент-менеджмент, аналитика социальных сетей",
        "risk": "нужно быстро реагировать на тренды, обратную связь и изменения площадок",
    },
    {
        "id": "operations_manager",
        "name": "операционный менеджер",
        "description": "Подходит системное мышление, управление процессами, контроль качества, сроки и оптимизация ресурсов.",
        "vector": {"practical": 58, "analytical": 72, "social": 62, "creative": 28, "enterprising": 80, "conventional": 88, "digital": 50, "science": 24, "care": 28, "risk": 44, "autonomy": 60, "learning": 64},
        "education": "операционный менеджмент, экономика, логистика, управление процессами",
        "risk": "много координации, контроля и ответственности за сбои в процессах",
    },
    {
        "id": "event_manager",
        "name": "event-менеджер",
        "description": "Профиль близок к организации событий, коммуникации, креативной подаче и работе в динамике.",
        "vector": {"practical": 46, "analytical": 46, "social": 86, "creative": 76, "enterprising": 86, "conventional": 58, "digital": 34, "science": 12, "care": 42, "risk": 74, "autonomy": 62, "learning": 56},
        "education": "ивент-менеджмент, коммуникации, маркетинг, продюсирование мероприятий",
        "risk": "много дедлайнов, подрядчиков и непредвиденных ситуаций в день события",
    },
    {
        "id": "video_editor",
        "name": "видеомонтажер",
        "description": "Подходит визуальное мышление, цифровые инструменты, чувство ритма и самостоятельная проектная работа.",
        "vector": {"practical": 42, "analytical": 42, "social": 32, "creative": 92, "enterprising": 28, "conventional": 42, "digital": 84, "science": 12, "care": 18, "risk": 28, "autonomy": 78, "learning": 70},
        "education": "медиапроизводство, монтаж, режиссура, motion design, цифровой контент",
        "risk": "важно выдерживать правки, сроки и много часов за монтажной программой",
    },
    {
        "id": "social_worker",
        "name": "специалист по социальной работе",
        "description": "Подходит устойчивое желание помогать людям, решать жизненные ситуации и работать в системе поддержки.",
        "vector": {"practical": 40, "analytical": 48, "social": 92, "creative": 28, "enterprising": 42, "conventional": 68, "digital": 20, "science": 24, "care": 96, "risk": 42, "autonomy": 44, "learning": 68},
        "education": "социальная работа, психология, педагогика, социальная политика",
        "risk": "возможна эмоциональная нагрузка и необходимость работать с ограниченными ресурсами",
    },
    {
        "id": "veterinarian",
        "name": "ветеринар",
        "description": "Подходит сочетание естественных наук, практики, заботы и ответственности за здоровье животных.",
        "vector": {"practical": 72, "analytical": 68, "social": 46, "creative": 18, "enterprising": 32, "conventional": 78, "digital": 18, "science": 88, "care": 86, "risk": 56, "autonomy": 46, "learning": 84},
        "education": "ветеринария, биология, зоотехния, лабораторная диагностика",
        "risk": "профессия требует устойчивости к сложным случаям и практической ответственности",
    },
    {
        "id": "interior_designer",
        "name": "дизайнер интерьеров",
        "description": "Подходит визуальная культура, работа с пространством, общение с заказчиком и практическое воплощение идеи.",
        "vector": {"practical": 58, "analytical": 46, "social": 58, "creative": 96, "enterprising": 48, "conventional": 56, "digital": 54, "science": 18, "care": 34, "risk": 28, "autonomy": 72, "learning": 66},
        "education": "дизайн интерьера, архитектурная среда, 3D-визуализация, материаловедение",
        "risk": "нужно учитывать бюджет, ограничения помещения и частые правки заказчика",
    },
    {
        "id": "ml_engineer",
        "name": "инженер машинного обучения",
        "description": "Профиль близок к алгоритмам, экспериментам с моделями, данным, коду и постоянному развитию.",
        "vector": {"practical": 44, "analytical": 96, "social": 30, "creative": 54, "enterprising": 34, "conventional": 64, "digital": 98, "science": 90, "care": 20, "risk": 34, "autonomy": 82, "learning": 96},
        "education": "машинное обучение, прикладная математика, Computer Science, анализ данных",
        "risk": "нужны сильная математика, терпение к экспериментам и готовность постоянно обновлять инструменты",
    },
    {
        "id": "data_engineer",
        "name": "data-инженер",
        "description": "Подходит системная работа с данными, инфраструктурой, надежными пайплайнами и автоматизацией.",
        "vector": {"practical": 58, "analytical": 86, "social": 28, "creative": 32, "enterprising": 36, "conventional": 84, "digital": 96, "science": 58, "care": 18, "risk": 36, "autonomy": 70, "learning": 84},
        "education": "информатика, базы данных, распределенные системы, инженерия данных",
        "risk": "часть задач связана с надежностью, мониторингом и невидимой для пользователя инфраструктурой",
    },
    {
        "id": "frontend_developer",
        "name": "frontend-разработчик",
        "description": "Сильны цифровая среда, визуальное мышление, логика интерфейсов и внимание к пользовательскому опыту.",
        "vector": {"practical": 46, "analytical": 72, "social": 48, "creative": 78, "enterprising": 38, "conventional": 56, "digital": 96, "science": 34, "care": 32, "risk": 24, "autonomy": 76, "learning": 82},
        "education": "веб-разработка, программная инженерия, интерфейсный дизайн",
        "risk": "важно нормально относиться к правкам интерфейса, совместимости браузеров и деталям верстки",
    },
    {
        "id": "backend_developer",
        "name": "backend-разработчик",
        "description": "Подходит логика сервисов, архитектура, базы данных, надежность и самостоятельное решение сложных задач.",
        "vector": {"practical": 50, "analytical": 88, "social": 28, "creative": 42, "enterprising": 34, "conventional": 72, "digital": 98, "science": 56, "care": 18, "risk": 34, "autonomy": 82, "learning": 86},
        "education": "программная инженерия, информатика, базы данных, распределенные системы",
        "risk": "много невидимой пользователю логики, отладки и ответственности за стабильность сервисов",
    },
    {
        "id": "cloud_architect",
        "name": "облачный архитектор",
        "description": "Профиль соединяет цифровую инфраструктуру, системность, архитектурные решения и ответственность за масштабирование.",
        "vector": {"practical": 62, "analytical": 84, "social": 42, "creative": 42, "enterprising": 58, "conventional": 82, "digital": 98, "science": 42, "care": 20, "risk": 58, "autonomy": 74, "learning": 88},
        "education": "облачные технологии, сетевые системы, DevOps, информационные системы",
        "risk": "нужно учитывать стоимость, безопасность, отказоустойчивость и быстрые изменения платформ",
    },
    {
        "id": "network_engineer",
        "name": "сетевой инженер",
        "description": "Подходит практическая работа с цифровой инфраструктурой, схемами, протоколами и надежностью связи.",
        "vector": {"practical": 72, "analytical": 76, "social": 32, "creative": 20, "enterprising": 34, "conventional": 86, "digital": 94, "science": 38, "care": 18, "risk": 46, "autonomy": 58, "learning": 76},
        "education": "компьютерные сети, телекоммуникации, системное администрирование",
        "risk": "часть работы связана с инцидентами, регламентами и точной настройкой оборудования",
    },
    {
        "id": "business_analyst",
        "name": "бизнес-аналитик",
        "description": "Подходит перевод потребностей бизнеса в требования, схемы процессов, аналитику и понятные решения для команды.",
        "vector": {"practical": 36, "analytical": 82, "social": 70, "creative": 44, "enterprising": 68, "conventional": 78, "digital": 64, "science": 28, "care": 34, "risk": 34, "autonomy": 62, "learning": 74},
        "education": "бизнес-информатика, системный анализ, менеджмент, экономика",
        "risk": "нужно много уточнять, документировать и согласовывать интересы разных участников",
    },
    {
        "id": "systems_analyst",
        "name": "системный аналитик",
        "description": "Профиль тяготеет к структуре требований, логике систем, документации и связи бизнеса с разработкой.",
        "vector": {"practical": 34, "analytical": 88, "social": 56, "creative": 36, "enterprising": 52, "conventional": 88, "digital": 82, "science": 36, "care": 24, "risk": 26, "autonomy": 66, "learning": 76},
        "education": "системный анализ, бизнес-информатика, разработка ПО, управление требованиями",
        "risk": "много внимания к деталям, ограничениям и точности формулировок",
    },
    {
        "id": "technical_writer",
        "name": "технический писатель",
        "description": "Подходит работа на стыке технологий, текстов, структуры, обучения пользователей и точности объяснений.",
        "vector": {"practical": 22, "analytical": 72, "social": 48, "creative": 62, "enterprising": 24, "conventional": 86, "digital": 68, "science": 36, "care": 38, "risk": 14, "autonomy": 78, "learning": 82},
        "education": "техническая коммуникация, лингвистика, IT, редактура, документация ПО",
        "risk": "нужно глубоко разбираться в продукте и выдерживать большое количество уточнений",
    },
    {
        "id": "3d_artist",
        "name": "3D-художник",
        "description": "Сильны визуальная форма, цифровые инструменты, пространственное мышление и самостоятельная проектная работа.",
        "vector": {"practical": 50, "analytical": 42, "social": 24, "creative": 98, "enterprising": 26, "conventional": 46, "digital": 88, "science": 18, "care": 16, "risk": 24, "autonomy": 82, "learning": 74},
        "education": "3D-графика, анимация, гейм-арт, визуализация, цифровое искусство",
        "risk": "важны портфолио, терпение к правкам и постоянное освоение новых инструментов",
    },
    {
        "id": "motion_designer",
        "name": "motion-дизайнер",
        "description": "Подходит сочетание визуального вкуса, ритма, цифровых инструментов и умения доносить смысл через движение.",
        "vector": {"practical": 36, "analytical": 38, "social": 34, "creative": 98, "enterprising": 32, "conventional": 38, "digital": 86, "science": 12, "care": 16, "risk": 34, "autonomy": 78, "learning": 72},
        "education": "моушн-дизайн, графический дизайн, видеопроизводство, анимация",
        "risk": "понадобится выдерживать дедлайны, визуальные правки и конкуренцию портфолио",
    },
    {
        "id": "game_developer",
        "name": "разработчик игр",
        "description": "Профиль соединяет код, интерактивные системы, творческие задачи и регулярную проверку результата игроком.",
        "vector": {"practical": 50, "analytical": 82, "social": 36, "creative": 82, "enterprising": 32, "conventional": 48, "digital": 96, "science": 36, "care": 18, "risk": 38, "autonomy": 78, "learning": 86},
        "education": "разработка игр, программирование, компьютерная графика, интерактивные системы",
        "risk": "нужно сочетать творчество с техническими ограничениями, оптимизацией и частыми итерациями",
    },
    {
        "id": "chemist",
        "name": "химик-технолог",
        "description": "Подходит естественно-научное мышление, эксперименты, производство, точность и работа с материалами.",
        "vector": {"practical": 68, "analytical": 82, "social": 22, "creative": 34, "enterprising": 28, "conventional": 84, "digital": 28, "science": 94, "care": 28, "risk": 42, "autonomy": 54, "learning": 82},
        "education": "химическая технология, химия, материаловедение, промышленная безопасность",
        "risk": "важны техника безопасности, регламенты и аккуратность экспериментов",
    },
    {
        "id": "geologist",
        "name": "геолог",
        "description": "Профиль близок к природным системам, полевой работе, анализу данных и практическим исследованиям.",
        "vector": {"practical": 74, "analytical": 76, "social": 26, "creative": 24, "enterprising": 28, "conventional": 64, "digital": 36, "science": 94, "care": 22, "risk": 64, "autonomy": 66, "learning": 78},
        "education": "геология, геофизика, природопользование, горное дело",
        "risk": "возможны выезды, полевые условия и работа с неопределенными данными",
    },
    {
        "id": "laboratory_diagnostician",
        "name": "лабораторный диагност",
        "description": "Подходит точность, биомедицина, лабораторные протоколы и спокойная ответственность за результат анализа.",
        "vector": {"practical": 58, "analytical": 78, "social": 28, "creative": 12, "enterprising": 20, "conventional": 94, "digital": 32, "science": 92, "care": 70, "risk": 34, "autonomy": 42, "learning": 78},
        "education": "лабораторная диагностика, биология, медицина, клиническая лабораторная практика",
        "risk": "требуются высокая внимательность, соблюдение протоколов и ответственность за точность",
    },
    {
        "id": "nurse",
        "name": "медицинская сестра или брат",
        "description": "Профиль выражает практическую помощь людям, устойчивость, заботу и работу по медицинским стандартам.",
        "vector": {"practical": 72, "analytical": 54, "social": 78, "creative": 14, "enterprising": 34, "conventional": 82, "digital": 20, "science": 66, "care": 96, "risk": 62, "autonomy": 34, "learning": 72},
        "education": "сестринское дело, медицинский колледж, клиническая практика",
        "risk": "работа требует эмоциональной устойчивости, сменного графика и точного соблюдения процедур",
    },
    {
        "id": "dentist",
        "name": "стоматолог",
        "description": "Подходит сочетание медицины, точной ручной работы, общения с пациентами и ответственности за качество.",
        "vector": {"practical": 76, "analytical": 72, "social": 62, "creative": 28, "enterprising": 42, "conventional": 84, "digital": 28, "science": 84, "care": 88, "risk": 52, "autonomy": 52, "learning": 84},
        "education": "стоматология, медицинская биология, клиническая практика",
        "risk": "нужны мелкая моторика, выдержка и готовность к длительному обучению",
    },
    {
        "id": "physiotherapist",
        "name": "физиотерапевт или реабилитолог",
        "description": "Профиль подходит для практической помощи людям через восстановление движения, здоровье и регулярный прогресс.",
        "vector": {"practical": 78, "analytical": 58, "social": 78, "creative": 24, "enterprising": 32, "conventional": 70, "digital": 22, "science": 72, "care": 94, "risk": 34, "autonomy": 48, "learning": 78},
        "education": "физическая реабилитация, медицина, кинезиология, адаптивная физическая культура",
        "risk": "нужно терпение к постепенному результату и внимательность к состоянию человека",
    },
    {
        "id": "speech_therapist",
        "name": "логопед",
        "description": "Подходит работа с людьми, речью, обучением, диагностикой и длительным сопровождением прогресса.",
        "vector": {"practical": 36, "analytical": 58, "social": 90, "creative": 52, "enterprising": 28, "conventional": 66, "digital": 22, "science": 44, "care": 90, "risk": 16, "autonomy": 52, "learning": 78},
        "education": "логопедия, дефектология, педагогика, психология развития",
        "risk": "нужны терпение, регулярная практика и готовность работать с разной динамикой прогресса",
    },
    {
        "id": "career_counselor",
        "name": "карьерный консультант",
        "description": "Профиль соединяет работу с людьми, анализ опыта, обучение, поддержку выбора и структурирование решений.",
        "vector": {"practical": 24, "analytical": 64, "social": 92, "creative": 46, "enterprising": 56, "conventional": 58, "digital": 28, "science": 32, "care": 82, "risk": 22, "autonomy": 64, "learning": 82},
        "education": "психология, HR, карьерное консультирование, педагогика, коучинг",
        "risk": "нужны этичность, умение не навязывать выбор и постоянное знание рынка труда",
    },
    {
        "id": "economist",
        "name": "экономист",
        "description": "Подходит системная аналитика, модели, данные, финансы, прогнозы и понимание общественных процессов.",
        "vector": {"practical": 24, "analytical": 88, "social": 38, "creative": 22, "enterprising": 54, "conventional": 88, "digital": 54, "science": 58, "care": 20, "risk": 26, "autonomy": 58, "learning": 74},
        "education": "экономика, финансы, статистика, математические методы в экономике",
        "risk": "работа требует аккуратной интерпретации данных и терпимости к абстрактным моделям",
    },
    {
        "id": "urban_planner",
        "name": "урбанист",
        "description": "Подходит анализ городской среды, общественная польза, проектирование пространств и работа с разными участниками.",
        "vector": {"practical": 48, "analytical": 72, "social": 70, "creative": 66, "enterprising": 48, "conventional": 66, "digital": 46, "science": 52, "care": 60, "risk": 28, "autonomy": 62, "learning": 76},
        "education": "урбанистика, градостроительство, социология города, архитектура, география",
        "risk": "много согласований, долгих проектов и ограничений реальной городской среды",
    },
    {
        "id": "quality_manager",
        "name": "менеджер по качеству",
        "description": "Профиль близок к стандартам, процессам, проверкам, системному улучшению и предотвращению ошибок.",
        "vector": {"practical": 52, "analytical": 72, "social": 42, "creative": 18, "enterprising": 56, "conventional": 96, "digital": 42, "science": 36, "care": 28, "risk": 26, "autonomy": 48, "learning": 66},
        "education": "управление качеством, стандартизация, производственный менеджмент, аудит",
        "risk": "много регламентов, проверок и необходимости убеждать команды соблюдать стандарты",
    },
    {
        "id": "procurement_specialist",
        "name": "специалист по закупкам",
        "description": "Подходит работа с поставщиками, условиями, документами, цифрами, переговорами и сроками.",
        "vector": {"practical": 38, "analytical": 64, "social": 58, "creative": 16, "enterprising": 72, "conventional": 90, "digital": 36, "science": 16, "care": 20, "risk": 42, "autonomy": 46, "learning": 58},
        "education": "логистика, экономика, закупки, управление цепями поставок, юриспруденция",
        "risk": "важны внимательность к условиям, ответственность за сроки и работа с конфликтами интересов",
    },
    {
        "id": "pilot",
        "name": "пилот гражданской авиации",
        "description": "Профиль сочетает практические навыки, регламенты, ответственность, динамику и устойчивость к давлению.",
        "vector": {"practical": 82, "analytical": 70, "social": 42, "creative": 10, "enterprising": 46, "conventional": 96, "digital": 48, "science": 52, "care": 34, "risk": 82, "autonomy": 38, "learning": 82},
        "education": "летная эксплуатация, авиационные системы, аэродинамика, безопасность полетов",
        "risk": "очень высокая цена ошибки, медицинские требования и строгие регламенты",
    },
]


QUESTION_BANK = [
    {
        "id": "q_start_focus",
        "type": "single",
        "text": "Какая рабочая ситуация кажется вам наиболее естественной?",
        "hint": "Выберите один вариант, который ближе по ощущению, а не самый престижный.",
        "stage": "early",
        "options": [
            {"id": "build", "label": "Собрать, настроить или улучшить реальный объект", "weights": {"practical": 0.92, "analytical": 0.55, "conventional": 0.52}},
            {"id": "analyze", "label": "Разобраться в сложной задаче и найти закономерность", "weights": {"analytical": 0.95, "science": 0.76, "autonomy": 0.68}},
            {"id": "people", "label": "Помочь человеку, объяснить или поддержать", "weights": {"social": 0.94, "care": 0.9, "learning": 0.62}},
            {"id": "create", "label": "Придумать визуальное, текстовое или продуктовое решение", "weights": {"creative": 0.94, "digital": 0.58, "autonomy": 0.68}},
            {"id": "lead", "label": "Организовать людей и довести проект до результата", "weights": {"enterprising": 0.95, "social": 0.7, "risk": 0.54}},
        ],
    },
    {
        "id": "q_activities",
        "type": "multi",
        "text": "Какие занятия вы бы выбрали для пробной недели?",
        "hint": "Можно выбрать несколько вариантов.",
        "stage": "early",
        "options": [
            {"id": "code", "label": "Написать программу или автоматизировать процесс", "weights": {"digital": 0.95, "analytical": 0.86, "learning": 0.72}},
            {"id": "lab", "label": "Провести эксперимент или лабораторную проверку", "weights": {"science": 0.94, "analytical": 0.82, "conventional": 0.62}},
            {"id": "interview", "label": "Провести интервью и понять потребности людей", "weights": {"social": 0.86, "care": 0.68, "creative": 0.52}},
            {"id": "layout", "label": "Собрать макет, чертеж, схему или прототип", "weights": {"practical": 0.84, "creative": 0.74, "digital": 0.58}},
            {"id": "budget", "label": "Рассчитать бюджет, план и риски", "weights": {"conventional": 0.9, "analytical": 0.74, "enterprising": 0.62}},
            {"id": "pitch", "label": "Представить идею и убедить команду", "weights": {"enterprising": 0.88, "social": 0.72, "creative": 0.64}},
        ],
    },
    {
        "id": "q_people_scale",
        "type": "scale",
        "text": "Насколько вам комфортно, когда работа почти каждый день строится вокруг общения с людьми?",
        "hint": "1 - лучше минимум общения, 100 - общение заряжает и помогает работать.",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Минимум общения",
        "rightLabel": "Много общения",
        "weights": {"social": 1.0, "care": 0.7, "enterprising": 0.45},
    },
    {
        "id": "q_data_scale",
        "type": "scale",
        "text": "Насколько вам интересно искать выводы в числах, данных, таблицах и графиках?",
        "hint": "1 - почти неинтересно, 100 - хочется глубоко разбираться.",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не мое",
        "rightLabel": "Очень интересно",
        "weights": {"analytical": 1.0, "digital": 0.72, "conventional": 0.58},
    },
    {
        "id": "q_problem_style",
        "type": "single",
        "text": "Как вы обычно подходите к новой сложной задаче?",
        "options": [
            {"id": "decompose", "label": "Разбиваю на части и строю понятный алгоритм", "weights": {"analytical": 0.88, "digital": 0.7, "conventional": 0.62}},
            {"id": "prototype", "label": "Быстро пробую руками и улучшаю по результату", "weights": {"practical": 0.86, "creative": 0.58, "risk": 0.48}},
            {"id": "ask_people", "label": "Сначала выясняю, кому и зачем это нужно", "weights": {"social": 0.82, "care": 0.66, "enterprising": 0.58}},
            {"id": "invent", "label": "Ищу нестандартный ход и новую форму решения", "weights": {"creative": 0.92, "autonomy": 0.68, "learning": 0.62}},
            {"id": "rules", "label": "Уточняю правила, ограничения и критерии качества", "weights": {"conventional": 0.9, "analytical": 0.64, "risk": 0.28}},
        ],
    },
    {
        "id": "q_creative_scale",
        "type": "scale",
        "text": "Насколько для вас важна возможность придумывать новое и влиять на форму результата?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше готовая схема",
        "rightLabel": "Нужна свобода",
        "weights": {"creative": 1.0, "autonomy": 0.65, "enterprising": 0.32},
    },
    {
        "id": "q_system_scale",
        "type": "scale",
        "text": "Насколько вам подходит работа, где важны порядок, точность, регламенты и документы?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не люблю регламенты",
        "rightLabel": "Люблю порядок",
        "weights": {"conventional": 1.0, "analytical": 0.46, "risk": -0.34},
    },
    {
        "id": "q_subjects",
        "type": "multi",
        "text": "Какие области вам хочется изучать глубже?",
        "hint": "Отметьте все подходящие.",
        "options": [
            {"id": "math", "label": "Математика, логика, статистика", "weights": {"analytical": 0.94, "science": 0.72, "digital": 0.58}},
            {"id": "biology", "label": "Биология, медицина, человек", "weights": {"science": 0.88, "care": 0.8, "conventional": 0.52}},
            {"id": "tech", "label": "Техника, механизмы, электроника", "weights": {"practical": 0.92, "analytical": 0.68, "digital": 0.62}},
            {"id": "business", "label": "Бизнес, рынок, управление", "weights": {"enterprising": 0.9, "analytical": 0.58, "risk": 0.54}},
            {"id": "art", "label": "Дизайн, медиа, культура", "weights": {"creative": 0.94, "social": 0.48, "autonomy": 0.6}},
            {"id": "law", "label": "Право, правила, общественные системы", "weights": {"conventional": 0.88, "analytical": 0.66, "social": 0.52}},
        ],
    },
    {
        "id": "q_leadership_scale",
        "type": "scale",
        "text": "Насколько вам комфортно брать ответственность за решения команды?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше отвечать за свою часть",
        "rightLabel": "Готов вести команду",
        "weights": {"enterprising": 1.0, "social": 0.54, "risk": 0.46, "autonomy": 0.42},
    },
    {
        "id": "q_risk_scale",
        "type": "scale",
        "text": "Насколько вам подходит динамичная среда с непредсказуемостью, срочностью и давлением?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Нужна стабильность",
        "rightLabel": "Нужна динамика",
        "weights": {"risk": 1.0, "enterprising": 0.42, "conventional": -0.46},
    },
    {
        "id": "q_work_environment",
        "type": "single",
        "text": "В какой рабочей среде вам было бы проще показывать сильный результат?",
        "options": [
            {"id": "quiet", "label": "Спокойная аналитическая среда с фокусом", "weights": {"analytical": 0.82, "autonomy": 0.72, "risk": 0.18}},
            {"id": "studio", "label": "Студия или продуктовая команда с обсуждением идей", "weights": {"creative": 0.84, "social": 0.62, "digital": 0.58}},
            {"id": "field", "label": "Производство, лаборатория, объект или мастерская", "weights": {"practical": 0.9, "science": 0.58, "conventional": 0.56}},
            {"id": "clients", "label": "Клиенты, переговоры, сервис или обучение", "weights": {"social": 0.9, "enterprising": 0.72, "care": 0.68}},
            {"id": "operations", "label": "Операционный центр, документы, сроки и контроль", "weights": {"conventional": 0.9, "enterprising": 0.58, "analytical": 0.54}},
        ],
    },
    {
        "id": "q_tools",
        "type": "multi",
        "text": "Какие инструменты вам скорее понравились бы?",
        "options": [
            {"id": "editor", "label": "Редактор кода, базы данных, скрипты", "weights": {"digital": 0.96, "analytical": 0.78, "autonomy": 0.66}},
            {"id": "cad", "label": "CAD, 3D-модели, чертежи, прототипы", "weights": {"practical": 0.84, "creative": 0.72, "digital": 0.62}},
            {"id": "crm", "label": "CRM, презентации, доски задач, встречи", "weights": {"enterprising": 0.78, "social": 0.72, "conventional": 0.52}},
            {"id": "lab_tools", "label": "Лабораторное оборудование и методики", "weights": {"science": 0.94, "practical": 0.62, "conventional": 0.74}},
            {"id": "texts", "label": "Тексты, интервью, сценарии, редактура", "weights": {"creative": 0.86, "social": 0.66, "autonomy": 0.58}},
            {"id": "finance", "label": "Таблицы, отчеты, модели и бюджетирование", "weights": {"conventional": 0.94, "analytical": 0.82, "digital": 0.46}},
        ],
    },
    {
        "id": "q_help_scale",
        "type": "scale",
        "text": "Насколько вам важно видеть, что работа прямо помогает конкретным людям?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Можно без прямой помощи",
        "rightLabel": "Это важно",
        "weights": {"care": 1.0, "social": 0.76, "science": 0.22},
    },
    {
        "id": "q_tech_scale",
        "type": "scale",
        "text": "Насколько вас привлекает работа с техникой, устройствами, кодом или сложными системами?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Скорее нет",
        "rightLabel": "Очень привлекает",
        "weights": {"digital": 0.82, "practical": 0.78, "analytical": 0.52},
    },
    {
        "id": "q_project_role",
        "type": "single",
        "text": "Какую роль вы чаще занимаете в групповом проекте?",
        "options": [
            {"id": "expert", "label": "Эксперт, который глубоко разбирается в задаче", "weights": {"analytical": 0.86, "science": 0.72, "autonomy": 0.62}},
            {"id": "maker", "label": "Исполнитель, который превращает идею в рабочую вещь", "weights": {"practical": 0.86, "digital": 0.58, "conventional": 0.48}},
            {"id": "facilitator", "label": "Человек, который связывает команду и пользователей", "weights": {"social": 0.88, "care": 0.58, "enterprising": 0.56}},
            {"id": "leader", "label": "Лидер, который распределяет задачи и принимает решения", "weights": {"enterprising": 0.94, "risk": 0.56, "social": 0.62}},
            {"id": "author", "label": "Автор концепции, формы, текста или визуального решения", "weights": {"creative": 0.94, "autonomy": 0.68, "social": 0.36}},
        ],
    },
    {
        "id": "q_learning_style",
        "type": "single",
        "text": "Как вам легче учиться новому?",
        "options": [
            {"id": "practice", "label": "Через практику, ошибки и реальные задачи", "weights": {"practical": 0.82, "learning": 0.72, "risk": 0.38}},
            {"id": "theory", "label": "Через теорию, книги, лекции и модели", "weights": {"science": 0.82, "analytical": 0.78, "learning": 0.82}},
            {"id": "mentor", "label": "Через наставника, обсуждение и обратную связь", "weights": {"social": 0.72, "care": 0.52, "learning": 0.76}},
            {"id": "project", "label": "Через собственный проект и свободу выбора", "weights": {"autonomy": 0.86, "creative": 0.64, "enterprising": 0.52}},
            {"id": "plan", "label": "Через четкую программу, контрольные точки и порядок", "weights": {"conventional": 0.84, "learning": 0.62, "analytical": 0.48}},
        ],
    },
    {
        "id": "q_independence_scale",
        "type": "scale",
        "text": "Насколько вам важна самостоятельность в выборе способов работы?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше четкие инструкции",
        "rightLabel": "Нужна автономия",
        "weights": {"autonomy": 1.0, "creative": 0.44, "enterprising": 0.32, "conventional": -0.36},
    },
    {
        "id": "q_detail_scale",
        "type": "scale",
        "text": "Насколько вам комфортно долго работать с деталями, проверками и точностью?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Быстро устаю",
        "rightLabel": "Комфортно",
        "weights": {"conventional": 0.92, "analytical": 0.66, "science": 0.44},
    },
    {
        "id": "q_values",
        "type": "multi",
        "text": "Что для вас особенно важно в будущей профессии?",
        "options": [
            {"id": "income", "label": "Понятный карьерный и финансовый рост", "weights": {"enterprising": 0.72, "conventional": 0.62, "risk": 0.34}},
            {"id": "meaning", "label": "Польза людям и ощущение смысла", "weights": {"care": 0.92, "social": 0.76}},
            {"id": "complexity", "label": "Сложные интеллектуальные задачи", "weights": {"analytical": 0.92, "science": 0.78, "learning": 0.78}},
            {"id": "freedom", "label": "Свобода, гибкость и личная ответственность", "weights": {"autonomy": 0.92, "creative": 0.58, "risk": 0.46}},
            {"id": "stability", "label": "Стабильность, правила и предсказуемость", "weights": {"conventional": 0.86, "risk": 0.12}},
            {"id": "visible", "label": "Заметный результат, которым можно гордиться", "weights": {"creative": 0.72, "practical": 0.62, "enterprising": 0.58}},
        ],
    },
    {
        "id": "q_research_scale",
        "type": "scale",
        "text": "Насколько вам интересно проверять гипотезы, сравнивать варианты и искать доказательства?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше готовые ответы",
        "rightLabel": "Люблю исследовать",
        "weights": {"science": 1.0, "analytical": 0.86, "learning": 0.58},
    },
    {
        "id": "q_business_scale",
        "type": "scale",
        "text": "Насколько вам интересны рынок, переговоры, стратегия и влияние на общий результат?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не привлекает",
        "rightLabel": "Очень интересно",
        "weights": {"enterprising": 1.0, "social": 0.58, "risk": 0.52},
    },
    {
        "id": "q_visual_scale",
        "type": "scale",
        "text": "Насколько вам важны визуальная форма, эстетика, язык и впечатление от результата?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не главное",
        "rightLabel": "Очень важно",
        "weights": {"creative": 1.0, "social": 0.36, "autonomy": 0.48},
    },
    {
        "id": "q_stability",
        "type": "single",
        "text": "Какой темп профессиональной среды вам ближе?",
        "options": [
            {"id": "stable", "label": "Стабильные правила, понятная зона ответственности", "weights": {"conventional": 0.88, "risk": 0.12, "autonomy": 0.36}},
            {"id": "balanced", "label": "План есть, но иногда появляются новые задачи", "weights": {"conventional": 0.62, "learning": 0.58, "enterprising": 0.44}},
            {"id": "changing", "label": "Быстрые изменения, гипотезы и новые решения", "weights": {"risk": 0.72, "enterprising": 0.72, "creative": 0.58}},
            {"id": "mission", "label": "Срочные ситуации, где нужно действовать сразу", "weights": {"risk": 0.96, "practical": 0.72, "care": 0.58}},
        ],
    },
    {
        "id": "q_result_type",
        "type": "single",
        "text": "Какой результат работы вам приятнее всего видеть?",
        "options": [
            {"id": "working_system", "label": "Рабочую систему, устройство или программу", "weights": {"practical": 0.8, "digital": 0.76, "analytical": 0.58}},
            {"id": "clear_answer", "label": "Точный вывод, прогноз или доказательство", "weights": {"analytical": 0.92, "science": 0.72, "conventional": 0.56}},
            {"id": "person_change", "label": "Прогресс человека, которому стало понятнее или легче", "weights": {"care": 0.92, "social": 0.86}},
            {"id": "public_effect", "label": "Решение, которое увидели и оценили другие", "weights": {"creative": 0.78, "enterprising": 0.66, "social": 0.52}},
            {"id": "controlled_process", "label": "Процесс без сбоев, ошибок и лишних потерь", "weights": {"conventional": 0.9, "analytical": 0.62, "practical": 0.48}},
        ],
    },
    {
        "id": "q_team_style",
        "type": "single",
        "text": "Какой формат командной работы вам ближе?",
        "options": [
            {"id": "solo", "label": "Самостоятельно делаю сложную часть и показываю результат", "weights": {"autonomy": 0.9, "analytical": 0.66, "digital": 0.5}},
            {"id": "pair", "label": "Работаю в паре с сильным специалистом", "weights": {"learning": 0.76, "social": 0.52, "analytical": 0.5}},
            {"id": "team", "label": "Плотно взаимодействую с командой каждый день", "weights": {"social": 0.84, "enterprising": 0.56, "care": 0.42}},
            {"id": "coordinate", "label": "Координирую роли, сроки и коммуникацию", "weights": {"enterprising": 0.92, "conventional": 0.72, "social": 0.68}},
        ],
    },
    {
        "id": "q_pressure_scale",
        "type": "scale",
        "text": "Насколько вы готовы работать в профессии, где цена ошибки заметна и нужна выдержка?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше низкая цена ошибки",
        "rightLabel": "Готов к ответственности",
        "weights": {"risk": 0.86, "care": 0.48, "conventional": 0.44, "enterprising": 0.36},
    },
    {
        "id": "q_public_scale",
        "type": "scale",
        "text": "Насколько вам комфортно публично представлять идеи, спорить и защищать позицию?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Предпочитаю не выступать",
        "rightLabel": "Комфортно выступать",
        "weights": {"social": 0.72, "enterprising": 0.82, "creative": 0.36},
    },
    {
        "id": "q_domain_choice",
        "type": "single",
        "text": "Если выбрать один главный фокус, что вы бы взяли?",
        "options": [
            {"id": "technology", "label": "Технологии и инженерные системы", "weights": {"digital": 0.86, "practical": 0.84, "analytical": 0.62}},
            {"id": "human", "label": "Человек, обучение, здоровье или поддержка", "weights": {"care": 0.94, "social": 0.9, "science": 0.42}},
            {"id": "business", "label": "Бизнес, продукт, управление или рынок", "weights": {"enterprising": 0.94, "social": 0.62, "analytical": 0.52}},
            {"id": "knowledge", "label": "Наука, данные, гипотезы и доказательства", "weights": {"science": 0.96, "analytical": 0.9, "learning": 0.7}},
            {"id": "expression", "label": "Дизайн, текст, медиа или визуальные решения", "weights": {"creative": 0.96, "social": 0.52, "autonomy": 0.68}},
            {"id": "order", "label": "Правила, финансы, документы или контроль", "weights": {"conventional": 0.96, "analytical": 0.66, "risk": 0.18}},
        ],
    },
    {
        "id": "q_quality_or_speed",
        "type": "single",
        "text": "Что для вас важнее в рабочей задаче?",
        "options": [
            {"id": "quality", "label": "Точность, проверка и отсутствие ошибок", "weights": {"conventional": 0.94, "analytical": 0.74, "risk": 0.18}},
            {"id": "speed", "label": "Быстрое решение и движение вперед", "weights": {"risk": 0.72, "enterprising": 0.66, "practical": 0.42}},
            {"id": "meaning", "label": "Польза для человека или общества", "weights": {"care": 0.92, "social": 0.7, "science": 0.32}},
            {"id": "originality", "label": "Оригинальность и выразительная форма", "weights": {"creative": 0.94, "autonomy": 0.62}},
            {"id": "scalability", "label": "Чтобы решение работало для многих людей или процессов", "weights": {"digital": 0.72, "analytical": 0.68, "enterprising": 0.56}},
        ],
    },
    {
        "id": "q_preferred_output",
        "type": "multi",
        "text": "Какие рабочие результаты вам было бы приятно регулярно создавать?",
        "hint": "Можно выбрать несколько результатов.",
        "options": [
            {"id": "software", "label": "Работающий сервис, скрипт, приложение или автоматизацию", "weights": {"digital": 0.96, "analytical": 0.76, "practical": 0.5}},
            {"id": "report", "label": "Отчет, прогноз, юридическую позицию или финансовую модель", "weights": {"conventional": 0.9, "analytical": 0.82}},
            {"id": "content", "label": "Видео, текст, визуал, пост или концепцию", "weights": {"creative": 0.94, "digital": 0.56, "social": 0.42}},
            {"id": "event", "label": "Событие, встречу, переговоры или клиентский результат", "weights": {"social": 0.86, "enterprising": 0.82, "risk": 0.5}},
            {"id": "care_result", "label": "Улучшение состояния человека, животного или среды", "weights": {"care": 0.96, "science": 0.66, "practical": 0.48}},
            {"id": "physical_object", "label": "Объект, интерьер, механизм, прототип или чертеж", "weights": {"practical": 0.92, "creative": 0.62, "conventional": 0.52}},
        ],
    },
    {
        "id": "q_error_tolerance",
        "type": "scale",
        "text": "Насколько вам подходит работа, где нужно методично искать ошибки и слабые места?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше создавать новое",
        "rightLabel": "Люблю проверять",
        "weights": {"conventional": 0.9, "analytical": 0.82, "digital": 0.46, "creative": -0.28},
    },
    {
        "id": "q_client_contact",
        "type": "scale",
        "text": "Насколько вам комфортны клиенты, заказчики, переговоры и защита решения?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше без клиентов",
        "rightLabel": "Комфортно с людьми",
        "weights": {"social": 0.86, "enterprising": 0.78, "creative": 0.34, "autonomy": 0.22},
    },
    {
        "id": "q_field_work",
        "type": "scale",
        "text": "Насколько вас привлекает работа вне кабинета: объект, лаборатория, выезды, производство, практика?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше рабочее место",
        "rightLabel": "Хочу практику",
        "weights": {"practical": 0.96, "science": 0.56, "risk": 0.44, "digital": -0.18},
    },
    {
        "id": "q_media_interest",
        "type": "scale",
        "text": "Насколько вам интересны медиа, социальные сети, тексты, видео и работа с вниманием аудитории?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не мой формат",
        "rightLabel": "Очень интересно",
        "weights": {"creative": 0.9, "social": 0.66, "digital": 0.58, "enterprising": 0.44},
    },
    {
        "id": "q_infrastructure_interest",
        "type": "scale",
        "text": "Насколько вам интересно поддерживать сложные системы, чтобы они работали стабильно и без сбоев?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Скорее скучно",
        "rightLabel": "Это интересно",
        "weights": {"digital": 0.9, "conventional": 0.84, "practical": 0.68, "risk": 0.34},
    },
    {
        "id": "q_animals_nature",
        "type": "single",
        "text": "Какая тема вам ближе, если думать о пользе и заботе?",
        "options": [
            {"id": "people_health", "label": "Здоровье и состояние людей", "weights": {"care": 0.96, "science": 0.7, "social": 0.58}},
            {"id": "animals", "label": "Животные и их здоровье", "weights": {"care": 0.9, "science": 0.78, "practical": 0.62}},
            {"id": "nature", "label": "Природа, экология и среда", "weights": {"science": 0.94, "care": 0.62, "practical": 0.48}},
            {"id": "community", "label": "Социальная поддержка и жизненные ситуации людей", "weights": {"social": 0.9, "care": 0.94, "conventional": 0.44}},
            {"id": "not_care", "label": "Лучше задачи без постоянной темы заботы", "weights": {"analytical": 0.48, "digital": 0.42, "care": 0.12}},
        ],
    },
    {
        "id": "q_language_text",
        "type": "scale",
        "text": "Насколько вам нравится долго работать со смыслом текста, языком, формулировками и нюансами?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не люблю тексты",
        "rightLabel": "Люблю язык",
        "weights": {"creative": 0.72, "analytical": 0.58, "conventional": 0.66, "autonomy": 0.5},
    },
    {
        "id": "q_process_ownership",
        "type": "single",
        "text": "Что вам ближе в большом процессе?",
        "options": [
            {"id": "design_process", "label": "Придумать форму, сценарий или пользовательский опыт", "weights": {"creative": 0.88, "digital": 0.58, "social": 0.42}},
            {"id": "keep_process", "label": "Сделать процесс стабильным, понятным и управляемым", "weights": {"conventional": 0.92, "enterprising": 0.62, "analytical": 0.58}},
            {"id": "sell_process", "label": "Найти людей, убедить их и довести до сделки", "weights": {"enterprising": 0.96, "social": 0.88, "risk": 0.58}},
            {"id": "research_process", "label": "Проверить гипотезы и доказать, какой вариант лучше", "weights": {"science": 0.86, "analytical": 0.88, "learning": 0.58}},
            {"id": "build_process", "label": "Собрать рабочую систему или материальный результат", "weights": {"practical": 0.9, "digital": 0.58, "conventional": 0.44}},
        ],
    },
    {
        "id": "q_deadline_pressure",
        "type": "scale",
        "text": "Насколько вам подходит работа с жесткими сроками, быстрыми правками и внешним давлением?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Нужен спокойный ритм",
        "rightLabel": "Справляюсь с темпом",
        "weights": {"risk": 0.86, "enterprising": 0.6, "creative": 0.38, "conventional": -0.18},
    },
    {
        "id": "q_formality_preference",
        "type": "single",
        "text": "Какая степень формальности работы вам комфортнее?",
        "options": [
            {"id": "strict", "label": "Четкие правила, инструкции, ответственность и проверка", "weights": {"conventional": 0.96, "risk": 0.28, "analytical": 0.58}},
            {"id": "semi", "label": "Понятная структура, но есть место решениям", "weights": {"conventional": 0.62, "autonomy": 0.52, "learning": 0.48}},
            {"id": "flex", "label": "Гибкий формат, поиск, эксперименты, неопределенность", "weights": {"creative": 0.72, "autonomy": 0.82, "risk": 0.58}},
            {"id": "people_rules", "label": "Правила важны, но главное - договориться с людьми", "weights": {"social": 0.8, "enterprising": 0.72, "conventional": 0.46}},
        ],
    },
    {
        "id": "q_specialization_depth",
        "type": "scale",
        "text": "Насколько вам хочется стать узким экспертом в сложной области?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше широкий круг задач",
        "rightLabel": "Хочу глубокую экспертизу",
        "weights": {"science": 0.78, "analytical": 0.82, "learning": 0.86, "autonomy": 0.5},
    },
    {
        "id": "q_tools_preference",
        "type": "multi",
        "text": "С какими рабочими инструментами вы бы хотели иметь дело чаще?",
        "hint": "Можно выбрать несколько инструментов.",
        "options": [
            {"id": "server_tools", "label": "Серверы, сети, терминал, мониторинг", "weights": {"digital": 0.96, "practical": 0.72, "conventional": 0.66}},
            {"id": "test_tools", "label": "Чек-листы, баг-репорты, автотесты", "weights": {"conventional": 0.9, "digital": 0.78, "analytical": 0.76}},
            {"id": "creative_tools", "label": "Графика, монтаж, 3D, редакторы контента", "weights": {"creative": 0.96, "digital": 0.68, "autonomy": 0.54}},
            {"id": "human_tools", "label": "Анкеты, консультации, переговоры, встречи", "weights": {"social": 0.88, "care": 0.62, "enterprising": 0.56}},
            {"id": "science_tools", "label": "Лаборатория, измерения, наблюдения, протоколы", "weights": {"science": 0.94, "practical": 0.62, "conventional": 0.7}},
            {"id": "business_tools", "label": "CRM, воронка продаж, бюджеты, KPI", "weights": {"enterprising": 0.92, "conventional": 0.62, "social": 0.58}},
        ],
    },
    {
        "id": "q_service_vs_product",
        "type": "single",
        "text": "Что вам ближе: сервисная работа, продукт или экспертная область?",
        "options": [
            {"id": "service", "label": "Помогать людям здесь и сейчас", "weights": {"social": 0.88, "care": 0.84, "risk": 0.34}},
            {"id": "product", "label": "Развивать продукт, который используют многие", "weights": {"digital": 0.76, "enterprising": 0.72, "creative": 0.58}},
            {"id": "expert", "label": "Глубоко разбираться в сложной теме", "weights": {"analytical": 0.88, "science": 0.76, "learning": 0.82}},
            {"id": "operation", "label": "Обеспечивать надежный процесс без сбоев", "weights": {"conventional": 0.9, "practical": 0.62, "enterprising": 0.54}},
            {"id": "artifacts", "label": "Создавать конкретные объекты, визуалы или материалы", "weights": {"creative": 0.86, "practical": 0.72, "autonomy": 0.54}},
        ],
    },
    {
        "id": "q_code_depth",
        "type": "scale",
        "text": "Насколько вам интересно писать код, разбираться в архитектуре программ и улучшать технические решения?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Скорее нет",
        "rightLabel": "Очень интересно",
        "weights": {"digital": 1.0, "analytical": 0.82, "autonomy": 0.62, "learning": 0.54},
    },
    {
        "id": "q_data_pipelines",
        "type": "single",
        "text": "Какая работа с данными кажется вам более привлекательной?",
        "options": [
            {"id": "insights", "label": "Искать выводы и объяснять их людям", "weights": {"analytical": 0.92, "social": 0.46, "digital": 0.62}},
            {"id": "pipelines", "label": "Строить надежные потоки данных и базы", "weights": {"digital": 0.96, "conventional": 0.84, "practical": 0.56}},
            {"id": "models", "label": "Экспериментировать с алгоритмами и моделями", "weights": {"science": 0.94, "analytical": 0.96, "digital": 0.88}},
            {"id": "requirements", "label": "Переводить задачи бизнеса в понятные требования", "weights": {"social": 0.68, "conventional": 0.82, "enterprising": 0.64}},
        ],
    },
    {
        "id": "q_interface_or_logic",
        "type": "single",
        "text": "Если делать цифровой продукт, какая часть вам ближе?",
        "options": [
            {"id": "interface", "label": "Интерфейс, внешний вид и удобство пользователя", "weights": {"creative": 0.86, "digital": 0.82, "social": 0.48}},
            {"id": "server", "label": "Серверная логика, данные и надежность", "weights": {"analytical": 0.88, "digital": 0.96, "conventional": 0.68}},
            {"id": "infrastructure", "label": "Инфраструктура, мониторинг и стабильность", "weights": {"practical": 0.7, "digital": 0.96, "risk": 0.48}},
            {"id": "product_rules", "label": "Требования, сценарии и согласование решений", "weights": {"conventional": 0.82, "social": 0.62, "analytical": 0.72}},
        ],
    },
    {
        "id": "q_security_suspicion",
        "type": "scale",
        "text": "Насколько вам нравится искать уязвимости, слабые места и сценарии, где система может сломаться?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не люблю искать сбои",
        "rightLabel": "Люблю проверять",
        "weights": {"analytical": 0.86, "digital": 0.82, "conventional": 0.58, "risk": 0.52},
    },
    {
        "id": "q_networks_systems",
        "type": "scale",
        "text": "Насколько вам интересны сети, серверы, доступы, отказоустойчивость и связь между системами?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не привлекает",
        "rightLabel": "Очень интересно",
        "weights": {"digital": 0.94, "practical": 0.72, "conventional": 0.74, "analytical": 0.54},
    },
    {
        "id": "q_health_role",
        "type": "single",
        "text": "Если рассматривать помощь в сфере здоровья, какой формат ближе?",
        "options": [
            {"id": "diagnosis", "label": "Ставить диагноз и принимать клинические решения", "weights": {"science": 0.92, "care": 0.92, "analytical": 0.78, "risk": 0.62}},
            {"id": "procedures", "label": "Выполнять процедуры и быть рядом с пациентом", "weights": {"practical": 0.82, "care": 0.96, "social": 0.74, "conventional": 0.72}},
            {"id": "rehab", "label": "Постепенно восстанавливать навыки и движение", "weights": {"practical": 0.76, "care": 0.94, "social": 0.78, "learning": 0.58}},
            {"id": "lab", "label": "Работать с анализами, пробами и точными протоколами", "weights": {"science": 0.94, "conventional": 0.94, "analytical": 0.72}},
            {"id": "speech", "label": "Помогать с речью, обучением и коммуникацией", "weights": {"social": 0.92, "care": 0.88, "creative": 0.5}},
        ],
    },
    {
        "id": "q_manual_precision",
        "type": "scale",
        "text": "Насколько вам комфортна точная ручная работа, где результат зависит от аккуратности движений?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не мой формат",
        "rightLabel": "Комфортно",
        "weights": {"practical": 0.9, "conventional": 0.58, "science": 0.42, "risk": 0.32},
    },
    {
        "id": "q_teaching_patience",
        "type": "scale",
        "text": "Насколько вам подходит долго объяснять, возвращаться к базовым вещам и видеть постепенный прогресс человека?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Быстро устаю",
        "rightLabel": "Мне это подходит",
        "weights": {"social": 0.92, "care": 0.78, "learning": 0.74, "risk": -0.18},
    },
    {
        "id": "q_empathy_boundaries",
        "type": "scale",
        "text": "Насколько вы готовы регулярно работать с эмоциями, переживаниями и сложными жизненными ситуациями людей?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше без этого",
        "rightLabel": "Готов работать",
        "weights": {"care": 0.94, "social": 0.86, "risk": 0.34, "autonomy": 0.22},
    },
    {
        "id": "q_negotiation_sales",
        "type": "scale",
        "text": "Насколько вам комфортно убеждать, вести переговоры, работать с отказами и доводить до сделки?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Скорее некомфортно",
        "rightLabel": "Комфортно",
        "weights": {"enterprising": 0.98, "social": 0.84, "risk": 0.66},
    },
    {
        "id": "q_financial_models",
        "type": "scale",
        "text": "Насколько вам интересны финансовые модели, бюджеты, экономические прогнозы и проверка цифр?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Неинтересно",
        "rightLabel": "Очень интересно",
        "weights": {"analytical": 0.92, "conventional": 0.9, "enterprising": 0.42, "digital": 0.42},
    },
    {
        "id": "q_law_argument",
        "type": "scale",
        "text": "Насколько вам нравится разбирать правила, находить точные формулировки и аргументировать позицию?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не люблю формальности",
        "rightLabel": "Люблю аргументы",
        "weights": {"conventional": 0.96, "analytical": 0.78, "social": 0.44, "enterprising": 0.36},
    },
    {
        "id": "q_spatial_design",
        "type": "scale",
        "text": "Насколько вам интересно продумывать пространство, планировку, форму объекта или 3D-сцену?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не мое",
        "rightLabel": "Очень интересно",
        "weights": {"creative": 0.96, "practical": 0.68, "digital": 0.54, "conventional": 0.32},
    },
    {
        "id": "q_motion_visual",
        "type": "scale",
        "text": "Насколько вам интересны анимация, монтаж, динамическая графика и выразительная подача идеи?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не привлекает",
        "rightLabel": "Очень привлекает",
        "weights": {"creative": 0.98, "digital": 0.72, "autonomy": 0.52, "risk": 0.22},
    },
    {
        "id": "q_text_explanation",
        "type": "single",
        "text": "Какая работа с текстом вам ближе?",
        "options": [
            {"id": "technical_docs", "label": "Понятно объяснять сложный продукт или инструкцию", "weights": {"conventional": 0.86, "analytical": 0.76, "digital": 0.58}},
            {"id": "media_story", "label": "Искать историю, писать материал или сценарий", "weights": {"creative": 0.9, "social": 0.72, "risk": 0.42}},
            {"id": "translation", "label": "Точно передавать смысл между языками и культурами", "weights": {"creative": 0.72, "conventional": 0.78, "analytical": 0.62}},
            {"id": "legal_text", "label": "Добиваться точности формулировок в правилах и документах", "weights": {"conventional": 0.96, "analytical": 0.74, "risk": 0.26}},
        ],
    },
    {
        "id": "q_materials_laboratory",
        "type": "scale",
        "text": "Насколько вам интересны вещества, материалы, лабораторные опыты и технологические процессы?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Скорее нет",
        "rightLabel": "Очень интересно",
        "weights": {"science": 0.98, "practical": 0.68, "conventional": 0.76, "analytical": 0.62},
    },
    {
        "id": "q_field_nature",
        "type": "scale",
        "text": "Насколько вам подходит работа с природными объектами, выездами, наблюдениями и полевыми данными?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше офис",
        "rightLabel": "Нужны выезды",
        "weights": {"science": 0.86, "practical": 0.78, "risk": 0.54, "autonomy": 0.42},
    },
    {
        "id": "q_city_systems",
        "type": "single",
        "text": "Какая задача про город или среду кажется интереснее?",
        "options": [
            {"id": "buildings", "label": "Рассчитать и спроектировать надежный объект", "weights": {"practical": 0.86, "conventional": 0.86, "analytical": 0.7}},
            {"id": "public_space", "label": "Понять сценарии людей и улучшить городское пространство", "weights": {"social": 0.72, "creative": 0.72, "care": 0.58}},
            {"id": "ecology", "label": "Оценить влияние на природу и среду", "weights": {"science": 0.92, "care": 0.66, "analytical": 0.62}},
            {"id": "interior", "label": "Сделать удобное и красивое пространство внутри", "weights": {"creative": 0.94, "practical": 0.56, "social": 0.44}},
        ],
    },
    {
        "id": "q_process_control",
        "type": "scale",
        "text": "Насколько вам интересно контролировать процессы, стандарты, поставки, качество и отсутствие сбоев?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не люблю контроль",
        "rightLabel": "Люблю управлять процессом",
        "weights": {"conventional": 0.96, "enterprising": 0.68, "analytical": 0.62, "practical": 0.38},
    },
    {
        "id": "q_procurement_tradeoffs",
        "type": "single",
        "text": "Что вам ближе в операционной работе?",
        "options": [
            {"id": "logistics", "label": "Маршруты, склады, сроки и оптимизация потоков", "weights": {"practical": 0.72, "conventional": 0.86, "analytical": 0.7}},
            {"id": "quality", "label": "Стандарты, проверки, аудит и предотвращение ошибок", "weights": {"conventional": 0.96, "analytical": 0.68, "care": 0.28}},
            {"id": "procurement", "label": "Поставщики, условия, закупки и переговоры", "weights": {"enterprising": 0.74, "conventional": 0.88, "social": 0.56}},
            {"id": "operations", "label": "Настроить весь процесс так, чтобы команда работала ровно", "weights": {"enterprising": 0.78, "conventional": 0.86, "social": 0.52}},
        ],
    },
    {
        "id": "q_aviation_responsibility",
        "type": "scale",
        "text": "Насколько вам подходит строго регламентированная работа с высокой ответственностью и быстрыми решениями?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Лучше спокойнее",
        "rightLabel": "Готов к регламенту",
        "weights": {"conventional": 0.94, "risk": 0.82, "practical": 0.62, "analytical": 0.42},
    },
    {
        "id": "q_emergency_action",
        "type": "scale",
        "text": "Насколько вы готовы действовать в срочных ситуациях, где нужно быстро помогать и брать ответственность?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не мой формат",
        "rightLabel": "Готов действовать",
        "weights": {"risk": 0.96, "care": 0.78, "practical": 0.78, "social": 0.46},
    },
    {
        "id": "q_user_research",
        "type": "scale",
        "text": "Насколько вам интересно изучать потребности людей, проводить интервью и превращать наблюдения в решения?",
        "min": 1,
        "max": 100,
        "step": 1,
        "leftLabel": "Не очень",
        "rightLabel": "Очень интересно",
        "weights": {"social": 0.82, "analytical": 0.62, "creative": 0.72, "care": 0.44},
    },
    {
        "id": "q_product_strategy",
        "type": "single",
        "text": "Какая продуктовая задача вам ближе?",
        "options": [
            {"id": "roadmap", "label": "Выбрать приоритеты и вести команду к результату", "weights": {"enterprising": 0.92, "analytical": 0.7, "social": 0.62}},
            {"id": "design", "label": "Сделать понятный сценарий и интерфейс", "weights": {"creative": 0.86, "social": 0.58, "digital": 0.68}},
            {"id": "metrics", "label": "Разобраться в метриках и улучшить рост продукта", "weights": {"analytical": 0.86, "digital": 0.62, "enterprising": 0.68}},
            {"id": "delivery", "label": "Организовать сроки, ресурсы и запуск", "weights": {"conventional": 0.78, "enterprising": 0.86, "risk": 0.46}},
        ],
    },
    {
        "id": "q_learning_market",
        "type": "multi",
        "text": "Какие темы вы готовы изучать даже без внешнего давления?",
        "hint": "Выберите все темы, к которым есть живой интерес.",
        "options": [
            {"id": "programming", "label": "Языки программирования, архитектура, автоматизация", "weights": {"digital": 0.96, "analytical": 0.82, "learning": 0.82}},
            {"id": "medicine", "label": "Здоровье, организм, диагностика, восстановление", "weights": {"care": 0.92, "science": 0.84, "learning": 0.76}},
            {"id": "markets", "label": "Рынки, деньги, продажи, стратегия", "weights": {"enterprising": 0.9, "analytical": 0.56, "risk": 0.46}},
            {"id": "visual_culture", "label": "Визуальная культура, интерфейсы, видео, пространство", "weights": {"creative": 0.96, "digital": 0.58, "autonomy": 0.54}},
            {"id": "systems", "label": "Стандарты, процессы, документы, качество", "weights": {"conventional": 0.94, "analytical": 0.64, "learning": 0.54}},
            {"id": "people_development", "label": "Обучение, консультации, развитие людей", "weights": {"social": 0.92, "care": 0.78, "learning": 0.84}},
        ],
    },
    {
        "id": "q_work_rhythm",
        "type": "single",
        "text": "Какой рабочий ритм кажется наиболее продуктивным лично для вас?",
        "options": [
            {"id": "deep_focus", "label": "Глубокая концентрация над сложной задачей", "weights": {"analytical": 0.88, "autonomy": 0.78, "science": 0.56}},
            {"id": "hands_on", "label": "Много практики, прототипов и действий руками", "weights": {"practical": 0.9, "risk": 0.42, "learning": 0.54}},
            {"id": "many_contacts", "label": "Много встреч, людей и обратной связи", "weights": {"social": 0.9, "enterprising": 0.66, "care": 0.48}},
            {"id": "creative_sprints", "label": "Короткие творческие рывки и правки результата", "weights": {"creative": 0.88, "risk": 0.46, "digital": 0.48}},
            {"id": "regulated", "label": "Понятный порядок, чек-листы и контроль качества", "weights": {"conventional": 0.94, "risk": 0.16, "analytical": 0.48}},
        ],
    },
]


AnswerValue = Union[str, int, float, List[str]]


class AnswerInput(BaseModel):
    question_id: str
    value: AnswerValue


class NextRequest(BaseModel):
    answers: List[AnswerInput] = []


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def softmax(values: List[float]) -> List[float]:
    max_value = max(values)
    exps = [math.exp(value - max_value) for value in values]
    total = sum(exps) or 1.0
    return [value / total for value in exps]


def vector_from_profession(profession: Dict[str, Any]) -> List[float]:
    source = profession["vector"]
    return [clamp(float(source.get(key, 45)) / 100.0) for key in DIMENSION_KEYS]


PROFESSION_VECTORS = [vector_from_profession(item) for item in PROFESSIONS]


class TinyCareerNeuralNet:
    def __init__(self, input_size: int, hidden_size: int, output_size: int) -> None:
        rng = random.Random(42)
        self.w1 = [[rng.uniform(-0.35, 0.35) for _ in range(input_size)] for _ in range(hidden_size)]
        self.b1 = [0.0 for _ in range(hidden_size)]
        self.w2 = [[rng.uniform(-0.35, 0.35) for _ in range(hidden_size)] for _ in range(output_size)]
        self.b2 = [0.0 for _ in range(output_size)]

    def _forward(self, x: List[float]) -> Dict[str, List[float]]:
        hidden_raw = [
            sum(weight * item for weight, item in zip(row, x)) + bias
            for row, bias in zip(self.w1, self.b1)
        ]
        hidden = [math.tanh(value) for value in hidden_raw]
        logits = [
            sum(weight * item for weight, item in zip(row, hidden)) + bias
            for row, bias in zip(self.w2, self.b2)
        ]
        return {"hidden": hidden, "probs": softmax(logits)}

    def train(self, samples: List[List[float]], labels: List[int], epochs: int = 42, learning_rate: float = 0.038) -> None:
        order = list(range(len(samples)))
        rng = random.Random(7)
        for _ in range(epochs):
            rng.shuffle(order)
            for sample_index in order:
                x = samples[sample_index]
                label = labels[sample_index]
                forward = self._forward(x)
                hidden = forward["hidden"]
                probs = forward["probs"]

                d_logits = probs[:]
                d_logits[label] -= 1.0

                old_w2 = [row[:] for row in self.w2]

                for output_index, delta in enumerate(d_logits):
                    for hidden_index, hidden_value in enumerate(hidden):
                        self.w2[output_index][hidden_index] -= learning_rate * delta * hidden_value
                    self.b2[output_index] -= learning_rate * delta

                d_hidden = []
                for hidden_index, hidden_value in enumerate(hidden):
                    upstream = sum(old_w2[output_index][hidden_index] * d_logits[output_index] for output_index in range(len(d_logits)))
                    d_hidden.append(upstream * (1.0 - hidden_value * hidden_value))

                for hidden_index, delta in enumerate(d_hidden):
                    for input_index, input_value in enumerate(x):
                        self.w1[hidden_index][input_index] -= learning_rate * delta * input_value
                    self.b1[hidden_index] -= learning_rate * delta

    def predict(self, x: List[float]) -> List[float]:
        return self._forward(x)["probs"]


def build_training_set() -> Dict[str, Any]:
    rng = random.Random(100)
    samples: List[List[float]] = []
    labels: List[int] = []

    for profession_index, vector in enumerate(PROFESSION_VECTORS):
        samples.append(vector[:])
        labels.append(profession_index)
        for _ in range(5):
            noisy = [clamp(value + rng.gauss(0, 0.07)) for value in vector]
            samples.append(noisy)
            labels.append(profession_index)
        for _ in range(2):
            softened = [clamp((value * 0.82) + (0.45 * 0.18) + rng.gauss(0, 0.035)) for value in vector]
            samples.append(softened)
            labels.append(profession_index)
        sorted_dimensions = sorted(range(len(vector)), key=lambda index: vector[index], reverse=True)
        strong_dimensions = set(sorted_dimensions[:4])
        weak_dimensions = set(sorted_dimensions[-3:])
        for _ in range(2):
            accented = []
            for dimension_index, value in enumerate(vector):
                if dimension_index in strong_dimensions:
                    accented.append(clamp(value + rng.gauss(0.045, 0.035)))
                elif dimension_index in weak_dimensions:
                    accented.append(clamp(value + rng.gauss(-0.035, 0.03)))
                else:
                    accented.append(clamp(value + rng.gauss(0, 0.045)))
            samples.append(accented)
            labels.append(profession_index)
        for _ in range(1):
            partial = []
            for dimension_index, value in enumerate(vector):
                keep_signal = 0.72 if dimension_index in strong_dimensions else 0.58
                partial.append(clamp((value * keep_signal) + (0.45 * (1.0 - keep_signal)) + rng.gauss(0, 0.04)))
            samples.append(partial)
            labels.append(profession_index)

    return {"samples": samples, "labels": labels}


def train_model() -> TinyCareerNeuralNet:
    dataset = build_training_set()
    model = TinyCareerNeuralNet(len(DIMENSION_KEYS), 22, len(PROFESSIONS))
    model.train(dataset["samples"], dataset["labels"])
    return model


class CareerAiEngine:
    def __init__(self) -> None:
        self.questions = {question["id"]: question for question in QUESTION_BANK}
        self.model = train_model()

    def normalize_answers(self, answers: List[AnswerInput]) -> Dict[str, AnswerValue]:
        normalized: Dict[str, AnswerValue] = {}
        for answer in answers:
            if answer.question_id in self.questions:
                normalized[answer.question_id] = answer.value
        return normalized

    def build_profile(self, answers: Dict[str, AnswerValue]) -> List[float]:
        totals = {key: 0.42 for key in DIMENSION_KEYS}
        weights = {key: 1.0 for key in DIMENSION_KEYS}

        for question_id, value in answers.items():
            question = self.questions.get(question_id)
            if not question:
                continue

            if question["type"] == "scale":
                minimum = float(question.get("min", 1))
                maximum = float(question.get("max", 100))
                try:
                    raw_value = float(value)  # type: ignore[arg-type]
                except (TypeError, ValueError):
                    continue
                normalized_value = clamp((raw_value - minimum) / max(maximum - minimum, 1.0))
                for dimension, direction in question.get("weights", {}).items():
                    factor = abs(float(direction))
                    target = normalized_value if direction >= 0 else 1.0 - normalized_value
                    totals[dimension] += target * factor
                    weights[dimension] += factor
                continue

            selected_options = self.get_selected_options(question, value)
            for option in selected_options:
                for dimension, target in option.get("weights", {}).items():
                    totals[dimension] += float(target)
                    weights[dimension] += 1.0

        return [clamp(totals[key] / weights[key]) for key in DIMENSION_KEYS]

    def get_selected_options(self, question: Dict[str, Any], value: AnswerValue) -> List[Dict[str, Any]]:
        selected_ids: Set[str]
        if question["type"] == "multi":
            selected_ids = {str(item) for item in value} if isinstance(value, list) else set()
        else:
            selected_ids = {str(value)}

        return [option for option in question.get("options", []) if str(option["id"]) in selected_ids]

    def probabilities(self, profile: List[float]) -> List[float]:
        neural = self.model.predict(profile)
        similarities = []
        for vector in PROFESSION_VECTORS:
            distance = math.sqrt(sum((left - right) ** 2 for left, right in zip(profile, vector)) / len(profile))
            similarities.append(clamp(1.0 - distance))
        similarity_probs = softmax([value * 7.2 for value in similarities])
        return [(neural[index] * 0.42) + (similarity_probs[index] * 0.58) for index in range(len(PROFESSIONS))]

    def choose_question(self, answered_ids: Set[str], profile: List[float], probabilities: List[float]) -> Dict[str, Any]:
        if not answered_ids:
            return self.questions["q_start_focus"]

        ranked = sorted(range(len(probabilities)), key=lambda index: probabilities[index], reverse=True)
        top_candidates = ranked[:6]
        total_prob = sum(probabilities[index] for index in top_candidates) or 1.0
        dimension_variance: Dict[str, float] = {}
        for dimension_index, dimension in enumerate(DIMENSION_KEYS):
            mean = sum(PROFESSION_VECTORS[index][dimension_index] * probabilities[index] for index in top_candidates) / total_prob
            variance = sum(((PROFESSION_VECTORS[index][dimension_index] - mean) ** 2) * probabilities[index] for index in top_candidates) / total_prob
            dimension_variance[dimension] = variance

        if len(ranked) > 1:
            first = PROFESSION_VECTORS[ranked[0]]
            second = PROFESSION_VECTORS[ranked[1]]
            dimension_gap = {
                dimension: abs(first[index] - second[index])
                for index, dimension in enumerate(DIMENSION_KEYS)
            }
        else:
            dimension_gap = {dimension: 0.0 for dimension in DIMENSION_KEYS}

        used_types = {self.questions[question_id]["type"] for question_id in answered_ids if question_id in self.questions}
        answered_count = len(answered_ids)
        dimension_counts = self.answered_dimension_counts(answered_ids)
        best_question: Optional[Dict[str, Any]] = None
        best_score = -1.0

        for question in QUESTION_BANK:
            if question["id"] in answered_ids:
                continue
            dimensions = self.question_dimensions(question)
            score = sum((dimension_variance.get(dimension, 0.0) * 2.4) + (dimension_gap.get(dimension, 0.0) * 0.8) for dimension in dimensions)
            score += sum(0.18 for dimension in dimensions if dimension_counts.get(dimension, 0) == 0)
            score += sum(0.08 for dimension in dimensions if dimension_counts.get(dimension, 0) == 1)
            score += sum(max(0.0, profile[DIMENSION_KEYS.index(dimension)] - 0.58) * 0.22 for dimension in dimensions)

            if question.get("stage") == "early" and answered_count < 4:
                score += 0.18
            if question["type"] not in used_types and answered_count >= 2:
                score += 0.16
            if question["type"] == "multi" and answered_count in {2, 3, 7, 11}:
                score += 0.1
            if question["type"] == "scale" and answered_count < 2:
                score -= 0.08
            score += self.question_focus_boost(question, profile)

            if score > best_score:
                best_score = score
                best_question = question

        return best_question or next(question for question in QUESTION_BANK if question["id"] not in answered_ids)

    def question_dimensions(self, question: Dict[str, Any]) -> Set[str]:
        dimensions: Set[str] = set()
        if question["type"] == "scale":
            dimensions.update(question.get("weights", {}).keys())
        for option in question.get("options", []):
            dimensions.update(option.get("weights", {}).keys())
        return dimensions

    def answered_dimension_counts(self, answered_ids: Set[str]) -> Dict[str, int]:
        counts = {dimension: 0 for dimension in DIMENSION_KEYS}
        for question_id in answered_ids:
            question = self.questions.get(question_id)
            if not question:
                continue
            for dimension in self.question_dimensions(question):
                counts[dimension] += 1
        return counts

    def question_focus_boost(self, question: Dict[str, Any], profile: List[float]) -> float:
        values = {dimension: profile[index] for index, dimension in enumerate(DIMENSION_KEYS)}
        question_id = question["id"]
        boost = 0.0

        if values["conventional"] >= 0.64 and values["risk"] <= 0.46:
            if question_id in {"q_process_control", "q_procurement_tradeoffs", "q_formality_preference", "q_detail_scale", "q_error_tolerance"}:
                boost += 1.05
        if values["digital"] >= 0.64 and values["analytical"] >= 0.58:
            if question_id in {"q_code_depth", "q_interface_or_logic", "q_data_pipelines", "q_networks_systems", "q_security_suspicion"}:
                boost += 0.36
        if values["care"] >= 0.62 and values["social"] >= 0.56:
            if question_id in {"q_health_role", "q_empathy_boundaries", "q_teaching_patience", "q_manual_precision", "q_emergency_action"}:
                boost += 0.38
        if values["creative"] >= 0.62:
            if question_id in {"q_spatial_design", "q_motion_visual", "q_text_explanation", "q_interface_or_logic", "q_user_research"}:
                boost += 0.34
        if values["science"] >= 0.64 and values["practical"] >= 0.5 and values["conventional"] < 0.72:
            if question_id in {"q_materials_laboratory", "q_field_nature", "q_health_role", "q_city_systems"}:
                boost += 0.32
        if values["enterprising"] >= 0.62 and values["social"] >= 0.5:
            if question_id in {"q_negotiation_sales", "q_product_strategy", "q_procurement_tradeoffs", "q_process_control"}:
                boost += 0.32

        return boost

    def should_finish(self, answered_count: int, probabilities: List[float]) -> bool:
        if answered_count >= MAX_QUESTIONS:
            return True
        if answered_count < MIN_QUESTIONS:
            return False
        ranked = sorted(probabilities, reverse=True)
        confidence = ranked[0] if ranked else 0.0
        gap = ranked[0] - ranked[1] if len(ranked) > 1 else ranked[0]
        return confidence >= 0.32 and gap >= 0.045

    def next_step(self, answers: List[AnswerInput]) -> Dict[str, Any]:
        normalized_answers = self.normalize_answers(answers)
        profile = self.build_profile(normalized_answers)
        probabilities = self.probabilities(profile)
        answered_ids = set(normalized_answers.keys())
        answered_count = len(answered_ids)

        if self.should_finish(answered_count, probabilities):
            return {
                "done": True,
                "answeredCount": answered_count,
                "progress": 100,
                "confidence": round(max(probabilities) * 100),
                "result": self.build_result(profile, probabilities, answered_count),
            }

        question = self.choose_question(answered_ids, profile, probabilities)
        progress = min(96, round((answered_count / MAX_QUESTIONS) * 92))
        return {
            "done": False,
            "answeredCount": answered_count,
            "progress": progress,
            "confidence": round(max(probabilities) * 100),
            "question": self.serialize_question(question),
        }

    def serialize_question(self, question: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "id": question["id"],
            "type": question["type"],
            "text": question["text"],
            "hint": question.get("hint", ""),
        }
        if question["type"] in {"single", "multi"}:
            payload["options"] = [{"id": option["id"], "label": option["label"]} for option in question.get("options", [])]
        if question["type"] == "scale":
            payload.update({
                "min": question.get("min", 1),
                "max": question.get("max", 100),
                "step": question.get("step", 1),
                "leftLabel": question.get("leftLabel", ""),
                "rightLabel": question.get("rightLabel", ""),
            })
        return payload

    def build_result(self, profile: List[float], probabilities: List[float], answered_count: int) -> Dict[str, Any]:
        matches = self.build_profession_matches(profile, probabilities)
        primary = matches[0]
        profession = next(item for item in PROFESSIONS if item["id"] == primary["id"])
        trait_items = [
            {
                "key": dimension,
                "label": DIMENSION_LABELS[dimension],
                "value": round(profile[index] * 100),
                "description": self.trait_description(dimension, profile[index]),
            }
            for index, dimension in enumerate(DIMENSION_KEYS)
        ]
        top_traits = sorted(trait_items, key=lambda item: item["value"], reverse=True)[:4]

        return {
            "primaryProfession": profession["name"],
            "summary": self.result_summary(profession, top_traits, answered_count),
            "professionMatches": matches[:6],
            "traits": trait_items,
            "charts": {
                "interestRose": [item for item in trait_items if item["key"] in {"practical", "analytical", "social", "creative", "enterprising", "conventional"}],
                "workStyle": [item for item in trait_items if item["key"] in {"digital", "science", "care", "risk", "autonomy", "learning"}],
                "professionFit": [{"key": item["id"], "label": item["profession"], "value": item["score"]} for item in matches[:6]],
            },
            "guidance": self.guidance_for(profession, top_traits),
            "facts": self.facts_for(profession, trait_items),
        }

    def build_profession_matches(self, profile: List[float], probabilities: List[float]) -> List[Dict[str, Any]]:
        rows = []
        max_probability = max(probabilities) or 1.0
        for index, profession in enumerate(PROFESSIONS):
            vector = PROFESSION_VECTORS[index]
            distance = math.sqrt(sum((left - right) ** 2 for left, right in zip(profile, vector)) / len(profile))
            similarity = clamp(1.0 - distance)
            score = round((((probabilities[index] / max_probability) * 0.54) + (similarity * 0.46)) * 100)
            rows.append({
                "id": profession["id"],
                "profession": profession["name"],
                "score": max(1, min(100, score)),
                "reason": profession["description"],
            })
        rows.sort(key=lambda item: item["score"], reverse=True)
        return rows

    def result_summary(self, profession: Dict[str, Any], top_traits: List[Dict[str, Any]], answered_count: int) -> str:
        trait_text = ", ".join(item["label"].lower() for item in top_traits[:3])
        return (
            f"Специальный алгоритм сравнил ваш профиль с {len(PROFESSIONS)} профессиограммами "
            f"и после {answered_count} ответов выделил направление: {profession['name']}. "
            f"Главные признаки профиля: {trait_text}. {profession['description']}"
        )

    def guidance_for(self, profession: Dict[str, Any], top_traits: List[Dict[str, Any]]) -> List[str]:
        first_trait = top_traits[0]["label"].lower()
        return [
            f"Проверьте направление через короткий проект или профпробу, где главный акцент - {first_trait}.",
            f"Подходящие образовательные траектории: {profession['education']}.",
            f"Зона риска: {profession['risk']}.",
            "Сравните первые три профессии из рейтинга: если две из них одинаково привлекательны, выбирайте обучение с общей базой навыков.",
        ]

    def facts_for(self, profession: Dict[str, Any], traits: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        trait_map = {item["key"]: item for item in traits}
        work_mode = "самостоятельная экспертная работа" if trait_map["autonomy"]["value"] >= 62 else "работа с понятной структурой и регулярной обратной связью"
        environment = "динамичная среда" if trait_map["risk"]["value"] >= 62 else "предсказуемая среда с управляемой нагрузкой"
        learning = "быстрое обновление навыков" if trait_map["learning"]["value"] >= 65 else "постепенное углубление в выбранную область"
        return [
            {"label": "Лучший формат работы", "value": work_mode},
            {"label": "Комфортная среда", "value": environment},
            {"label": "Как развиваться", "value": learning},
            {"label": "Что проверить перед выбором", "value": profession["risk"]},
        ]

    def trait_description(self, dimension: str, value: float) -> str:
        level = "высокая" if value >= 0.66 else "средняя" if value >= 0.45 else "низкая"
        return f"{level.capitalize()} выраженность направления «{DIMENSION_LABELS[dimension]}»."


engine = CareerAiEngine()

app = FastAPI(title="Career Guidance Service", version="1.0.0")

origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3033,http://127.0.0.1:3033").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "selector": "adaptive-career-algorithm",
        "professions": len(PROFESSIONS),
        "questions": len(QUESTION_BANK),
        "minQuestions": MIN_QUESTIONS,
        "maxQuestions": MAX_QUESTIONS,
    }


@app.post("/career-test/next")
def next_question(payload: NextRequest) -> Dict[str, Any]:
    return engine.next_step(payload.answers)


@app.post("/career-test/result")
def result(payload: NextRequest) -> Dict[str, Any]:
    normalized_answers = engine.normalize_answers(payload.answers)
    profile = engine.build_profile(normalized_answers)
    probabilities = engine.probabilities(profile)
    return engine.build_result(profile, probabilities, len(normalized_answers))
