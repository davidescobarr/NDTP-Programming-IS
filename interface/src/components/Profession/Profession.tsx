import * as React from 'react';
import {useModal} from "@model/ModalContext";
import Registration from "@pages/Registration";
import {HeaderPanel} from "@components/Header";
import {FooterPanel} from "@components/Footer";

export const Profession = ({ idProfession, name, description, photo }) => {
    const { openModal } = useModal();


export const Profession = ({ idProfession, name, description, photo }) => {
    return (
        <div className="card_profession" id={idProfession}>
            <img src={photo} alt="profession" />
            <div className="profession-description">
                <h2>{name}</h2>
                <p>{description}</p>
                <button className="btn_profession" onClick={() => {
                    openModal(FooterPanel, null)
                }}>Подробнее
                </button>
            </div>
        </div>
    );
};