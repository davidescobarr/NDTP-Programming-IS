import React from "react";
import { registerUser } from "@api/sc/agents/userRegistrationAgent";
import {PROFILE} from "../../constants/routes";
import { NavigateFunction } from "react-router-dom";

interface RegistrationFormProps {
    navigate: NavigateFunction; // Указываем тип для navigate
}

export class RegistrationForm extends React.Component<RegistrationFormProps> {
    firstname = '';
    surname = '';
    patronymic = '';
    login = '';
    password = '';

    constructor(props) {
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();
    }

    userRegistrationCallBack = async () => {
        const user = await registerUser(this.login, this.firstname, this.surname, this.patronymic, this.password);
        if (user !== null){
            this.goToProfilePage();
        }
    }

    goToProfilePage = () => {
        this.props.navigate(PROFILE);
    };

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Фамилия:
                    <input type="text" onChange={event => this.surname = event.target.value} />
                </label>
                <label>
                    Имя:
                    <input type="text" onChange={event => this.firstname = event.target.value}/>
                </label>
                <label>
                    Отчество:
                    <input type="text" onChange={event => this.patronymic = event.target.value}/>
                </label>
                <label>
                    Имя пользователя:
                    <input type="text" onChange={event => this.login = event.target.value}/>
                </label>
                <label>
                    Пароль:
                    <input type="password" onChange={event => this.password = event.target.value}/>
                </label>
                <input type="submit" value="Зарегистрироваться" onClick={() => {this.userRegistrationCallBack()}}/>
            </form>
        );
    }
}