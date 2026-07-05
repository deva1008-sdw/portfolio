# Nexalith Prime — Technical Documentation
*Futuristic Corporate Portal & Security Agency Showcase*

This document provides a comprehensive technical overview of the **Nexalith Prime** corporate portal located at `D:/projects/RoBlockSec`.

---

## 1. Executive Summary
**Nexalith Prime** is a commercial portal designed for a cybersecurity agency (RoBlockSec). Built using React, Vite, and TailwindCSS, it displays interactive service descriptions (GRC, Red Teaming, Pen testing), careers portals, and downloadable product details. It features page transitions (Framer Motion), interactive particle backgrounds (tsparticles), and SEO-optimized routing (React Helmet Async).

---

## 2. Directory Layout & Key Modules

* **`src/pages/`**: Includes sections for:
  * `HomePage.tsx`: General landing with service showcases and call-to-actions.
  * `ServicesPage.tsx`: Breakdown of Red Teaming, SOC monitoring, and GRC consulting.
  * `ProductsPage.tsx`: Downloadable technical whitepapers and specifications.
  * `CareersPage.tsx`: Active jobs (SOC Analyst, Pentester) and application portals.
  * `TeamPage.tsx`, `AboutPage.tsx`, `BlogPage.tsx`: Administrative profiles and research.
* **`src/components/`**: Custom reusable UI components, headers, footers, and cards.
* **`src/constants/`**: Hardcoded texts and lists.

---

## 3. Frontend Technology & Libraries

* **Framework**: React 18, Vite.
* **Visual Styling**: TailwindCSS (responsive layouts, custom dark backgrounds).
* **Animations**: Framer Motion (fade-ins, scroll-triggered card translations).
* **Interactive Backdrop**: `tsparticles` (custom floating network nodes and nodes-linking lines).
* **SEO Metadata**: `react-helmet-async` (injects custom page meta headers dynamically for search indexers).
* **Routing**: React Router DOM (client-side routing).

---

## 4. How to Run the Application

To install dependencies and start the local development server:

### Step 1: Install Node Dependencies
1. Navigate to the project folder:
   ```bash
   cd D:/projects/RoBlockSec
   ```
2. Install npm packages:
   ```bash
   npm install
   ```

### Step 2: Start Vite Dev Server
1. Launch the server:
   ```bash
   npm run dev
   ```
2. Open the page:
   * **Local Address**: [http://localhost:5173](http://localhost:5173)

### Step 3: Build for Production
To generate a static distribution folder:
```bash
npm run build
```
*Creates a `dist/` directory ready for deployment on Netlify, Vercel, or AWS S3.*
