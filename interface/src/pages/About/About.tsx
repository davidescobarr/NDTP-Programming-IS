import * as React from 'react';

export const About = () => {
    return (
        <div className="about-page-container">
            <div className="about-page">
                <h1 className="about-page-text" style={{textAlign: "justify", marginLeft: "100px", marginRight: "100px"}}>
                    Обучающая диалоговая экспертная система <b>MIKO</b> (<b>M</b>iko is an <b>I</b>ntelligent <b>K</b>nowledge-driven <b>A</b>ssistant),
                    разработанный на основе технологии{' '}
                        <a href="http://ims.ostis.net/" className="text">
                          OSTIS
                        </a>
                    . Обучающая диалоговая экспертная ostis-система MIKO
способна помочь школьникам с выбором профессии, а также, расскажет, чем занимается тот или иной специалист и приведёт
примеры задач, с которыми он сталкивается на работе. MIKO умеет проводить тест и анализируя его результаты делать вывод
и рекомендовать пользователю попробовать себя в профессии которая по мнению MIKO ему больше всего подходит.
                </h1>

                <h1 className="about-page-text">
                    Разработано{' '}
                        <a href="https://sem.systems/" className="text">
                          Intelligent Semantic Systems LLC
                        </a>
                    , Все права защищены.{' '}
                </h1>
            </div>
        </div>
    );
}
