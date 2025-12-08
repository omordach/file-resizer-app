# Implementation Plan: Frontend Library Upgrade

- [x] 1. Prepare for upgrade
  - Create a backup of current package.json and package-lock.json
  - Document current versions of all packages
  - Ensure git working directory is clean
  - _Requirements: 8.1_

- [x] 2. Upgrade React and React DOM
  - Update React to latest stable 18.x version in package.json (DO NOT use 19.x - security vulnerability)
  - Update React DOM to match React version
  - Run `npm install` to update package-lock.json
  - **Security Note**: React 19.0, 19.1.0, 19.1.1, 19.2.0 have known vulnerabilities - stay on 18.x
  - _Requirements: 1.1, 1.2, 1.5, 8.1_

- [x] 2.1 Validate React upgrade
  - Run `npm run build` to verify build succeeds
  - Check that React and React DOM versions match
  - Verify React version is 18.x (not 19.x)
  - _Requirements: 1.3, 1.2, 1.5_

- [ ]* 2.2 Run E2E tests after React upgrade
  - Execute `npx playwright test` to verify functionality
  - _Requirements: 7.3_

- [x] 3. Upgrade Vite and build tools
  - Update Vite to latest stable version (5.x or 6.x)
  - Update @vitejs/plugin-react to compatible version
  - Review Vite changelog for breaking changes
  - Update vite.config.js if necessary
  - Run `npm install` to update package-lock.json
  - _Requirements: 2.1, 2.2, 8.1_

- [x] 3.1 Validate Vite upgrade
  - Run `npm run build` to verify production build succeeds
  - Start dev server with `npm run dev` and verify it runs without errors
  - _Requirements: 2.3, 2.4_

- [ ]* 3.2 Run E2E tests after Vite upgrade
  - Execute `npx playwright test` to verify functionality
  - _Requirements: 7.3_

- [x] 4. Upgrade TailwindCSS and styling dependencies (in docker)
  - Update TailwindCSS to latest stable version
  - Update PostCSS to compatible version
  - Update Autoprefixer to compatible version
  - Update tailwindcss-animate to latest version
  - Run `npm install` to update package-lock.json
  - _Requirements: 3.1, 3.2, 3.3, 5.7, 8.1_

- [x] 4.1 Validate TailwindCSS upgrade (in docker)
  - Run `npm run build` to verify build succeeds
  - Visually inspect the application to verify styling renders correctly
  - _Requirements: 7.1_

- [ ]* 4.2 Run E2E tests after TailwindCSS upgrade
  - Execute `npx playwright test` to verify functionality
  - _Requirements: 7.3_

- [x] 5. Upgrade Radix UI components (in docker)
  - Update @radix-ui/react-label to latest stable version
  - Update @radix-ui/react-select to latest stable version
  - Update @radix-ui/react-slot to latest stable version
  - Run `npm install` to update package-lock.json
  - _Requirements: 4.1, 4.2, 4.3, 8.1_

- [x] 5.1 Validate Radix UI upgrade (in docker)
  - Run `npm run build` to verify build succeeds
  - Manually test UI components (select dropdown, labels)
  - _Requirements: 7.1_

- [ ]* 5.2 Run E2E tests after Radix UI upgrade
  - Execute `npx playwright test` to verify functionality
  - _Requirements: 7.3_

- [x] 6. Upgrade utility and feature libraries (in docker)
  - Update lucide-react to latest stable version
  - Update react-dropzone to latest stable version
  - Update react-google-recaptcha to latest stable version
  - Update class-variance-authority to latest stable version
  - Update clsx to latest stable version
  - Update tailwind-merge to latest stable version
  - Run `npm install` to update package-lock.json
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 8.1_

- [x] 6.1 Validate utility library upgrades (in docker)
  - Run `npm run build` to verify build succeeds
  - Test file upload via drag-and-drop
  - Verify icons render correctly
  - _Requirements: 7.1, 7.4_

- [ ]* 6.2 Run E2E tests after utility upgrades
  - Execute `npx playwright test` to verify functionality
  - _Requirements: 7.3_

- [x] 7. Upgrade Playwright testing framework (in docker)
  - Update @playwright/test to latest stable version
  - Run `npm install` to update package-lock.json
  - Run `npx playwright install` to update browser binaries
  - _Requirements: 6.1, 8.1_

- [x] 7.1 Validate Playwright upgrade
  - Execute `npx playwright test` to verify all tests pass
  - _Requirements: 6.2, 7.3_

- [x] 8. Final validation and verification (in docker)
  - Run `npm run build` to ensure clean production build
  - Start dev server and perform manual testing checklist
  - Verify file upload and processing workflow
  - Verify reCAPTCHA integration works
  - Check browser console for any errors or warnings
  - _Requirements: 7.1, 7.2, 7.4, 7.5_

- [ ]* 8.1 Write validation script for peer dependencies
  - **Property 1: Version synchronization for coupled packages**
  - Create script to verify peer dependency requirements are satisfied
  - **Validates: Requirements 1.2, 2.2, 3.2, 3.3**

- [x] 9. Update documentation
  - Update tech.md steering file with new version numbers
  - Update README.md if it contains version information
  - Commit all changes with descriptive message
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
