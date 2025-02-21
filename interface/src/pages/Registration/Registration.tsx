import {RegistrationForm} from "@components/RegistrationForm";
import {NavLink} from "react-router-dom";
import { routes } from '@constants';
import FadeInSection from "@components/FadeInSection/FadeInSection";

export const Registration = () => {
    return (
        <FadeInSection>
            <div className="main-auth">
                <div className="auth">
                    <div className="auth-top">
                        <NavLink to={routes.REGISTRATION} className="active">
                            Регистрация
                        </NavLink>
                        <NavLink to={routes.LOGIN}>
                            Авторизация
                        </NavLink>
                    </div>
                    <RegistrationForm/>
                </div>
            </div>
        </FadeInSection>
    );
}