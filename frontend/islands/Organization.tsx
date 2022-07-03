/** @jsx h */
import { h } from "preact";
import { tw } from "@twind";

interface Organization {
  id: number;
  title: string;
  session_key: string;
}

export default function Organization({ id, title }: Organization) {
  return (
    <tr class={tw`hover:cursor-pointer hover:bg-gray-100`}>
      <td
        class={tw`whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6`}
      >
        <p>{{ title }}</p>
      </td>
      <td
        class={tw`w-20 relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6`}
      >
        <button
          onClick={() =>
            fetch(`http://127.0.0.1:8000/delete/${id}`, {
              method: "DELETE",
            })
          }
          class={tw`text-sky-600 hover:text-sky-900`}
        >
          Delete
        </button>
      </td>
    </tr>
  );
}
