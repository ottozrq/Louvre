import React, { useEffect, useState } from 'react';
import {
  IonContent,
  IonDatetime,
  IonIcon,
  IonInfiniteScroll,
  IonInfiniteScrollContent,
  IonLoading,
  IonPage,
  IonSearchbar,
  IonSelect,
  IonSelectOption,
  IonToolbar,
} from '@ionic/react';
import {
  calendarOutline,
} from 'ionicons/icons';

import { Activity } from '../../api';
import api from "../../components/api";
import { getTranslate, toJson} from '../../components/utils';
import Header from '../../components/Header/Header';

import BigItemCard from '../../components/BigItemCard/BigItemCard';
import './Activities.css';

const ActivitiesPage: React.FC = () => {
  const [showLoading, setShowLoading] = useState(true);
  const [searchText, setSearchText] = useState<string>("");
  const [searchDate, setSearchDate] = useState<string>();
  const [searchField, setSearchField] = useState<string>("");
  const [activities, setActivities] = useState<Activity[]>([]);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [pageToken, setPageToken] = useState<string>("1");
  const [isInfiniteDisabled, setInfiniteDisabled] = useState<boolean>(false);
  const [showCalendar, setShowCalendar] = useState<boolean>(false);

  const setActivitiesWithData = (data: any) => {
    setActivities(data ? [...activities, ...data.data.contents] : []);
    setTotalPages(data ? data.data.total_pages : 1);
    setPageToken((parseInt(pageToken) + 1).toString());
    if (parseInt(pageToken) < data.data.total_pages)
      setInfiniteDisabled(false);
    setShowLoading(false);
  }
  const getActivities = () => {
    if (searchText || searchDate || searchField)
      api.activities.searchSearchActivitiesGet(
        searchText ? searchText : undefined,
        searchField ? searchField: undefined,
        searchDate ? searchDate : undefined,
        pageToken,
        30,
      )
        .then((data) => {
          setActivitiesWithData(data);
        });
    else
      api.activities
        .getActivitiesActivitiesGet(pageToken, 30)
        .then((data) => {
          setActivitiesWithData(data);
        });
  }
  useEffect(() => getActivities(), []);
  const showDate = (startDate: string, endDate: string) => {
    return (startDate ? startDate.split("T")[0] : "") + (endDate ? " - " + endDate.split("T")[0] : "")
  }
  return (
    <IonPage>
      <Header name="Louvre"></Header>
      <IonToolbar>
        <IonSelect
          value={searchField}
          slot="secondary"
          onIonChange={(e) => {
            var results = e.detail.value
            setSearchField(results)
          }}
        >
          <IonSelectOption value="">All</IonSelectOption>
          <IonSelectOption value="name.cn,name.en,name.fr">Name</IonSelectOption>
          <IonSelectOption value="keywords">Category</IonSelectOption>
        </IonSelect>
        <IonSearchbar
          onIonChange={e => {
            setSearchText(e.detail.value!)
          }}
          onFocus={() => {
            setActivities([]);
            setPageToken("1");
          }}
          onKeyUp={e => {
            setActivities([]);
            setPageToken("1");
            if (e.key === "Enter") {
              setInfiniteDisabled(true);
              setShowLoading(true);
              getActivities();
            }
          }}
          onIonClear={() => {
            setActivities([]);
            setPageToken("1");
            setSearchText("");
            setSearchField("");
            setSearchDate("");
          }}
        ></IonSearchbar>
        <IonIcon
          className="calendar-icon"
          slot="primary"
          icon={calendarOutline}
          onClick={() => {
            setShowCalendar(!showCalendar);
          }}
        ></IonIcon>
      </IonToolbar>
      <IonContent fullscreen>
        {
          showCalendar &&
          <IonDatetime
            className="calendar"
            presentation="date"
            onIonChange={(e) => {
              setSearchDate(e.detail.value ? e.detail.value.split("T")[0] : "");
              setShowCalendar(false);
              console.log(e.detail.value)
            }}
          ></IonDatetime>
        }
        {
          activities.map((activity) => {
            return <BigItemCard
              key={activity.activity_id}
              title={getTranslate(activity.activity_name)}
              coverImage={activity.cover_image}
              subTitle={showDate(toJson(activity.extra)["date_start"], toJson(activity.extra)["date_end"])}
              subTitle2={toJson(activity.extra)["lead_text"]}
              href={activity.self_link}
            >
            </BigItemCard>
          })
        }
        <IonInfiniteScroll
          onIonInfinite={() => {
            setInfiniteDisabled(true);
            setShowLoading(true);
            getActivities();
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
          message={"Loading Activities.. (" + pageToken + "/" + totalPages + ")"}
        />
      </IonContent>
    </IonPage>
  );
};

export default ActivitiesPage;
