import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { AnalysisResult, JobSummary, SystemStatsResponse } from '@/types'

interface AppState {
  // UI State
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  
  // Current Analysis
  currentJobId: string | null
  currentAnalysis: AnalysisResult | null
  
  // History
  analysisHistory: JobSummary[]
  
  // Stats
  systemStats: SystemStatsResponse | null
  
  // Settings
  settings: {
    autoRefresh: boolean
    refreshInterval: number
    defaultAnalysisType: string
    notifications: boolean
  }
}

interface AppActions {
  // UI Actions
  setTheme: (theme: 'light' | 'dark') => void
  toggleSidebar: () => void
  setSidebarOpen: (open: boolean) => void
  
  // Analysis Actions
  setCurrentJobId: (jobId: string | null) => void
  setCurrentAnalysis: (analysis: AnalysisResult | null) => void
  
  // History Actions
  addToHistory: (job: JobSummary) => void
  updateHistoryItem: (jobId: string, updates: Partial<JobSummary>) => void
  removeFromHistory: (jobId: string) => void
  clearHistory: () => void
  
  // Stats Actions
  setSystemStats: (stats: SystemStatsResponse) => void
  
  // Settings Actions
  updateSettings: (settings: Partial<AppState['settings']>) => void
  
  // Reset
  reset: () => void
}

const initialState: AppState = {
  theme: 'light',
  sidebarOpen: true,
  currentJobId: null,
  currentAnalysis: null,
  analysisHistory: [],
  systemStats: null,
  settings: {
    autoRefresh: true,
    refreshInterval: 5000,
    defaultAnalysisType: 'comprehensive',
    notifications: true,
  },
}

export const useAppStore = create<AppState & AppActions>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,
        
        // UI Actions
        setTheme: (theme) => set({ theme }),
        toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
        setSidebarOpen: (open) => set({ sidebarOpen: open }),
        
        // Analysis Actions
        setCurrentJobId: (jobId) => set({ currentJobId: jobId }),
        setCurrentAnalysis: (analysis) => set({ currentAnalysis: analysis }),
        
        // History Actions
        addToHistory: (job) => set((state) => ({
          analysisHistory: [job, ...state.analysisHistory.filter(h => h.job_id !== job.job_id)]
        })),
        updateHistoryItem: (jobId, updates) => set((state) => ({
          analysisHistory: state.analysisHistory.map(item =>
            item.job_id === jobId ? { ...item, ...updates } : item
          )
        })),
        removeFromHistory: (jobId) => set((state) => ({
          analysisHistory: state.analysisHistory.filter(item => item.job_id !== jobId)
        })),
        clearHistory: () => set({ analysisHistory: [] }),
        
        // Stats Actions
        setSystemStats: (stats) => set({ systemStats: stats }),
        
        // Settings Actions
        updateSettings: (newSettings) => set((state) => ({
          settings: { ...state.settings, ...newSettings }
        })),
        
        // Reset
        reset: () => set(initialState),
      }),
      {
        name: 'instagram-analyzer-store',
        partialize: (state) => ({
          theme: state.theme,
          sidebarOpen: state.sidebarOpen,
          analysisHistory: state.analysisHistory,
          settings: state.settings,
        }),
      }
    ),
    {
      name: 'instagram-analyzer-store',
    }
  )
)
