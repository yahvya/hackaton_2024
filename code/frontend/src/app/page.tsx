import {redirect } from "next/navigation"
export default function Home() {

    redirect("/client");
  return (
    <div className="flex min-h-screen flex-col">
      <main className="flex-1">{/* Your page content */}</main>
    </div>
  );
}
