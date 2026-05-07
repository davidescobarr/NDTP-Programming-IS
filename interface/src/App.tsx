import React, { lazy } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { loadingComponent } from '@components/LoadingComponent';
import { routes } from '@constants';

import 'antd/dist/antd.css';
import './assets/main.css';

import { Layout } from 'antd';
const { Header, Content, Footer } = Layout;

import { HeaderPanel } from "@components/Header";
import { FooterPanel } from "@components/Footer";
import { ModalProvider } from "@model/ModalContext";
import Modal from "@components/Modal/Modal";

const Main = loadingComponent(lazy(() => import('@pages/Main')));
const EstablishmentsLazy = loadingComponent(lazy(() => import('@pages/Establishments')));
const ProfessionsLazy = loadingComponent(lazy(() => import('@pages/Professions')));
const LoginLazy = loadingComponent(lazy(() => import('@pages/Login')));
const RegistrationLazy = loadingComponent(lazy(() => import('@pages/Registration')));
const TestsLazy = loadingComponent(lazy(() => import('@pages/Tests')));
const CareerTestLazy = loadingComponent(lazy(() => import('@pages/CareerTest')));

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
                        <Route path={routes.PROFILE} element={<Navigate to={routes.MAIN} replace />} />
                        <Route path={routes.TESTS} element={<TestsLazy />} />
                        <Route path={routes.CAREER_TEST} element={<CareerTestLazy />} />
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
