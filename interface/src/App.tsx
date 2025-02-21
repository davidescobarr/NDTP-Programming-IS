import React, { lazy, useEffect, useState } from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import { loadingComponent } from '@components/LoadingComponent';
import { routes } from '@constants';
import { client } from "@api";
import { ScAddr, ScEventParams, ScEventType, ScTemplate, ScType } from "ts-sc-client";

import 'antd/dist/antd.css';
import './assets/main.css';

import { Layout } from 'antd';
const { Header, Content, Footer } = Layout;

import { HeaderPanel } from "@components/Header";
import { FooterPanel } from "@components/Footer";
import {FormPanel} from "@components/Chat/Forms/Form";
import {ModalProvider} from "@model/ModalContext";
import Modal from "@components/Modal/Modal";
import Tests from "@pages/Tests";

const Main = loadingComponent(lazy(() => import('@pages/Main')));
const EstablishmentsLazy = loadingComponent(lazy(() => import('@pages/Establishments')));
const ProfessionsLazy = loadingComponent(lazy(() => import('@pages/Professions')));
const LoginLazy = loadingComponent(lazy(() => import('@pages/Login')));
const RegistrationLazy = loadingComponent(lazy(() => import('@pages/Registration')));
const ProfileLazy = loadingComponent(lazy(() => import('@pages/Profile')));
const TestsLazy = loadingComponent(lazy(() => import('@pages/Tests')));

const MainRoutes = () => (
    <Route path={routes.MAIN} element={<Main/>}/>
);

const EstablishmentsRoutes = () => (
    <Route path={routes.ESTABLISHMENTS} element={<EstablishmentsLazy />} />
);

const ProfessionsRoutes = () => (
    <Route path={routes.PROFESSIONS} element={<ProfessionsLazy/>}/>
);

const LoginRoutes = () => (
    <Route path={routes.LOGIN} element={<LoginLazy/>} />
);

const RegistrationRoutes = () => (
    <Route path={routes.REGISTRATION} element={<RegistrationLazy />} />
);

const ProfileRoutes = () => (
    <Route path={routes.PROFILE} element={<ProfileLazy />} />
);

const TestsRoutes = () => (
    <Route path={routes.TESTS} element={<TestsLazy />} />
);

export const App = () => {
    return (
        <Layout>
            <ModalProvider>
                <Header>
                    <HeaderPanel />
                </Header>
                <Content>
                    <Routes>
                        <Route path={routes.MAIN} element={<Main/>}/>
                        <Route path={routes.ESTABLISHMENTS} element={<EstablishmentsLazy />} />
                        <Route path={routes.PROFESSIONS} element={<ProfessionsLazy/>}/>
                        <Route path={routes.LOGIN} element={<LoginLazy/>} />
                        <Route path={routes.REGISTRATION} element={<RegistrationLazy />} />
                        <Route path={routes.PROFILE} element={<ProfileLazy />} />
                        <Route path={routes.TESTS} element={<TestsLazy />} />
                    </Routes>
                </Content>
                <Footer>
                    <FooterPanel />
                </Footer>
                <Modal />
            </ModalProvider>
        </Layout>
    );
};