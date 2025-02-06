import React from "react";
import {registerUser} from "@agents/userRegistrationAgent";
import {PROFILE} from "../../constants/routes";
import {authenticateUser} from "@agents/userAuthorizationAgent";

export class LoginForm extends React.Component {
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

    userAuthorizationCallBack = async () => {
        const user = authenticateUser(this.login, this.password);
        if (user !== null){
            this.goToProfilePage();
        }
        else{
            console.log("user isn't exist or password is wrong")
        }
    }

    goToProfilePage = () => {
        window.history.pushState({}, '', PROFILE);
    };

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Имя пользователя:
                    <input type="text" onChange={event => this.login = event.target.value} />
                </label>
                <label>
                    Пароль:
                    <input type="password" onChange={event => this.password = event.target.value}/>
                </label>
                <input type="submit" value="Войти" onClick={() => {this.userAuthorizationCallBack()}}/>
            </form>
        );
    }
}