# React App Development Workflow Specification

## 1. Purpose & Objective
Govern the design, build, state management, testing, and bundling of modern React single-page or server-rendered web applications.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Node.js environment, Vite/Next.js setup, component specs, backend API endpoints.
- **Trigger Conditions**: Frontend feature sprint allocation.

## 3. Participating Agent Roles & Responsibilities
- **Frontend Lead**: Establishes React patterns, state management architecture (Zustand/Redux), and bundle optimization targets.
- **React Developer**: Builds React components, custom hooks, and route handlers.
- **UI Auditor**: Checks visual compliance, accessibility tree, and bundle size limits.

## 4. Step-by-Step Execution Sequence

### Step 1: Component & Hook Architecture
- **Inputs**: Feature specification, API contract, state management guidelines.
- **Actions**: Design component breakdown, custom hooks for data fetching (TanStack Query/SWR), and client-side state schema.
- **Outputs**: TypeScript definitions and custom hook skeletons.
- **Verification**: TypeScript compiler verification (`tsc --noEmit`) passing with zero errors.

### Step 2: Interactive Component Construction
- **Inputs**: TypeScript interfaces, Tailwind CSS / Styled Components design tokens.
- **Actions**: Implement JSX/TSX components, apply responsive styles, manage local component state, handle loading/error states.
- **Outputs**: Functional React components co-located with tests and styles.
- **Verification**: Visual check and unit tests (React Testing Library) verifying state rendering.

### Step 3: API & Global State Binding
- **Inputs**: REST/GraphQL endpoints, mock server handlers (MSW).
- **Actions**: Connect custom hooks to live API endpoints, handle authentication headers, implement optimistic updates.
- **Outputs**: End-to-end data-bound React views.
- **Verification**: Integration tests passing with MSW mock server and live staging server.

### Step 4: Bundle Optimization & Code Splitting
- **Inputs**: Built React application assets, bundler analyzer (rollup-plugin-visualizer / webpack-bundle-analyzer).
- **Actions**: Implement route-based dynamic imports (`React.lazy`), optimize tree-shaking, audit vendor bundle size.
- **Outputs**: Optimized production bundle with chunk splitting.
- **Verification**: Initial JS bundle size below 150KB gzipped.

### Step 5: E2E Testing & Staging Deploy
- **Inputs**: Staging environment configuration, Playwright / Cypress test suites.
- **Actions**: Run full E2E user flow tests on staging build; publish deployment preview.
- **Outputs**: E2E test run video/trace artifacts and staging URL.
- **Verification**: 100% E2E test pass rate across Chrome, Firefox, and Safari viewports.

## 5. Decision Gates & Branching Rules
- Gate 1: Strict TypeScript compilation (`strict: true`) must pass before merging code into develop branch.
- Gate 2: Initial bundle size budget check must pass before production deployment approval.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: React re-render loop causing performance degradation -> Action: Profile component via React DevTools, introduce `useMemo`/`useCallback` or state structure simplification.
- Failure Mode 2: Dynamic import chunk loading failure -> Action: Add Error Boundary wrapping lazy components, implement fallback retry logic.

## 7. Artifact Delivery & Output Standard
Production build dist directory, clean TypeScript build output, zero ESLint/React Hooks warnings, and Playwright test execution reports.
