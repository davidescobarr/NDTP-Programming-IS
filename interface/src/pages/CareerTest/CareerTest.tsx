import * as React from 'react';
import FadeInSection from '@components/FadeInSection/FadeInSection';
import {
    CareerAnswer,
    CareerAnswerValue,
    CareerChartDatum,
    CareerQuestion,
    CareerResult,
    getCareerStep,
} from '@api/careerAi';
import '@components/Tests/test.css';

const heroImage = require('@assets/img/proftest.png');

type PageStage = 'landing' | 'test' | 'results';
type DraftAnswer = string | string[] | number | null;

const chartColors = ['#F86F03', '#717BE6', '#42A5A3', '#E45858', '#2F4858', '#F2A541'];

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

const getPolygonPoints = (data: CareerChartDatum[], radius: number, center: number) =>
    data.map((item, index) => {
        const angle = -90 + (360 / data.length) * index;
        const valueRadius = (Math.max(0, Math.min(item.value, 100)) / 100) * radius;
        const point = polarToCartesian(center, center, valueRadius, angle + 90);
        return `${point.x},${point.y}`;
    }).join(' ');

const activateOnKeyboard = (event: React.KeyboardEvent, onActivate: () => void) => {
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        onActivate();
    }
};

const ChartDetail = ({ item, color }: { item: CareerChartDatum; color: string }) => (
    <div className="career-chart-detail" style={{ borderLeftColor: color }}>
        <div>
            <span>{item.label}</span>
            <b>{item.value}%</b>
        </div>
        {item.description && <p>{item.description}</p>}
    </div>
);

const getStrongestTrait = (result: CareerResult) =>
    [...result.traits].sort((left, right) => right.value - left.value)[0];

const CareerNextSteps = ({ result }: { result: CareerResult }) => {
    const strongestTrait = getStrongestTrait(result);
    const alternativeProfession = result.professionMatches.find((match) => match.profession !== result.primaryProfession);

    return (
        <div className="career-next-steps">
            <div>
                <span>01</span>
                <p>
                    Разберите реальные задачи направления «{result.primaryProfession}» и отметьте, какие из них хочется
                    попробовать на практике.
                </p>
            </div>
            <div>
                <span>02</span>
                <p>
                    Сравните основной вариант
                    {alternativeProfession ? ` с альтернативой «${alternativeProfession.profession}»` : ' с близкими профессиями'}
                    , чтобы выбрать более точную траекторию обучения.
                </p>
            </div>
            <div>
                <span>03</span>
                <p>
                    Соберите первый мини-проект под сильную сторону
                    {strongestTrait ? ` «${strongestTrait.label}»` : ' вашего профиля'} и проверьте интерес в реальной задаче.
                </p>
            </div>
        </div>
    );
};

const getChartLabelLines = (label: string) => {
    if (label.includes(' ') && label.length > 12) {
        return label.split(' ');
    }

    if (label.length > 13) {
        const splitIndex = Math.ceil(label.length / 2);
        return [`${label.slice(0, splitIndex)}-`, label.slice(splitIndex)];
    }

    return [label];
};

const SvgChartLabel = ({ x, y, label }: { x: number; y: number; label: string }) => {
    const lines = getChartLabelLines(label);
    const lineHeight = 12;
    const startOffset = lines.length > 1 ? -((lines.length - 1) * lineHeight) / 2 : 0;

    return (
        <text x={x} y={y + startOffset} className="career-chart-label">
            {lines.map((line, index) => (
                <tspan key={`${line}-${index}`} x={x} dy={index === 0 ? 0 : lineHeight}>
                    {line}
                </tspan>
            ))}
        </text>
    );
};

