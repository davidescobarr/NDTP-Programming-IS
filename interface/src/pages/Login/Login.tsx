import React, {useEffect} from "react";
import {LoginForm} from "@components/LoginForm";
import { NavLink, useNavigate } from "react-router-dom";
import { routes } from '@constants';
import FadeInSection from "@components/FadeInSection/FadeInSection";
import {PROFILE} from "../../constants/routes";
import {authenticateUser} from "@agents/userAuthorizationAgent";


export const Login = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const nickname = localStorage.getItem("nickname");
        const password = localStorage.getItem("password");
        if(nickname !== null && password !== null) {
            const user = authenticateUser(nickname, password);
            if (user !== null){
                navigate(PROFILE);
            } else {
                localStorage.clear();
            }
        }
    });

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
                    <LoginForm navigate={navigate}/>
                </div>
            </div>
        </FadeInSection>
    );
}