import React, { useEffect, useState } from 'react';
import {
  IonCol,
  IonContent,
  IonGrid,
  IonInfiniteScroll,
  IonInfiniteScrollContent,
  IonLoading,
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
  const [showLoading, setShowLoading] = useState(true);
  const [searchText, setSearchText] = useState<string>('');
  const [artworks, setArtworks] = useState<Artwork[]>([]);
  const [pageToken, setPageToken] = useState<string>('1');
  const [isInfiniteDisabled, setInfiniteDisabled] = useState(false);

  const get_artworks = () => {
    api.artworks
      .getArtworksLandmarksLandmarkIdArtworksGet(1, pageToken, 42)
      .then((data) => {
        setArtworks(data ? [...artworks, ...data.data.contents] : []);
        setPageToken((parseInt(pageToken) + 1).toString());
        setInfiniteDisabled(false);
        setShowLoading(false);
      });

  }
  useEffect(() => {
    get_artworks();
  }, []);

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
                return <IonCol key={artwork.artwork_id} sizeMd="12" sizeLg="6" sizeXl="4">
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
            <IonInfiniteScroll
              onIonInfinite={() => {
                setInfiniteDisabled(true);
                setShowLoading(true);
                get_artworks();
              }}
              threshold="100px"
              disabled={isInfiniteDisabled}
            >
              <IonInfiniteScrollContent
                loadingSpinner="bubbles"
                loadingText="Loading more data..."
              ></IonInfiniteScrollContent>
            </IonInfiniteScroll>
          </IonRow>
        </IonGrid>
        <IonLoading
          isOpen={showLoading}
          onDidDismiss={() => setShowLoading(false)}
          message="Loading Artworks.."
        />
      </IonContent>
    </IonPage>
  );
};

export default ArtworksPage;