const WindRoseChart = ({ data }: { data: CareerChartDatum[] }) => {
    const center = 130;
    const innerRadius = 22;
    const segmentSize = data.length ? 360 / data.length : 0;
    const firstKey = data[0]?.key ?? '';
    const [activeKey, setActiveKey] = React.useState(firstKey);

    React.useEffect(() => {
        if (firstKey && !data.some((item) => item.key === activeKey)) {
            setActiveKey(firstKey);
        }
    }, [activeKey, data, firstKey]);

    if (!data.length) return null;

    const activeItem = data.find((item) => item.key === activeKey) ?? data[0];
    const activeIndex = Math.max(data.findIndex((item) => item.key === activeItem.key), 0);
    const activeColor = chartColors[activeIndex % chartColors.length];

    return (
        <div className="career-chart-figure">
            <svg viewBox="0 0 260 260" role="img" aria-label="Роза ветров профессиональных склонностей">
                <g transform="translate(-6 0)">
                    {[40, 70, 100].map((radius) => (
                        <circle key={radius} cx={center} cy={center} r={radius} className="career-chart-grid" />
                    ))}
                    {data.map((item, index) => {
                        const startAngle = index * segmentSize + 4;
                        const endAngle = (index + 1) * segmentSize - 4;
                        const outerRadius = innerRadius + 18 + ((item.value / 100) * 82);
                        const labelPoint = polarToCartesian(center, center, 104, startAngle + segmentSize / 2);
                        const color = chartColors[index % chartColors.length];
                        const activate = () => setActiveKey(item.key);

                        return (
                            <g
                                key={item.key}
                                className={`career-wind-segment ${activeItem.key === item.key ? 'active' : ''}`}
                                role="button"
                                tabIndex={0}
                                aria-label={`${item.label}: ${item.value}%`}
                                onMouseEnter={activate}
                                onFocus={activate}
                                onClick={activate}
                                onKeyDown={(event) => activateOnKeyboard(event, activate)}
                                style={{ animationDelay: `${index * 70}ms` }}
                            >
                                <path
                                    className="career-wind-path"
                                    d={describeArcSegment(center, center, innerRadius, outerRadius, startAngle, endAngle)}
                                    fill={color}
                                    opacity="0.9"
                                />
                                <SvgChartLabel x={labelPoint.x} y={labelPoint.y} label={item.label} />
                            </g>
                        );
                    })}
                    <circle cx={center} cy={center} r={innerRadius} className="career-chart-center" />
                </g>
            </svg>
            <ChartDetail item={activeItem} color={activeColor} />
        </div>
    );
};

const RadarChart = ({ data }: { data: CareerChartDatum[] }) => {
    const center = 130;
    const radius = 88;
    const firstKey = data[0]?.key ?? '';
    const [activeKey, setActiveKey] = React.useState(firstKey);

    React.useEffect(() => {
        if (firstKey && !data.some((item) => item.key === activeKey)) {
            setActiveKey(firstKey);
        }
    }, [activeKey, data, firstKey]);

    if (!data.length) return null;

    const activeItem = data.find((item) => item.key === activeKey) ?? data[0];
    const activeIndex = Math.max(data.findIndex((item) => item.key === activeItem.key), 0);
    const activeColor = chartColors[activeIndex % chartColors.length];

    return (
        <div className="career-chart-figure">
            <svg viewBox="0 0 260 260" role="img" aria-label="Радарная диаграмма рабочего стиля">
                {[25, 50, 75, 100].map((value) => (
                    <polygon
                        key={value}
                        points={getPolygonPoints(data.map((item) => ({ ...item, value })), radius, center)}
                        className="career-radar-grid"
                    />
                ))}
                {data.map((item, index) => {
                    const angle = -90 + (360 / data.length) * index;
                    const edge = polarToCartesian(center, center, radius, angle + 90);
                    const labelPoint = polarToCartesian(center, center, 102, angle + 90);
                    const isActive = activeItem.key === item.key;
                    return (
                        <g key={item.key} className={isActive ? 'active' : ''}>
                            <line x1={center} y1={center} x2={edge.x} y2={edge.y} className="career-radar-axis" />
                            <SvgChartLabel x={labelPoint.x} y={labelPoint.y} label={item.label} />
                        </g>
                    );
                })}
                <polygon points={getPolygonPoints(data, radius, center)} className="career-radar-area" />
                {data.map((item, index) => {
                    const angle = -90 + (360 / data.length) * index;
                    const point = polarToCartesian(center, center, (item.value / 100) * radius, angle + 90);
                    const activate = () => setActiveKey(item.key);
                    return (
                        <g
                            key={item.key}
                            className={`career-radar-point ${activeItem.key === item.key ? 'active' : ''}`}
                            role="button"
                            tabIndex={0}
                            aria-label={`${item.label}: ${item.value}%`}
                            onMouseEnter={activate}
                            onFocus={activate}
                            onClick={activate}
                            onKeyDown={(event) => activateOnKeyboard(event, activate)}
                            style={{ animationDelay: `${index * 80}ms` }}
                        >
                            <circle cx={point.x} cy={point.y} r="16" className="career-radar-hitarea" />
                            <circle cx={point.x} cy={point.y} r="4" className="career-radar-dot" />
                        </g>
                    );
                })}
            </svg>
            <ChartDetail item={activeItem} color={activeColor} />
        </div>
    );
};

