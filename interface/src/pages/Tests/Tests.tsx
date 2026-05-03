import * as React from 'react';
import FadeInSection from "@components/FadeInSection/FadeInSection";
import {
    analyzeStaticTest,
    StaticQuestion,
    StaticTestDefinition,
    StaticTestResult,
    staticTests,
} from "@model/staticTests";
import "@components/Tests/test.css";

const heroImage = require('@assets/img/proftest.png');

type PageStage = 'landing' | 'test' | 'results';
type AnswerMap = Record<string, number>;
type ScoreMap = Record<string, number>;

type CombinedQuestion = {
    key: string;
    globalIndex: number;
    questionIndex: number;
    test: StaticTestDefinition;
    displayName: string;
    answers: StaticQuestion['answers'];
};

type ChartDatum = {
    key: string;
    label: string;
    value: number;
};

type CareerSummary = {
    primaryProfession: string;
    professions: string[];
    hollandData: ChartDatum[];
    iovaishiData: ChartDatum[];
    hollandTop: ProfileDefinition;
    iovaishiTop: ProfileDefinition;
    motivation: MotivationProfile;
    success: SuccessProfile;
    successScore: number;
    totalPointScore: number;
    totalPointMax: number;
    resultsByTest: Record<string, StaticTestResult>;
};

type ProfileDefinition = {
    label: string;
    short: string;
    description: string;
    professions: string[];
};

type MotivationProfile = {
    label: string;
    description: string;
};

type SuccessProfile = {
    label: string;
    description: string;
};

const chartColors = ['#F86F03', '#717BE6', '#42A5A3', '#E45858', '#2F4858', '#F2A541'];

const hollandProfiles: Record<string, ProfileDefinition> = {
    category1: {
        label: 'Реалистический тип',
        short: 'Практика',
        description: 'Вам ближе техника, инструменты, материальные объекты и понятный прикладной результат.',
        professions: ['инженер-технолог', 'техник', 'автомеханик', 'строитель', 'водитель', 'оператор оборудования'],
    },
    category2: {
        label: 'Интеллектуальный тип',
        short: 'Исследования',
        description: 'Вам подходит анализ, самостоятельный поиск решений, исследование и работа со сложными идеями.',
        professions: ['программист-аналитик', 'исследователь', 'инженер-разработчик', 'химик', 'биолог', 'data-аналитик'],
    },
    category3: {
        label: 'Социальный тип',
        short: 'Люди',
        description: 'Сильная сторона профиля - коммуникация, помощь, обучение, консультирование и поддержка людей.',
        professions: ['психолог', 'преподаватель', 'HR-специалист', 'врач', 'логопед', 'консультант'],
    },
    category4: {
        label: 'Конвенциальный тип',
        short: 'Система',
        description: 'Вам ближе структурная работа: порядок, документы, расчеты, регламенты и точность.',
        professions: ['экономист', 'бухгалтер', 'финансовый аналитик', 'планировщик', 'архивариус', 'оператор данных'],
    },
    category5: {
        label: 'Предприимчивый тип',
        short: 'Управление',
        description: 'Вам подходят инициативные задачи, переговоры, влияние, организация процессов и принятие решений.',
        professions: ['менеджер проекта', 'предприниматель', 'маркетолог', 'директор', 'риэлтор', 'бизнес-аналитик'],
    },
    category6: {
        label: 'Артистический тип',
        short: 'Творчество',
        description: 'Ваш профиль связан с образами, гибким мышлением, дизайном, текстами, сценой и визуальными решениями.',
        professions: ['дизайнер', 'архитектор', 'журналист', 'писатель', 'музыкант', 'актер'],
    },
};

