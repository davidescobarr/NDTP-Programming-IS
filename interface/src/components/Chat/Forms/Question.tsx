import './question.css';
import { client } from '@api/sc/client';
import * as React from 'react';
import { ScAddr, ScConstruction, ScTemplate, ScType } from 'ts-sc-client';
import { useCallback, useEffect, useState } from 'react';

export const Question = ({endTest}) => {
    const [questionNumber, setQuestionNumber] = useState(1);
    const external_questions = new Map<String, String>();

    external_questions.set("question1", "Вы любите рисовать?");
    external_questions.set("question2", "Вы умеете работать с инструментами?");
    external_questions.set("question3", "Вам нравится помогать людям?");
    external_questions.set("question4", "Вы любите готовить еду?");
    external_questions.set("question5", "Вы хорошо разбираетесь в компьютерах?");
    external_questions.set("question6", "Вы любите учить других людей?");
    external_questions.set("question7", "Вы спокойно реагируете на экстренные ситуации?");
    external_questions.set("question8", "Вам нравится проектировать и придумывать новые решения?");
    external_questions.set("question9", "Вы готовы к физически тяжёлой работе?");
    external_questions.set("question10", "Вы любите работать с детьми?");
    external_questions.set("question11", "Вам нравится анализировать поведение людей?");
    external_questions.set("question12", "Вам интересны законы и правовые вопросы?");
    external_questions.set("question13", "Вы легко находите общий язык с разными людьми?");

    const answerYes = async (event: React.FormEvent<HTMLFormElement>) => {
        connectSkillByName("question" + questionNumber)
        nextQuestion()
    };

    const answerNo = async (event: React.FormEvent<HTMLFormElement>) => {
        nextQuestion()
    };

    async function connectSkillByName(name) {
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

        template.triple(
            res[concept_skill],
            ScType.EdgeAccessVarPosPerm,
            [ScType.Node, "_node"]
        )

        const res_skills = await client.templateSearch(template);

        var skill_names = new Map<String, ScAddr>();

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
            
            skill_names.set(res[0]['_data'], skill.get("_node"));
        };

        var skill = skill_names.get(name);

        if(skill instanceof ScAddr) {
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

            const finally_res = await client.createElements(construction);
        }
    };

    function nextQuestion() {
        setQuestionNumber(questionNumber + 1);
        if(questionNumber >= external_questions.size) {
            setQuestionNumber(1)
            endTest();
        }
    };

    return (
        <div>
            <p>{external_questions.get("question" + questionNumber)}</p>
            <button onClick={() => answerYes}>Да</button>
            <button onClick={() => answerNo}>Нет</button>
        </div>
    );
};