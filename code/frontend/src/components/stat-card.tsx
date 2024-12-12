import { Card, CardContent } from "@/components/ui/card";
import { History, ThumbsUp } from "lucide-react";

export default function StatsCards() {
  return (
    <div className="flex gap-4 max-w-4xl mx-auto p-4 w-full items-center justify-center">
      <Card className="relative overflow-hidden w-56 h-28">
        <CardContent className="flex flex-col items-center justify-center p-6 text-center">
          <div className="flex  items-center justify-center gap-2">
            <p className="text-xl font-bold text-[#4fd1c5] ">92%</p>
            <ThumbsUp className="w-6 h-6 text-[#1a365d] " />
          </div>
          <p className="text-gray-600 ">
            des utilisateurs sont satisfaits de Zeendoc
          </p>
        </CardContent>
      </Card>
      <Card className="relative overflow-hidden w-56 h-28">
        <CardContent className="flex flex-col items-center justify-center p-6 text-center">
          <div className="flex  items-center justify-center gap-2">
            <History className="w-6 h-6 text-[#1a365d] " />
            <p className="text-xl font-bold text-[#4fd1c5] ">95%</p>
          </div>
          <p className="text-gray-600 ">
            des utilisateurs affirment gagner du temps
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
