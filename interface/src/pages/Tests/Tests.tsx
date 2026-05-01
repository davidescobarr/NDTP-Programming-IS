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
import { GetMotivationalTestAgent } from '@api/sc/agents/getMotivationalTestAgent';
import { analyzeMotivationalTestAgent } from '@api/sc/agents/analyzeMotivationalTestAgent';


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
                const motivationalData = await GetMotivationalTestAgent();
                console.log("Motivational Test Data:", motivationalData);
                setMotivationalTestData(motivationalData);
            }
        })();
    }, []);

    const testConfig = {
    'test_holand': [{ questions: holandTestData }, createEndTestHandler(analyzeHolandTestAgent, 'Холланда')],
    'test_iovaishi': [{ questions: iovaishiTestData }, createEndTestHandler(analyzeIovaishiTestAgent, 'Йоваши')],
    'test_motivational': [{ questions: motivationalTestData}, createEndTestHandler(analyzeMotivationalTestAgent, 'Мотивационный тест')]
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
                            const propsTest = testConfig[key] || createEndTestHandler(analyzeHolandTestAgent, 'Холланда');
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
                            description="Пройдя данный тест вы сможете определить свою профессию."
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