const iovaishiProfiles: Record<string, ProfileDefinition> = {
    category1: {
        label: 'Работа с людьми',
        short: 'Люди',
        description: 'Коммуникация, сервис, обучение, медицина, управление и регулярное взаимодействие.',
        professions: ['психолог', 'преподаватель', 'HR-специалист', 'менеджер', 'врач'],
    },
    category2: {
        label: 'Исследовательская работа',
        short: 'Наука',
        description: 'Аналитика, эксперименты, гипотезы, самостоятельное мышление и интеллектуальная глубина.',
        professions: ['исследователь', 'программист-аналитик', 'инженер-разработчик', 'лаборант', 'аналитик'],
    },
    category3: {
        label: 'Практическая деятельность',
        short: 'Практика',
        description: 'Производство, техника, ремонт, сборка, транспорт, материалы и предметная работа.',
        professions: ['инженер-технолог', 'техник', 'механик', 'строитель', 'оператор оборудования'],
    },
    category4: {
        label: 'Эстетическая деятельность',
        short: 'Эстетика',
        description: 'Дизайн, музыка, литература, сцена, визуальная культура и творческие профессии.',
        professions: ['дизайнер', 'архитектор', 'журналист', 'актер', 'музыкант'],
    },
    category5: {
        label: 'Экстремальная деятельность',
        short: 'Динамика',
        description: 'Спорт, служба, экспедиции, охрана, высокая нагрузка и ситуации с риском.',
        professions: ['спасатель', 'полицейский', 'военнослужащий', 'пилот', 'охранник'],
    },
    category6: {
        label: 'Планово-экономическая деятельность',
        short: 'Планирование',
        description: 'Расчеты, планирование, документы, схемы, тексты, точность и аккуратность.',
        professions: ['экономист', 'бухгалтер', 'планировщик', 'финансовый аналитик', 'редактор'],
    },
};

const exactProfessionMap: Record<string, string> = {
    'category1:category2': 'инженер-исследователь',
    'category1:category3': 'инженер-технолог',
    'category1:category5': 'спасатель или технический специалист службы',
    'category2:category2': 'программист-аналитик',
    'category2:category3': 'инженер-разработчик',
    'category2:category6': 'data-аналитик',
    'category3:category1': 'психолог-консультант',
    'category3:category2': 'преподаватель исследовательских дисциплин',
    'category3:category6': 'HR-аналитик',
    'category4:category2': 'финансовый аналитик',
    'category4:category6': 'экономист-планировщик',
    'category5:category1': 'менеджер по работе с людьми',
    'category5:category6': 'бизнес-аналитик',
    'category6:category4': 'дизайнер',
    'category6:category6': 'редактор или UX-писатель',
};

const getQuestionKey = (testId: string, questionIndex: number) => `${testId}:${questionIndex}`;

const combinedQuestions: CombinedQuestion[] = staticTests.flatMap((test) =>
    test.questions.map((question, questionIndex) => ({
        key: getQuestionKey(test.id, questionIndex),
        globalIndex: 0,
        questionIndex,
        test,
        displayName: question.display_name,
        answers: question.answers,
    })),
).map((question, index) => ({ ...question, globalIndex: index }));

const hasAnswer = (answers: AnswerMap, key: string) => Object.prototype.hasOwnProperty.call(answers, key);

const getAnsweredQuestions = (test: StaticTestDefinition, answers: AnswerMap): StaticQuestion[] =>
    test.questions.map((question, questionIndex) => ({
        ...question,
        answers: question.answers.map((answer) => ({ ...answer })),
        answer: answers[getQuestionKey(test.id, questionIndex)],
    }));

const getTopKey = (scores: ScoreMap | undefined, fallback = 'category1') => {
    if (!scores || !Object.keys(scores).length) return fallback;
    return Object.keys(scores).reduce((bestKey, key) =>
        (scores[key] ?? 0) > (scores[bestKey] ?? 0) ? key : bestKey,
    Object.keys(scores)[0]);
};

const getChartData = (scores: ScoreMap | undefined, profiles: Record<string, ProfileDefinition>): ChartDatum[] =>
    Object.keys(profiles).map((key) => ({
        key,
        label: profiles[key].short,
        value: scores?.[key] ?? 0,
    }));

const getMotivationProfile = (zeroAnswersCount: number): MotivationProfile => {
    if ([3, 4, 7, 17, 18, 19, 21, 24].includes(zeroAnswersCount)) {
        return {
            label: 'Престиж и статус',
            description: 'Вы ориентируетесь на заметное положение, признание и высокий уровень профессиональных притязаний.',
        };
    }

    if ([5, 8, 11, 14, 15, 16, 20, 23].includes(zeroAnswersCount)) {
        return {
            label: 'Материальная устойчивость',
            description: 'Для вас значимы доход, стабильность и практическая польза выбранной профессиональной траектории.',
        };
    }

    return {
        label: 'Творческое развитие',
        description: 'Вы заметно реагируете на новые технологии, развитие навыков и возможность делать содержательную работу.',
    };
};

