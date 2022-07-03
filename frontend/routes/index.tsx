/** @jsx h */
import { h } from "preact";
import { Handlers, PageProps } from "$fresh/server.ts";
import Layout from "../islands/Layout.tsx";
import Organization from "../islands/Organization.tsx";

interface Organization {
  id: number;
  title: string;
  session_key: string;
}

export const handler: Handlers<Organization[] | null> = {
  async GET(_, ctx) {
    const resp = await fetch("http://127.0.0.1:8000/");
    if (resp.status === 404) return ctx.render(null);
    const organizations: Organization[] = await resp.json();
    return ctx.render(organizations);
  },
};

export default function Home({ data }: PageProps<Organization[] | null>) {
  return (
    <Layout
      children={
        <div>
          {!data?.length ? (
            <div>No organizations</div>
          ) : (
            data.map((organization) => (
              <Organization key={organization.id} organization={organization} />
            ))
          )}
        </div>
      }
    />
  );
}
