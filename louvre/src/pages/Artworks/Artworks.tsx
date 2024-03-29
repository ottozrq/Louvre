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

import { Artwork, ItemOrder } from '../../api';
import api from "../../components/api";
import { getTranslate, getImageUrl, toJson} from '../../components/utils';
import Header from '../../components/Header/Header';

import ItemCard from '../../components/ItemCard/ItemCard';
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
    if (parseInt(pageToken) < data.data.total_pages)
      setInfiniteDisabled(false);
    setShowLoading(false);
  }
  const getArtworks = () => {
    if (searchText)
      api.artworks.searchArtworksSearchArtworksGet(searchText, ItemOrder.Rate, pageToken, 30)
        .then((data) => {
          setArtworksWithData(data);
        });
    else
      api.artworks
        .getArtworksLandmarksLandmarkIdArtworksGet(1, ItemOrder.Rate, pageToken, 30)
        .then((data) => {
          setArtworksWithData(data);
        });
  }
  useEffect(() => getArtworks(), []);

  return (
    <IonPage>
      <Header name="Artworks"></Header>
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
                  <ItemCard
                    key={artwork.artwork_id}
                    title={getTranslate(artwork.artwork_name)}
                    coverImage={getImageUrl(artwork.cover_image)}
                    subTitle={toJson(artwork.extra)["author"] || "Louvre"}
                    href={artwork.self_link}
                  >
                  </ItemCard>
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
          message={"Loading Artworks.. (" + pageToken + "/" + totalPages + ")"}
        />
      </IonContent>
    </IonPage>
  );
};

export default ArtworksPage;
