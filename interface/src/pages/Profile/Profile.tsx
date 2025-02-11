import * as React from 'react';
import {Profession} from "@components/Profession";
import {searchAllUserInfo} from "@api/sc/search/searchUserInfo";
import {useParams} from "react-router-dom";

const avatar = require('@assets/img/avatar.png')
const settings = require('@assets/icon/settings.png')
const bsuir = require('@assets/img/establishment_bsuir.png')

export const Profile = () => {
    const { userId } = useParams<{ userId: string }>();
    const [userNickname, setUserNickname] = React.useState<string>();
    const [userPassword, setUserPassword] = React.useState<string>();
    const [userFirstName, setUserFirstName] = React.useState<string>();
    const [userSurname, setUserSurname] = React.useState<string>();
    const [userPatronymic, setUserPatronymic] = React.useState<string>();


    React.useEffect(() => {
        (async () => {
            const [nickname, password, first_name, surname, patronymic] = await searchAllUserInfo(Number(userId));
            setUserNickname(nickname);
            setUserPassword(password);
            setUserFirstName(first_name);
            setUserSurname(surname);
            setUserPatronymic(patronymic);
        })();
    }, [userId]);
    return (
        <div className="main">
            <div className="main-profile">
                <div className="profile">
                    <div className="profile-content">
                        <div className="profile-main">
                            <article className="avatar">
                                <img src={avatar} alt="logo" />
                                <div>
                                    <h1>
                                        {userSurname} {userFirstName} {userPatronymic}
                                    </h1>
                                    <p>{userNickname}</p>
                                </div>
                            </article>
                            <button>
                                <img src={settings} alt="settings" />
                                <p>Настройки пользователя</p>
                            </button>
                            <button>
                                <img src={settings} alt="settings" />
                                <p>Чёрный список пользователей</p>
                            </button>
                        </div>
                        <div className="profile-friends">
                            <h3>Друзья</h3>
                            <ul>
                                <li>
                                    <img src={avatar} alt="logo" />
                                    <p>Имя пользователя</p>
                                </li>
                                <li>
                                    <img src={avatar} alt="logo" />
                                    <p>Имя пользователя</p>
                                </li>
                                <li>
                                    <img src={avatar} alt="logo" />
                                    <p>Имя пользователя</p>
                                </li>
                                <li>
                                    <img src={avatar} alt="logo" />
                                    <p>Имя пользователя</p>
                                </li>
                                <li>
                                    <img src={avatar} alt="logo" />
                                    <p>Имя пользователя</p>
                                </li>
                            </ul>
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
                            <li><p>Тест №3</p>
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