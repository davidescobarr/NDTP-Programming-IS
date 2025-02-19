import React, {useState} from "react";
import {registerUser} from "@agents/userRegistrationAgent";
import {PROFILE} from "../../constants/routes";
import {authenticateUser} from "@agents/userAuthorizationAgent";
import {useNavigate} from "react-router-dom";

export function LoginForm () {
    const [login, setLogin] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        alert('Отправленное имя: ' + login);
        event.preventDefault();
    }

    const userAuthorizationCallBack = async () => {
        const user = await authenticateUser(login, password);
        if (user !== null){
            goToProfilePage(user.value);
        }
        else{
            console.log("user doesn't exist or password is uncorrect");
        }
    }

    const goToProfilePage = (userId : number) => {
        window.history.pushState({userId}, '', PROFILE);
        navigate(`/Profile/${userId}`);
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Имя пользователя:
                <input type="text" onChange={event => setLogin(event.target.value)}/>
            </label>
            <label>
                Пароль:
                <input type="password" onChange={event => setPassword(event.target.value)}/>
            </label>
            <input type="submit" value="Войти" onClick={() => {userAuthorizationCallBack()}}/>
        </form>
    );
}