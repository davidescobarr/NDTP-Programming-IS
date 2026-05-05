import * as React from 'react';
import { Test } from "@components/Test";
import { DefaultTest } from "@components/Tests/DefaultTest";
import { FormPanelComponent } from "@components/Chat/Forms/Form";
import { getTestsWithDescriptionsAgent } from "@agents/getTestsAndDescriptionsAgent";
import { getHolandTestAgent } from "@agents/getHolandTestAgent";
import { getIovaishiTestAgent } from "@agents/getIovaishiTestAgent";
import {useModal} from "@model/ModalContext"; // Импорт агента
import { analyzeHolandTestAgent } from "@agents/analyzeHolandTestAgent";
import { analyzeIovaishiTestAgent } from "@agents/analyzeIovaishiTestAgent";
import FadeInSection from "@components/FadeInSection/FadeInSection";
import { getMotivationalTestAgent } from '@api/sc/agents/getMotivationalTestAgent';
import { analyzeMotivationalTestAgent } from '@api/sc/agents/analyzeMotivationalTestAgent';
import { getPersonalityToSuccessTestAgent } from '@api/sc/agents/getPersonalityToSuccessTestAgent';
import { analyzePersonalityToSuccessTestAgent } from '@api/sc/agents/analyzePersonalityToSuccessTestAgent';
import { getNeedInAchievementTestAgent } from '@api/sc/agents/getNeedInAchievementAgent';
import { analyzeNeedInAchievementTestAgent } from '@api/sc/agents/analyzeNeedInAchievementTestAgent';
import { getNeedInApprovalTestAgent } from '@api/sc/agents/getNeedInApprovalAgent';
import { analyzeNeedInApprovalTestAgent } from '@api/sc/agents/analyzeNeedInApprovalTestAgent';
import { getAbilityInSympathyTestAgent } from '@api/sc/agents/getAbilityInSympathyAgent';
import { analyzeAbilityInSympathyTestAgent } from '@api/sc/agents/analyzeAbilityInSympathyTestAgent';
import { GetAdvancedTestAgent } from '@api/sc/agents/getAdvancedAgent';
import { AnalyzeAdvancedTestAgent } from '@api/sc/agents/analyzeAdvancedTestAgent';


const getTestImage = (key: string) => {
    try {
        return require(`@assets/image/${key}/image.png`);
    } catch (e) {
        return require(`@assets/image/default_profession.png`);
    }
};


const bsuir = require('@assets/img/proftest.png');
export const endTestTestComponent = ({ text, closeModal }) => {
    return (
        <div>
            <h1>Ваши итоги теста</h1>
            <p>{text}</p>
            <button onClick={() => closeModal()}>
                Закрыть
            </button>
        </div>
    );
};

const createEndTestHandler = (analyzeFunction, testName) => {
  return async ({ questions, closeModal, openModal }) => {
    closeModal();
    console.log(`Завершение теста: ${testName}`);

    try {
      const resultText = await analyzeFunction(questions);
      console.log("Результат:", resultText);
      openModal(endTestTestComponent, { text: resultText.text, closeModal });
    } catch (error) {
      console.error(`Ошибка при анализе теста ${testName}:`, error);
      openModal(endTestTestComponent, { text: "Ошибка при обработке теста", closeModal });
    }
  };
};