const getSuccessProfile = (score: number): SuccessProfile => {
    if (score <= 10) {
        return {
            label: 'Низкая мотивация к успеху',
            description: 'Лучше выбирать среду с понятной поддержкой, короткими целями и постепенным ростом ответственности.',
        };
    }

    if (score <= 16) {
        return {
            label: 'Средняя мотивация к успеху',
            description: 'Подходит большинство образовательных и карьерных траекторий: баланс риска и стабильности сохранен.',
        };
    }

    if (score <= 20) {
        return {
            label: 'Высокая мотивация к успеху',
            description: 'Вам подойдут амбициозные задачи, конкурсы, проекты и роли, где важен измеримый результат.',
        };
    }

    return {
        label: 'Очень высокая мотивация к успеху',
        description: 'Можно выбирать сложные цели, но важно контролировать нагрузку и не превращать карьеру в постоянный стресс.',
    };
};

const getMaxPointScore = (test: StaticTestDefinition) =>
    test.questions.reduce((sum, question) => sum + Math.max(...question.answers.map((answer) => answer.point ?? 0)), 0);

const getCareerSummary = (answers: AnswerMap): CareerSummary => {
    const resultsByTest = staticTests.reduce<Record<string, StaticTestResult>>((acc, test) => {
        acc[test.id] = analyzeStaticTest(test, getAnsweredQuestions(test, answers));
        return acc;
    }, {});

    const hollandScores = resultsByTest.test_holand?.scores ?? {};
    const iovaishiScores = resultsByTest.test_iovaishi?.scores ?? {};
    const hollandTopKey = getTopKey(hollandScores);
    const iovaishiTopKey = getTopKey(iovaishiScores);
    const hollandTop = hollandProfiles[hollandTopKey] ?? hollandProfiles.category1;
    const iovaishiTop = iovaishiProfiles[iovaishiTopKey] ?? iovaishiProfiles.category1;
    const motivationScore = resultsByTest.test_motivational?.totalScore ?? 0;
    const successScore = resultsByTest.test_personalitytosuccess?.totalScore ?? 0;
    const totalPointScore = (resultsByTest.test_express?.totalScore ?? 0) + (resultsByTest.test_advanced?.totalScore ?? 0);
    const totalPointMax = staticTests
        .filter((test) => test.analyzer === 'points')
        .reduce((sum, test) => sum + getMaxPointScore(test), 0);
    const primaryProfession = exactProfessionMap[`${hollandTopKey}:${iovaishiTopKey}`] ?? hollandTop.professions[0];
    const professions = Array.from(new Set([
        primaryProfession,
        ...hollandTop.professions,
        ...iovaishiTop.professions,
    ])).slice(0, 8);

    return {
        primaryProfession,
        professions,
        hollandData: getChartData(hollandScores, hollandProfiles),
        iovaishiData: getChartData(iovaishiScores, iovaishiProfiles),
        hollandTop,
        iovaishiTop,
        motivation: getMotivationProfile(motivationScore),
        success: getSuccessProfile(successScore),
        successScore,
        totalPointScore,
        totalPointMax,
        resultsByTest,
    };
};

const polarToCartesian = (centerX: number, centerY: number, radius: number, angleInDegrees: number) => {
    const angleInRadians = (angleInDegrees - 90) * Math.PI / 180;
    return {
        x: centerX + (radius * Math.cos(angleInRadians)),
        y: centerY + (radius * Math.sin(angleInRadians)),
    };
};

const describeArcSegment = (
    centerX: number,
    centerY: number,
    innerRadius: number,
    outerRadius: number,
    startAngle: number,
    endAngle: number,
) => {
    const outerStart = polarToCartesian(centerX, centerY, outerRadius, startAngle);
    const outerEnd = polarToCartesian(centerX, centerY, outerRadius, endAngle);
    const innerStart = polarToCartesian(centerX, centerY, innerRadius, endAngle);
    const innerEnd = polarToCartesian(centerX, centerY, innerRadius, startAngle);
    const largeArcFlag = endAngle - startAngle <= 180 ? '0' : '1';

    return [
        `M ${outerStart.x} ${outerStart.y}`,
        `A ${outerRadius} ${outerRadius} 0 ${largeArcFlag} 1 ${outerEnd.x} ${outerEnd.y}`,
        `L ${innerStart.x} ${innerStart.y}`,
        `A ${innerRadius} ${innerRadius} 0 ${largeArcFlag} 0 ${innerEnd.x} ${innerEnd.y}`,
        'Z',
    ].join(' ');
};

const getPolygonPoints = (data: ChartDatum[], maxValue: number, radius: number, center: number) =>
    data.map((item, index) => {
        const angle = -90 + (360 / data.length) * index;
        const valueRadius = maxValue > 0 ? (item.value / maxValue) * radius : 0;
        const point = polarToCartesian(center, center, valueRadius, angle + 90);
        return `${point.x},${point.y}`;
    }).join(' ');

