import * as React from 'react';
import {Profession} from "@components/Profession";
import {useModal} from "@model/ModalContext";
import {ProfileSettings, ProfileSettingsDOM} from "@components/ProfileSettings";

const avatar = require('@assets/img/avatar.png')
const settings = require('@assets/icon/settings.png')
const bsuir = require('@assets/img/establishment_bsuir.png')

export const Profile = () => {
    const { openModal } = useModal();

    return (
        <div className="main">
            <div className="main-profile">
                <div className="profile">
                    <div className="profile-content">
                        <div className="profile-main">
                            <article className="avatar">
                                <img src={avatar} alt="logo"/>
                                <div>
                                    <h1>Фамилия Имя Отчество</h1>
                                    <p>Имя пользователя</p>
                                </div>
                            </article>
                            <button onClick={() => {
                                openModal(ProfileSettingsDOM, null);
                            }}>
                                <img src={settings} alt="settings"/>
                                <p>Настройки пользователя</p>
                            </button>
                        </div>
                    </div>
                    <aside className="profile-tests">
                        <p>История тестов</p>
                        <ul>
                            <li>
                                <p>Тест №1</p>
                                <p>04.01.25</p>
                            </li>
                            <li>
                                <p>Тест №2</p>
                                <p>16.01.25</p>
                            </li>
                            <li>
                                <p>Тест №3</p>
                                <p>21.01.25</p>
                            </li>
                            <li>
                                <p>Тест №3</p>
                                <p>21.01.25</p>
                            </li>
                        </ul>
                    </aside>
                </div>
            </div>
        </div>
    );
}