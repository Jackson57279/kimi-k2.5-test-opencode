"use client"

import { useEffect, useState, useRef, Suspense } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { useAuth } from "@/hooks/use-auth"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

type CallbackState = "loading" | "success" | "error"

function LoadingSpinner({ className }: { className?: string }) {
  return (
    <svg
      className={`animate-spin ${className}`}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  )
}

function CallbackContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { refreshAuth } = useAuth()
  const [state, setState] = useState<CallbackState>("loading")
  const [errorMessage, setErrorMessage] = useState<string>("")
  const processedRef = useRef(false)

  useEffect(() => {
    // Prevent double processing in React StrictMode
    if (processedRef.current) return
    processedRef.current = true

    async function handleCallback() {
      const code = searchParams.get("code")
      const error = searchParams.get("error")
      const errorDescription = searchParams.get("error_description")

      // Handle OAuth errors from GitHub
      if (error) {
        setState("error")
        setErrorMessage(errorDescription || `OAuth error: ${error}`)
        return
      }

      // No code means invalid callback
      if (!code) {
        setState("error")
        setErrorMessage("No authorization code received. Please try again.")
        return
      }

      try {
        // Exchange code for token via backend
        const response = await fetch(
          `${API_URL}/auth/github/callback?code=${encodeURIComponent(code)}`,
          {
            method: "GET",
            credentials: "include",
          }
        )

        if (!response.ok) {
          const data = await response.json().catch(() => ({}))
          throw new Error(data.detail || "Failed to complete authentication")
        }

        // Refresh auth state to get user info
        await refreshAuth()
        
        setState("success")
        
        // Redirect to dashboard after short delay
        setTimeout(() => {
          router.push("/dashboard")
        }, 1000)
      } catch (err) {
        setState("error")
        setErrorMessage(
          err instanceof Error ? err.message : "An unexpected error occurred"
        )
      }
    }

    handleCallback()
  }, [searchParams, refreshAuth, router])

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="w-full max-w-sm space-y-6">
        {/* Logo */}
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500 to-purple-600">
          <svg
            className="h-6 w-6 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 10V3L4 14h7v7l9-11h-7z"
            />
          </svg>
        </div>

        {/* Loading State */}
        {state === "loading" && (
          <div className="text-center">
            <LoadingSpinner className="mx-auto h-8 w-8" />
            <h2 className="mt-4 text-lg font-semibold">Completing sign in...</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Please wait while we verify your account
            </p>
          </div>
        )}

        {/* Success State */}
        {state === "success" && (
          <div className="text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-500/20">
              <svg
                className="h-6 w-6 text-green-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <h2 className="mt-4 text-lg font-semibold">Welcome back!</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Redirecting to your dashboard...
            </p>
          </div>
        )}

        {/* Error State */}
        {state === "error" && (
          <div className="space-y-4 text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-destructive/20">
              <svg
                className="h-6 w-6 text-destructive"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </div>
            <div>
              <h2 className="text-lg font-semibold">Authentication failed</h2>
              <p className="mt-1 text-sm text-muted-foreground">{errorMessage}</p>
            </div>
            <div className="flex flex-col gap-2">
              <button
                onClick={() => router.push("/login")}
                className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
              >
                Try again
              </button>
              <button
                onClick={() => router.push("/")}
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                Return home
              </button>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}

export default function CallbackPage() {
  return (
    <Suspense
      fallback={
        <main className="flex min-h-screen flex-col items-center justify-center">
          <LoadingSpinner className="h-8 w-8" />
        </main>
      }
    >
      <CallbackContent />
    </Suspense>
  )
}
