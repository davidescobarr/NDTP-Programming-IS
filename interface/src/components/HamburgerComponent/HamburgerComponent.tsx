import React, {ReactNode} from "react";
import Hamburger from 'hamburger-react';
import './HamburgerComponent.css';

type HamburgerComponentProps = {
    children?: ReactNode;
};

const CROSS = require('@assets/icon/cross.png');

export const HamburgerComponent: React.FC<HamburgerComponentProps> = ({ children }) => {
    const [open, setOpen] = React.useState(false);
    return (
        <div className="hamburger">
            <Hamburger
                size={18}
                toggled={open}
                toggle={setOpen}/>
            {open && <div className="hamburger-content">
                <button onClick={() => setOpen(false)} className="hamburger-close">
                    <img src={CROSS} alt="cross"/>
                </button>
                <div className="content">
                    {children}
                </div>
            </div>}
        </div>
    );
}