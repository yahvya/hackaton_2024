import Image from "next/image";
import Link from "next/link";

export function Navbar() {
  return (
    <div className="w-full bg-[#56BAA2]">
      <div className="container flex h-16 items-center gap-6">
        <div className="flex items-center gap-2">
          <Image
            src="/Zeendoc-EDM.png"
            alt="Logo"
            width={150}
            height={150}
            className="relative left-4"
          />
        </div>
        <Link href="/support" className="text-white hover:text-green-100">
          Services Support
        </Link>
        <Link href="/client" className="text-white hover:text-green-100">
          Côté client
        </Link>
      </div>
    </div>
  );
}
