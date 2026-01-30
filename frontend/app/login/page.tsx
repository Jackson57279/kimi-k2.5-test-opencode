"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { useAuth, useRedirectIfAuthenticated } from "@/hooks/use-auth"
import { Button } from "@/components/ui/button"

function GitHubIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="currentColor"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
    </svg>
  )
}

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

export default function LoginPage() {
  const { login, error, clearError, isLoading: authLoading } = useAuth()
  const { isAuthenticated, isLoading } = useRedirectIfAuthenticated("/dashboard")
  const [isRedirecting, setIsRedirecting] = useState(false)

  const handleLogin = () => {
    setIsRedirecting(true)
    login()
  }

  // Show loading while checking auth or redirecting
  if (isLoading || (isAuthenticated && !isRedirecting)) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center">
        <LoadingSpinner className="h-8 w-8" />
      </main>
    )
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="w-full max-w-sm space-y-8">
        {/* Logo/Brand */}
        <div className="text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500 to-purple-600">
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
          <h1 className="text-2xl font-bold tracking-tight">Railway Clone</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Deploy your applications with ease
          </p>
        </div>

        {/* Login Card */}
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <div className="space-y-4">
            <div className="text-center">
              <h2 className="text-lg font-semibold">Welcome back</h2>
              <p className="text-sm text-muted-foreground">
                Sign in to continue to your dashboard
              </p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="rounded-md border border-destructive/50 bg-destructive/10 p-3">
                <div className="flex items-start gap-2">
                  <svg
                    className="mt-0.5 h-4 w-4 text-destructive"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <div className="flex-1">
                    <p className="text-sm text-destructive">{error}</p>
                    <button
                      onClick={clearError}
                      className="mt-1 text-xs text-muted-foreground underline hover:text-foreground"
                    >
                      Dismiss
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* GitHub OAuth Button */}
            <Button
              onClick={handleLogin}
              disabled={isRedirecting || authLoading}
              className="w-full gap-2 bg-[#24292f] text-white hover:bg-[#24292f]/90"
              size="lg"
            >
              {isRedirecting ? (
                <>
                  <LoadingSpinner className="h-5 w-5" />
                  Redirecting...
                </>
              ) : (
                <>
                  <GitHubIcon className="h-5 w-5" />
                  Continue with GitHub
                </>
              )}
            </Button>

            <p className="text-center text-xs text-muted-foreground">
              By continuing, you agree to our{" "}
              <a href="#" className="underline hover:text-foreground">
                Terms of Service
              </a>{" "}
              and{" "}
              <a href="#" className="underline hover:text-foreground">
                Privacy Policy
              </a>
            </p>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-muted-foreground">
          Don&apos;t have a GitHub account?{" "}
          <a
            href="https://github.com/signup"
            target="_blank"
            rel="noopener noreferrer"
            className="underline hover:text-foreground"
          >
            Create one
          </a>
        </p>
      </div>
    </main>
  )
}
