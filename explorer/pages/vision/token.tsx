import { Button, FormGroup, TextField } from "@material-ui/core";
import { useRouter } from "next/router";
import React, { useState } from "react";

import api, { config } from "../../components/api";
import Layout from "../../components/layout";

export default function TokenPage() {
  const router = useRouter();
  const [{ username, password, loggedIn }, setState] = useState({
    username: "",
    password: "",
    loggedIn: false,
  });
  return (
    <Layout>
      <h1>Log in</h1>
      <FormGroup>
        <TextField
          id="username"
          label="Username"
          value={username}
          onChange={({ target: { value } }) =>
            setState((s) => ({ ...s, username: value }))
          }
        />
        <TextField
          id="password"
          label="Password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={({ target: { value } }) =>
            setState((s) => ({ ...s, password: value }))
          }
        />
        <Button
          onClick={() =>
            api.root
              .tokenTokenPost(username, password)
              .then(({ data: { access_token } }) => {
                window.localStorage.setItem("access_token", access_token);
                return (config.accessToken = access_token);
              })
              .then(() => setState((s) => ({ ...s, loggedIn: true })))
              .then(() => router.push("/vision"))
          }
        >
          Log in
        </Button>
      </FormGroup>
      {loggedIn ? <h2>Logged in!</h2> : undefined}
    </Layout>
  );
}
