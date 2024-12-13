import { ScrollArea } from "@/components/ui/scroll-area";
import type { PDFFile } from "../types/file";

interface ChangeLogProps {
  file: PDFFile | null;
}

export function ChangeLog({ file }: ChangeLogProps) {
  if (!file) {
    return (
      <div className="p-4 text-center text-muted-foreground">
        Select a file to view changes
      </div>
    );
  }

  // Extraction des métadonnées si elles existent
  const metadata = file.entitiesConfig?.metadata_entities;

  return (
    <ScrollArea className="h-full">
      <div>
        <h3 className="font-semibold mb-2">Métadonnées du PDF</h3>
        {file.changes && file.changes.length > 0 ? (
          <ul className="space-y-2">
            {file.changes.map((change, index) => (
              <li key={index} className="text-sm">
                • {change}
              </li>
            ))}
          </ul>
        ) : (
          <pre className="text-sm">{JSON.stringify(file, null, 2)}</pre>
        )}
      </div>
    </ScrollArea>
  );
}
