import React, { useEffect, useState } from 'react';
import {
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonCol,
  IonContent,
  IonIcon,
  IonLoading,
  IonPage,
  IonRow,
  IonSegment,
  IonSegmentButton,
  IonToolbar,
} from '@ionic/react';
import {
  bookmarksOutline,
  bookOutline,
  calendarOutline,
  cropOutline,
  earthOutline,
  gridOutline,
  informationCircleOutline,
  list,
  locationOutline,
  personOutline,
  schoolOutline,
  starOutline,
} from 'ionicons/icons';

import { Artwork, ItemOrder } from '../../api';
import api from "../../components/api";
import { getImageUrl, getTranslate, toJson } from "../../components/utils"
import Header from '../../components/Header/Header';

import './ArtworkRate.css';

const ArtworkRatePage: React.FC = ({ }) => {
  const [showLoading, setShowLoading] = useState(true);
  const [artwork, setArtwork] = useState<Artwork>();
  const [segmentValue, setSegmentValue] = useState<string>("rate");
  const [artworkRate, setArtworkRate] = useState<string>();
  const getArtwork = () => {
    setShowLoading(true);
    api.artworks.getArtworksLandmarksLandmarkIdArtworksGet(1, ItemOrder.RateBackwards, "1", 1)
      .then((data) => {
        setArtwork(data.data.contents[0]);
        setShowLoading(false);
        setArtworkRate(data.data.contents[0].artwork_rate?.toString());
      });
  }
  useEffect(() => {
    getArtwork();
  }, []);

  return (
    <IonPage>
      <Header name="Louvre" back></Header>
      <IonContent fullscreen>
        <IonCard>
          <img alt="artwork" className="artwork-image" src={getImageUrl(artwork?.cover_image)}></img>
          <IonCardHeader>
            <IonCardSubtitle>{toJson(artwork?.extra)["author"] || "Louvre"}</IonCardSubtitle>
            <IonCardTitle>{getTranslate(artwork?.artwork_name)}</IonCardTitle>
          </IonCardHeader>
          <IonSegment
            onIonChange={e => {
              if (e.detail.value)
                setSegmentValue(e.detail.value)
            }}
            value={segmentValue}
          >
            <IonSegmentButton value="rate">
              <IonIcon icon={starOutline} />
            </IonSegmentButton>
            <IonSegmentButton value="description">
              <IonIcon icon={bookOutline} />
            </IonSegmentButton>
            <IonSegmentButton value="info">
              <IonIcon icon={informationCircleOutline} />
            </IonSegmentButton>
          </IonSegment>
          {
            segmentValue === "rate" &&
            <IonToolbar>
              <IonSegment
                onIonChange={e => {
                  if (e.detail.value)
                    setArtworkRate(e.detail.value)
                  if (artwork) {
                    api.artworks.patchArtworksArtworkIdArtworksArtworkIdPatch(
                      artwork?.artwork_id,
                      { artwork_rate: e.detail.value ? parseInt(e.detail.value) : 0 }
                    );
                    getArtwork();
                  }
                }}
                value={artworkRate}
              >
                {
                  Array.from(Array(5).keys()).map((index) => {
                    return <IonSegmentButton key={index} value={index.toString()} color="light">
                      {index}
                    </IonSegmentButton>
                  })
                }
              </IonSegment>
            </IonToolbar>
          }
          {segmentValue === "description" &&
            <IonCardContent className="artwork-content">
              {getTranslate(artwork?.description)}
              {toJson(artwork?.extra)["Description/Features"] &&
                <>
                  <br /> <br />
                  {toJson(artwork?.extra)["Description/Features"]}
                </>
              }
              {toJson(artwork?.extra)["Object history"] &&
                <>
                  <br /> <br />
                  {toJson(artwork?.extra)["Object history"]}
                </>
              }
            </IonCardContent>
          }
          {segmentValue === "info" &&
            <>
              {toJson(artwork?.extra)["Category"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={gridOutline} /></IonCol>
                  <IonCol size="10">{toJson(artwork?.extra)["Category"]}</IonCol>
                </IonRow>}
              {toJson(artwork?.extra)["author"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={personOutline} /></IonCol>
                  <IonCol size="10">{toJson(artwork?.extra)["author"]}</IonCol>
                </IonRow>}
              {toJson(artwork?.extra)["Artist/maker / School / Artistic centre"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={schoolOutline} /></IonCol>
                  <IonCol size="10">{toJson(artwork?.extra)["Artist/maker / School / Artistic centre"]}</IonCol>
                </IonRow>}
              {toJson(artwork?.extra)["Date"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={calendarOutline} /></IonCol>
                  <IonCol size="10">{toJson(artwork?.extra)["Date"]}</IonCol>
                </IonRow>}
              {toJson(artwork?.extra)["Place of origin"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={earthOutline} /></IonCol>
                  <IonCol size="10">{toJson(artwork?.extra)["Place of origin"]}</IonCol>
                </IonRow>}
              {toJson(artwork?.extra)["Dimensions"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={cropOutline} /></IonCol>
                  <IonCol size="10">{toJson(artwork?.extra)["Dimensions"]}</IonCol>
                </IonRow>}
              {toJson(artwork?.extra)["Inventory number"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={bookmarksOutline} /></IonCol>
                  <IonCol size="10">{toJson(artwork?.extra)["Inventory number"]}</IonCol>
                </IonRow>}
              {toJson(artwork?.extra)["Current location"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={locationOutline} /></IonCol>
                  <IonCol size="10">{toJson(artwork?.extra)["Current location"]}</IonCol>
                </IonRow>}
            </>
          }
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

export default ArtworkRatePage;
