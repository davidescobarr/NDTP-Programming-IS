import React from "react";
import { registerUser } from "@api/sc/agents/userRegistrationAgent";
import {PROFILE} from "../../constants/routes";

export class RegistrationForm extends React.Component {
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
        alert('Отправленное имя: ' + this.login);
        event.preventDefault();
    }

    userRegistrationCallBack = async () => {
        const user = registerUser(this.login, this.firstname, this.surname, this.patronymic, this.password);
        if (user !== null){
            this.goToProfilePage();
        }
    }

    goToProfilePage = () => {
        window.history.pushState({}, '', PROFILE);
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