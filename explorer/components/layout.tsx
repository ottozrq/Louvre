import {
  AppBar,
  Button,
  ButtonGroup,
  IconButton,
  TextField,
  Toolbar,
} from "@material-ui/core";
import AccountCircle from "@material-ui/icons/AccountCircle";
import HomeIcon from "@material-ui/icons/Home";
import PersonAdd from "@material-ui/icons/PersonAdd";
import { find } from "lodash";
import Head from "next/head";
import Link from "next/link";
import { useRouter } from "next/router";
import React, { useState } from "react";

import { setApiBasePath } from "./api";

const serverLookup = {
  Prod: "https://vision.ottozhang.com",
  Dev: "https://vision.ottozhang.com",
  Local: "http://localhost:8000",
};
export default function Layout({ children, title = "Vision" }) {
  const router = useRouter();
  const [basePath, setBasePath] = useState(
    typeof window !== "undefined" && window.localStorage.base_path
  );
  function setBP(s: string, keyCode?: number, skip = false) {
    if (!skip) {
      setBasePath(s);
    }
    if (keyCode === 13) {
      setApiBasePath(s);
    }
  }
  return (
    <>
      <Head>
        <title>{title}</title>
      </Head>
      <div>
        <AppBar position="static">
          <Toolbar>
            <IconButton color="inherit">
              <Link href="/vision">
                <HomeIcon />
              </Link>
            </IconButton>
            <IconButton color="inherit">
              <Link href="/vision/token">
                <PersonAdd />
              </Link>
            </IconButton>
            <IconButton color="inherit">
              <Link href="/vision/user">
                <AccountCircle />
              </Link>
            </IconButton>
            <TextField
              style={{ width: "200px", marginRight: "50px" }}
              placeholder="Search…"
              onKeyDown={({ keyCode, target }) => {
                if (keyCode === 13) {
                  router.push(`/vision/search?q=${target["value"]}`);
                }
              }}
            />
            <ButtonGroup style={{ width: "200px", marginRight: "50px" }}>
              {Object.entries(serverLookup).map(([k, v]) => (
                <Button key={k} onClick={() => setBP(v, 13)}>
                  <span style={{ color: v === basePath && "white" }}>{k}</span>
                </Button>
              ))}
            </ButtonGroup>
            <TextField
              style={{ width: "200px" }}
              placeholder="Server URL"
              value={
                (() => {
                  const search = find(
                    Object.entries(serverLookup),
                    ([, v]) => v === basePath
                  );
                  return search && search[0];
                })() || basePath
              }
              onChange={({ target: { value } }) => setBP(value)}
              onKeyDown={({ keyCode, target }) => {
                setBP(target["value"], keyCode, true);
              }}
            />
          </Toolbar>
        </AppBar>
      </div>
      <div
        style={{
          padding: "0 1rem",
          margin: "1rem 1rem 2rem 1rem",
          marginTop: "4rem",
        }}
      >
        {children}
      </div>
    </>
  );
}
