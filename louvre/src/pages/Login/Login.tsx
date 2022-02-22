import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import {
  IonItem,
  IonInput,
  IonPage,
  IonContent,
  IonButton,
} from '@ionic/react';

import api from '../../components/api';
import Header from '../../components/Header/Header';

import './Login.css';

const LoginPage: React.FC = () => {
  const history = useHistory()
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  useEffect(() => {
  });

  return (
    <IonPage>
      <Header name="Louvre"></Header>
      <IonContent>
        <IonItem>
          <IonInput
            value={username}
            placeholder="Username"
            onIonChange={e => setUsername(e.detail.value!)}
          >
          </IonInput>
        </IonItem>
        <IonItem>
          <IonInput
            value={password}
            type="password"
            placeholder="Password"
            onIonChange={e => setPassword(e.detail.value!)}
          >
          </IonInput>
        </IonItem>
      </IonContent>
      <IonButton
        color="light"
        onClick={() => {
          api.root.tokenTokenPost(username, password).then((data) => {
            window.localStorage.setItem("access_token", data.data.access_token)
            history.push('/user')
          });
        }}
      >
        Login
      </IonButton>

    </IonPage>
  );
};

export default LoginPage;
