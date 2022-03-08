import React, { useEffect, useState, useCallback } from 'react';
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
import { getTranslate } from '../../components/utils';
import Header from '../../components/Header/Header';

import ArtworkCard from '../../components/ItemCard/ItemCard';
import './Artworks.css';

const ArtworksPage: React.FC = () => {
  const [showLoading, setShowLoading] = useState(true);
  const [searchText, setSearchText] = useState<string>("");
  const [artworks, setArtworks] = useState<Artwork[]>([]);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [pageToken, setPageToken] = useState<string>("1");
  const [isInfiniteDisabled, setInfiniteDisabled] = useState(false);

  const setArtworksWithData = (data: any) => {
    setArtworks(data ? [...artworks, ...data.data.contents] : []);
    setTotalPages(data ? data.data.total_pages : 1);
    setPageToken((parseInt(pageToken) + 1).toString());
    console.log(parseInt(pageToken), data.data.total_pages, parseInt(pageToken) >= data.data.total_pages)
    if (parseInt(pageToken) < data.data.total_pages)
      setInfiniteDisabled(false);
    setShowLoading(false);
  }
  const getArtworks = () => {
    if (searchText)
      api.artworks.searchSearchArtworksGet(searchText, pageToken, 30)
        .then((data) => {
          setArtworksWithData(data);
        });
    else
      api.artworks
        .getArtworksLandmarksLandmarkIdArtworksGet(1, pageToken, 30)
        .then((data) => {
          setArtworksWithData(data);
        });
  }
  useEffect(() => getArtworks(), []);

  return (
    <IonPage>
      <Header name="Louvre"></Header>
      <IonToolbar>
        <IonSearchbar
          onIonChange={e => {
            setSearchText(e.detail.value!)
          }}
          onKeyUp={e => {
            setArtworks([]);
            setPageToken("1");
            if (e.key === "Enter") {
              setInfiniteDisabled(true);
              setShowLoading(true);
              getArtworks();
            }
          }}
          onIonClear={() => {
            setArtworks([]);
            setPageToken("1");
          }}
        ></IonSearchbar>
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
                getArtworks();
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
