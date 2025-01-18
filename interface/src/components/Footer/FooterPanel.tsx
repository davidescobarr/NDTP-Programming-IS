import { routes } from '@constants';
import * as React from 'react';
import { NavLink } from 'react-router-dom';

export const FooterPanel = () => {
    return (
        <div className="footer">
            <div className="nav-container">
                <ul className="nav">
                    <li>
                        <NavLink exact to={routes.MAIN}>Главная</NavLink>
                    </li>
                    <li>
                        <NavLink to={routes.TESTS}>Тесты</NavLink>
                    </li>
                    <li>
                        <NavLink to={routes.ESTABLISHMENTS}>Учебные заведения</NavLink>
                    </li>
                    <li>
                        <NavLink to={routes.PROFESSIONS}>Профессии</NavLink>
                    </li>
                </ul>
            </div>
            <hr/>
            <div className="about-container">
                <p>
                    Copyright © 2024-2025 OSTIS
                </p>
                <p>
                    Developed by DavidEscobarr and Jun_k01
                </p>
            </div>
        </div>
    );
}