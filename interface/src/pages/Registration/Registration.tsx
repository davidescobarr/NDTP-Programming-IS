import {RegistrationForm} from "@components/RegistrationForm";
import {NavLink} from "react-router-dom";
import { routes } from '@constants';

export const Registration = () => {
    return (
        <div className="main-auth">
            <div className="auth">
                <div className="auth-top">
                    <NavLink to={routes.REGISTRATION}>
                        <button className="active">Регистрация</button>
                    </NavLink>
                    <NavLink to={routes.REGISTRATION}>
                        <button>Авторизация</button>
                    </NavLink>
                </div>
                <RegistrationForm />
            </div>
        </div>
    );
}