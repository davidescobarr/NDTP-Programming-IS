import { client } from '@api/sc';
import {
  ScAddr,
  ScConstruction,
  ScLinkContent,
  ScTemplate,
  ScType,
  ScLinkContentType,
} from 'ts-sc-client';
import { makeAgent } from '@api/sc/agents/makeAgent';

const question = 'question';
const actionAnalyzeHolandTestAgent = 'action_analyze_holand_test_agent';
const rrel1 = 'rrel_1';

const baseKeynodes = [
  { id: question, type: ScType.NodeConstClass },
  { id: actionAnalyzeHolandTestAgent, type: ScType.NodeConstClass },
  { id: rrel1, type: ScType.NodeConstRole },
];

const createJsonLink = async (jsonData: object): Promise<ScAddr | null> => {
  try {
    const jsonString = JSON.stringify(jsonData);
    const construction = new ScConstruction();
    construction.createLink(
      ScType.LinkConst,
      new ScLinkContent(jsonString, ScLinkContentType.String)
    );
    const result = await client.createElements(construction);
    return result.length ? result[0] : null;
  } catch (error) {
    console.error("Ошибка при создании ссылки с JSON:", error);
    return null;
  }
};

const describeAgent = async (
  keynodes: Record<string, ScAddr>,
  jsonLink: ScAddr
) => {
  const actionNodeAlias = '_action_node';
  const template = new ScTemplate();

  template.triple(
    keynodes[question],
    ScType.EdgeAccessVarPosPerm,
    [ScType.NodeVar, actionNodeAlias]
  );

  template.triple(
    keynodes[actionAnalyzeHolandTestAgent],
    ScType.EdgeAccessVarPosPerm,
    actionNodeAlias
  );

  template.tripleWithRelation(
    actionNodeAlias,
    ScType.EdgeAccessVarPosPerm,
    jsonLink,
    ScType.EdgeAccessVarPosPerm,
    keynodes[rrel1]
  );

  return [template, actionNodeAlias] as const;
};

export const getAgentAnswer = async (circuitAddr: ScAddr) => {
  const link_with_json = '_link';
  const template = new ScTemplate();

  template.triple(
    circuitAddr,
    ScType.EdgeAccessVarPosPerm,
    [ScType.LinkVar, link_with_json]
  );

  const resultNode = await client.templateSearch(template);
  if (resultNode.length) {
    const link = resultNode[0].get(link_with_json);
    if (link) {
      const linkContent = (await client.getLinkContents([link]))[0];
      try {
        return JSON.parse(String(linkContent.data));
      } catch (error) {
        console.error('Ошибка при разборе JSON ответа:', error);
      }
    }
  }
  return null;
};

export const analyzeHolandTestAgent = async (userAnswers: object) => {
  const keynodes = await client.resolveKeynodes(baseKeynodes);
  console.log("Ключевые узлы получены");

  const jsonLink = await createJsonLink(userAnswers);
  if (!jsonLink) return null;

  const [template, userActionNodeAlias] = await describeAgent(keynodes, jsonLink);
  console.log("Агент описан");

  const circuitAddr = await makeAgent(template, userActionNodeAlias);
  console.log("Агент вызван:", circuitAddr);

  if (!circuitAddr) return null;

  return await getAgentAnswer(circuitAddr);
};
