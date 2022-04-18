import React, { useEffect, useState } from 'react';
import {
  IonContent,
  IonInfiniteScroll,
  IonInfiniteScrollContent,
  IonLoading,
  IonPage,
} from '@ionic/react';
import {
  calendarOutline,
} from 'ionicons/icons';

import { Landmark } from '../../api';
import api from "../../components/api";
import { getTranslate, getImageUrl, toJson } from '../../components/utils';
import Header from '../../components/Header/Header';

import BigItemCard from '../../components/BigItemCard/BigItemCard';
import './Landmarks.css';

const LandmarksPage: React.FC = () => {
  const [showLoading, setShowLoading] = useState(true);
  const [landmarks, setLandmarks] = useState<Landmark[]>([]);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [pageToken, setPageToken] = useState<string>("1");
  const [isInfiniteDisabled, setInfiniteDisabled] = useState<boolean>(false);

  const setLandmarksWithData = (data: any) => {
    setLandmarks(data ? [...landmarks, ...data.data.contents] : []);
    setTotalPages(data ? data.data.total_pages : 1);
    setPageToken((parseInt(pageToken) + 1).toString());
    if (parseInt(pageToken) < data.data.total_pages)
      setInfiniteDisabled(false);
    setShowLoading(false);
  }
  const getLandmarks = () => {
    setInfiniteDisabled(true);
    api.landmarks
      .getLandmarksLandmarksGet(pageToken, 30)
      .then((data) => {
        setLandmarksWithData(data);
      });
  }
  useEffect(() => {
    getLandmarks();
  }, []);
  return (
    <IonPage>
      <Header name="Landmarks"></Header>
      <IonContent fullscreen>
        {
          landmarks.map((landmark) => {
            return <BigItemCard
              key={landmark.landmark_id}
              title={getTranslate(landmark.landmark_name)}
              coverImage={getImageUrl(landmark.cover_image)}
              href={landmark.self_link}
            >
            </BigItemCard>
          })
        }
        <IonInfiniteScroll
          onIonInfinite={() => {
            setInfiniteDisabled(true);
            setShowLoading(true);
            getLandmarks();
          }}
          threshold="100px"
          disabled={isInfiniteDisabled}
        >
          <IonInfiniteScrollContent
            loadingSpinner="bubbles"
            loadingText="Loading more data..."
          ></IonInfiniteScrollContent>
        </IonInfiniteScroll>
        <IonLoading
          isOpen={showLoading}
          onDidDismiss={() => setShowLoading(false)}
          message={"Loading Landmarks.. (" + pageToken + "/" + totalPages + ")"}
        />
      </IonContent>
    </IonPage>
  );
};

export default LandmarksPage;
