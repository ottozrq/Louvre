import L, { popup } from "leaflet";
import {
  IonBackButton,
  IonButtons,
  IonHeader,
  IonTitle,
  IonToolbar,
} from '@ionic/react';
import { useHistory } from 'react-router';
import { Marker, Popup } from 'react-leaflet'
import './MapMarker.css';

interface ContainerProps {
  popup: boolean;
  geometry: any;
  type: string;
  name?: string;
  cover_image?: string;
  href?: string;
}

const activityIcon = L.icon({
  iconUrl: "/assets/images/activity.png",
  iconSize: new L.Point(30, 30),
});

const meIcon = L.icon({
  iconUrl: "/assets/images/me.png",
  iconSize: new L.Point(25, 25),
});

const lonLat2LatLon: any = (lonLat: Array<number>) => {
  return [lonLat[1], lonLat[0]]
}

const MapMarker: React.FC<ContainerProps> = ({ popup, geometry, name, type, cover_image, href }) => {
  const history = useHistory();

  return (
    <>
      {geometry["type"] === "Point" && type === "activity" &&
        < Marker position={lonLat2LatLon(geometry["coordinates"])} icon={activityIcon}>
          {popup &&
            <Popup>
              <img 
                src={cover_image}
                onClick={() => {
                  if (href)
                    history.push(href);
                }}
                ></img>
              <h3>{name}</h3>
            </Popup>}
        </Marker>
      }
      {type === "me" &&
        < Marker position={geometry} icon={meIcon}>
        </Marker>
      }
    </>
  );
};

export default MapMarker;
