import * as React from 'react';
import {useEffect, useState} from "react";
import {useModal} from "@model/ModalContext";
import { StaticQuestion, StaticTestDefinition } from "@model/staticTests";
import './test.css';

const cloneQuestions = (questions: StaticQuestion[]) =>
    questions.map((question) => ({
        ...question,
        answer: undefined,
        answers: question.answers.map((answer) => ({ ...answer })),
    }));

export const DefaultTest = ({ test, onEnd }: { test: StaticTestDefinition; onEnd: any }) => {
    const [numberQuestions, setNumberQuestions] = useState(0);
    const [questions, setQuestions] = useState<StaticQuestion[]>(() => cloneQuestions(test.questions));
    const { closeModal, openModal } = useModal();

    useEffect(() => {
        setNumberQuestions(0);
        setQuestions(cloneQuestions(test.questions));
    }, [test.id, test.questions]);

    if (!questions.length) {
        return (
            <div className="test-content">
                <h1>Тест временно недоступен</h1>
                <button onClick={() => closeModal()}>Закрыть</button>
            </div>
        );
    }

    const currentQuestion = questions[numberQuestions];

    return (
        <div className="test-content">
            <p className="test-progress">Вопрос {numberQuestions + 1} из {questions.length}</p>
            <h1>{currentQuestion.display_name}</h1>
            {currentQuestion.answers.map((answer) => {
                return (
                    <button
                        key={answer.id}
                        onClick={() => {
                            const nextQuestions = questions.map((question, index) =>
                                index === numberQuestions ? { ...question, answer: answer.id } : question
                            );
                            setQuestions(nextQuestions);

                            if (numberQuestions + 1 >= questions.length) {
                                onEnd({ test, questions: nextQuestions, closeModal, openModal });
                            } else {
                                setNumberQuestions(numberQuestions + 1);
                            }
                        }}
                    >
                        {answer.name}
                    </button>
                );
            })}
        </div>
    );
}
