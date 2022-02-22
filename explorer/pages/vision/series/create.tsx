import { Paper, TextField, Button, Select, MenuItem } from "@material-ui/core";
import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";

import { SeriesCreate, Landmark, Language } from "../../../api";
import api from "../../../components/api";
import Layout from "../../../components/layout";

const baseStyle = { padding: "10px", margin: "10px", maxWidth: "300px" };
const fullStyle = { padding: "10px", margin: "10px", width: "100%" };

export default function SeriesCreatePage() {
  const router = useRouter();
  const [series, setSeries] = useState<SeriesCreateInterface>({});
  const [landmarks, setLandmarks] = useState<Landmark[]>([]);
  useEffect(() => {
    api.landmarks
      .getLandmarksLandmarksGet("1", 1000)
      .then((data) => (data ? setLandmarks(data.data.contents) : []));
  }, []);
  return <Layout title="Create Series">
    <h1>Create Series</h1>
    <Paper style={{ padding: "10px", margin: "10px", maxWidth: "1000px" }}>
      <TextField
        style={baseStyle}
        onChange={({ target: { value } }) =>
          setSeries({ ...series, series_name: value })
        }
        label="Series Name"
      />
      <Select
        style={{ margin: "10px", padding: "12px", width: "200px" }}
        id="standard-basic"
        onChange={({ target: { value } }) => {
          setSeries({ ...series, landmark_id: value as number })
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
      </Select>
      <Select
        style={{ margin: "10px", padding: "12px", width: "200px" }}
        id="standard-basic"
        onChange={({ target: { value } }) => {
          setSeries({ ...series, language: Language[value as string] })
        }}
      >
        <MenuItem
          key="en"
          style={baseStyle}
          value="en"
        >EN</MenuItem>
        <MenuItem
          key="cn"
          style={baseStyle}
          value="cn"
        >CN</MenuItem>
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
            api.images.postImageImagesDirPost("series", e.target.files[0]).then(data => {
              setSeries({ ...series, cover_image: data.data.file_path })
            });
          }}
        />
      </Button><br />
      {typeof window !== "undefined" ?
        <img style={baseStyle} src={window.localStorage.getItem("base_path") + "/images/" + series.cover_image} /> : <div />
      }<br />
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setSeries({ ...series, description: value })
        }
        multiline
        rows={6}
        label="Description"
      /><br />
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setSeries({ ...series, price: +value })
        }
        type="number"
        label="Price"
      /><br />
      <Button
        style={baseStyle}
        variant="contained"
        onClick={async () => {
          const seriesCreate: SeriesCreate = {
            series_name: series.series_name,
            language: series.language,
            cover_image: series.cover_image,
            description: series.description,
            price: series.price,
          };
          router.push(
            `/vision${(await api.series.postLandmarksLandmarkIdSeriesLandmarksLandmarkIdSeriesPost(series.landmark_id, seriesCreate)).data.self_link
            }`
          );
        }}
      >Create</Button>
    </Paper>
  </Layout>;
}

interface SeriesCreateInterface {
  series_name?: string,
  landmark_id?: number,
  language?: Language,
  cover_image?: string,
  description?: string,
  price?: number,
}