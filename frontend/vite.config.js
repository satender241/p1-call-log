// Vite is the tool that runs the page on your laptop (npm run dev)
// and packs it into plain files for Vercel (npm run build).
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
});
