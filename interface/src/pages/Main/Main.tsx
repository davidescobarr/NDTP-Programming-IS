import * as React from 'react';

const banner1 = require('@assets/img/banner1.png'); // with require
const banner2 = require('@assets/img/banner2.png'); // with require
const icon_modern = require('@assets/icon/icon-modern.png');
const icon_question = require('@assets/icon/icon_question.png');
const icon_cogwheel = require('@assets/icon/icon-cogwheel.png');
const icon_people_example = require('@assets/img/icon_people_example.png');

export const Main = () => {
    return (
        <div className="main">
            <section className="banner">
                <div className="section-content">
                    <div className="about">
                        <p>Как выбрать профессию?</p>
                        <h1>Наш сайт поможет с выбором профессии</h1>
                    </div>
                    <div className="photo">
                        <img src={banner1} alt="banner1" />
                        <img src={banner2} alt="banner2" />
                    </div>
                </div>
            </section>
            <section className="ourbest">
                <div className="section-content">
                    <h1>Наши преимущества</h1>
                    <hr />
                    <section className="ourbest-points">
                        <div>
                            <img src={icon_modern} alt="icon-modern" />
                            <p>
                                <b>Современные технологии</b>
                            </p>
                            <p>Мы используем современные методы и технологии для проведения тестирования</p>
                        </div>
                        <div>
                            <img src={icon_cogwheel} alt="icon-modern" />
                            <p>
                                <b>Большой функционал</b>
                            </p>
                            <p>У нас есть большое количество инструментов для проведения тестов</p>
                        </div>
                        <div>
                            <img src={icon_question} alt="icon-modern"/>
                            <p><b>Возможность вопросов</b></p>
                            <p>На сайте можно задавать вопросы касаемо учебных заведений и профессий</p>
                        </div>
                    </section>
                </div>
            </section>
            <section className="registration">
                <div className="section-content">
                    <aside>
                        <img src={icon_people_example} alt="people_example" />
                        <div className="circle_users">
                            <p>253 пользователей</p>
                        </div>
                    </aside>
                    <div className="registration-description">
                        <p>Не знаешь куда поступить?</p>
                        <p><b>Пройди профориентационный тест и просмотри информацию о профессии и об учебном заведении</b></p>
                        <button>Зарегистрироваться</button>
                    </div>
                </div>
            </section>
        </div>
    );
}