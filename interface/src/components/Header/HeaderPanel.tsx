import { routes } from '@constants';
import * as React from 'react';
import { NavLink } from 'react-router-dom';

export const HeaderPanel = () => {
    return (
        <div className="header">
            <h1 className="header-logo-text"><NavLink to={routes.MAIN}>MIKO</NavLink></h1>
            <div className="nav-container">
                <ul className="nav">
                    <li>
                        <NavLink to={routes.TESTS}>Тесты</NavLink>
                    </li>
                    <li>
                        <NavLink to={routes.ESTABLISHMENTS}>Учебные заведения</NavLink>
                    </li>
                    <li>
                        <NavLink to={routes.PROFESSIONS}>Профессии</NavLink>
                    </li>
                    <li>
                        <NavLink to={routes.PROFILE}>Личный кабинет</NavLink>
                    </li>
                </ul>
            </div>
        </div>
    );
}
