import React, {useState} from "react";
import {registerUser} from "@agents/userRegistrationAgent";
import {PROFILE} from "../../constants/routes";
import {useNavigate} from "react-router-dom";

export function RegistrationForm () {
    const [login, setLogin] = useState("");
    const [password, setPassword] = useState("");
    const [firstname, setFirstname] = useState("");
    const [surname, setSurname] = useState("");
    const [patronymic, setPatronymic] = useState("");
    const navigate = useNavigate();

    const userRegistrationCallBack = async () => {
        const user = await registerUser(login, firstname, surname, patronymic, password);
        if (user !== null){
            goToProfilePage(user.value);
        }
        else{
            console.log("user doesn't exist or password is uncorrected");
        }
    }

    const goToProfilePage = (userId : number) => {
        window.history.pushState({userId}, '', PROFILE);
        navigate(`/Profile/${userId}`);
    };

    return (
        <form onSubmit={userRegistrationCallBack}>
            <label>
                Фамилия:
                <input type="text" onChange={event => setSurname(event.target.value)} />
            </label>
            <label>
                Имя:
                <input type="text" onChange={event => setFirstname(event.target.value)} />
            </label>
            <label>
                Отчество:
                <input type="text" onChange={event => setPatronymic(event.target.value)} />
            </label>
            <label>
                Имя пользователя:
                <input type="text" onChange={event => setLogin(event.target.value)} />
            </label>
            <label>
                Пароль:
                <input type="password" onChange={event => setPassword(event.target.value)} />
            </label>
            <input type="submit" value="Зарегистрироваться" onClick={() => {userRegistrationCallBack()}}/>
        </form>
    );
}