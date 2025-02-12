import * as React from 'react';
import { Test } from "@components/Test";
import { DefaultTest } from "@components/Tests/DefaultTest";
import { FormPanelComponent } from "@components/Chat/Forms/Form";
import { getTestsWithDescriptionsAgent } from "@agents/getTestsAndDescriptionsAgent";
import { getHolandTestAgent } from "@agents/getHolandTestAgent"; // Импорт агента

const bsuir = require('@assets/img/establishment_bsuir.png');

export const Tests = () => {
    const [tests, setTests] = React.useState<Map<string, string>>(new Map());
    const [holandTestData, setHolandTestData] = React.useState(null);

    React.useEffect(() => {
        (async () => {
            const testsData = await getTestsWithDescriptionsAgent();
            console.log(testsData);
            setTests(testsData);

            // Если тест Холланда есть в списке, запрашиваем его JSON-данные
            if (testsData["test_holand"]) {
                const holandData = await getHolandTestAgent();
                console.log("Holand Test Data:", holandData);
                setHolandTestData(holandData);
            }
        })();
    }, []);
    return (
        <div className="main">
            <section className="establishments">
                <div className="section-content">
                    <h1 className="title">Тесты</h1>
                    <div className="professions-list">
                        {
                            //Object.entries(tests).map(([key, value]) => {
                                //return <Test name={value.name} description={value.info} idTest={key} photo={bsuir} componentTest={DefaultTest} propsTest={{}}/>
                            //})
                        }
                        {
                            Object.entries(tests).map(([key, value]) => {
                                return (
                                    <Test
                                        name={value.name}
                                        description={value.info}
                                        idTest={key}
                                        photo={bsuir}
                                        componentTest={DefaultTest}
                                        propsTest={key === "test_holand" ? { questions: holandTestData } : {}}
                                    />
                                );
                            })
                        }
                        <Test name="test" description="description" idTest="test" photo={bsuir} componentTest={DefaultTest} propsTest={{
                            questions: [
                                {
                                    'display_name': 'Как вы относитесь к животным?',
                                    'answers': [
                                        {
                                            'name': 'Хорошо',
                                            'id': 0
                                        },
                                        {
                                            'name': 'Нормально',
                                            'id': 1
                                        },
                                        {
                                            'name': 'Плохо',
                                            "id": 2
                                        }
                                    ]
                                },
                                {
                                    'display_name': 'Как часто вы занимаетесь спортом?',
                                    'answers': [
                                        {
                                            'name': 'Часто',
                                            'id': 0
                                        },
                                        {
                                            'name': 'Достаточно',
                                            'id': 1
                                        },
                                        {
                                            'name': 'Иногда',
                                            'id': 2
                                        },
                                        {
                                            'name': 'Редко',
                                            'id': 3
                                        }
                                    ]}
                            ]
                        }}/>
                        <Test name="Профориентационный тест" description="Пройдя данный тест вы сможете определить свою профессию." idTest="test" photo={bsuir} componentTest={FormPanelComponent} propsTest={{}}/>
                    </div>
                </div>
            </section>
        </div>
    );
}