const WindRoseChart = ({ data }: { data: ChartDatum[] }) => {
    const maxValue = Math.max(...data.map((item) => item.value), 1);
    const center = 130;
    const innerRadius = 22;
    const segmentSize = 360 / data.length;

    return (
        <div className="career-chart-figure">
            <svg viewBox="0 0 260 260" role="img" aria-label="Роза ветров профессиональных склонностей">
                {[40, 70, 100].map((radius) => (
                    <circle key={radius} cx={center} cy={center} r={radius} className="career-chart-grid" />
                ))}
                {data.map((item, index) => {
                    const startAngle = index * segmentSize + 4;
                    const endAngle = (index + 1) * segmentSize - 4;
                    const outerRadius = innerRadius + 18 + ((item.value / maxValue) * 82);
                    const labelPoint = polarToCartesian(center, center, 116, startAngle + segmentSize / 2);

                    return (
                        <g key={item.key}>
                            <path
                                d={describeArcSegment(center, center, innerRadius, outerRadius, startAngle, endAngle)}
                                fill={chartColors[index % chartColors.length]}
                                opacity="0.88"
                            />
                            <text x={labelPoint.x} y={labelPoint.y} className="career-chart-label">
                                {item.label}
                            </text>
                        </g>
                    );
                })}
                <circle cx={center} cy={center} r={innerRadius} className="career-chart-center" />
            </svg>
        </div>
    );
};

const RadarChart = ({ data }: { data: ChartDatum[] }) => {
    const maxValue = Math.max(...data.map((item) => item.value), 1);
    const center = 130;
    const radius = 88;

    return (
        <div className="career-chart-figure">
            <svg viewBox="0 0 260 260" role="img" aria-label="Радарная диаграмма профиля">
                {[0.25, 0.5, 0.75, 1].map((level) => (
                    <polygon
                        key={level}
                        points={getPolygonPoints(data.map((item) => ({ ...item, value: maxValue * level })), maxValue, radius, center)}
                        className="career-radar-grid"
                    />
                ))}
                {data.map((item, index) => {
                    const angle = -90 + (360 / data.length) * index;
                    const edge = polarToCartesian(center, center, radius, angle + 90);
                    const labelPoint = polarToCartesian(center, center, 113, angle + 90);
                    return (
                        <g key={item.key}>
                            <line x1={center} y1={center} x2={edge.x} y2={edge.y} className="career-radar-axis" />
                            <text x={labelPoint.x} y={labelPoint.y} className="career-chart-label">
                                {item.label}
                            </text>
                        </g>
                    );
                })}
                <polygon points={getPolygonPoints(data, maxValue, radius, center)} className="career-radar-area" />
                {data.map((item, index) => {
                    const angle = -90 + (360 / data.length) * index;
                    const point = polarToCartesian(center, center, maxValue ? (item.value / maxValue) * radius : 0, angle + 90);
                    return <circle key={item.key} cx={point.x} cy={point.y} r="4" className="career-radar-dot" />;
                })}
            </svg>
        </div>
    );
};

const HorizontalBars = ({ data }: { data: ChartDatum[] }) => {
    const maxValue = Math.max(...data.map((item) => item.value), 1);

    return (
        <div className="career-bars">
            {data.map((item, index) => (
                <div className="career-bar-row" key={item.key}>
                    <div className="career-bar-label">
                        <span>{item.label}</span>
                        <b>{item.value}</b>
                    </div>
                    <div className="career-bar-track">
                        <div
                            className="career-bar-fill"
                            style={{
                                width: `${Math.max(6, (item.value / maxValue) * 100)}%`,
                                backgroundColor: chartColors[index % chartColors.length],
                            }}
                        />
                    </div>
                </div>
            ))}
        </div>
    );
};

const CircularGauge = ({ value, max, label }: { value: number; max: number; label: string }) => {
    const radius = 52;
    const circumference = 2 * Math.PI * radius;
    const percent = max > 0 ? Math.min(value / max, 1) : 0;

    return (
        <div className="career-gauge">
            <svg viewBox="0 0 140 140" role="img" aria-label={label}>
                <circle cx="70" cy="70" r={radius} className="career-gauge-track" />
                <circle
                    cx="70"
                    cy="70"
                    r={radius}
                    className="career-gauge-value"
                    strokeDasharray={circumference}
                    strokeDashoffset={circumference * (1 - percent)}
                />
                <text x="70" y="68" className="career-gauge-number">{value}</text>
                <text x="70" y="88" className="career-gauge-caption">из {max}</text>
            </svg>
        </div>
    );
};

