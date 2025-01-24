import { client } from '@api/sc';
import { ScAddr, ScConstruction, ScLinkContent, ScTemplate, ScType, ScLinkContentType } from 'ts-sc-client';
import { makeAgent } from '@api/sc/agents/makeAgent';

const question = 'question';
const questionInitiated = 'question_initiated';
const questionFinished = 'question_finished';
const nrelAnswer = 'nrel_answer';
const actionGetEstablishmentsWithDescriptionsAgent = 'action_get_estabilishments_with_descriptions_agent';

const rrel1 = 'rrel_1';
const rrel2 = 'rrel_2';
const langEn = 'lang_en';
const langRu = 'lang_ru';
const answer = 'nrel_answer';


const baseKeynodes = [
    { id: question, type: ScType.NodeConstClass },
    { id: questionInitiated, type: ScType.NodeConstClass },
    { id: actionGetEstablishmentsWithDescriptionsAgent, type: ScType.NodeConstClass },
    { id: questionFinished, type: ScType.NodeConstClass },
];

// вызывает работу агента путём создания двух классов необходимых для запуска(33, 34 строки)
const describeAgent = async (
    keynodes: Record<string, ScAddr>,
) => {
    const actionNodeAlias = '_action_node';

    const template = new ScTemplate();

    template.triple(keynodes[question], ScType.EdgeAccessVarPosPerm, [ScType.NodeVar, actionNodeAlias]); //
    template.triple(keynodes[actionGetEstablishmentsWithDescriptionsAgent], ScType.EdgeAccessVarPosPerm, actionNodeAlias); //

    return [template, actionNodeAlias] as const;
};

// получает адресс ответа, находит структуру ответа(ссылку в нашем случае) и пытается вернуть преобразованный json
export const getAgentAnswer = async (circuitAddr: ScAddr) => {
    const link_with_json = '_link';
    const template = new ScTemplate();

    // ищет связь с узлом ответа и структурой ответа, далее работает с resultNode
    template.triple(circuitAddr, ScType.EdgeAccessVarPosPerm, [ScType.LinkVar, link_with_json]);
    const resultNode = await client.templateSearch(template);

    if (resultNode.length) {
        const linkContent = resultNode[0].get(link_with_json);
        if (linkContent && typeof linkContent === 'string') {
            try {
                return JSON.parse(linkContent);
            } catch (error) {
                console.error('Failed to parse JSON content:', error);
            }
        }
    }
    return null;
};

// Вызывать при необходимости вызвать агента
export const getEstablishmentsWithDescriptionsAgent = async () => {
    const keynodes = await client.resolveKeynodes(baseKeynodes);

    const [template, userActionNodeAlias] = await describeAgent(keynodes);

    const circuitAddr = await makeAgent(template, userActionNodeAlias);

    if (!circuitAddr) return null;

    return await getAgentAnswer(circuitAddr);
};