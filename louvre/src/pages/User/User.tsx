import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import {
  IonItem,
  IonLabel,
  IonPage,
  IonContent,
  IonIcon,
} from '@ionic/react';

import { User, UserRole } from '../../api';
import api from '../../components/api';
import { validateUserToken, logout } from '../../components/utils';
import Header from '../../components/Header/Header';

import { chevronForwardOutline } from 'ionicons/icons';
import './User.css';

const UserPage: React.FC = () => {
  const history = useHistory();
  const [user, setUser] = useState<User>();

  useEffect(() => {
    if (!validateUserToken()) {
      history.replace("/login");
    }
    api.users.userUserGet().then((data) => {
      setUser(data.data);
    });
  }, [history]);

  return (
    <IonPage>
      <Header name="Louvre"></Header>
      <IonContent>
        <IonItem>
          <h1>Hi {user?.first_name}!</h1>
        </IonItem>
        <IonItem>
          <IonLabel>You are</IonLabel>
          <IonLabel slot='end'>{user?.role}</IonLabel>
        </IonItem>
        {user?.role === UserRole.Admin &&
          <IonItem onClick={() => history.push('/artwork_rate')}>
            <IonLabel>Rate Artworks</IonLabel>
            <IonIcon icon={chevronForwardOutline}></IonIcon>
          </IonItem>
        }
        <IonItem onClick={() => {
          logout();
          setUser(undefined);
          history.replace("/login");
        }}>
          <IonLabel>Logout</IonLabel>
        </IonItem>
      </IonContent>
    </IonPage>
  );
};

export default UserPage;
