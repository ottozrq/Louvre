import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import {
  IonItem,
  IonInput,
  IonPage,
  IonContent,
  IonButton,
} from '@ionic/react';

import {config} from '../../components/api';
import Header from '../../components/Header/Header';

import './User.css';

const UserPage: React.FC = () => {
  const history = useHistory();

  useEffect(() => {
    if (! config.accessToken) history.push("/login");
  });

  return (
    <IonPage>
      <Header name="Louvre"></Header>
      <IonContent>
        login successfully!
      </IonContent>
    </IonPage>
  );
};

export default UserPage;
