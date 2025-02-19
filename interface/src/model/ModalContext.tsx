import React, { createContext, useContext, useState, ReactNode } from "react";

interface ModalContextType {
    isOpen: boolean;
    content: ReactNode | null;
    openModal: <T>(Component: React.FC<T>, props: T) => void;
    closeModal: () => void;
}

const ModalContext = createContext<ModalContextType | undefined>(undefined);

export const ModalProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [content, setContent] = useState<ReactNode | null>(null);

    const openModal = <T,>(Component: React.FC<T>, props: T) => {
        setContent(<Component {...props} />);
        setIsOpen(true);
    };

    const closeModal = () => {
        setIsOpen(false);
        setContent(null);
    };

    return (
        <ModalContext.Provider value={{ isOpen, content, openModal, closeModal }}>
            {children}
        </ModalContext.Provider>
    );
};

export const useModal = (): ModalContextType => {
    const context = useContext(ModalContext);
    if (!context) {
        throw new Error("useModal must be used within a ModalProvider");
    }
    return context;
};
