/** @jsx h */
import { h } from "preact";
import { tw } from "@twind";
import Header from "./Header.tsx";

interface LayoutProps {
  children: any;
  header: any;
}

export default function Layout(props: LayoutProps) {
  return (
    <html lang="en" class={tw`h-full bg-gray-100`}>
      <body class={tw`h-full`}>
        <Header />
        <div class={tw`min-h-full`}>
          <header class={tw`bg-white shadow`}>
            <div class={tw`max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8`}>
              <h1 class={tw`text-3xl font-bold text-gray-900`}>
                Organizations
              </h1>
            </div>
          </header>
          <main>
            <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
              {props.children}
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}
