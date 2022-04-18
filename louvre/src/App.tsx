import { Redirect, Route } from 'react-router-dom';
import {
  IonApp,
  IonIcon,
  IonLabel,
  IonRouterOutlet,
  IonTabBar,
  IonTabButton,
  IonTabs,
  setupIonicReact
} from '@ionic/react';

/* Core CSS required for Ionic components to work properly */
import '@ionic/react/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';

/* Theme variables */
import './theme/variables.css';
import { IonReactRouter } from '@ionic/react-router';
import { listOutline, locationOutline, personOutline, scanOutline } from 'ionicons/icons';
import Activities from './pages/Activities/Activities';
import ActivityPage from './pages/Activity/Activity';
import ArtworksPage from './pages/Artworks/Artworks';
import ArtworkPage from './pages/Artwork/Artwork';
import LandmarkPage from './pages/Landmark/Landmark';
import LandmarksPage from './pages/Landmarks/Landmarks';
import LoginPage from './pages/Login/Login';
import UserPage from './pages/User/User';
import ScanPage from './pages/Scan/Scan';

setupIonicReact();

const App: React.FC = () => (
  <IonApp>
    <IonReactRouter>
      <IonTabs>
        <IonRouterOutlet>
          <Route exact path="/activities">
            <Activities />
          </Route>
          <Route exact
            path="/activities/:activity_id"
            component={ActivityPage}
          ></Route>
          <Route exact
            path="/artworks/:artwork_id"
            component={ArtworkPage}
          >
          </Route>
          <Route exact path="/landmarks">
            <LandmarksPage />
          </Route>
          <Route exact
            path="/landmarks/:landmark_id"
            component={LandmarkPage}
          ></Route>
          <Route exact
            path="/landmarks/:landmark_id/artworks"
            component={ArtworksPage}
          ></Route>
          <Route exact path="/login">
            <LoginPage />
          </Route>
          <Route exact path="/scan">
            <ScanPage />
          </Route>
          <Route exact path="/user">
            <UserPage />
          </Route>
          <Route exact path="/">
            <Redirect to="/activities" />
          </Route>
        </IonRouterOutlet>
        <IonTabBar slot="bottom">
          <IonTabButton tab="landmarks" href="/landmarks">
            <IonIcon icon={locationOutline} />
            <IonLabel>Scan</IonLabel>
          </IonTabButton>
          <IonTabButton tab="activities" href="/activities">
            <IonIcon icon={listOutline} />
            <IonLabel>Activities</IonLabel>
          </IonTabButton>
          <IonTabButton tab="user" href="/user">
            <IonIcon icon={personOutline} />
            <IonLabel>User</IonLabel>
          </IonTabButton>
        </IonTabBar>
      </IonTabs>
    </IonReactRouter>
  </IonApp>
);

export default App;
