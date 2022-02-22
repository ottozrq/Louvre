import React, { useEffect } from 'react';
import { CameraPreview, CameraPreviewOptions } from '@capacitor-community/camera-preview';
import {
    IonButton,
    IonContent,
    IonIcon,
    IonPage,
} from '@ionic/react';
import { scanOutline } from 'ionicons/icons';

import './Scan.css';
import api from '../../components/api';

const ScanPage: React.FC = () => {

  useEffect(() => {
    const cameraPreviewOptions: CameraPreviewOptions = {
      className: "camera",
      parent: "camera",
      position: "rear",
    };
    CameraPreview.start(cameraPreviewOptions);
  });

  return (
    <IonPage className="scan-container">
      <IonContent id="camera" scrollEvents={false} fullscreen></IonContent>
      <IonIcon className="scan-icon" icon={scanOutline} />
      <IonButton 
        color="light"
        onClick={async () => {
          const result = await CameraPreview.capture({quality: 80});
          console.log(result.value);
          const file = new File([result.value], "detect_file.png",{ type: "image/png" })
          api.images.detectImageDetectPost(file).then((data) => {
            console.log(data);
          });
        }}
      >
          SCAN
      </IonButton>
    </IonPage>
  );
};

export default ScanPage;
