import {useModal} from "@model/ModalContext";

export const modalHistoryTest = ({ resultTest }) => {
    return (
        <p>{resultTest}</p>
    );
}

export const HistoryTest = ({nameTest, dateTest, resultTest}) => {
    const { openModal } = useModal();

    return (
      <div onClick={() => {openModal(modalHistoryTest, { resultTest });}}>
          <p>{nameTest}</p>
          <p>{dateTest}</p>
      </div>
    );
}