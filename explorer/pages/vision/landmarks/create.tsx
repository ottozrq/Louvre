import { Paper, TextField, Button, Select, MenuItem } from "@material-ui/core";
import { useRouter } from "next/router";
import React, { useState } from "react";

import { LandmarkCreate, Country } from "../../../api";
import api from "../../../components/api";
import Layout from "../../../components/layout";

const baseStyle = { padding: "10px", margin: "10px", maxWidth: "300px" };
const fullStyle = { padding: "10px", margin: "10px", width: "100%" };

export default function LandmarkCreatePage() {
  const router = useRouter();
  const [landmark, setLandmark] = useState<LandmarkCreateInterface>({
    extra: "{}",
    geometry: "{}",
  });
  return <Layout title="Create Landmark">
    <h1>Create Landmark</h1>
    <Paper style={{ padding: "10px", margin: "10px", maxWidth: "1000px" }}>
      <TextField
        style={baseStyle}
        onChange={({ target: { value } }) =>
          setLandmark({ ...landmark, landmark_name: { ...landmark.landmark_name, en: value } })
        }
        label="Landmark Name EN"
      /><br />
      <TextField
        style={baseStyle}
        onChange={({ target: { value } }) =>
          setLandmark({ ...landmark, landmark_name: { ...landmark.landmark_name, cn: value } })
        }
        label="Landmark Name CN"
      /><br />
      <Select
        style={{ margin: "10px", padding: "12px", width: "200px" }}
        id="standard-basic"
        onChange={({ target: { value } }) => {
          setLandmark({ ...landmark, country: Country[value as string] })
        }}
      >
        {Object.values(Country).map(
          (country, index) => {
            return (
              <MenuItem
                key={index}
                style={baseStyle}
                value={country as string}
              >
                {country}
              </MenuItem>
            );
          }
        )}
      </Select>
      <TextField
        style={baseStyle}
        onChange={({ target: { value } }) =>
          setLandmark({ ...landmark, city: value })
        }
        label="City"
      /><br />
      <Button
        style={baseStyle}
        variant="contained"
        component="label"
      >
        Upload Cover Image
        <input
          type="file"
          hidden
          onChange={(e) => {
            api.images.postImageImagesDirPost("landmark", e.target.files[0]).then(data => {
              setLandmark({ ...landmark, cover_image: data.data.file_path })
            });
          }}
        />
      </Button><br />
      {typeof window !== "undefined" ?
        <img style={baseStyle} src={window.localStorage.getItem("base_path") + "/images/" + landmark.cover_image} /> : <div />
      }<br />
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setLandmark({ ...landmark, description: { ...landmark.description, en: value } })
        }
        multiline
        rows={6}
        label="Description EN"
      /><br />
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setLandmark({ ...landmark, description: { ...landmark.description, cn: value } })
        }
        multiline
        rows={6}
        label="Description CN"
      /><br />
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setLandmark({ ...landmark, extra: value })
        }
        multiline
        rows={6}
        label="Extra"
      /><br />
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setLandmark({ ...landmark, geometry: value })
        }
        multiline
        rows={6}
        label="Geometry"
      /><br />
      <Button
        style={baseStyle}
        variant="contained"
        onClick={async () => {
          const landmarkCreate: LandmarkCreate = {
            landmark_name: landmark.landmark_name,
            country: landmark.country,
            city: landmark.city,
            cover_image: landmark.cover_image,
            description: landmark.description,
            extra: JSON.parse(landmark.extra),
            geometry: JSON.parse(landmark.geometry),
          };
          router.push(
            `/vision${(await api.landmarks.postLandmarksLandmarksPost(landmarkCreate)).data.self_link
            }`
          );
        }}
      >Create</Button>
    </Paper>
  </Layout>;
}

interface LandmarkCreateInterface {
  landmark_name?: Object,
  country?: Country,
  city?: string,
  cover_image?: string,
  description?: Object,
  extra?: string,
  geometry?: string,
}