import { create } from 'zustand'

interface AGV {
  id: number
  name: string
  row: number
  col: number
  state: string
  battery: number
  cargo: number | null
}

interface AGVStore {
  agvs: AGV[]
  setAGVs: (agvs: AGV[]) => void
  updateAGV: (agv: AGV) => void
}

export const useAGVStore = create<AGVStore>((set) => ({
  agvs: [],
  setAGVs: (agvs) => set({ agvs }),
  updateAGV: (agv) =>
    set((state) => ({
      agvs: state.agvs.map((a) => (a.id === agv.id ? agv : a)),
    })),
}))
