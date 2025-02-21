import React from "react";
import {LoginForm} from "@components/LoginForm";
import {NavLink} from "react-router-dom";
import { routes } from '@constants';
import FadeInSection from "@components/FadeInSection/FadeInSection";

export const Login = () => {
    return (
        <FadeInSection>
            <div className="main-auth">
                <div className="auth">
                    <div className="auth-top">
                        <NavLink to={routes.REGISTRATION}>
                            Регистрация
                        </NavLink>
                        <NavLink to={routes.LOGIN}>
                            Авторизация
                        </NavLink>
                    </div>
                    <LoginForm/>
                </div>
            </div>
        </FadeInSection>
    );
}