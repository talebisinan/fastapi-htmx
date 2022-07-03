/** @jsx h */
import { h } from "preact";
import { PageProps, Handlers } from "$fresh/server.ts";
import Layout from "../islands/Layout.tsx";

interface Organization {
  id: number;
  title: string;
  session_key: string;
}
export const handler: Handlers<Organization | null> = {
  async GET(_, ctx) {
    const resp = await fetch(`http://127.0.0.1:8000/edit/${ctx.params.id}`);
    if (resp.status === 404) return ctx.render(null);
    const organization: Organization = await resp.json();
    return ctx.render(organization);
  },
};

export default function Greet({
  data,
  params,
}: PageProps<Organization[] | null>) {
  return (
    <Layout
      children={
        <div>
          id: {data.id}
          <br />
          title:{data.title}
        </div>
      }
    />
  );
}
