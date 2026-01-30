"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuthContext } from "@/lib/auth"

/**
 * Primary hook for authentication
 * Re-exports auth context with additional utilities
 */
export function useAuth() {
  return useAuthContext()
}

/**
 * Hook to protect routes - redirects to login if not authenticated
 */
export function useRequireAuth(redirectTo: string = "/login") {
  const { isAuthenticated, isLoading } = useAuthContext()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push(redirectTo)
    }
  }, [isAuthenticated, isLoading, redirectTo, router])

  return { isAuthenticated, isLoading }
}

/**
 * Hook to redirect authenticated users away (e.g., from login page)
 */
export function useRedirectIfAuthenticated(redirectTo: string = "/dashboard") {
  const { isAuthenticated, isLoading } = useAuthContext()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push(redirectTo)
    }
  }, [isAuthenticated, isLoading, redirectTo, router])

  return { isAuthenticated, isLoading }
}

/**
 * Hook to get current user or null
 */
export function useUser() {
  const { user, isLoading } = useAuthContext()
  return { user, isLoading }
}