const HorizontalBars = ({ data }: { data: CareerChartDatum[] }) => {
    const firstKey = data[0]?.key ?? '';
    const [activeKey, setActiveKey] = React.useState(firstKey);

    React.useEffect(() => {
        if (firstKey && !data.some((item) => item.key === activeKey)) {
            setActiveKey(firstKey);
        }
    }, [activeKey, data, firstKey]);

    if (!data.length) return null;

    const activeItem = data.find((item) => item.key === activeKey) ?? data[0];
    const activeIndex = Math.max(data.findIndex((item) => item.key === activeItem.key), 0);
    const activeColor = chartColors[activeIndex % chartColors.length];

    return (
        <div className="career-bars">
            {data.map((item, index) => {
                const color = chartColors[index % chartColors.length];
                return (
                    <button
                        type="button"
                        className={`career-bar-row ${activeItem.key === item.key ? 'active' : ''}`}
                        key={item.key}
                        onMouseEnter={() => setActiveKey(item.key)}
                        onFocus={() => setActiveKey(item.key)}
                        onClick={() => setActiveKey(item.key)}
                        style={{
                            '--bar-width': `${Math.max(6, item.value)}%`,
                            '--bar-color': color,
                            animationDelay: `${index * 80}ms`,
                        } as React.CSSProperties}
                    >
                        <div className="career-bar-label">
                            <span>{item.label}</span>
                            <b>{item.value}%</b>
                        </div>
                        <div className="career-bar-track">
                            <div className="career-bar-fill" />
                        </div>
                    </button>
                );
            })}
            <ChartDetail item={activeItem} color={activeColor} />
        </div>
    );
};

const getInitialDraft = (question?: CareerQuestion): DraftAnswer => {
    if (!question) return null;
    if (question.type === 'multi') return [];
    if (question.type === 'scale') return Math.round(((question.min ?? 1) + (question.max ?? 100)) / 2);
    return '';
};

const hasValidDraft = (question: CareerQuestion | undefined, draft: DraftAnswer) => {
    if (!question) return false;
    if (question.type === 'multi') return Array.isArray(draft) && draft.length > 0;
    if (question.type === 'scale') return typeof draft === 'number';
    return typeof draft === 'string' && draft.length > 0;
};

const normalizeDraft = (question: CareerQuestion, draft: DraftAnswer): CareerAnswerValue => {
    if (question.type === 'multi') return Array.isArray(draft) ? draft : [];
    if (question.type === 'scale') return typeof draft === 'number' ? draft : Math.round(((question.min ?? 1) + (question.max ?? 100)) / 2);
    return typeof draft === 'string' ? draft : '';
};

const questionTypeLabel = (question?: CareerQuestion) => {
    if (!question) return 'Адаптивный вопрос';
    if (question.type === 'multi') return 'Можно выбрать несколько';
    if (question.type === 'scale') return 'Оценка по шкале';
    return 'Выберите один вариант';
};

const QuestionControl = ({
    question,
    draft,
    setDraft,
}: {
    question: CareerQuestion;
    draft: DraftAnswer;
    setDraft: (value: DraftAnswer) => void;
}) => {
    if (question.type === 'scale') {
        const value = typeof draft === 'number' ? draft : Math.round(((question.min ?? 1) + (question.max ?? 100)) / 2);

        return (
            <div className="career-scale-control">
                <div className="career-scale-value">{value}</div>
                <input
                    type="range"
                    min={question.min ?? 1}
                    max={question.max ?? 100}
                    step={question.step ?? 1}
                    value={value}
                    onChange={(event) => setDraft(Number(event.target.value))}
                />
                <div className="career-scale-labels">
                    <span>{question.leftLabel}</span>
                    <span>{question.rightLabel}</span>
                </div>
            </div>
        );
    }

    if (question.type === 'multi') {
        const selected = Array.isArray(draft) ? draft : [];

        return (
            <div className="career-answer-list career-answer-list-multi">
                {(question.options ?? []).map((option) => {
                    const isSelected = selected.includes(option.id);
                    return (
                        <button
                            key={option.id}
                            className={isSelected ? 'selected' : ''}
                            onClick={() => {
                                setDraft(isSelected
                                    ? selected.filter((item) => item !== option.id)
                                    : [...selected, option.id]);
                            }}
                        >
                            <span>{option.label}</span>
                        </button>
                    );
                })}
            </div>
        );
    }

    return (
        <div className="career-answer-list">
            {(question.options ?? []).map((option) => {
                const selected = draft === option.id;
                return (
                    <button
                        key={option.id}
                        className={selected ? 'selected' : ''}
                        onClick={() => setDraft(option.id)}
                    >
                        {option.label}
                    </button>
                );
            })}
        </div>
    );
};

