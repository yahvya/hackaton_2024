import FileUpload from "@/components/file-upload";
import StatsCards from "@/components/stat-card";

export default function Home() {
  return (
    <div className="h-screen">
      <div className="p-4">
        <div className="flex flex-col items-center justify-center w-full h-1/5">
          <h1 className="text-2xl font-bold">
            Vous avez eu un problème avec un de vos PDF ?
          </h1>
          <p className="text-sm text-gray-500">
            Envoyez vos PDF au service support Zeendoc
          </p>
          <p className="text-sm text-gray-500">
            Ne vous inquiétez toutes vos données sont anonymisées
          </p>
        </div>
        <StatsCards />
      </div>

      <FileUpload />
    </div>
  );
}
