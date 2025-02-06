import React from "react";
import "./modal.css"
import {useModal} from "@model/ModalContext";

const Modal: React.FC = () => {
    const { isOpen, content, closeModal } = useModal();

    return (
        <div className={isOpen ? "modal active" : "modal"} onClick={() => {closeModal();}}>
            <div className={isOpen ? "modal__content active" : "modal__content"} onClick={e => e.stopPropagation()}>
                {content}
                <button
                    className="absolute top-2 right-2 text-xl"
                    onClick={closeModal}
                >
                    ❌
                </button>
            </div>
        </div>
    );
}

export default Modal;