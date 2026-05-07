import { CAREER_AI_URL } from '@constants';

export type CareerQuestionType = 'single' | 'multi' | 'scale';

export type CareerQuestionOption = {
    id: string;
    label: string;
};

export type CareerQuestion = {
    id: string;
    type: CareerQuestionType;
    text: string;
    hint?: string;
    options?: CareerQuestionOption[];
    min?: number;
    max?: number;
    step?: number;
    leftLabel?: string;
    rightLabel?: string;
};

export type CareerAnswerValue = string | string[] | number;

export type CareerAnswer = {
    question_id: string;
    value: CareerAnswerValue;
};

export type CareerChartDatum = {
    key: string;
    label: string;
    value: number;
    description?: string;
};

export type CareerProfessionMatch = {
    id: string;
    profession: string;
    score: number;
    reason: string;
};

export type CareerFact = {
    label: string;
    value: string;
};

export type CareerResult = {
    primaryProfession: string;
    summary: string;
    professionMatches: CareerProfessionMatch[];
    traits: CareerChartDatum[];
    charts: {
        interestRose: CareerChartDatum[];
        workStyle: CareerChartDatum[];
        professionFit: CareerChartDatum[];
    };
    guidance: string[];
    facts: CareerFact[];
};

export type CareerStepResponse = {
    done: boolean;
    answeredCount: number;
    progress: number;
    confidence: number;
    question?: CareerQuestion;
    result?: CareerResult;
};

const requestCareerAi = async <T>(path: string, payload: unknown): Promise<T> => {
    const response = await fetch(`${CAREER_AI_URL}${path}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        throw new Error(`Career AI service responded with ${response.status}`);
    }

    return response.json() as Promise<T>;
};

export const getCareerStep = (answers: CareerAnswer[]) =>
    requestCareerAi<CareerStepResponse>('/career-test/next', { answers });

export const getCareerResult = (answers: CareerAnswer[]) =>
    requestCareerAi<CareerResult>('/career-test/result', { answers });
