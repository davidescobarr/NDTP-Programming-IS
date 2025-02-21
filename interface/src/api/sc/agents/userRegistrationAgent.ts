import { client } from '@api/sc';
import { ScAddr, ScConstruction, ScLinkContent, ScTemplate, ScType, ScLinkContentType, sc_type_arc_pos_const_perm } from 'ts-sc-client';
import { makeAgent } from '@api/sc/agents/makeAgent';
import { createAction } from '@reduxjs/toolkit';

const question = 'question';
const questionInitiated = 'question_initiated';
const questionFinished = 'question_finished';
const nrelAnswer = 'nrel_answer';
const actionUserRegistrationAgent = 'action_user_registration_agent';

const rrel1 = 'rrel_1';
const rrel2 = 'rrel_2';
const rrel3 = 'rrel_3';
const rrel4 = 'rrel_4';
const rrel5 = 'rrel_5';
const langEn = 'lang_en';
const langRu = 'lang_ru';
const answer = 'nrel_answer';


const baseKeynodes = [
    { id: question, type: ScType.NodeConstClass },
    { id: questionInitiated, type: ScType.NodeConstClass },
    { id: actionUserRegistrationAgent, type: ScType.NodeConstClass },
    { id: questionFinished, type: ScType.NodeConstClass },
    { id: rrel1, type: ScType.NodeConstRole},
    { id: rrel2, type: ScType.NodeConstRole},
    { id: rrel3, type: ScType.NodeConstRole},
    { id: rrel4, type: ScType.NodeConstRole},
    { id: rrel5, type: ScType.NodeConstRole},
];

// вызывает работу агента путём создания двух классов необходимых для запуска(33, 34 строки)
const describeAgent = async (
    keynodes: Record<string, ScAddr>,
    nickname: string,
    firstname: string,
    surname: string,
    patronymic: string,
    password: string
) => {
    const actionNodeAlias = '_action_node';

    const construction = new ScConstruction();
    construction.createLink(ScType.LinkConst, new ScLinkContent(nickname, ScLinkContentType.String), "nickname");
    construction.createLink(ScType.LinkConst, new ScLinkContent(firstname, ScLinkContentType.String), "firstname");
    construction.createLink(ScType.LinkConst, new ScLinkContent(surname, ScLinkContentType.String), "surname");
    construction.createLink(ScType.LinkConst, new ScLinkContent(patronymic, ScLinkContentType.String), "patronymic");
    construction.createLink(ScType.LinkConst, new ScLinkContent(password, ScLinkContentType.String), "password");
    const links = await client.createElements(construction);
    const template = new ScTemplate();

    template.triple(keynodes[question], ScType.EdgeAccessVarPosPerm, [ScType.NodeVar, actionNodeAlias]); //
    template.triple(keynodes[actionUserRegistrationAgent], ScType.EdgeAccessVarPosPerm, actionNodeAlias); //

    template.tripleWithRelation(actionNodeAlias, ScType.EdgeAccessVarPosPerm, links[construction.getIndex("nickname")], ScType.EdgeAccessVarPosPerm, keynodes["rrel_1"]);
    template.tripleWithRelation(actionNodeAlias, ScType.EdgeAccessVarPosPerm, links[construction.getIndex("firstname")], ScType.EdgeAccessVarPosPerm, keynodes["rrel_2"]);
    template.tripleWithRelation(actionNodeAlias, ScType.EdgeAccessVarPosPerm, links[construction.getIndex("surname")], ScType.EdgeAccessVarPosPerm, keynodes["rrel_3"]);
    template.tripleWithRelation(actionNodeAlias, ScType.EdgeAccessVarPosPerm, links[construction.getIndex("patronymic")], ScType.EdgeAccessVarPosPerm, keynodes["rrel_4"]);
    template.tripleWithRelation(actionNodeAlias, ScType.EdgeAccessVarPosPerm, links[construction.getIndex("password")], ScType.EdgeAccessVarPosPerm, keynodes["rrel_5"]);

    return [template, actionNodeAlias] as const;
};

// Вызывать при необходимости вызвать агента
export const registerUser = async (nickname, firstname, surname, patronymic, password) => {
    const keynodes = await client.resolveKeynodes(baseKeynodes);
    console.log("Resolve call");

    const [template, userActionNodeAlias] = await describeAgent(keynodes, nickname, firstname, surname, patronymic, password);
    console.log("DescribeAgent call");

    const circuitAddr = await makeAgent(template, userActionNodeAlias);
    console.log("Make call");
    console.log(circuitAddr);
    const user_data = "user_data";

    if (!circuitAddr) return;

    template.triple(circuitAddr, ScType.EdgeAccessVarPosPerm, [ScType.NodeVar, user_data]);
    const resultNode = await client.templateSearch(template);
    console.log(resultNode);

    if (resultNode.length) {
        const user = resultNode[0].get(user_data);
        console.log(user);
        if (user) {
            localStorage.setItem("nickname", nickname);
            localStorage.setItem("password", password);
            return user;
        }
    }
    return null;
};