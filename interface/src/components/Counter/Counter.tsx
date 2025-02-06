import React, { useState, useEffect, ReactNode } from "react";

type CounterProps = {
    targetNumber: number; // Число, до которого нужно считать
    duration?: number;    // Продолжительность эффекта (в миллисекундах)
    children?: ReactNode; // Контент внутри компонента
};

const Counter: React.FC<CounterProps> = ({ targetNumber, duration = 2000, children }) => {
    const [currentNumber, setCurrentNumber] = useState(0);

    useEffect(() => {
        const stepTime = duration / targetNumber; // Время на один шаг
        let current = 0;

        const interval = setInterval(() => {
            current += 1;
            setCurrentNumber(current);

            if (current >= targetNumber) {
                clearInterval(interval); // Останавливаем, когда достигли цели
            }
        }, stepTime);

        return () => clearInterval(interval); // Очищаем интервал при размонтировании
    }, [targetNumber, duration]);

    return (
        <p>{currentNumber} {children}</p>
    );
};

export default Counter;
