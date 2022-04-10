import React, { useEffect, useState } from 'react';
import { RouteComponentProps } from 'react-router';
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
} from '@ionic/react';
import {
  bookOutline,
  busOutline,
  calendarOutline,
  callOutline,
  globeOutline,
  gridOutline,
  informationCircleOutline,
  locationOutline,
  logoFacebook,
  logoTwitter,
  ticketOutline,
  walletOutline
} from 'ionicons/icons';

import { Activity, ItemOrder } from '../../api';
import api from "../../components/api";
import { getImageUrl, getTranslate, toJson, isAdmin } from "../../components/utils"
import Header from '../../components/Header/Header';

import './Activity.css';

interface ActivityPageProps
  extends RouteComponentProps<{
    activity_id: string;
  }> { }

const ActivityPage: React.FC<ActivityPageProps> = ({ match }) => {
  const activity_id = parseInt(match.params.activity_id);
  const [showLoading, setShowLoading] = useState(true);
  const [activity, setActivity] = useState<Activity>();
  const [segmentValue, setSegmentValue] = useState<string>("info");
  useEffect(() => {
    api.activities
      .getActivitiesActivityIdActivitiesActivityIdGet(activity_id)
      .then((data) => {
        setActivity(data.data)
        setShowLoading(false);
      });
  }, [activity_id]);

  return (
    <IonPage>
      <Header name="Louvre" back></Header>
      <IonContent fullscreen>
        <IonCard>
          <img alt="artwork" className="artwork-image" src={activity?.cover_image}></img>
          <IonCardHeader>
            <IonCardSubtitle className="artwork-content">{toJson(activity?.extra)["lead_text"]}</IonCardSubtitle>
            <IonCardTitle className="artwork-content">{getTranslate(activity?.activity_name)}</IonCardTitle>
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
            <IonSegmentButton value="info">
              <IonIcon icon={informationCircleOutline} />
            </IonSegmentButton>
          </IonSegment>
          {segmentValue === "description" &&
            <IonCardContent className="artwork-content">
              <div dangerouslySetInnerHTML={{ __html: getTranslate(activity?.description) }} ></div>
            </IonCardContent>
          }
          {segmentValue === "info" &&
            <>
              <IonRow className="info-row">
                {toJson(activity?.extra)["contact_url"] &&
                  <IonCol>
                    <a target="_blank" href={toJson(activity?.extra)["contact_url"]}>
                      <IonIcon icon={globeOutline} />
                    </a>
                  </IonCol>
                }
                {toJson(activity?.extra)["access_link"] &&
                  <IonCol>
                    <a target="_blank" href={toJson(activity?.extra)["access_link"]}>
                      <IonIcon icon={ticketOutline} />
                    </a>
                  </IonCol>
                }
                {toJson(activity?.extra)["contact_twitter"] &&
                  <IonCol>
                    <a target="_blank" href={toJson(activity?.extra)["contact_twitter"]}>
                      <IonIcon icon={logoTwitter} />
                    </a>
                  </IonCol>
                }
                {toJson(activity?.extra)["contact_facebook"] &&
                  <IonCol>
                    <a target="_blank" href={toJson(activity?.extra)["contact_facebook"]}>
                      <IonIcon icon={logoFacebook} />
                    </a>
                  </IonCol>
                }
              </IonRow>
              {toJson(activity?.extra)["tags"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={gridOutline} /></IonCol>
                  <IonCol size="10">{toJson(activity?.extra)["tags"]}</IonCol>
                </IonRow>}
              {toJson(activity?.extra)["contact_phone"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={callOutline} /></IonCol>
                  <IonCol size="10">{toJson(activity?.extra)["contact_phone"]}</IonCol>
                </IonRow>}
              {toJson(activity?.extra)["date_start"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={calendarOutline} /></IonCol>
                  <IonCol size="10">{toJson(activity?.extra)["date_start"]}</IonCol>
                  <IonCol size="2"></IonCol>
                  <IonCol size="10">{toJson(activity?.extra)["date_end"]}</IonCol>
                </IonRow>}
              {toJson(activity?.extra)["price_detail"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={walletOutline} /></IonCol>
                  <IonCol size="10">{toJson(activity?.extra)["price_detail"]}</IonCol>
                </IonRow>}
              {toJson(activity?.extra)["address_street"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={locationOutline} /></IonCol>
                  <IonCol size="10">{toJson(activity?.extra)["address_street"] + ", " + toJson(activity?.extra)["address_zipcode"] + ", " + toJson(activity?.extra)["address_city"]}</IonCol>
                </IonRow>}
              {toJson(activity?.extra)["transport"] &&
                <IonRow className="info-row">
                  <IonCol size="2"><IonIcon icon={busOutline} /></IonCol>
                  <IonCol size="10">{toJson(activity?.extra)["transport"]}</IonCol>
                </IonRow>}
            </>
          }
          <IonLoading
            isOpen={showLoading}
            onDidDismiss={() => setShowLoading(false)}
            message="Loading Artworks.."
          />
        </IonCard>
      </IonContent>
    </IonPage>
  );
};

export default ActivityPage;
