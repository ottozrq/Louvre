import {
  IonThumbnail,
  IonCardSubtitle,
  IonCardTitle,
  IonLabel,
  IonItem,
} from '@ionic/react';
import { useHistory } from 'react-router';
import { getImageUrl } from '../utils';
import './ItemCard.css';

interface ContainerProps {
  title: string;
  subTitle?: string;
  coverImage?: string;
  description?: string;
  href?: string;
}

const ItemCard: React.FC<ContainerProps> = ({ title, subTitle, coverImage, href }) => {
  const history = useHistory()
  return (
    <IonItem
      className="card-container"
      onClick={() => { if (href) history.push(href) }}
    >
      <IonThumbnail className="card-image">
        <img src={coverImage} />
      </IonThumbnail>
      <IonLabel>
        <IonCardTitle className="card-title">{title}</IonCardTitle>
        <IonCardSubtitle className="card-subtitle">{subTitle}</IonCardSubtitle>
      </IonLabel>
    </IonItem>
  );
};

export default ItemCard;
