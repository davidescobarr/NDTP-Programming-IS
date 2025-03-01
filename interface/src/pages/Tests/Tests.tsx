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


const bsuir = require('@assets/img/establishment_bsuir.png');
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


const endTestTest = async ({ questions, closeModal, openModal }) => {
    closeModal(); // Закрываем текущий модал
    console.log("okay");

    try {
        const resultText = await analyzeHolandTestAgent(questions);

        console.log("dasdasd", resultText);
        openModal(endTestTestComponent, { text: resultText.text, closeModal });
    } catch (error) {
        console.error("Ошибка при анализе теста Холланда:", error);
        openModal(endTestTestComponent, { text: "Ошибка при обработке теста", closeModal });
    }
};

const endTestIovaishi = async ({ questions, closeModal, openModal }) => {
    closeModal(); // Закрываем текущий модал
    console.log("okay");

    try {
        const resultText = await analyzeIovaishiTestAgent(questions);

        console.log("dasdasd", resultText);
        openModal(endTestTestComponent, { text: resultText.text, closeModal });
    } catch (error) {
        console.error("Ошибка при анализе теста Йовайши:", error);
        openModal(endTestTestComponent, { text: "Ошибка при обработке теста", closeModal });
    }
};


export const Tests = () => {
    const [tests, setTests] = React.useState<Map<string, string>>(new Map());
    const [holandTestData, setHolandTestData] = React.useState(null);
    const [iovaishiTestData, setIovaishiTestData] = React.useState(null);

    React.useEffect(() => {
        (async () => {
            const testsData = await getTestsWithDescriptionsAgent();
            console.log(testsData);
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
        })();
    }, []);
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
                            return (
                                <Test
                                    name={value.name}
                                    description={value.info}
                                    idTest={key}
                                    photo={bsuir}
                                    componentTest={DefaultTest}
                                    propsTest={
                                        key === 'test_holand' ? [{ questions: holandTestData }, endTestTest] : key === "test_iovaishi" ? [{ questions: iovaishiTestData }, endTestIovaishi] : [{ questions: holandTestData}, endTestTest]

                                    }
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