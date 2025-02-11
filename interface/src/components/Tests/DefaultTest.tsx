import * as React from 'react';
import {useState} from "react";
import {useModal} from "@model/ModalContext";
import './test.css';

export const DefaultTest = ({questions}) => {
    const [numberQuestions, setNumberQuestions] = useState(0);
    const { closeModal } = useModal();

    return (
        <div className="test-content">
            <h1>{
                questions[numberQuestions]['display_name']
            }</h1>
            {
                questions[numberQuestions]['answers'].map((answer) => {
                    return (
                    <button onClick={() => {
                        questions[numberQuestions]['answer'] = answer['id'];
                        if(numberQuestions + 1 >= questions.length) {
                            alert(JSON.stringify(questions));
                            closeModal();
                        } else {
                            setNumberQuestions(numberQuestions + 1);
                        }
                    }}>
                        {answer['name']}
                    </button>);
                })
            }
        </div>
    );
}