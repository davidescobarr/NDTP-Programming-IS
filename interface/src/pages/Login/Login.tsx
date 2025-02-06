import React from "react";
import {LoginForm} from "@components/LoginForm";

export const Login = () => {
    return (
        <div className="main-auth">
            <div className="auth">
                <div className="auth-top">
                    <button>Регистрация</button>
                    <button className="active">Авторизация</button>
                </div>
                <LoginForm/>
            </div>
        </div>
    );
}