const getProfessionFitData = (result: CareerResult): CareerChartDatum[] =>
    result.charts.professionFit.map((item) => {
        const match = result.professionMatches.find((profession) => profession.id === item.key);
        return {
            ...item,
            description: match?.reason,
        };
    });

export const CareerTest = () => {
    const [stage, setStage] = React.useState<PageStage>('landing');
    const [answers, setAnswers] = React.useState<CareerAnswer[]>([]);
    const [question, setQuestion] = React.useState<CareerQuestion | undefined>();
    const [draft, setDraft] = React.useState<DraftAnswer>(null);
    const [result, setResult] = React.useState<CareerResult | undefined>();
    const [progress, setProgress] = React.useState(0);
    const [isLoading, setIsLoading] = React.useState(false);
    const [error, setError] = React.useState('');

    const loadStep = React.useCallback(async (nextAnswers: CareerAnswer[]) => {
        setIsLoading(true);
        setError('');
        try {
            const step = await getCareerStep(nextAnswers);
            setProgress(step.progress);
            if (step.done && step.result) {
                setResult(step.result);
                setQuestion(undefined);
                setDraft(null);
                setStage('results');
            } else if (step.question) {
                setQuestion(step.question);
                setDraft(getInitialDraft(step.question));
                setStage('test');
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (requestError) {
            setError('Сервис подбора профессии недоступен. Запустите сервис подбора через Docker Compose или на порту 8010.');
        } finally {
            setIsLoading(false);
        }
    }, []);

    const startTest = () => {
        setAnswers([]);
        setQuestion(undefined);
        setResult(undefined);
        setProgress(0);
        setStage('test');
        loadStep([]);
    };

    const submitAnswer = () => {
        if (!question || !hasValidDraft(question, draft)) return;
        const nextAnswers = [
            ...answers,
            {
                question_id: question.id,
                value: normalizeDraft(question, draft),
            },
        ];
        setAnswers(nextAnswers);
        loadStep(nextAnswers);
    };

    const undoLastAnswer = () => {
        if (!answers.length) {
            setStage('landing');
            return;
        }

        const nextAnswers = answers.slice(0, -1);
        setAnswers(nextAnswers);
        setResult(undefined);
        loadStep(nextAnswers);
    };

    if (stage === 'landing') {
        return (
            <div className="main career-page">
                <section className="career-test-hero" style={{ backgroundImage: `url(${heroImage})` }}>
                    <div className="career-test-hero-content">
                        <span>Адаптивный подбор профессии</span>
                        <h1>Пройти тест</h1>
                        <p>
                            Отвечайте на вопросы, а специальный алгоритм будет перестраивать маршрут после каждого ответа,
                            чтобы точнее подобрать подходящую профессию.
                        </p>
                        <button onClick={startTest}>Пройти тест</button>
                    </div>
                </section>

                <section className="career-landing-section">
                    <FadeInSection>
                        <div className="career-landing-heading">
                            <h2>Единый профориентационный маршрут</h2>
                            <p>
                                Вместо набора отдельных методик используется один адаптивный тест: варианты с одним ответом,
                                множественным выбором и шкалами помогают построить цельный профиль интересов, стиля работы и мотивации.
                            </p>
                        </div>
                    </FadeInSection>
                    <div className="career-benefits">
                        <div>
                            <b>15</b>
                            <span>вопросов максимум для подбора профессионального направления</span>
                        </div>
                        <div>
                            <b>→</b>
                            <span>каждый следующий вопрос подбирается по предыдущим ответам</span>
                        </div>
                        <div>
                            <b>%</b>
                            <span>итог содержит профессию, совпадения и графики профиля</span>
                        </div>
                    </div>
                </section>

                <section className="career-ai-section">
                    <div className="career-ai-description">
                        <h2>Как работает тест</h2>
                        <p>
                            Специальный алгоритм сравнивает ответы с профессиограммами, находит неопределенные зоны профиля
                            и задает вопрос, который лучше всего различает близкие карьерные направления.
                        </p>
                    </div>
                    <div className="career-ai-steps">
                        <span>Ответ</span>
                        <span>Профиль</span>
                        <span>Новый вопрос</span>
                        <span>Профессия</span>
                    </div>
                </section>
            </div>
        );
    }

    if (stage === 'results' && result) {
        return (
            <div className="main career-page career-results-page">
                <section className="career-results-hero">
                    <span>Итоги адаптивного теста</span>
                    <h1>Подходящая профессия: {result.primaryProfession}</h1>
                    <p>{result.summary}</p>
                    <div className="career-result-actions">
                        <button onClick={startTest}>Пройти заново</button>
                        <button className="career-secondary-button" onClick={undoLastAnswer}>Вернуться к вопросам</button>
                    </div>
                </section>

                <section className="career-results-grid">
                    <article className="career-result-panel career-main-result">
                        <h2>Профориентационный вывод</h2>
                        <div className="career-result-summary">
                            <div>
                                <h3>{result.primaryProfession}</h3>
                                <p>{result.summary}</p>
                            </div>
                        </div>
                    </article>

                    <article className="career-result-panel">
                        <h2>Роза ветров интересов</h2>
                        <WindRoseChart data={result.charts.interestRose} />
                    </article>

                    <article className="career-result-panel">
                        <h2>Рабочий стиль</h2>
                        <RadarChart data={result.charts.workStyle} />
                    </article>

                    <article className="career-result-panel">
                        <h2>Совпадение профессий</h2>
                        <HorizontalBars data={getProfessionFitData(result)} />
                    </article>

                    <article className="career-result-panel">
                        <h2>Профиль склонностей</h2>
                        <div className="career-trait-grid">
                            {result.traits.map((trait) => (
                                <div className="career-trait" key={trait.key}>
                                    <div>
                                        <span>{trait.label}</span>
                                        <b>{trait.value}%</b>
                                    </div>
                                    <p>{trait.description}</p>
                                </div>
                            ))}
                        </div>
                    </article>

                    <article className="career-result-panel">
                        <h2>Рекомендации</h2>
                        <div className="career-guidance-list">
                            {result.guidance.map((item) => (
                                <p key={item}>{item}</p>
                            ))}
                        </div>
                    </article>

                    <article className="career-result-panel">
                        <h2>Следующие шаги</h2>
                        <CareerNextSteps result={result} />
                    </article>
                </section>

                <section className="career-details-section">
                    <h2>Что еще видно по профилю</h2>
                    <div className="career-detail-list">
                        {result.facts.map((fact) => (
                            <div className="career-detail-item" key={fact.label}>
                                <h3>{fact.label}</h3>
                                <p>{fact.value}</p>
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
                <span>{questionTypeLabel(question)}</span>
                <h1>Пройти тест</h1>
                <p>Специальный алгоритм анализирует ответы и выбирает следующий вопрос под ваш текущий профиль.</p>
                <div className="career-progress">
                    <div className="career-progress-label">
                        <span>{answers.length} ответов</span>
                        <b>{progress}%</b>
                    </div>
                    <div className="career-progress-track">
                        <div className="career-progress-fill" style={{ width: `${progress}%` }} />
                    </div>
                </div>
                <div className="career-test-metrics">
                    <div>
                        <span>Формат</span>
                        <b>{questionTypeLabel(question)}</b>
                    </div>
                </div>
            </section>

            <section className="career-test-workspace career-test-workspace-single">
                <article className="career-question-panel">
                    {isLoading && (
                        <div className="career-loading-state">
                            <h2>Алгоритм подбирает следующий вопрос</h2>
                            <p>Профиль пересчитывается по вашим ответам.</p>
                        </div>
                    )}

                    {!isLoading && error && (
                        <div className="career-error-state">
                            <h2>Не удалось подключиться к сервису подбора</h2>
                            <p>{error}</p>
                            <div className="career-question-actions">
                                <button className="career-secondary-button" onClick={() => setStage('landing')}>На главную</button>
                                <button onClick={() => loadStep(answers)}>Повторить</button>
                            </div>
                        </div>
                    )}

                    {!isLoading && !error && question && (
                        <>
                            <div className="career-question-meta">
                                <span>Адаптивный вопрос</span>
                                <b>{questionTypeLabel(question)}</b>
                            </div>
                            <h2>{question.text}</h2>
                            {question.hint && <p className="career-question-hint">{question.hint}</p>}
                            <QuestionControl question={question} draft={draft} setDraft={setDraft} />
                            <div className="career-question-actions">
                                <button className="career-secondary-button" onClick={undoLastAnswer} disabled={isLoading}>
                                    {answers.length ? 'Назад' : 'На главную'}
                                </button>
                                <button onClick={submitAnswer} disabled={!hasValidDraft(question, draft) || isLoading}>
                                    Далее
                                </button>
                            </div>
                        </>
                    )}
                </article>
            </section>
        </div>
    );
};