export const Tests = () => {
    const [tests, setTests] = React.useState<Map<string, string>>(new Map());
    const [holandTestData, setHolandTestData] = React.useState(null);
    const [iovaishiTestData, setIovaishiTestData] = React.useState(null);
    const [motivationalTestData, setMotivationalTestData] = React.useState(null);
    const [personalityToSuccessTestData, setPersonalityToSuccessTestData] = React.useState(null);
    const [needInAchievementTestData, setNeedInAchievementTestData] = React.useState(null);
    const [needInApprovalTestData, setneedInApprovalTestData] = React.useState(null);
    const [abilityInSympathyTestData, setAbilityInSympathyTestData] = React.useState(null);
    const [advancedTestData, setAdvancedTestData] = React.useState(null);

    React.useEffect(() => {
        (async () => {
            const testsData = await getTestsWithDescriptionsAgent();
            console.log("Finded tests", testsData);
            setTests(testsData);

            if (testsData["test_holand"]) {
                const holandData = await getHolandTestAgent();
                console.log("Holand Test Data:", holandData);
                setHolandTestData(holandData);
            }
            if (testsData["test_iovaishi"]) {
                const iovaishiData = await getIovaishiTestAgent();
                console.log("Iovaishi Test Data:", iovaishiData);
                setIovaishiTestData(iovaishiData);
            }
            if (testsData["test_motivational"]) {
                const motivationalData = await getMotivationalTestAgent();
                console.log("Motivational Test Data:", motivationalData);
                setMotivationalTestData(motivationalData);
            }
            if (testsData["test_personalitytosuccess"]) {
                const personalityToSuccessData = await getPersonalityToSuccessTestAgent();
                console.log("PersonalityToSuccess Test Data:", personalityToSuccessData);
                setPersonalityToSuccessTestData(personalityToSuccessData);
            }
            if (testsData["test_needinachievement"]) {
                const needInAchievementTestData = await getNeedInAchievementTestAgent();
                console.log("NeedInAchievement Test Data:", needInAchievementTestData);
                setNeedInAchievementTestData(needInAchievementTestData);
            }
            if (testsData["test_needinapproval"]) {
                const needInApprovalTestData = await getNeedInApprovalTestAgent();
                console.log("NeedInApproval Test Data:", needInApprovalTestData);
                setneedInApprovalTestData(needInApprovalTestData);
            }
            if (testsData["test_abilityinsympathy"]) {
                const abilityInSympathyTestData = await getAbilityInSympathyTestAgent();
                console.log("AbilityInSympathy Test Data:", abilityInSympathyTestData);
                setAbilityInSympathyTestData(abilityInSympathyTestData);
            }
            if (testsData["test_advanced"]) {
                const advancedTestData = await GetAdvancedTestAgent();
                console.log("Advanced Test Data:", advancedTestData);
                setAdvancedTestData(advancedTestData);
            }
        })();
    }, []);

    const testConfig = {
    'test_holand': [{ questions: holandTestData }, createEndTestHandler(analyzeHolandTestAgent, 'Холланда')],
    'test_iovaishi': [{ questions: iovaishiTestData }, createEndTestHandler(analyzeIovaishiTestAgent, 'Йоваши')],
    'test_motivational': [{ questions: motivationalTestData}, createEndTestHandler(analyzeMotivationalTestAgent, 'Мотивационный тест')],
    'test_personalitytosuccess': [{ questions: personalityToSuccessTestData}, createEndTestHandler(analyzePersonalityToSuccessTestAgent, 'Диагностика личности на мотивацию к успеху')],
    'test_needinachievement': [{ questions: needInAchievementTestData}, createEndTestHandler(analyzeNeedInAchievementTestAgent, 'Оценка потребности в достижении')],
    'test_needinapproval': [{ questions: needInApprovalTestData}, createEndTestHandler(analyzeNeedInApprovalTestAgent, 'Оценка потребности в одобрении')],
    'test_abilityinsympathy': [{ questions: abilityInSympathyTestData}, createEndTestHandler(analyzeAbilityInSympathyTestAgent, 'Диагностика способности к эмпатии')],
    'test_advanced': [{ questions: advancedTestData}, createEndTestHandler(AnalyzeAdvancedTestAgent, 'Расширенный тест')]
    };

    
    return (
        <div className="main">
            <section className="establishments">
                <div className="section-content">
                    <FadeInSection>
                        <h1 className="title">Тесты</h1>
                    </FadeInSection>
                    <div className="professions-list">
                        {
                            //Object.entries(tests).map(([key, value]) => {
                                //return <Test name={value.name} description={value.info} idTest={key} photo={bsuir} componentTest={DefaultTest} propsTest={{}}/>
                                //})
                            }
                        {Object.entries(tests).map(([key, value]) => {
                            console.log(key);
                            const propsTest = testConfig[key] || [{questions: holandTestData}, createEndTestHandler(analyzeHolandTestAgent, 'Холланда')];
                            return (
                                <Test
                                    name={value.name}
                                    description={value.info}
                                    idTest={key}
                                    photo={getTestImage(key)}
                                    componentTest={DefaultTest}
                                    propsTest={propsTest}
                                />
                            );
                        })}
                        <Test
                            name="Профориентационный тест"
                            description="Глубокий анализ интересов, способностей и предпочтений.
Даёт более точный и развернутый профиль, чем экспресс‑тест, и помогает выбрать подходящие сферы."
                            idTest="test"
                            photo={bsuir}
                            componentTest={FormPanelComponent}
                            propsTest={{}}
                        />
                    </div>
                </div>
            </section>
        </div>
    );
}