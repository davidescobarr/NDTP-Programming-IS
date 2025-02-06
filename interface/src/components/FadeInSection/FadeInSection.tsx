import React, { useEffect, useRef, useState } from "react";

type FadeInSectionProps = {
    children: React.ReactNode; // Контент внутри анимационного блока
    threshold?: number; // Порог видимости элемента (от 0 до 1)
};

const FadeInSection: React.FC<FadeInSectionProps> = ({ children, threshold = 0.1 }) => {
    const [isVisible, setIsVisible] = useState(false); // Состояние видимости элемента
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true); // Показываем элемент
                    observer.disconnect(); // Отключаем наблюдатель для этого элемента
                }
            },
            { threshold }
        );

        if (ref.current) observer.observe(ref.current);

        return () => observer.disconnect();
    }, [threshold]);

    return (
        <div
            ref={ref}
            className={`fade-in-section ${isVisible ? "visible" : ""}`}
        >
            {children}
        </div>
    );
};

export default FadeInSection;