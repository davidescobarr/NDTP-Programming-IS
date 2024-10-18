import { client } from '@api/sc/client';
import * as React from 'react';
import { ScAddr, ScConstruction, ScEventParams, ScEventType, ScLinkContent, ScTemplate, ScType } from 'ts-sc-client';

export const FormPanel = (props:any) => {
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

        console.log(res_skills)

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
        };
    };

    return (
        <form onSubmit={handleSubmit}>
            <select name="options" multiple={true}>
            <option value="creative_thinking">Творческое мышление </option>
<option value="attention_to_detail">Внимание к деталям </option>
<option value="patience">Терпеливость</option>
<option value="responsibility">Ответственность</option>
<option value="communicativeness">Коммуникативность</option>
<option value="physical_endurance">Физическая выносливость</option>
<option value="accuracy">Точность</option>
<option value="efficiency">Работоспособность</option>
<option value="attention_to_safety">Внимание к безопасности</option>
<option value="compassion">Сострадание</option>
<option value="stress_resistance">Стрессоустойчивость</option>
<option value="organization">Организованность</option>
<option value="logical_thinking">Логическое мышление</option>
<option value="bravery">Храбрость</option>
<option value="team_spirit">Командный дух</option>
<option value="analytical_thinking">Аналитическое мышление</option>
<option value="creativity">Креативность</option>
<option value="empathy">Эмпатия</option>
<option value="polite">Вежливость</option>
<option value="perseverance">Упорство</option>
            </select>
            <input type="submit"/>
        </form>
    );
}
