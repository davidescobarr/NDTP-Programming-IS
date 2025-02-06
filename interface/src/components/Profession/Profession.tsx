import * as React from 'react';

export const Profession = ({ idProfession, name, description, photo }) => {
    return (
        <div className="card_profession" id={idProfession}>
            <img src={photo} alt="profession" />
            <div className="profession-description">
                <h2>{name}</h2>
                <p>{description}</p>
                <button className="btn_profession" onClick={() => {
                }}>Подробнее
                </button>
            </div>
        </div>
    );
};