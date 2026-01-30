// Application types
export interface Application {
  id: string
  name: string
  status: "running" | "stopped" | "deploying" | "failed"
  createdAt: string
  updatedAt: string
}

// User types
export interface User {
  id: string
  email: string
  name: string
  avatar?: string
}

// Project types
export interface Project {
  id: string
  name: string
  description?: string
  applications: Application[]
  createdAt: string
  updatedAt: string
}

// API Response types
export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

// Pagination types
export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  totalPages: number
}
