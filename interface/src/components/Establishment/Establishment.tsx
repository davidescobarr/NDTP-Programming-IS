import * as React from 'react';
import {App} from "@pages/../App";

export const Establishment = ({ idEstablishment, name, description, photo }) => {
    return (
        <div className="card_establishment" id={idEstablishment}>
            <img src={photo} alt="establishment" />
            <div className="establishment-description">
                <h2>{name}</h2>
                <p>{description}</p>
                <button className="btn_establishment" onClick={() => {

                }}>Подробнее
                </button>
            </div>
        </div>
    );
};