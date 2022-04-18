import React, { useEffect, useState } from 'react';
import { RouteComponentProps, useHistory } from 'react-router';
import {
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonContent,
  IonFab,
  IonFabButton,
  IonIcon,
  IonList,
  IonLoading,
  IonPage,
  IonSegment,
  IonSegmentButton,
} from '@ionic/react';
import {
  arrowForwardOutline,
  bookOutline,
  listOutline,
} from 'ionicons/icons';

import { Artwork, ItemOrder, Landmark } from '../../api';
import api from "../../components/api";
import { getImageUrl, getTranslate, toJson, isAdmin } from "../../components/utils"
import Header from '../../components/Header/Header';

import './Landmark.css';
import ItemCard from '../../components/ItemCard/ItemCard';

interface LandmarkPageProps
  extends RouteComponentProps<{
    landmark_id: string;
  }> { }

const LandmarkPage: React.FC<LandmarkPageProps> = ({ match }) => {
  const history = useHistory();
  const landmark_id = parseInt(match.params.landmark_id);
  const [showLoading, setShowLoading] = useState(true);
  const [landmark, setLandmark] = useState<Landmark>();
  const [artworks, setArtworks] = useState<Artwork[]>([]);
  const [segmentValue, setSegmentValue] = useState<string>("list");
  useEffect(() => {
    api.landmarks
      .getLandmarksLandmarkIdLandmarksLandmarkIdGet(landmark_id)
      .then((data) => {
        setLandmark(data.data)
        setShowLoading(false);
      });
    api.artworks
      .getArtworksLandmarksLandmarkIdArtworksGet(landmark_id, ItemOrder.Rate, "1", 10)
      .then((data) => {
        setArtworks(data.data.contents);
      })
  }, [landmark_id]);

  return (
    <IonPage>
      <Header name="Landmark" back></Header>
      <IonContent fullscreen>
        <IonCard>
          <img alt="artwork" className="artwork-image" src={getImageUrl(landmark?.cover_image)}></img>
          <IonCardHeader>
            <IonCardSubtitle className="artwork-content">{toJson(landmark?.extra)["lead_text"]}</IonCardSubtitle>
            <IonCardTitle className="artwork-content">{getTranslate(landmark?.landmark_name)}</IonCardTitle>
          </IonCardHeader>
          <IonSegment
            onIonChange={e => {
              if (e.detail.value)
                setSegmentValue(e.detail.value)
            }}
            value={segmentValue}
          >
            <IonSegmentButton value="description">
              <IonIcon icon={bookOutline} />
            </IonSegmentButton>
            <IonSegmentButton value="list">
              <IonIcon icon={listOutline} />
            </IonSegmentButton>
          </IonSegment>
          {segmentValue === "description" &&
            <IonCardContent className="artwork-content">
              <div dangerouslySetInnerHTML={{ __html: getTranslate(landmark?.description) }} ></div>
            </IonCardContent>
          }
          {segmentValue === "list" &&
            <IonList>
              {artworks.map((artwork) => {
                return <ItemCard
                  key={artwork.artwork_id}
                  title={getTranslate(artwork.artwork_name)}
                  coverImage={getImageUrl(artwork.cover_image)}
                  href={artwork.self_link}>
                </ItemCard>
              })}
            </IonList>
          }
        </IonCard>
        <IonFab vertical="bottom" horizontal="end" slot="fixed">
          <IonFabButton
            onClick={() => history.push(landmark?.artworks || "")}
            color="light">
            <IonIcon icon={arrowForwardOutline} />
          </IonFabButton>
        </IonFab>
      </IonContent>
      <IonLoading
        isOpen={showLoading}
        onDidDismiss={() => setShowLoading(false)}
        message={"Loading Landmark.. "}
      />
    </IonPage>
  );
};

export default LandmarkPage;
