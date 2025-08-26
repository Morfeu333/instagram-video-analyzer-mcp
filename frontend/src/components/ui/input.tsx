import * as React from "react"
import { cn } from "@/lib/utils"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "file:text-white placeholder:text-gray-400 selection:bg-blue-500 selection:text-white bg-gray-800/50 backdrop-blur-sm border-gray-600/50 flex h-12 w-full min-w-0 rounded-xl border px-4 py-3 text-base shadow-lg transition-all outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 text-white",
        "focus:border-blue-500/70 focus:ring-2 focus:ring-blue-500/30 focus:bg-gray-800/70",
        "hover:border-gray-500/70 hover:bg-gray-800/60",
        className
      )}
      {...props}
    />
  )
}

export { Input }
