import * as React from 'react';
import {useModal} from "@model/ModalContext";
import {FooterPanel} from "@components/Footer";

export const Test = ({ idTest, name, description, photo }) => {
    const { openModal } = useModal();

    return (
        <div className="card_profession" id={idTest}>
            <img src={photo} alt="profession" />
            <div className="profession-description">
                <h2>{name}</h2>
                <p>{description}</p>
                <button className="btn_profession" onClick={() => {
                    openModal(FooterPanel, null);
                }}>Пройти тест
                </button>
            </div>
        </div>
    );
};