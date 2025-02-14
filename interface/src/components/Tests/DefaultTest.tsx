import * as React from 'react';
import {useState} from "react";
import {useModal} from "@model/ModalContext";
import './test.css';

export const DefaultTest = (array) => {
    const [numberQuestions, setNumberQuestions] = useState(0);
    const { closeModal, openModal } = useModal();

    if(array.length === 0) {
        return (
          <h1>
              ошибка
          </h1>
        );
    }
    const questions = array[0].questions;
    let functionEndTest = ({questions, closeModal, openModal}) => {};
    if(array.length > 1) {
        functionEndTest = array[1];
    }

    return (
        <div className="test-content">
            <h1>{questions[numberQuestions]['display_name']}</h1>
            {questions[numberQuestions]['answers'].map((answer) => {
                return (
                    <button
                        onClick={() => {
                            questions[numberQuestions]['answer'] = answer['id'];
                            if (numberQuestions + 1 >= questions.length) {
                                functionEndTest({questions, closeModal, openModal});
                            } else {
                                setNumberQuestions(numberQuestions + 1);
                            }
                        }}
                    >
                        {answer['name']}
                    </button>
                );
            })}
        </div>
    );
}