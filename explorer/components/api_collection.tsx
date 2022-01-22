import { NextRouter } from "next/router";
import React from "react";
import { Card } from "react-bootstrap";
import Collapsible from "react-collapsible";
import { IoMdArrowDropdownCircle } from "react-icons/io";
import ReactPaginate from "react-paginate";

import styles from "./api_collection.module.scss";
import ApiLink from "./api_link";
import ApiLinks from "./api_links";

interface SelfLink {
  self_link?: string;
}
interface ApiCollectionProps<T extends SelfLink> {
  collection: {
    contents?: T[];
    page_token: string;
    next_page_token: string;
    page_size: number;
    total_size: number;
    total_pages: number;
  };
  title(item: T): string;
  children?;
  router: NextRouter;
}

export default function ApiCollectionPage<T extends SelfLink>({
  collection,
  title,
  children,
  router,
}: ApiCollectionProps<T>) {
  return (
    <div>
      <Card>
        <Card.Body>
          <ReactPaginate
            previousLabel={"previous"}
            nextLabel={"next"}
            breakLabel={"..."}
            pageCount={collection.total_pages}
            marginPagesDisplayed={2}
            pageRangeDisplayed={5}
            onPageChange={(x) => {
              const selected = x.selected + 1;
              const currentPath = router.pathname;
              const currentQuery = router.query;
              currentQuery.page_token = selected.toString();

              router.push({
                pathname: currentPath,
                query: currentQuery,
              });
            }}
            containerClassName={styles.pagination}
            activeClassName={styles.active}
            initialPage={parseInt(collection.page_token) - 1}
            disableInitialCallback={true}
          />
        </Card.Body>
      </Card>
      {children}
      {collection?.contents?.map((x, i) => (
        <div style={{ padding: "5px", maxWidth: "800px" }} key={i}>
          <Card>
            <Card.Header>
              <ApiLink text={title(x)} value={x.self_link} />
            </Card.Header>
            <Card.Body>
              <Collapsible
                trigger={
                  <div style={{ cursor: "pointer" }}>
                    <span style={{ padding: "3px" }}>
                      <IoMdArrowDropdownCircle />
                    </span>
                    Expand Links
                  </div>
                }
              >
                <ApiLinks resource={x} />
              </Collapsible>
            </Card.Body>
          </Card>
        </div>
      ))}
    </div>
  );
}
