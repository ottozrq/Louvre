import React from "react";
import { Card } from "react-bootstrap";

import ApiLink from "./api_link";
import ReactJson from "./react_json";

export default function ApiLinks({ resource }: { [key: string]: any }) {
  return (
    <Card style={{ margin: "10px", maxWidth: "700px" }}>
      <Card.Header>
        <Card.Title>Properties</Card.Title>
      </Card.Header>
      <Card.Body>
        <ul>
          {Object.entries(resource)
            .filter(([x]) => !["contents", "geometry"].includes(x))
            .map(([x, value]) => (
              <li key={x}>
                <label style={{ fontWeight: "bold", marginRight: "3px" }}>
                  {x}:
                </label>
                {value === undefined || value === null ? (
                  value
                ) : typeof value === "object" ? (
                  <ReactJson src={value} />
                ) : value.toString()?.startsWith("/") ? (
                  <ApiLink text={x} value={value.toString()} />
                ) : (
                  value
                )}
              </li>
            ))}
        </ul>
      </Card.Body>
    </Card>
  );
}
