import React, { useEffect, useState } from 'react';
import { LayerGroup, MapContainer, TileLayer, useMap } from 'react-leaflet'
import { useHistory } from 'react-router';
import {
  IonCard,
  IonCol,
  IonContent,
  IonIcon,
  IonLoading,
  IonPage,
  IonRange,
  IonRow,
} from '@ionic/react';
import { Geolocation } from '@capacitor/geolocation';

import MapMarker from "../../components/Map/MapMarker/MapMarker";

import './Map.css';
import 'leaflet/dist/leaflet.css'
import { Activity, GeometryItem } from '../../api';
import api from '../../components/api';
import { getTranslate } from '../../components/utils';
import { accessibilityOutline, leafOutline, manOutline, storefrontOutline, waterOutline, wifiOutline } from 'ionicons/icons';

const MapComponent: React.FC = () => {
  const map = useMap();
  setTimeout(() => {
    map.invalidateSize();
  }, 10);
  return null
};

const MapPage: React.FC = () => {
  const history = useHistory();
  const [showLoading, setShowLoading] = useState(false);
  const [currentLocation, setCurrentLocation] = useState<any>([48.8566, 2.3522]);
  const [range, setRange] = useState<number>(15);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [geoItems, setGeoItems] = useState<GeometryItem[]>([]);
  const [geoType, setGeoType] = useState<string | undefined>(undefined);
  useEffect(() => {
    console.log(range);
    if (!geoType || geoType === "activity")
      api.activities.searchActivitiesSearchActivitiesGet(
        undefined,
        undefined,
        undefined,
        currentLocation[0],
        currentLocation[1],
        range * 100
      ).then((data) => {
        setActivities(data.data.contents);
      });
    else
      setActivities([]);
    if (!geoType || geoType !== "activity")
      api.geometries.getGeometriesGeometriesGet(
        currentLocation[0],
        currentLocation[1],
        range * 100,
        geoType
      ).then((data) => {
        setGeoItems(data.data.contents);
      });
    else
      setGeoItems([]);
    printCurrentPosition();
  }, [currentLocation, range, geoType]);

  const printCurrentPosition = async () => {
    const coordinates = await Geolocation.getCurrentPosition();
    setCurrentLocation([coordinates.coords.latitude, coordinates.coords.longitude]);
    console.log('Current position:', coordinates);
    setShowLoading(false);
    // mapRef.flyTo()
  };

  const geoTypeFilter = (gt: string) => {
    if (geoType !== gt)
      setGeoType(gt);
    else
      setGeoType(undefined);
  }

  return (
    <IonPage className="scan-container">
      <IonContent fullscreen>
        <MapContainer
          className="map"
          center={currentLocation}
          zoom={12}
        >
          <MapComponent></MapComponent>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <LayerGroup>
            {activities.map((activity) => {
              return <MapMarker
                key={activity?.activity_id}
                popup={true}
                type="activity"
                geometry={activity?.geometry}
                name={getTranslate(activity?.activity_name)}
                cover_image={activity?.cover_image}
                href={activity?.self_link}
              >
              </MapMarker>
            })}
            {geoItems.map((geoItem) => {
              return <MapMarker
                key={geoItem.geometry_id}
                popup={true}
                type={geoItem.geometry_type}
                geometry={geoItem.geometry}
                extra={geoItem.extra}
              ></MapMarker>
            })}
          </LayerGroup>
          <MapMarker
            popup={false}
            type="me"
            geometry={currentLocation}>
          </MapMarker>
        </MapContainer>
        <IonCard className='map-tool-box'>
          <IonRow>
            <IonCol><IonIcon color={geoType === 'activity' ? "primary" : ""} src={accessibilityOutline} onClick={() => geoTypeFilter("activity")} /></IonCol>
            <IonCol><IonIcon color={geoType === 'cool_green' ? "primary" : ""} src={leafOutline} onClick={() => geoTypeFilter("cool_green")} /></IonCol>
            <IonCol><IonIcon color={geoType === 'drinking_water' ? "primary" : ""} src={waterOutline} onClick={() => geoTypeFilter("drinking_water")} /></IonCol>
            <IonCol><IonIcon color={geoType === 'wifi' ? "primary" : ""} src={wifiOutline} onClick={() => geoTypeFilter("wifi")} /></IonCol>
            <IonCol><IonIcon color={geoType === 'toilet' ? "primary" : ""} src={manOutline} onClick={() => geoTypeFilter("toilet")} /></IonCol>
            <IonCol><IonIcon color={geoType === 'market' ? "primary" : ""} src={storefrontOutline} onClick={() => geoTypeFilter("market")} /></IonCol>
          </IonRow>
          <IonRange min={10} max={40} value={range} onIonKnobMoveEnd={({ detail }) => setRange(detail.value as number)}></IonRange>
        </IonCard>
        <IonLoading
          isOpen={showLoading}
          onDidDismiss={() => setShowLoading(false)}
          message="Loading Map.."
        />
      </IonContent>
    </IonPage>
  );
};

export default MapPage;
