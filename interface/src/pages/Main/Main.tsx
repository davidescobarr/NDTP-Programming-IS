import * as React from 'react';

const banner1 = require('@assets/img/banner1.png'); // with require
const banner2 = require('@assets/img/banner2.png'); // with require

export const Main = () => {
    return (
        <div className="main">
            <section className="banner">
                <div className="about">
                    <p>Как выбрать профессию?</p>
                    <h1>Наш сайт поможет с выбором профессии</h1>
                </div>
                <div className="photo">
                    <img src={banner1} alt="banner1" />
                    <img src={banner2} alt="banner2" />
                </div>
            </section>
            <section className="best">
                <h1>Наши преимущества</h1>
                <hr />
                <div>
                    <div></div>
                    <div></div>
                    <div></div>
                </div>
            </section>
        </div>
    );
}