import { create } from "zustand"

interface AppState {
  // UI State
  sidebarOpen: boolean
  theme: "light" | "dark"
  
  // Actions
  toggleSidebar: () => void
  setTheme: (theme: "light" | "dark") => void
}

export const useAppStore = create<AppState>((set) => ({
  sidebarOpen: true,
  theme: "dark",
  
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => set({ theme }),
}))
