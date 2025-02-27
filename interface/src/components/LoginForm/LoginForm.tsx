import React, {ReactNode} from "react";
import {registerUser} from "@agents/userRegistrationAgent";
import {LOGIN, PROFILE} from "../../constants/routes";
import {authenticateUser} from "@agents/userAuthorizationAgent";
import { NavigateFunction } from "react-router-dom";

interface LoginFormProps {
    navigate: NavigateFunction; // Указываем тип для navigate
}

export class LoginForm extends React.Component<LoginFormProps> {
    login = '';
    password = '';

    constructor(props) {
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
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
        this.props.navigate(PROFILE);
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