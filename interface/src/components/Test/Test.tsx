import * as React from 'react';
import {useModal} from "@model/ModalContext";
import FadeInSection from "@components/FadeInSection/FadeInSection";

export const Test = ({ idTest, name, description, photo, componentTest, propsTest }) => {
    const { openModal } = useModal();

    return (
        <FadeInSection>
            <div className="card_profession" id={idTest}>
                <img src={photo} alt="profession"/>
                <div className="profession-description">
                    <h2>{name}</h2>
                    <p>{description}</p>
                    <button className="btn_profession" onClick={() => {
                        openModal(componentTest, propsTest);
                    }}>Пройти тест
                    </button>
                </div>
            </div>
        </FadeInSection>
    );
};