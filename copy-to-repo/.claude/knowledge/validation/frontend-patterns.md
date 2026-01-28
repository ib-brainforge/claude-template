# Frontend Validation Patterns

<!--
PROJECT-SPECIFIC: Update with your frontend patterns and grep patterns.
This is referenced by: frontend-pattern-validator
-->

## Framework Detection

| Framework | package.json Dependency | File Extension | Component Path |
|-----------|------------------------|----------------|----------------|
| React | `react` | `.tsx`, `.jsx` | `src/components/**/*` |
| Vue | `vue` | `.vue` | `src/components/**/*` |
| Angular | `@angular/core` | `.ts` | `src/app/**/*` |
| Svelte | `svelte` | `.svelte` | `src/**/*` |
| Next.js | `next` | `.tsx` | `pages/**/*`, `app/**/*` |

---

## React Patterns

### Component Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Function components | `function\s+[A-Z].*\(.*\).*{` | Named function components |
| Arrow components | `const\s+[A-Z].*=.*=>` | Arrow function components |
| Props interface | `interface.*Props\s*{` | TypeScript props |
| FC typing | `: FC<\|: React\.FC<` | Function component typing |

### State Management

| Library | package.json Dependency | Usage Pattern |
|---------|------------------------|---------------|
| React Query | `@tanstack/react-query` or `react-query` | `useQuery\|useMutation` |
| Zustand | `zustand` | `create\(\|useStore` |
| Redux | `@reduxjs/toolkit` or `redux` | `useSelector\|useDispatch` |
| Recoil | `recoil` | `useRecoilState\|atom\(` |

---

## Vue Patterns

### Component Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Script setup | `<script setup` | Composition API |
| Define props | `defineProps<\|defineProps\(` | Props definition |
| Define emits | `defineEmits<\|defineEmits\(` | Events definition |

### State Management

| Library | package.json Dependency | Usage Pattern |
|---------|------------------------|---------------|
| Pinia | `pinia` | `defineStore\|useStore` |
| Vuex | `vuex` | `useStore\|mapState` |

---

## Styling Detection

| Methodology | Detection Pattern | File Pattern |
|-------------|-------------------|--------------|
| CSS Modules | - | `**/*.module.css`, `**/*.module.scss` |
| Styled Components | `styled-components` in deps | `**/*.styled.ts` |
| Tailwind | `tailwindcss` in deps | `className=".*"` |
| Emotion | `@emotion/` in deps | `css\`\|styled\(` |

---

## Build Config Detection

| Bundler | Config File |
|---------|-------------|
| Vite | `vite.config.ts`, `vite.config.js` |
| Webpack | `webpack.config.js`, `webpack.config.ts` |
| Next.js | `next.config.js`, `next.config.mjs` |
| Parcel | `package.json` (parcel field) |

---

## Anti-Patterns to Detect

| Anti-Pattern | Grep Pattern | Severity | Suggestion |
|--------------|--------------|----------|------------|
| Direct fetch | `fetch\s*\(\|axios\.` | error | Use API client from core |
| Inline styles | `style\s*=\s*\{\s*\{` | warning | Use CSS classes or Tailwind |
| Index as key | `key=\{index\}\|key=\{i\}` | warning | Use stable unique ID |
| Console.log | `console\.log` | warning | Remove or use logger |
| Window globals | `window\.[a-z]` | warning | Avoid global state |
| LocalStorage direct | `localStorage\.` | warning | Use state management |
| Any type | `: any` | warning | Use proper types |
| Props spreading | `\{\.\.\.props\}` | info | Be explicit with props |
