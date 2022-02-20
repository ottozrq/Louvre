import {
  IonBackButton,
  IonButtons,
  IonHeader,
  IonTitle,
  IonToolbar,
} from '@ionic/react';
import './Header.css';

interface ContainerProps {
  name: string;
  back?: boolean;
}

const Header: React.FC<ContainerProps> = ({ name, back }) => {
  return (
    <IonHeader>
      <IonToolbar>
        {back?
          <IonButtons slot="start">
            <IonBackButton defaultHref="/" />
          </IonButtons>: <></>
        }
        <IonTitle class="ion-text-center">{name}</IonTitle>
      </IonToolbar>
    </IonHeader>
  );
};

export default Header;
