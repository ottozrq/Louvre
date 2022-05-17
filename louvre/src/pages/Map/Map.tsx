import React, { useEffect, useState } from 'react';
import { LayerGroup, MapContainer, Marker, TileLayer, useMap } from 'react-leaflet'
import { useHistory } from 'react-router';
import {
  IonContent,
  IonLoading,
  IonPage,
} from '@ionic/react';
import { Geolocation, Position } from '@capacitor/geolocation';

import MapMarker from "../../components/Map/MapMarker/MapMarker";

import './Map.css';
import 'leaflet/dist/leaflet.css'
import { Activity, GeometryItem } from '../../api';
import api from '../../components/api';
import { getTranslate } from '../../components/utils';

const MapComponent: React.FC = () => {
  const map = useMap();
  setTimeout(() => {
    map.invalidateSize();
  }, 10);
  return null
};

const MapPage: React.FC = () => {
  const history = useHistory();
  const [showLoading, setShowLoading] = useState(true);
  const [currentLocation, setCurrentLocation] = useState<any>([48.8566, 2.3522]);
  const [activities, setActivities] = useState<Activity[]>([]);
  useEffect(() => {
    api.activities.searchActivitiesSearchActivitiesGet(
      undefined,
      undefined,
      undefined,
      currentLocation[0],
      currentLocation[1],
      3000).then((data) => {
        setActivities(data.data.contents);
      });
    printCurrentPosition();
  }, [currentLocation]);

  const printCurrentPosition = async () => {
    const coordinates = await Geolocation.getCurrentPosition();
    setCurrentLocation([coordinates.coords.latitude, coordinates.coords.longitude]);
    console.log('Current position:', coordinates);
    setShowLoading(false);
  };

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
            })
            }
          </LayerGroup>
          <MapMarker
            popup={false}
            type="me"
            geometry={currentLocation}>
          </MapMarker>
        </MapContainer>
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
