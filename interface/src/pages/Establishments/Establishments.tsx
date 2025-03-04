import * as React from 'react';
import {Establishment} from "@components/Establishment";
import {getEstablishmentsWithDescriptionsAgent} from "@agents/getEstablishmentsAndDescriptionsAgent";
import FadeInSection from "@components/FadeInSection/FadeInSection";

const bsuir = require('@assets/img/establishment_bsuir.png')

export const Establishments = () => {
    const [establishments, setEstablishments] = React.useState<Map<string, string>>(new Map());
    React.useEffect(() => {
        (async () => {
            const establishments = await getEstablishmentsWithDescriptionsAgent();
            console.log(establishments);
            setEstablishments(establishments);
        })();
    }, []);


    return (
        <div className="main">
            <section className="establishments">
                <div className="section-content">
                    <FadeInSection>
                        <h1 className="title">Учебные заведения</h1>
                    </FadeInSection>
                    <div className="establishments-list">
                        {
                            establishments !== null && Object.entries(establishments).map(([key, value]) => {
                                return <Establishment idEstablishment={key} name={value.name} description={value.info} photo={require(`@assets/image/${key}/image.png`)}/>
                            })
                        }
                    </div>
                </div>
            </section>
        </div>
    );
}