import * as React from 'react';
import {Profession} from "@components/Profession";

const bsuir = require('@assets/img/establishment_bsuir.png')

export const Profile = () => {
    return (
        <div className="main">
           <div className="profile">
               <div className="profile-content">
                   <div className="profile-main">
                        <article className="avatar">
                            <img src="" alt="logo"/>
                            <div>
                                <h1>Фамилия Имя Отчество</h1>
                                <p>Имя пользователя</p>
                            </div>
                        </article>
                       <div>
                           <button>
                               Настройки пользователя
                           </button>
                           <button>
                               Чёрный список пользователей
                           </button>
                       </div>
                   </div>
                   <div className="profile-friends">
                       <p>Друзья</p>
                   </div>
               </div>
               <aside className="profile-tests">
                   <p>История тестов</p>
               </aside>
           </div>
        </div>
    );
}