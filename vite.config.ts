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
          manager: join(INPUT_DIR, "/js/dashboard/manager.js"),

          // Рекламодатель
          adv_dashboard: join(INPUT_DIR, "/js/dashboard/advertiser/dashboard/dashboard.js"),
          adv_partners: join(INPUT_DIR, "/js/dashboard/advertiser/dashboard/partners.js"),
          adv_projects: join(INPUT_DIR, "/js/dashboard/advertiser/projects/projects.js"),
          adv_requisites: join(INPUT_DIR, "/js/dashboard/advertiser/requisites/requisites.js"),
          adv_sales: join(INPUT_DIR, "/js/dashboard/advertiser/sales/sales.js"),
          adv_settings: join(INPUT_DIR, "/js/dashboard/advertiser/settings/settings.js"),

          // Партнёр


          // Менеджер


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
