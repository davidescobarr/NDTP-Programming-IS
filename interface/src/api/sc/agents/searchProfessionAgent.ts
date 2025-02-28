import { client } from '@api/sc';
import { ScAddr, ScTemplate, ScType } from 'ts-sc-client';
import { makeAgent } from '@api/sc/agents/makeAgent';

const question = 'question';
const actionSearchProfession = 'action_search_profession';
const baseKeynodes = [
    { id: question, type: ScType.NodeConstClass },
    { id: actionSearchProfession, type: ScType.NodeConstClass },
];

const describeAgent = async (keynodes: Record<string, ScAddr>) => {
    const actionNodeAlias = '_action_node';

    const template = new ScTemplate();
    template.triple(keynodes[question], ScType.EdgeAccessVarPosPerm, [ScType.NodeVar, actionNodeAlias]);
    template.triple(keynodes[actionSearchProfession], ScType.EdgeAccessVarPosPerm, actionNodeAlias);

    return [template, actionNodeAlias] as const;
};

export const getAgentAnswer = async (circuitAddr: ScAddr) => {
    const link_with_json = '_link';
    const template = new ScTemplate();

    
    //template.triple(circuitAddr, ScType.EdgeDCommonVar, [ScType.LinkVar, link_with_json]);
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

export const SearchProfession = async () => {
    const keynodes = await client.resolveKeynodes(baseKeynodes);
    console.log("Resolved keynodes");

    const [template, userActionNodeAlias] = await describeAgent(keynodes);
    console.log("Created agent request");

    const circuitAddr = await makeAgent(template, userActionNodeAlias);
    console.log("Agent executed, circuitAddr:", circuitAddr);

    if (!circuitAddr) {
        console.error("❌ makeAgent failed: no circuitAddr returned");
        return null;
    }

console.log("✅ Agent executed successfully, circuitAddr:", circuitAddr);


    if (!circuitAddr) return null;

    return await getAgentAnswer(circuitAddr);
};
