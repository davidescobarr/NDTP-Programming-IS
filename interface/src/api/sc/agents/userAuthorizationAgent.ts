import { client } from '@api/sc';
import { ScAddr, ScConstruction, ScLinkContent, ScTemplate, ScType, ScLinkContentType, sc_type_arc_pos_const_perm } from 'ts-sc-client';
import { makeAgent } from '@api/sc/agents/makeAgent';

const question = 'question';
const questionInitiated = 'question_initiated';
const questionFinished = 'question_finished';
const nrelAnswer = 'nrel_answer';
const actionUserAuthAgent = 'action_user_authorization_agent';

const rrelNickname = 'rrel_1';
const rrelPassword = 'rrel_2';
const userNode = 'user_node';

const baseKeynodes = [
    { id: question, type: ScType.NodeConstClass },
    { id: questionInitiated, type: ScType.NodeConstClass },
    { id: actionUserAuthAgent, type: ScType.NodeConstClass },
    { id: questionFinished, type: ScType.NodeConstClass },
    { id: rrelNickname, type: ScType.NodeConstRole },
    { id: rrelPassword, type: ScType.NodeConstRole },
];

// Описывает работу агента авторизации
const describeAgent = async (keynodes: Record<string, ScAddr>, nickname: string, password: string) => {
    const actionNodeAlias = '_action_node';

    const construction = new ScConstruction();
    construction.createLink(ScType.LinkConst, new ScLinkContent(nickname, ScLinkContentType.String), "nickname");
    construction.createLink(ScType.LinkConst, new ScLinkContent(password, ScLinkContentType.String), "password");
    const links = await client.createElements(construction);

    const template = new ScTemplate();

    template.triple(keynodes[question], ScType.EdgeAccessVarPosPerm, [ScType.NodeVar, actionNodeAlias]);
    template.triple(keynodes[actionUserAuthAgent], ScType.EdgeAccessVarPosPerm, actionNodeAlias);

    template.tripleWithRelation(actionNodeAlias, ScType.EdgeAccessVarPosPerm, links[construction.getIndex("nickname")], ScType.EdgeAccessVarPosPerm, keynodes[rrelNickname]);
    template.tripleWithRelation(actionNodeAlias, ScType.EdgeAccessVarPosPerm, links[construction.getIndex("password")], ScType.EdgeAccessVarPosPerm, keynodes[rrelPassword]);

    return [template, actionNodeAlias] as const;
};

// Функция авторизации пользователя
export const authenticateUser = async (nickname: string, password: string) => {
    const keynodes = await client.resolveKeynodes(baseKeynodes);
    console.log("Resolve call");

    const [template, userActionNodeAlias] = await describeAgent(keynodes, nickname, password);
    console.log("DescribeAgent call");

    const circuitAddr = await makeAgent(template, userActionNodeAlias);
    console.log("Make call");
    console.log(circuitAddr);
    const user_data = "user_data";

    if (!circuitAddr) return null;

    template.triple(circuitAddr, ScType.EdgeAccessVarPosPerm, [ScType.NodeVar, user_data]);
    const resultNode = await client.templateSearch(template);
    console.log(resultNode);

    if (resultNode.length) {
        const user = resultNode[0].get(user_data);
        if (user) {
            console.log(user);
            return user;
        }
    }
    return null;
};
