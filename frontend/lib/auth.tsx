"use client"

import { createContext, useContext, useEffect, useState, useCallback, ReactNode } from "react"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export interface User {
  id: string
  email: string
  username: string
  avatar_url?: string
  created_at: string
}

export interface AuthState {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  error: string | null
}

export interface AuthContextType extends AuthState {
  login: () => void
  logout: () => Promise<void>
  refreshAuth: () => Promise<void>
  clearError: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
    error: null,
  })

  const setLoading = (isLoading: boolean) => {
    setState((prev) => ({ ...prev, isLoading }))
  }

  const setError = (error: string | null) => {
    setState((prev) => ({ ...prev, error, isLoading: false }))
  }

  const setUser = (user: User | null) => {
    setState({
      user,
      isAuthenticated: !!user,
      isLoading: false,
      error: null,
    })
  }

  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }))
  }, [])

  // Refresh auth state - check if user is authenticated via cookies
  const refreshAuth = useCallback(async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_URL}/auth/me`, {
        credentials: "include",
      })

      if (response.ok) {
        const data = await response.json()
        setUser(data.user)
      } else if (response.status === 401) {
        // Try to refresh token
        const refreshResponse = await fetch(`${API_URL}/auth/refresh`, {
          method: "POST",
          credentials: "include",
        })

        if (refreshResponse.ok) {
          // Retry getting user
          const retryResponse = await fetch(`${API_URL}/auth/me`, {
            credentials: "include",
          })
          if (retryResponse.ok) {
            const data = await retryResponse.json()
            setUser(data.user)
            return
          }
        }
        setUser(null)
      } else {
        setUser(null)
      }
    } catch (error) {
      console.error("Auth refresh error:", error)
      setUser(null)
    }
  }, [])

  // Initial auth check on mount
  useEffect(() => {
    refreshAuth()
  }, [refreshAuth])

  // Login - redirect to GitHub OAuth
  const login = useCallback(() => {
    const currentUrl = typeof window !== "undefined" ? window.location.origin : ""
    const callbackUrl = `${currentUrl}/auth/callback`
    const loginUrl = `${API_URL}/auth/github/login?redirect_uri=${encodeURIComponent(callbackUrl)}`
    window.location.href = loginUrl
  }, [])

  // Logout
  const logout = useCallback(async () => {
    try {
      setLoading(true)
      await fetch(`${API_URL}/auth/logout`, {
        method: "POST",
        credentials: "include",
      })
      setUser(null)
    } catch (error) {
      console.error("Logout error:", error)
      setError("Failed to logout. Please try again.")
    }
  }, [])

  return (
    <AuthContext.Provider
      value={{
        ...state,
        login,
        logout,
        refreshAuth,
        clearError,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuthContext() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuthContext must be used within an AuthProvider")
  }
  return context
}
