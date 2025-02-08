import * as React from "react";
import {registerUser} from "@agents/userRegistrationAgent";

export const ProfileSettingsDOM = () => {
    return <ProfileSettings />
}

export class ProfileSettings extends React.Component {
    firstname = '';
    surname = '';
    patronymic = '';
    password = '';

    constructor(props) {
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        alert(this.firstname);
        event.preventDefault();
    }

    userSaveSettings = async () => {

    }

    render() {
        return (
            <div className="profile-settings">
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Фамилия:
                        <input type="text" onChange={event => this.surname = event.target.value}/>
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
                        Пароль:
                        <input type="password" onChange={event => this.password = event.target.value}/>
                    </label>
                    <input type="submit" value="Сохранить" onClick={() => {
                        this.userSaveSettings()
                    }}/>
                </form>
            </div>
        );
    }
};