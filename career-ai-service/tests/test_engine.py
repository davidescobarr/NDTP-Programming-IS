import unittest
from typing import Any, Dict, Iterable, List, Sequence, Set

from app.main import (
    AnswerInput,
    DIMENSION_KEYS,
    MAX_QUESTIONS,
    MIN_QUESTIONS,
    PROFESSIONS,
    PROFESSION_VECTORS,
    QUESTION_BANK,
    clamp,
    engine,
)


def profession_index(profession_id: str) -> int:
    return next(index for index, profession in enumerate(PROFESSIONS) if profession["id"] == profession_id)


def top_match_ids(profile: List[float], limit: int = 6) -> List[str]:
    probabilities = engine.probabilities(profile)
    matches = engine.build_profession_matches(profile, probabilities)
    return [match["id"] for match in matches[:limit]]


def option_score(option: Dict[str, Any], target_vector: Sequence[float]) -> float:
    score = 0.0
    total_weight = 0.0
    for dimension, weight in option.get("weights", {}).items():
        dimension_value = target_vector[DIMENSION_KEYS.index(dimension)]
        numeric_weight = abs(float(weight))
        score += numeric_weight * (dimension_value if weight >= 0 else 1.0 - dimension_value)
        total_weight += numeric_weight
    return score / max(total_weight, 1.0)


def answer_for_target(question: Dict[str, Any], target_vector: Sequence[float]) -> Any:
    if question["type"] == "scale":
        weighted = []
        for dimension, direction in question.get("weights", {}).items():
            dimension_value = target_vector[DIMENSION_KEYS.index(dimension)]
            weighted.append(dimension_value if direction >= 0 else 1.0 - dimension_value)
        value = sum(weighted) / max(len(weighted), 1)
        minimum = float(question.get("min", 1))
        maximum = float(question.get("max", 100))
        return round(minimum + (clamp(value) * (maximum - minimum)))

    options = list(question.get("options", []))
    ranked = sorted(options, key=lambda option: option_score(option, target_vector), reverse=True)
    if question["type"] == "multi":
        selected = ranked[:3]
        return [option["id"] for option in selected]

    return ranked[0]["id"]


def run_adaptive_flow(target_profession_id: str) -> Dict[str, Any]:
    target_vector = PROFESSION_VECTORS[profession_index(target_profession_id)]
    answers: List[AnswerInput] = []
    seen_questions: Set[str] = set()

    for _ in range(MAX_QUESTIONS + 2):
        step = engine.next_step(answers)
        if step["done"]:
            return {"step": step, "seen": seen_questions}

        question_id = step["question"]["id"]
        if question_id in seen_questions:
            raise AssertionError(f"Question {question_id} was repeated")
        seen_questions.add(question_id)
        full_question = engine.questions[question_id]
        answers.append(AnswerInput(question_id=question_id, value=answer_for_target(full_question, target_vector)))

    raise AssertionError("Adaptive flow did not finish")


class CareerEngineQualityTest(unittest.TestCase):
    def test_profession_and_question_bases_are_broad(self) -> None:
        self.assertGreaterEqual(len(PROFESSIONS), 60)
        self.assertGreaterEqual(len(QUESTION_BANK), 65)
        self.assertEqual(MAX_QUESTIONS, 15)

    def test_model_classifies_builtin_professiograms(self) -> None:
        correct = 0
        for profession, vector in zip(PROFESSIONS, PROFESSION_VECTORS):
            if top_match_ids(vector, limit=1)[0] == profession["id"]:
                correct += 1

        accuracy = correct / len(PROFESSIONS)
        self.assertGreaterEqual(accuracy, 0.9)

    def test_archetype_profiles_land_in_expected_clusters(self) -> None:
        cases = [
            ("ml_engineer", {"ml_engineer", "data_engineer", "software_engineer", "backend_developer", "researcher"}),
            ("doctor", {"doctor", "dentist", "nurse", "laboratory_diagnostician", "physiotherapist"}),
            ("3d_artist", {"3d_artist", "motion_designer", "video_editor", "game_designer", "interior_designer"}),
            ("business_analyst", {"business_analyst", "systems_analyst", "product_manager", "project_manager", "operations_manager"}),
            ("pilot", {"pilot", "rescue_specialist", "network_engineer", "civil_engineer", "quality_manager"}),
        ]

        for profession_id, expected_cluster in cases:
            with self.subTest(profession_id=profession_id):
                vector = PROFESSION_VECTORS[profession_index(profession_id)]
                self.assertTrue(set(top_match_ids(vector)).intersection(expected_cluster))

    def test_adaptive_flow_finishes_without_repeats_and_with_reasonable_match(self) -> None:
        cases = [
            ("backend_developer", {"backend_developer", "software_engineer", "data_engineer", "devops_engineer"}),
            ("physiotherapist", {"physiotherapist", "doctor", "nurse", "dentist", "social_worker"}),
            ("quality_manager", {"quality_manager", "operations_manager", "accountant", "logistics", "procurement_specialist"}),
        ]

        for profession_id, expected_cluster in cases:
            with self.subTest(profession_id=profession_id):
                flow = run_adaptive_flow(profession_id)
                step = flow["step"]
                result_ids = {match["id"] for match in step["result"]["professionMatches"]}
                self.assertTrue(step["done"])
                self.assertLessEqual(step["answeredCount"], MAX_QUESTIONS)
                self.assertGreaterEqual(step["answeredCount"], MIN_QUESTIONS)
                self.assertEqual(len(flow["seen"]), step["answeredCount"])
                self.assertTrue(result_ids.intersection(expected_cluster))


if __name__ == "__main__":
    unittest.main()
