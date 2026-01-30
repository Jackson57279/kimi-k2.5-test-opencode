# FRONTEND KNOWLEDGE BASE

## OVERVIEW

Next.js 14 App Router with TypeScript, Tailwind CSS, shadcn/ui components, Zustand state management, TanStack Query for data fetching.

## STRUCTURE

```
frontend/
├── app/              # Next.js App Router pages
│   ├── layout.tsx    # Root layout (Inter font, dark mode)
│   ├── page.tsx      # Landing page
│   └── dashboard/    # Dashboard routes
├── components/
│   └── ui/           # shadcn/ui components (button, card, dialog, etc.)
├── hooks/            # Custom React hooks
├── lib/              # Utilities (cn() for classnames)
├── stores/           # Zustand stores
├── types/            # TypeScript type definitions
├── tailwind.config.ts
└── tsconfig.json
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add page | `app/[route]/page.tsx` | Server Component by default |
| Add UI component | `components/ui/` | Use shadcn/ui CLI: `bunx shadcn@latest add [component]` |
| Add store | `stores/` | Zustand pattern, see `app-store.ts` |
| Add hook | `hooks/` | Custom hooks, see `use-mounted.ts` |
| Add type | `types/index.ts` | Shared TypeScript types |
| Styling | `tailwind.config.ts` | Railway theme colors, animations |

## CONVENTIONS

- **Package manager**: bun (not npm/yarn)
- **Imports**: Use `@/*` alias for project root
- **Components**: Functional components with TypeScript
- **Styling**: Tailwind classes, use `cn()` for conditional classes
- **State**: Zustand for global state, React Query for server state
- **Dark mode**: Always-on (`className="dark"` on `<html>`)

## SHADCN/UI PATTERN

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

// Use cva variants
<Button variant="default" size="lg">Click me</Button>
```

Available components: `button`, `card`, `dialog`, `dropdown-menu`, `input`, `table`, `tabs`, `badge`

## ZUSTAND STORE PATTERN

```typescript
// stores/my-store.ts
import { create } from "zustand"

interface MyState {
  value: string
  setValue: (v: string) => void
}

export const useMyStore = create<MyState>((set) => ({
  value: "",
  setValue: (value) => set({ value }),
}))
```

## TAILWIND THEME

Custom Railway-inspired design system in `tailwind.config.ts`:

- **Colors**: `railway-indigo`, `railway-violet`, `railway-cyan`, `railway-purple`
- **Animations**: `fade-in`, `slide-up`, `shimmer`, `glow`, `gradient-shift`
- **Effects**: Glassmorphism with `backdrop-blur`

## TYPESCRIPT CONFIG

Strict mode enabled with additional safety:
- `noUncheckedIndexedAccess: true` — array access returns `T | undefined`
- `forceConsistentCasingInFileNames: true`
- `noFallthroughCasesInSwitch: true`

## ANTI-PATTERNS

- **NO** `any` types — use `unknown` and narrow
- **NO** `// @ts-ignore` or `// @ts-expect-error`
- **NO** inline styles — use Tailwind classes
- **NO** `useEffect` for data fetching — use TanStack Query
- **NO** prop drilling beyond 2 levels — use Zustand or context

## API INTEGRATION

```typescript
// Use TanStack Query for API calls
import { useQuery } from "@tanstack/react-query"

const { data, isLoading } = useQuery({
  queryKey: ["projects"],
  queryFn: () => fetch("/api/projects").then(r => r.json()),
})
```

Backend API URL configured via `NEXT_PUBLIC_API_URL` environment variable.

## NOTES

- Build artifacts in `.next/` — gitignored, regenerate with `bun run build`
- Socket.io client installed for real-time features
- Framer Motion installed for animations
- ESLint config in `.eslintrc.json`
