import * as React from 'react';
import {Profession} from "@components/Profession";
import {getProfessionsWithDescriptionsAgent} from "@agents/getProfessionsAndDescriptionsAgent";
import {Test} from "@components/Test";

const bsuir = require('@assets/img/establishment_bsuir.png')

export const Tests = () => {
    return (
        <div className="main">
            <section className="establishments">
                <div className="section-content">
                    <h1 className="title">Тесты</h1>
                    <div className="professions-list">
                        <Test name="test" description="description" idProfession="test" photo={bsuir}/>
                    </div>
                </div>
            </section>
        </div>
    );
}