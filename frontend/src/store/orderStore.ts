import { create } from 'zustand'

interface Task {
  id: number
  status: string
  priority: string
  from_location_id: number
  to_location_id: number
  from_row?: number
  from_col?: number
  to_row?: number
  to_col?: number
}

interface OrderStore {
  tasks: Task[]
  setTasks: (tasks: Task[]) => void
  addTask: (task: Task) => void
  updateTask: (task: Task) => void
}

export const useOrderStore = create<OrderStore>((set) => ({
  tasks: [],
  setTasks: (tasks) => set({ tasks }),
  addTask: (task) =>
    set((state) => ({ tasks: [...state.tasks, task] })),
  updateTask: (task) =>
    set((state) => ({
      tasks: state.tasks.map((t) => (t.id === task.id ? task : t)),
    })),
}))
