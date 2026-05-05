import {RegistrationForm} from "@components/RegistrationForm";
import {NavLink} from "react-router-dom";
import { routes } from '@constants';
import FadeInSection from "@components/FadeInSection/FadeInSection";
import {useEffect} from "react";
import {authenticateUser} from "@agents/userAuthorizationAgent";
import {PROFILE} from "../../constants/routes";
import {useNavigate} from "react-router-dom";

export const Registration = () => {
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
                        <NavLink to={routes.REGISTRATION} className="active">
                            Регистрация
                        </NavLink>
                        <NavLink to={routes.LOGIN}>
                            Авторизация
                        </NavLink>
                    </div>
                    <RegistrationForm navigate={navigate} />
                </div>
            </div>
        </FadeInSection>
    );
}