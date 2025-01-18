import { lazy, useEffect, useState } from "react";
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

const Main = loadingComponent(lazy(() => import('@pages/Main')));
const EstablishmentsLazy = loadingComponent(lazy(() => import('@pages/Establishments')));
const ProfessionsLazy = loadingComponent(lazy(() => import('@pages/Professions')));
const About = loadingComponent(lazy(() => import('@pages/About')));

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


export const App = () => {
    return (
        <Layout>
            <Header>
                <HeaderPanel />
            </Header>
            <Content>
                <MainRoutes />
                <EstablishmentsRoutes />
                <ProfessionsRoutes />
            </Content>
            <Footer>
                <FooterPanel />
            </Footer>
        </Layout>
    );
};
