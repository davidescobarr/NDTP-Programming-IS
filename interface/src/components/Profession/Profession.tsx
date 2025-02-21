import * as React from 'react';
import FadeInSection from "@components/FadeInSection/FadeInSection";

export const Profession = ({ idProfession, name, description, photo }) => {
    return (
        <FadeInSection>
            <div className="card_profession" id={idProfession}>
                <img src={photo} alt="profession"/>
                <div className="profession-description">
                    <h2>{name}</h2>
                    <p>{description}</p>
                </div>
            </div>
        </FadeInSection>
    );
};