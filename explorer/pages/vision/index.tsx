import api from "../../components/api";
import ApiResourcePage from "../../components/api_resource_page";

export default function Root() {
  return <ApiResourcePage title="Root" getter={api.root.readRootGet} />;
}
