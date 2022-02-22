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
import { IonReactRouter } from '@ionic/react-router';
import { listOutline, personOutline, scanOutline } from 'ionicons/icons';
import Artworks from './pages/Artworks/Artworks';
import ArtworkPage from './pages/Artwork/Artwork';
import LoginPage from './pages/Login/Login';
import UserPage from './pages/User/User';
import ScanPage from './pages/Scan/Scan';


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

setupIonicReact();

const App: React.FC = () => (
  <IonApp>
    <IonReactRouter>
      <IonTabs>
        <IonRouterOutlet>
          <Route exact path="/artworks">
            <Artworks />
          </Route>
          <Route exact
            path="/artworks/:artwork_id"
            component={ArtworkPage}
          >
          </Route>
          <Route path="/login">
            <LoginPage />
          </Route>
          <Route path="/scan">
            <ScanPage />
          </Route>
          <Route path="/user">
            <UserPage />
          </Route>
          <Route exact path="/">
            <Redirect to="/artworks" />
          </Route>
        </IonRouterOutlet>
        <IonTabBar slot="bottom">
          <IonTabButton tab="artworks" href="/artworks">
            <IonIcon icon={listOutline} />
            <IonLabel>Artworks</IonLabel>
          </IonTabButton>
          <IonTabButton tab="scan" href="/scan">
            <IonIcon icon={scanOutline} />
            <IonLabel>Scan</IonLabel>
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
