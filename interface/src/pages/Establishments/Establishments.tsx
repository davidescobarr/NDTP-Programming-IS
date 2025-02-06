import * as React from 'react';
import {Establishment} from "@components/Establishment";
import {getEstablishmentsWithDescriptionsAgent} from "@agents/getEstablishmentsAndDescriptionsAgent";

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
                    <h1 className="title">Учебные заведения</h1>
                    <div className="establishments-list">
                        {
                            Object.entries(establishments).map(([key, value]) => {
                            return <Establishment idEstablishment={key} name={key} description={value} photo={bsuir} />
                        })
                        }
                    </div>
                </div>
            </section>
        </div>
    );
}