import { ScrollArea } from '@/components/ui/scroll-area'
import type { PDFFile } from '../types/file'

interface ChangeLogProps {
  file: PDFFile | null
}

export function ChangeLog({ file }: ChangeLogProps) {
  if (!file) {
    return (
      <div className="p-4 text-center text-muted-foreground">
        Select a file to view changes
      </div>
    )
  }

  return (
    <ScrollArea className="h-full">
      <div className="p-4 space-y-2">
        <h3 className="font-semibold">Changes</h3>
        {file.changes && file.changes.length > 0 ? (
          <ul className="space-y-2">
            {file.changes.map((change, index) => (
              <li key={index} className="text-sm">
                • {change}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-muted-foreground">No changes recorded</p>
        )}
      </div>
    </ScrollArea>
  )
}

