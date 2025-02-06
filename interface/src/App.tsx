import React, { lazy, useEffect, useState } from "react";
import { Route, Redirect } from "react-router-dom";
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

const Main = loadingComponent(lazy(() => import('@pages/Main')));
const EstablishmentsLazy = loadingComponent(lazy(() => import('@pages/Establishments')));
const ProfessionsLazy = loadingComponent(lazy(() => import('@pages/Professions')));
const LoginLazy = loadingComponent(lazy(() => import('@pages/Login')));
const RegistrationLazy = loadingComponent(lazy(() => import('@pages/Registration')));
const ProfileLazy = loadingComponent(lazy(() => import('@pages/Profile')));

const MainRoutes = () => (
    <>
        <Route exact path={routes.MAIN} component={Main} />
    </>
);

const EstablishmentsRoutes = () => (
    <>
        <Route path={routes.ESTABLISHMENTS} component={EstablishmentsLazy} />
    </>
);

const ProfessionsRoutes = () => (
    <>
        <Route path={routes.PROFESSIONS} component={ProfessionsLazy} />
    </>
);

const LoginRoutes = () => (
    <>
        <Route path={routes.LOGIN} component={LoginLazy} />
    </>
);

const RegistrationRoutes = () => (
    <>
        <Route path={routes.REGISTRATION} component={RegistrationLazy} />
    </>
);

const ProfileRoutes = () => (
    <>
        <Route path={routes.PROFILE} component={ProfileLazy} />
    </>
);

export const App = () => {
    return (
        <Layout>
            <ModalProvider>
                <Header>
                    <HeaderPanel />
                </Header>
                <Content>
                    <MainRoutes />
                    <EstablishmentsRoutes />
                    <ProfessionsRoutes />
                    <LoginRoutes />
                    <RegistrationRoutes />
                    <ProfileRoutes />
                </Content>
                <Footer>
                    <FooterPanel />
                </Footer>
                <Modal />
            </ModalProvider>
        </Layout>
    );
};
