import React, { lazy, useEffect, useState } from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import { loadingComponent } from '@components/LoadingComponent';
import { routes } from '@constants';

import 'antd/dist/antd.css';
import './assets/main.css';

import { Layout } from 'antd';
const { Header, Content, Footer } = Layout;

import { HeaderPanel } from "@components/Header";
import { FooterPanel } from "@components/Footer";
import {FormPanel} from "@components/Chat/Forms/Form";
import {ModalProvider} from "@model/ModalContext";
import Modal from "@components/Modal/Modal";
import {DefaultLayout} from "./Layout";

const Main = loadingComponent(lazy(() => import('@pages/Main')));
const EstablishmentsLazy = loadingComponent(lazy(() => import('@pages/Establishments')));
const ProfessionsLazy = loadingComponent(lazy(() => import('@pages/Professions')));
const LoginLazy = loadingComponent(lazy(() => import('@pages/Login')));
const RegistrationLazy = loadingComponent(lazy(() => import('@pages/Registration')));
const ProfileLazy = loadingComponent(lazy(() => import('@pages/Profile')));
const TestsLazy = loadingComponent(lazy(() => import('@pages/Tests')));

export const App = () => {
    return (
        <ModalProvider>
            <BrowserRouter>
                <Routes>
                    <Route path={routes.MAIN} element={<DefaultLayout><Main/></DefaultLayout>} />
                    <Route path={routes.PROFESSIONS} element={<DefaultLayout><ProfessionsLazy/></DefaultLayout>} />
                    <Route path={routes.LOGIN} element={<DefaultLayout><LoginLazy/></DefaultLayout>} />
                    <Route path={routes.ESTABLISHMENTS} element={<DefaultLayout><EstablishmentsLazy/></DefaultLayout>} />
                    <Route path={routes.REGISTRATION} element={<DefaultLayout><RegistrationLazy/></DefaultLayout>} />
                    <Route path={routes.PROFILE} element={<DefaultLayout><ProfileLazy/></DefaultLayout>} />
                    <Route path={routes.TESTS} element={<DefaultLayout><TestsLazy/></DefaultLayout>} />
                </Routes>
            </BrowserRouter>
        </ModalProvider>
    );
};