const ResultPreview = ({ result }: { result?: StaticTestResult }) => {
    const firstLine = result?.text?.split('\n').find((line) => line.trim().length > 0) ?? 'Ответы учтены';
    return <p>{firstLine}</p>;
};

export const Tests = () => {
    const [stage, setStage] = React.useState<PageStage>('landing');
    const [currentIndex, setCurrentIndex] = React.useState(0);
    const [answers, setAnswers] = React.useState<AnswerMap>({});

    const currentQuestion = combinedQuestions[currentIndex];
    const answeredCount = combinedQuestions.filter((question) => hasAnswer(answers, question.key)).length;
    const allAnswered = answeredCount === combinedQuestions.length;
    const progress = combinedQuestions.length ? Math.round((answeredCount / combinedQuestions.length) * 100) : 0;
    const summary = React.useMemo(() => getCareerSummary(answers), [answers]);

    const startTest = () => {
        setStage('test');
        setCurrentIndex(0);
        setAnswers({});
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const finishTest = () => {
        setStage('results');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const chooseAnswer = (answerId: number) => {
        if (!currentQuestion) return;
        setAnswers((prev) => ({ ...prev, [currentQuestion.key]: answerId }));
    };

    const goNext = () => {
        if (currentIndex + 1 >= combinedQuestions.length) {
            if (allAnswered) {
                finishTest();
                return;
            }

            const firstUnansweredIndex = combinedQuestions.findIndex((question) => !hasAnswer(answers, question.key));
            if (firstUnansweredIndex >= 0) setCurrentIndex(firstUnansweredIndex);
            return;
        }

        setCurrentIndex((index) => index + 1);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const goPrev = () => {
        setCurrentIndex((index) => Math.max(index - 1, 0));
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    if (stage === 'landing') {
        return (
            <div className="main career-page">
                <section className="career-test-hero" style={{ backgroundImage: `url(${heroImage})` }}>
                    <div className="career-test-hero-content">
                        <span>Комплексная профориентация</span>
                        <h1>Пройти тест</h1>
                        <p>
                            Ответьте на вопросы из нескольких методик и получите цельный профиль склонностей,
                            мотивации и подходящих профессий.
                        </p>
                        <button onClick={startTest}>Пройти тест</button>
                    </div>
                </section>

                <section className="career-landing-section">
                    <FadeInSection>
                        <div className="career-landing-heading">
                            <h2>Что покажет результат</h2>
                            <p>
                                Тест объединяет данные из семантической базы и работает на сайте без запуска OSTIS.
                                Итоговая страница собирает ответы в понятную профессиональную рекомендацию.
                            </p>
                        </div>
                    </FadeInSection>
                    <div className="career-benefits">
                        <div>
                            <b>{staticTests.length}</b>
                            <span>методик в одном потоке</span>
                        </div>
                        <div>
                            <b>{combinedQuestions.length}</b>
                            <span>вопросов для профиля</span>
                        </div>
                        <div>
                            <b>3</b>
                            <span>ключевых вывода: склонность, мотивация, профессия</span>
                        </div>
                    </div>
                </section>

                <section className="career-methods-section">
                    <div className="career-methods">
                        {staticTests.map((test) => (
                            <div className="career-method" key={test.id}>
                                <h3>{test.name}</h3>
                                <p>{test.questions.length} вопросов</p>
                            </div>
                        ))}
                    </div>
                </section>
            </div>
        );
    }

    if (stage === 'results') {
        return (
            <div className="main career-page career-results-page">
                <section className="career-results-hero">
                    <span>Итоги комплексного теста</span>
                    <h1>Подходящая профессия: {summary.primaryProfession}</h1>
                    <p>
                        Основной профиль: {summary.hollandTop.label}. Дополнительная склонность:
                        {' '}{summary.iovaishiTop.label.toLowerCase()}.
                    </p>
                    <div className="career-result-actions">
                        <button onClick={startTest}>Пройти заново</button>
                        <button className="career-secondary-button" onClick={() => setStage('test')}>Вернуться к вопросам</button>
                    </div>
                </section>

                <section className="career-results-grid">
                    <article className="career-result-panel career-main-result">
                        <h2>Профориентационный вывод</h2>
                        <p>{summary.hollandTop.description}</p>
                        <p>{summary.iovaishiTop.description}</p>
                        <div className="career-profession-list">
                            {summary.professions.map((profession) => (
                                <span key={profession}>{profession}</span>
                            ))}
                        </div>
                    </article>

                    <article className="career-result-panel">
                        <h2>Роза ветров склонностей</h2>
                        <WindRoseChart data={summary.hollandData} />
                    </article>

                    <article className="career-result-panel">
                        <h2>Профиль Холланда</h2>
                        <RadarChart data={summary.hollandData} />
                    </article>

                    <article className="career-result-panel">
                        <h2>Склонности Йовайши</h2>
                        <HorizontalBars data={summary.iovaishiData} />
                    </article>

                    <article className="career-result-panel">
                        <h2>Мотивация к успеху</h2>
                        <div className="career-gauge-layout">
                            <CircularGauge value={summary.successScore} max={32} label="Мотивация к успеху" />
                            <div>
                                <h3>{summary.success.label}</h3>
                                <p>{summary.success.description}</p>
                            </div>
                        </div>
                    </article>

                    <article className="career-result-panel">
                        <h2>Мотив выбора профессии</h2>
                        <div className="career-motivation-box">
                            <b>{summary.motivation.label}</b>
                            <p>{summary.motivation.description}</p>
                        </div>
                        <div className="career-point-score">
                            <span>Практический индекс</span>
                            <b>{summary.totalPointScore} / {summary.totalPointMax}</b>
                        </div>
                    </article>
                </section>

                <section className="career-details-section">
                    <h2>Расшифровка по методикам</h2>
                    <div className="career-detail-list">
                        {staticTests.map((test) => (
                            <div className="career-detail-item" key={test.id}>
                                <h3>{test.name}</h3>
                                <ResultPreview result={summary.resultsByTest[test.id]} />
                            </div>
                        ))}
                    </div>
                </section>
            </div>
        );
    }

    return (
        <div className="main career-page career-test-flow">
            <section className="career-test-header">
                <span>Комплексный тест</span>
                <h1>Пройти тест</h1>
                <p>Все методики объединены в один маршрут. Ответы сохраняются на странице и анализируются локально.</p>
                <div className="career-progress">
                    <div className="career-progress-label">
                        <span>{answeredCount} из {combinedQuestions.length} ответов</span>
                        <b>{progress}%</b>
                    </div>
                    <div className="career-progress-track">
                        <div className="career-progress-fill" style={{ width: `${progress}%` }} />
                    </div>
                </div>
            </section>

            {currentQuestion && (
                <section className="career-test-workspace">
                    <aside className="career-test-map">
                        <h2>Методики</h2>
                        {staticTests.map((test) => {
                            const answeredInTest = test.questions.filter((_, index) => hasAnswer(answers, getQuestionKey(test.id, index))).length;
                            const isActive = currentQuestion.test.id === test.id;

                            return (
                                <button
                                    key={test.id}
                                    className={isActive ? 'active' : ''}
                                    onClick={() => {
                                        const targetIndex = combinedQuestions.findIndex((question) => question.test.id === test.id);
                                        if (targetIndex >= 0) setCurrentIndex(targetIndex);
                                    }}
                                >
                                    <span>{test.name}</span>
                                    <b>{answeredInTest}/{test.questions.length}</b>
                                </button>
                            );
                        })}
                    </aside>

                    <article className="career-question-panel">
                        <div className="career-question-meta">
                            <span>{currentQuestion.test.name}</span>
                            <b>Вопрос {currentQuestion.globalIndex + 1} из {combinedQuestions.length}</b>
                        </div>
                        <h2>{currentQuestion.displayName}</h2>
                        <div className="career-answer-list">
                            {currentQuestion.answers.map((answer) => {
                                const selected = answers[currentQuestion.key] === answer.id;
                                return (
                                    <button
                                        key={answer.id}
                                        className={selected ? 'selected' : ''}
                                        onClick={() => chooseAnswer(answer.id)}
                                    >
                                        {answer.name}
                                    </button>
                                );
                            })}
                        </div>
                        <div className="career-question-actions">
                            <button className="career-secondary-button" onClick={goPrev} disabled={currentIndex === 0}>
                                Назад
                            </button>
                            <button onClick={goNext} disabled={!hasAnswer(answers, currentQuestion.key)}>
                                {currentIndex + 1 >= combinedQuestions.length
                                    ? allAnswered ? 'Показать результат' : 'К незаполненному вопросу'
                                    : 'Далее'}
                            </button>
                        </div>
                    </article>
                </section>
            )}
        </div>
    );
}
