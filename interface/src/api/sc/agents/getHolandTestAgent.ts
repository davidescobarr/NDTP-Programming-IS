import { client } from '@api/sc';
import { ScAddr, ScTemplate, ScType } from 'ts-sc-client';
import { makeAgent } from '@api/sc/agents/makeAgent';

const question = 'question';
const actionGetHolandTestAgent = 'action_get_holand_test_agent';
const baseKeynodes = [
    { id: question, type: ScType.NodeConstClass },
    { id: actionGetHolandTestAgent, type: ScType.NodeConstClass },
];

// Функция, создающая действие для агента
const describeAgent = async (keynodes: Record<string, ScAddr>) => {
    const actionNodeAlias = '_action_node';

    const template = new ScTemplate();
    template.triple(keynodes[question], ScType.EdgeAccessVarPosPerm, [ScType.NodeVar, actionNodeAlias]);
    template.triple(keynodes[actionGetHolandTestAgent], ScType.EdgeAccessVarPosPerm, actionNodeAlias);

    return [template, actionNodeAlias] as const;
};

// Функция, получающая JSON-ответ агента
export const getAgentAnswer = async (circuitAddr: ScAddr) => {
    const link_with_json = '_link';
    const template = new ScTemplate();

    template.triple(circuitAddr, ScType.EdgeAccessVarPosPerm, [ScType.LinkVar, link_with_json]);

    const resultNode = await client.templateSearch(template);
    if (resultNode.length) {
        const link = resultNode[0].get(link_with_json);
        if (link) {
            const linkContent = (await client.getLinkContents([link]))[0];
            try {
                return JSON.parse(String(linkContent.data));
            } catch (error) {
                console.error('Failed to parse JSON content:', error);
            }
        }
    }
    return null;
};

// Функция для вызова агента
export const getHolandTestAgent = async () => {
    const keynodes = await client.resolveKeynodes(baseKeynodes);
    console.log("Resolved keynodes");

    const [template, userActionNodeAlias] = await describeAgent(keynodes);
    console.log("Created agent request");

    const circuitAddr = await makeAgent(template, userActionNodeAlias);
    console.log("Agent executed:", circuitAddr);

    if (!circuitAddr) return null;

    return await getAgentAnswer(circuitAddr);
};
