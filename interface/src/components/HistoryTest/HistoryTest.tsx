import {useModal} from "@model/ModalContext";
import './history-test.css';

export const modalHistoryTest = ({ resultTest }) => {
    return (
        <p className="history-test-modal">{resultTest}</p>
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