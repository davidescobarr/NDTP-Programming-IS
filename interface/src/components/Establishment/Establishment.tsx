import * as React from 'react';

export const Establishment = ({ idEstablishment, name, description, photo }) => {
    return (
        <div className="card_establishment" id={idEstablishment}>
            <img src={photo} alt="establishment" />
            <div className="establishment-description">
                <h2>{name}</h2>
                <p>{description}</p>
            </div>
        </div>
    );
};