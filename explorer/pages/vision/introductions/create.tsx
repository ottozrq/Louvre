import { Paper, TextField, Button, Select, MenuItem } from "@material-ui/core";
import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";

import { SeriesCreate, Landmark, Series, IntroductionCreate, Artwork } from "../../../api";
import api from "../../../components/api";
import Layout from "../../../components/layout";

const baseStyle = { padding: "10px", margin: "10px", maxWidth: "300px" };
const fullStyle = { padding: "10px", margin: "10px", width: "100%" };

export default function IntroductionCreatePage() {
  const router = useRouter();
  const [introduction, setIntroduction] = useState<IntroductionCreateInterface>({
    series_id: 1,
  });
  const [artworks, setArtworks] = useState<Artwork[]>([]);
  const [series, setSeries] = useState<Series[]>([]);
  useEffect(() => {
    api.artworks
      .getArtworksLandmarksLandmarkIdArtworksGet(1)
      .then((data) => (data ? setArtworks(data.data.contents) : []));
  }, []);
  return <Layout title="Create Introduction">
    <h1>Create Introduction</h1>
    <Paper style={{ padding: "10px", margin: "10px", maxWidth: "1000px" }}>
      <TextField
        style={baseStyle}
        onChange={({ target: { value } }) =>
          setIntroduction({ ...introduction, introduction_name: value })
        }
        label="Introduction Name"
      />
      <Select
        style={{ margin: "10px", padding: "12px", width: "200px" }}
        id="standard-basic"
        onChange={({ target: { value } }) => {
          setIntroduction({ ...introduction, artwork_id: value as number })
        }}
      >
        {artworks.map(
          (artwork, index) => {
            console.log(artwork.artwork_name["en"])
            return (
              <MenuItem
                key={index}
                style={baseStyle}
                value={artwork.artwork_id}
              >
                {artwork.artwork_name["en"]}
              </MenuItem>
            );
          }
        )}
      </Select>
      <Select
        style={{ margin: "10px", padding: "12px", width: "200px" }}
        id="standard-basic"
        onChange={({ target: { value } }) => {
          setIntroduction({ ...introduction, series_id: value as number })
        }}
      >
        {series.map(
          (s, index) => {
            console.log(s.series_name)
            return (
              <MenuItem
                key={index}
                style={baseStyle}
                value={s.series_id}
              >
                {s.series_name}
              </MenuItem>
            );
          }
        )}
      </Select>
      <Select
        style={{ margin: "10px", padding: "12px", width: "200px" }}
        id="standard-basic"
        onChange={({ target: { value } }) => {
          setIntroduction({ ...introduction, lang: value as string })
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
      <TextField
        style={fullStyle}
        onChange={({ target: { value } }) =>
          setIntroduction({ ...introduction, introduction: {...introduction.introduction, content: value} })
        }
        multiline
        rows={6}
        label="Introduction"
      /><br />
      <Button
        style={baseStyle}
        variant="contained"
        onClick={async () => {
          const introductionCreate: IntroductionCreate = {
            introduction_name: introduction.introduction_name,
            artwork_id: introduction.artwork_id,
            lang: introduction.lang,
            introduction: introduction.introduction,
          };
          router.push(
            `/vision${(await api.introductions.postSeriesSeriesIdIntroductionSeriesSeriesIdIntroductionsPost(introduction.artwork_id, introductionCreate)).data.self_link
            }`
          );
        }}
      >Create</Button>
    </Paper>
  </Layout>;
}

interface IntroductionCreateInterface {
  introduction_name?: string,
  artwork_id?: number,
  series_id?: number,
  lang?: string,
  introduction?: object,
}