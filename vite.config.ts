import { defineConfig, loadEnv } from "vite";
import { resolve, join } from "path";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig((mode) => {
  const env = loadEnv(mode, process.cwd(), "");

  const INPUT_DIR = "./partner_app/assets";
  const OUTPUT_DIR = "./static";

  return {
    base: "/static/",
    build: {
      outDir: resolve(OUTPUT_DIR),
      assetsDir: "",
      manifest: 'manifest.json',
      emptyOutDir: true,
      rollupOptions: {
        input: {
          home: join(INPUT_DIR, "/js/index.js"),
          partner: join(INPUT_DIR, "/js/dashboard/partner.js"),
          advertiser: join(INPUT_DIR, "/js/dashboard/advertiser.js"),
          manager: join(INPUT_DIR, "/js/dashboard/manager.js"),
          tracker:join(INPUT_DIR,"./tracker.js")
        },
      },
    },
    resolve: {
    },
    server: {
    },
    plugins: [tailwindcss()],
  };
});
