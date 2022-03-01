import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import { CameraPreview, CameraPreviewOptions } from '@capacitor-community/camera-preview';
import {
  IonButton,
  IonContent,
  IonIcon,
  IonLoading,
  IonPage,
} from '@ionic/react';
import { scanOutline } from 'ionicons/icons';

import './Scan.css';
import api from '../../components/api';

const ScanPage: React.FC = () => {
  const history = useHistory();
  const [showLoading, setShowLoading] = useState(false);

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
          setShowLoading(true);
          const result = await CameraPreview.capture({ quality: 80 });
          const image = "data:text/plain;base64," + result.value;
          var arr = image.split(','),
            bstr = atob(arr[1]),
            n = bstr.length,
            u8arr = new Uint8Array(n);

          while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
          }
          const file = new File([u8arr], "detect_file.png", { type: "image/png" })
          api.images.detectImageDetectPost(file).then((data) => {
            setShowLoading(false);
            history.push(data.data.self_link);
          });
        }}
      >
        SCAN
      </IonButton>
      <IonLoading
        isOpen={showLoading}
        onDidDismiss={() => setShowLoading(false)}
        message="Loading Artworks.."
      />
    </IonPage>
  );
};

export default ScanPage;
