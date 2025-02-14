import { client } from '@api/sc';
import { ScAddr, ScConstruction, ScLinkContent, ScTemplate, ScType, ScLinkContentType } from 'ts-sc-client';
import { makeAgent } from '@api/sc/agents/makeAgent';

const question = 'question';
const questionInitiated = 'question_initiated';
const questionFinished = 'question_finished';
const nrelAnswer = 'nrel_answer';
const actionGetProfessionsWithDescriptionsAgent = 'action_get_professions_with_descriptions_agent';

const rrel1 = 'rrel_1';
const rrel2 = 'rrel_2';
const langEn = 'lang_en';
const langRu = 'lang_ru';
const answer = 'nrel_answer';


const baseKeynodes = [
    { id: question, type: ScType.NodeConstClass },
    { id: questionInitiated, type: ScType.NodeConstClass },
    { id: actionGetProfessionsWithDescriptionsAgent, type: ScType.NodeConstClass },
    { id: questionFinished, type: ScType.NodeConstClass },
];

const describeAgent = async (
    keynodes: Record<string, ScAddr>,
) => {
    const actionNodeAlias = '_action_node';

    const template = new ScTemplate();

    template.triple(keynodes[question], ScType.EdgeAccessVarPosPerm, [ScType.NodeVar, actionNodeAlias]); //
    template.triple(keynodes[actionGetProfessionsWithDescriptionsAgent], ScType.EdgeAccessVarPosPerm, actionNodeAlias); //

    return [template, actionNodeAlias] as const;
};

export const getAgentAnswer = async (circuitAddr: ScAddr) => {
    const link_with_json = '_link';
    const template = new ScTemplate();

    template.triple(circuitAddr, ScType.EdgeAccessVarPosPerm, [ScType.LinkVar, link_with_json]);
    const resultNode = await client.templateSearch(template);
    console.log(resultNode);

    if (resultNode.length) {
        const link = resultNode[0].get(link_with_json);
        console.log(link);
        if (link) {
            const linkContent = (await client.getLinkContents([link]))[0];
            console.log(linkContent);
            try {
                 return JSON.parse(String(linkContent.data));
            } catch (error) {
                console.error('Failed to parse JSON content:', error);
            }
        }
    }
    return null;
};

export const getProfessionsWithDescriptionsAgent = async () => {
    const keynodes = await client.resolveKeynodes(baseKeynodes);
    console.log("Resolve call");

    const [template, userActionNodeAlias] = await describeAgent(keynodes);
    console.log("DescribeAgent call");

    const circuitAddr = await makeAgent(template, userActionNodeAlias);
    console.log("Make call");
    console.log(circuitAddr);

    if (!circuitAddr) return null;

    return await getAgentAnswer(circuitAddr);
};