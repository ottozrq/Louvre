import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import {
  IonButton,
  IonContent,
  IonItem,
  IonInput,
  IonLoading,
  IonPage,
} from '@ionic/react';

import api from '../../components/api';
import { login } from '../../components/utils';
import Header from '../../components/Header/Header';

import './Login.css';

const LoginPage: React.FC = () => {
  const history = useHistory();
  const [showLoading, setShowLoading] = useState(false);
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  useEffect(() => {
  });

  return (
    <IonPage>
      <Header name="Login"></Header>
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
          setShowLoading(true);
          api.root.tokenTokenPost(username, password).then((data) => {
            login(data.data.access_token);
            history.push('/user');
            setShowLoading(false);
          }).catch(() => {
            setShowLoading(false);
          });
        }}
      >
        Sign in
      </IonButton>
      <IonLoading
        isOpen={showLoading}
        onDidDismiss={() => setShowLoading(false)}
        message="Loading Artworks.."
      />
    </IonPage>
  );
};

export default LoginPage;
