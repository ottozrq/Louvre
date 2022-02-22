import { Paper, TextField, Button, Select, MenuItem } from "@material-ui/core";
import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";

import { ArtworkCreate, Landmark } from "../../../api";
import api from "../../../components/api";
import Layout from "../../../components/layout";

const baseStyle = { padding: "10px", margin: "10px", maxWidth: "300px" };
const fullStyle = { padding: "10px", margin: "10px", width: "100%" };

export default function ArtworkCreatePage() {
  const router = useRouter();
  const [artwork, setArtwork] = useState<ArtworkCreateInterface>({
    extra: "{}",
    geometry: "{}",
  });
  const [landmarks, setLandmarks] = useState<Landmark[]>([]);
  useEffect(() => {
    api.landmarks
      .getLandmarksLandmarksGet("1", 1000)
      .then((data) => (data ? setLandmarks(data.data.contents) : []));
  }, []);
  return <Layout title="Create Artwork">
    <h1>Create Artwork</h1>
    <Paper style={{ padding: "10px", margin: "10px", maxWidth: "1000px" }}>
      <TextField
        style={baseStyle}
        onChange={({ target: { value } }) =>
          setArtwork({ ...artwork, artwork_name: { ...artwork.artwork_name, en: value } })
        }
        label="Artwork Name EN"
      /><br />
      <TextField
        style={baseStyle}
        onChange={({ target: { value } }) =>
          setArtwork({ ...artwork, artwork_name: { ...artwork.artwork_name, cn: value } })
        }
        label="Artwork Name CN"
      /><br />
      <Select
        style={{ margin: "10px", padding: "12px", width: "200px" }}
        id="standard-basic"
        onChange={({ target: { value } }) => {
          setArtwork({ ...artwork, landmark_id: value as number })
        }}
      >
        {landmarks.map(
          (landmark, index) => {
            console.log(landmark.landmark_name["en"])
            return (
              <MenuItem
                key={index}
                style={baseStyle}
                value={landmark.landmark_id}
              >
                {landmark.landmark_name["en"]}
              </MenuItem>
            );
          }
        )}
      </Select><br />
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
            api.images.postImageImagesDirPost("artwork", e.target.files[0]).then(data => {
              setArtwork({ ...artwork, cover_image: data.data.file_path })
            });
          }}
        />
      </Button><br />
      {typeof window !== "undefined" ?
        <img style={baseStyle} src={window.localStorage.getItem("base_path") + "/images/" + artwork.cover_image} /> : <div />
      }<br />
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setArtwork({ ...artwork, description: { ...artwork.description, en: value } })
        }
        multiline
        rows={6}
        label="Description EN"
      /><br />
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setArtwork({ ...artwork, description: { ...artwork.description, cn: value } })
        }
        multiline
        rows={6}
        label="Description CN"
      /><br />
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setArtwork({ ...artwork, extra: value })
        }
        multiline
        rows={6}
        label="Extra"
      /><br />
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setArtwork({ ...artwork, geometry: value })
        }
        multiline
        rows={6}
        label="Geometry"
      /><br />
      <Button
        style={baseStyle}
        variant="contained"
        onClick={async () => {
          const artworkCreate: ArtworkCreate = {
            artwork_name: artwork.artwork_name,
            cover_image: artwork.cover_image,
            description: artwork.description,
            extra: JSON.parse(artwork.extra),
            geometry: JSON.parse(artwork.geometry),
          };
          router.push(
            `/vision${(await api.artworks.postArtworksLandmarksLandmarkIdArtworksPost(artwork.landmark_id, artworkCreate)).data.self_link
            }`
          );
        }}
      >Create</Button>
    </Paper>
  </Layout>;
}

interface ArtworkCreateInterface {
  artwork_name?: object,
  landmark_id?: number,
  cover_image?: string,
  description?: object,
  extra?: string,
  geometry?: string,
}