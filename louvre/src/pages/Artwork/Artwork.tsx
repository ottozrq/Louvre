import React, { useEffect, useState } from 'react';
import { RouteComponentProps } from 'react-router';
import {
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonContent,
  IonLoading,
  IonPage,
  IonSearchbar,
  IonToolbar,
} from '@ionic/react';

import { Artwork } from '../../api';
import api from "../../components/api";
import { getImageUrl, getTranslate } from "../../components/utils"
import Header from '../../components/Header/Header';

import './Artwork.css';

interface ArtworkPageProps
  extends RouteComponentProps<{
    artwork_id: string;
  }> { }

const ArtworkPage: React.FC<ArtworkPageProps> = ({ match }) => {
  const artwork_id = match.params.artwork_id;
  const [showLoading, setShowLoading] = useState(true);
  const [searchText, setSearchText] = useState('');
  const [artwork, setArtwork] = useState<Artwork>();
  useEffect(() => {
    api.artworks
      .getArtworksArtworkIdArtworksArtworkIdGet(parseInt(artwork_id))
      .then((data) => {
        setArtwork(data.data)
        setShowLoading(false);
      });
  }, [artwork_id]);

  return (
    <IonPage>
      <Header name="Louvre" back></Header>
      <IonToolbar>
        <IonSearchbar value={searchText} onIonChange={e => setSearchText(e.detail.value!)}></IonSearchbar>
      </IonToolbar>
      <IonContent fullscreen>
        <IonCard>
          <img alt="artwork" src={getImageUrl(artwork?.cover_image)}></img>
          <IonCardHeader>
            <IonCardSubtitle>Louvre</IonCardSubtitle>
            <IonCardTitle>{getTranslate(artwork?.artwork_name)}</IonCardTitle>
          </IonCardHeader>
          <IonCardContent className="artwork-content">
            {getTranslate(artwork?.description)}
          </IonCardContent>
        </IonCard>
        <IonLoading
          isOpen={showLoading}
          onDidDismiss={() => setShowLoading(false)}
          message="Loading Artworks.."
        />
      </IonContent>
    </IonPage>
  );
};

export default ArtworkPage;
