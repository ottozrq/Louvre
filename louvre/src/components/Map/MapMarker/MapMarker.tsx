import L, { popup } from "leaflet";
import {
  IonBackButton,
  IonButtons,
  IonHeader,
  IonTitle,
  IonToolbar,
} from '@ionic/react';
import { useHistory } from 'react-router';
import { Marker, Popup, Polygon } from 'react-leaflet'
import './MapMarker.css';

interface ContainerProps {
  popup: boolean;
  geometry: any;
  type: string;
  name?: string;
  cover_image?: string;
  href?: string;
  extra?: any;
}

const activityIcon = L.icon({
  iconUrl: "/assets/images/activity.png",
  iconSize: new L.Point(30, 30),
});

const meIcon = L.icon({
  iconUrl: "/assets/images/me.png",
  iconSize: new L.Point(25, 25),
});

const waterIcon = L.icon({
  iconUrl: "/assets/images/water.png",
  iconSize: new L.Point(30, 30),
});

const wifiIcon = L.icon({
  iconUrl: "/assets/images/wifi.png",
  iconSize: new L.Point(30, 30),
});

const toiletIcon = L.icon({
  iconUrl: "/assets/images/toilet.png",
  iconSize: new L.Point(30, 30),
});

const lonLat2LatLon: any = (lonLat: Array<number>) => {
  return [lonLat[1], lonLat[0]];
}

const allLonLat2LatLon: any = (lonLats: Array<Array<number>>) => {
  const result = [];
  for (const lonLat of lonLats)
    result.push(lonLat2LatLon(lonLat));
  return result;
}

const limeOptions = { color: 'lime' };
const purpleOptions = { color: 'purple' }

const MapMarker: React.FC<ContainerProps> = ({ popup, geometry, name, type, cover_image, href, extra }) => {
  const history = useHistory();
  console.log(type);
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
      {type == "cool_green" &&
        <Polygon
          pathOptions={limeOptions}
          positions={allLonLat2LatLon(geometry["coordinates"][0])}>
          {popup &&
            <Popup>
              <h3>{extra["nom"]}</h3>
              <p><b>Address: </b>{extra["adresse"]}</p>
            </Popup>}
        </Polygon>
      }
      {type == "drinking_water" &&
        < Marker position={lonLat2LatLon(geometry["coordinates"])} icon={waterIcon}>
          {popup &&
            <Popup>
              <h3>{extra["voie"]}</h3>
              <p><b>Type: </b>{extra["type_objet"]}</p>
            </Popup>}
        </Marker>
      }
      {type == "market" &&
        <Polygon
          pathOptions={purpleOptions}
          positions={allLonLat2LatLon(geometry["coordinates"][0])}>
          {popup &&
            <Popup>
              <h3>{extra["nom_long"]}</h3>
              <p><b>Address: </b>{extra["localisation"]}</p>
            </Popup>}
        </Polygon>
      }
            {type == "toilet" &&
        < Marker position={lonLat2LatLon(geometry["coordinates"][0])} icon={toiletIcon}>
          {popup &&
            <Popup>
              <h3>{extra["adresse"]}</h3>
              <p><b>type: </b>{extra["type"]}</p>
              <p><b>hour: </b>{extra["horaire"]}</p>
              <p><b>pmr: </b>{extra["acces_pmr"]}</p>
            </Popup>}
        </Marker>
      }
      {type == "wifi" &&
        < Marker position={lonLat2LatLon(geometry["coordinates"])} icon={wifiIcon}>
          {popup &&
            <Popup>
              <p>{extra["nom_site"]}</p>
            </Popup>}
        </Marker>
      }
    </>
  );
};

export default MapMarker;
