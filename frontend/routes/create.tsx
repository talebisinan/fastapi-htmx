/** @jsx h */
import { h } from "preact";
import { PageProps } from "$fresh/server.ts";
import { tw } from "@twind";
import Layout from "../islands/Layout.tsx";

export default function Page() {
  return (
    <Layout
      children={
        <form
          id="organizationForm"
          action="http://127.0.0.1:8000/add"
          method="post"
        >
          <label
            for="email"
            class={tw`block text-sm font-medium text-gray-700`}
          >
            New organization name
          </label>
          <div class={tw`mt-1`}>
            <input
              id="titleInput"
              autocomplete="off"
              type="text"
              name="title"
              class={tw`max-w-xl px-2 py-3 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md`}
              placeholder="Organization name"
            />
          </div>
          <button
            type="submit"
            class={tw`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded`}
          >
            Save
          </button>
        </form>
      }
    />
  );
}
