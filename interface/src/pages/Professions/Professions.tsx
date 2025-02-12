import * as React from 'react';
import {Profession} from "@components/Profession";
import {getProfessionsWithDescriptionsAgent} from "@agents/getProfessionsAndDescriptionsAgent";

const bsuir = require('@assets/img/establishment_bsuir.png')

export const Professions = () => {
    const [professions, setProfessions] = React.useState<Map<string, string>>(new Map());
    React.useEffect(() => {
        (async () => {
            const professions = await getProfessionsWithDescriptionsAgent();
            console.log(professions);
            setProfessions(professions);
        })();
    }, []);

    return (
        <div className="main">
            <section className="establishments">
                <div className="section-content">
                    <h1 className="title">Профессии</h1>
                    <div className="professions-list">
                        {
                            professions !== null && Object.entries(professions).map(([key, value]) => {
                                return <Profession idProfession={key} name={value.name} description={value.info} photo={bsuir} />
                            })
                        }
                    </div>
                </div>
            </section>
        </div>
    );
}