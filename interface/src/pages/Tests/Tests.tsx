import * as React from 'react';
import {Profession} from "@components/Profession";
import {getProfessionsWithDescriptionsAgent} from "@agents/getProfessionsAndDescriptionsAgent";
import {Test} from "@components/Test";
import {DefaultTest} from "@components/Tests/DefaultTest";
import {FormPanelComponent} from "@components/Chat/Forms/Form";

const bsuir = require('@assets/img/establishment_bsuir.png')

export const Tests = () => {
    return (
        <div className="main">
            <section className="establishments">
                <div className="section-content">
                    <h1 className="title">Тесты</h1>
                    <div className="professions-list">
                        <Test name="test" description="description" idTest="test" photo={bsuir} componentTest={DefaultTest} propsTest={{
                            questions: [
                                {
                                    'display_name': 'Как вы относитесь к животным?',
                                    'answers': [
                                        {
                                            'name': 'Хорошо',
                                            'id': 0
                                        },
                                        {
                                            'name': 'Нормально',
                                            'id': 1
                                        },
                                        {
                                            'name': 'Плохо',
                                            "id": 2
                                        }
                                    ]
                                },
                                {
                                    'display_name': 'Как часто вы занимаетесь спортом?',
                                    'answers': [
                                        {
                                            'name': 'Часто',
                                            'id': 0
                                        },
                                        {
                                            'name': 'Достаточно',
                                            'id': 1
                                        },
                                        {
                                            'name': 'Иногда',
                                            'id': 2
                                        },
                                        {
                                            'name': 'Редко',
                                            'id': 3
                                        }
                                    ]}
                            ]
                        }}/>
                        <Test name="Профориентационный тест" description="Пройдя данный тест вы сможете определить свою профессию." idTest="test" photo={bsuir} componentTest={FormPanelComponent} propsTest={{}}/>
                    </div>
                </div>
            </section>
        </div>
    );
}