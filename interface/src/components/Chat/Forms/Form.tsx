import { useCallback, useEffect, useState, FormEvent } from 'react';
import { client } from '@api/sc/client';
import * as React from 'react';
import './form.css';
import { ScAddr, ScConstruction, ScTemplate, ScType } from 'ts-sc-client';
import { number } from 'prop-types';
import { Question } from './Question';
import {useModal} from "@model/ModalContext";
import {SearchProfession} from "@agents/searchProfessionAgent";
const { Component, Fragment } = React
const rootNode = document.getElementById('app')

export const FormPanelComponent = () => {
    const { closeModal } = useModal();

    return FormPanel({closeModal});
}

export const FormPanel = ({closeModal}) => {
    const [test, setTest] = useState(false)

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData(event.target as HTMLFormElement);
        const selectedOptions = Array.from(formData.getAll('options')).map(option => option.toString());
        
        const concept_human_id = "concept_human";
        const nrel_skills = "nrel_skills";
        const concept_skill = "concept_skill";
        const nrel_system_identifier = "nrel_system_identifier";

        const keynodes = [
            {
                id: concept_human_id, type: ScType.NodeConstClass
            },
            {
                id: nrel_skills, type: ScType.NodeConstNoRole
            },
            {
                id: concept_skill, type: ScType.NodeConstClass
            },
            {
                id: nrel_system_identifier, type: ScType.NodeConstNoRole
            }
        ];

        const res = await client.resolveKeynodes(keynodes);

        var template = new ScTemplate();

        template.triple(res[concept_human_id], ScType.EdgeAccessVarPosPerm, [ScType.Node, "_node"]);

        const res_human = await client.templateSearch(template);

        template = new ScTemplate();

        template.tripleWithRelation(
            res_human[0].get("_node"),
            [ScType.EdgeDCommonVar, "_edge_common"],
            [ScType.NodeVar, "_node"],
            ScType.EdgeAccessVarPosPerm,
            [res[nrel_skills], "_edge_relation"]
        );

        var res_skills = await client.templateSearch(template);

        for (const element of res_skills) {
            const res_delete = await client.deleteElements([element.get("_edge_common")]);
        };

        template = new ScTemplate();

        template.triple(
            res[concept_skill],
            ScType.EdgeAccessVarPosPerm,
            [ScType.Node, "_node"]
        )

        res_skills = await client.templateSearch(template);

        var skill_names = new Map<ScAddr, String>();

        for (const skill of res_skills) {
            template = new ScTemplate();

            template.tripleWithRelation(
                skill.get("_node"),
                ScType.EdgeDCommonVar,
                (ScType.LinkConst, "_link"),
                ScType.EdgeAccessVarPosPerm,
                nrel_system_identifier
            );

            const res_id = await client.templateSearch(template);

            const res = await client.getLinkContents([res_id[0].get("_link")]);
            
            skill_names.set(skill.get("_node"), res[0]['_data']);
        };

        var skills_for_connect:ScAddr[];
        skills_for_connect = []
        
        selectedOptions.forEach(option => {
            skill_names.forEach((link_concent, scaddr) => {
                if(link_concent === option) {
                    skills_for_connect.push(scaddr);
                }
            })
        });

        for(const skill of skills_for_connect) {
            const construction = new ScConstruction();

            construction.createEdge(
                ScType.EdgeDCommonConst,
                res_human[0].get("_node"),
                skill,
                "_edge_skill"
            );

            construction.createEdge(
                ScType.EdgeAccessConstPosPerm,
                res[nrel_skills],
                "_edge_skill",
                "_edge_relation"
            );

            const finally_res = await client.createElements(construction)

            setTest(true)
        };
        
        const formElement = event.target as HTMLFormElement;
        const checkboxes = formElement.querySelectorAll('input[name="options"]');
        checkboxes.forEach((checkbox) => {
            if (checkbox instanceof HTMLInputElement) {
                checkbox.checked = false;
            }
        });
    };

    async function endTest() {
        closeModal();
        console.log("it works"); // to do calling agent ts and py

        try {
            const resultText = await SearchProfession();

            console.log("Всё в порядке", resultText);
            //openModal(endTestTestComponent, { text: resultText.text, closeModal });
        } catch (error) {
            console.error("Ошибка при анализе профориентацинного теста:", error);
            //openModal(endTestTestComponent, { text: "Ошибка при обработке теста", closeModal });
        }

        setTest(false);
    }

    return (
        (test ?
                <Question endTest={endTest}>
                    <p></p>
                </Question>
            :
        <div className='form__traits'>
            <p className='text__about__trait'>Выберите свои черты характера</p>
            <form onSubmit={handleSubmit}>
            <div className='in__form__block'>
                <div>
                    <article>
                        <input type="checkbox" name="options" value="creative_thinking" id="creative_thinking" />
                        <label htmlFor="creative_thinking">Творческое мышление</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="attention_to_detail" id="attention_to_detail" />
                        <label htmlFor="attention_to_detail">Внимание к деталям</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="patience" id="patience" />
                        <label htmlFor="patience">Терпеливость</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="responsibility" id="responsibility" />
                        <label htmlFor="responsibility">Ответственность</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="communicativeness" id="communicativeness" />
                        <label htmlFor="communicativeness">Коммуникативность</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="physical_endurance" id="physical_endurance" />
                        <label htmlFor="physical_endurance">Физическая выносливость</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="accuracy" id="accuracy" />
                        <label htmlFor="accuracy">Точность</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="efficiency" id="efficiency" />
                        <label htmlFor="efficiency">Работоспособность</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="attention_to_safety" id="attention_to_safety" />
                        <label htmlFor="attention_to_safety">Внимание к безопасности</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="compassion" id="compassion" />
                        <label htmlFor="compassion">Сострадание</label>
                    </article>
               </div>
                <div>
                    <article>
                        <input type="checkbox" name="options" value="stress_resistance" id="stress_resistance" />
                        <label htmlFor="stress_resistance">Стрессоустойчивость</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="organization" id="organization" />
                        <label htmlFor="organization">Организованность</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="logical_thinking" id="logical_thinking" />
                        <label htmlFor="logical_thinking">Логическое мышление</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="bravery" id="bravery" />
                        <label htmlFor="bravery">Храбрость</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="team_spirit" id="team_spirit" />
                        <label htmlFor="team_spirit">Командный дух</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="analytical_thinking" id="analytical_thinking" />
                        <label htmlFor="analytical_thinking">Аналитическое мышление</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="creativity" id="creativity" />
                        <label htmlFor="creativity">Креативность</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="empathy" id="empathy" />
                        <label htmlFor="empathy">Эмпатия</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="polite" id="polite" />
                        <label htmlFor="polite">Вежливость</label>
                    </article>
                    <article>
                        <input type="checkbox" name="options" value="perseverance" id="perseverance" />
                        <label htmlFor="perseverance">Упорство</label>
                    </article>
                </div>
            </div>
            <input type="submit" className='button__next' value={'Далее'}/>
            </form>
        </div>
        )
    );
}