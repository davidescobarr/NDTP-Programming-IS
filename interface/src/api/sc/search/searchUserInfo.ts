import { ScAddr, ScTemplate, ScType } from 'ts-sc-client';
import { client } from "@api";

const nrelNickname = 'nrel_nickname';
const nrelPassword = 'nrel_password';
const nrelFirstName = 'nrel_first_name';
const nrelSurname = 'nrel_surname';
const nrelPatronymic = 'nrel_patronymic';
const nrelAuth = 'nrel_authors';
const nrelScTextTranslation = 'nrel_sc_text_translation';
const nrelMessageSequence = 'nrel_message_sequence';
const rrelLast = 'rrel_last';

const baseKeynodes = [
    { id: nrelNickname, type: ScType.NodeConstNoRole },
    { id: nrelPassword, type: ScType.NodeConstNoRole },
    { id: nrelFirstName, type: ScType.NodeConstNoRole },
    { id: nrelSurname, type: ScType.NodeConstNoRole },
    { id: nrelPatronymic, type: ScType.NodeConstNoRole },
    { id: nrelAuth, type: ScType.NodeConstNoRole },
    { id: nrelScTextTranslation, type: ScType.NodeConstNoRole },
    { id: nrelMessageSequence, type: ScType.NodeConstNoRole },
    { id: rrelLast, type: ScType.NodeConstRole },
];

export const searchAllUserInfo = async (userId : number) => {
    const nickname = await searchUserInfo(userId, nrelNickname);
    const password = await searchUserInfo(userId, nrelPassword);
    const first_name = await searchUserInfo(userId, nrelFirstName);
    const surname = await searchUserInfo(userId, nrelSurname);
    const patronymic = await searchUserInfo(userId, nrelPatronymic);

    return [nickname, password, first_name, surname, patronymic];
};

const searchUserInfo = async (userId : number, nrelPart : string) => {
    const keynodes = await client.resolveKeynodes(baseKeynodes);
    const userAddr = new ScAddr(userId);
    const template = new ScTemplate();
    template.tripleWithRelation(
        userAddr,
        ScType.EdgeDCommonVar,
        [ScType.LinkVar, "_node"],
        ScType.EdgeAccessVarPosPerm,
        keynodes[nrelPart],
    );

    const result = await client.templateSearch(template);
    let part = "";
    if (result.length > 0) {
        const partAddr = result[0].get("_node");
        part = String((await client.getLinkContents([partAddr]))[0].data);
    }

    return part;
};