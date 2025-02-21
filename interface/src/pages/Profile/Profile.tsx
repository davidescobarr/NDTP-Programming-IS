import * as React from 'react';
import {Profession} from "@components/Profession";
import {useModal} from "@model/ModalContext";
import {ProfileSettings, ProfileSettingsDOM} from "@components/ProfileSettings";
import {HistoryTest} from "@components/HistoryTest";

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
                                <HistoryTest nameTest="Тест №1" dateTest="04.01.25" resultTest="Итоги теста 1"/>
                            </li>
                            <li>
                                <HistoryTest nameTest="Тест №2" dateTest="13.01.25" resultTest="Итоги теста 2"/>
                            </li>
                            <li>
                                <HistoryTest nameTest="Тест №3" dateTest="16.02.25" resultTest="Итоги теста 3"/>
                            </li>
                            <li>
                                <HistoryTest nameTest="Тест №4" dateTest="21.03.25" resultTest="Итоги теста 4"/>
                            </li>
                        </ul>
                    </aside>
                </div>
            </div>
        </div>
    );
}