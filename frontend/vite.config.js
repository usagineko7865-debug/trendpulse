import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  // GitHub Pagesはプロジェクトページとして /trendpulse/ 配下で配信されるため、
  // 本番ビルド時だけベースパスを合わせる（ローカルdevは"/"のまま）。
  base: process.env.GH_PAGES ? "/trendpulse/" : "/",
  server: {
    port: 5173,
  },
});
