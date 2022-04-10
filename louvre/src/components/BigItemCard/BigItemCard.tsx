import {
  IonCard,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonLabel,
} from '@ionic/react';
import { useHistory } from 'react-router';
import { getImageUrl } from '../utils';
import './BigItemCard.css';

interface ContainerProps {
  title: string;
  subTitle?: string;
  subTitle2?: string;
  coverImage?: string;
  description?: string;
  href?: string;
}

const BigItemCard: React.FC<ContainerProps> = ({ title, subTitle, subTitle2, coverImage, href }) => {
  const history = useHistory()
  return (
    <IonCard
      className="card-container"
      onClick={() => { if (href) history.push(href) }}
    >
      <img alt="artwork" className="artwork-image" src={coverImage}></img>
      <IonCardHeader>
        <IonCardTitle className="artwork-content">{title}</IonCardTitle>
        <IonCardSubtitle className="artwork-content">{subTitle}</IonCardSubtitle>
        <IonCardSubtitle className="artwork-content">{subTitle2}</IonCardSubtitle>
      </IonCardHeader>
    </IonCard>
  );
};

export default BigItemCard;
