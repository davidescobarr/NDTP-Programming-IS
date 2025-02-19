
import { Layout } from 'antd';
const { Header, Content, Footer } = Layout;

import { HeaderPanel } from "@components/Header";
import { FooterPanel } from "@components/Footer";
import {Modifiers} from "chalk";
import {ModalProvider} from "@model/ModalContext";

export function DefaultLayout ({children}) {
    return (
        <Layout>
            <Header>
                <HeaderPanel/>
            </Header>
            <Content>
                {children}
            </Content>
            <Footer>
                <FooterPanel/>
            </Footer>
        </Layout>
    );
}