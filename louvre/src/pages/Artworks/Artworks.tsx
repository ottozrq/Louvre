import React, { useEffect, useState } from 'react';
import {
  IonCol,
  IonContent,
  IonGrid,
  IonPage,
  IonRow,
  IonSearchbar,
  IonToolbar,
} from '@ionic/react';

import { Artwork } from '../../api';
import api from "../../components/api";
import { getTranslate } from "../../components/utils"
import Header from '../../components/Header/Header';

import ArtworkCard from '../../components/ItemCard/ItemCard';
import './Artworks.css';

const ArtworksPage: React.FC = () => {
  const [searchText, setSearchText] = useState('');
  const [artworks, setArtworks] = useState<Artwork[]>([]);
  useEffect(() => {
    api.artworks
      .getArtworksLandmarksLandmarkIdArtworksGet(1)
      .then((data) => (data ? setArtworks(data.data.contents) : []));
  }, []);
  console.log(artworks);

  return (
    <IonPage>
      <Header name="Louvre"></Header>
      <IonToolbar>
        <IonSearchbar value={searchText} onIonChange={e => setSearchText(e.detail.value!)}></IonSearchbar>
      </IonToolbar>
      <IonContent fullscreen>
        <IonGrid>
          <IonRow>
            {
              artworks.map((artwork) => {
                return <IonCol sizeMd="12" sizeLg="6" sizeXl="4">
                  <ArtworkCard
                    key={artwork.artwork_id}
                    title={getTranslate(artwork.artwork_name)}
                    coverImage={artwork.cover_image}
                    subTitle="Louvre"
                    href={artwork.self_link}
                  >
                  </ArtworkCard>
                </IonCol>
              })
            }
          </IonRow>
        </IonGrid>
      </IonContent>
    </IonPage>
  );
};

export default ArtworksPage;
