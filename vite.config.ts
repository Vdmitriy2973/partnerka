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

          // index.html
          home: join(INPUT_DIR, "/js/main/index.js"),

          // Рекламодатель
          adv_dashboard: join(INPUT_DIR, "/js/dashboard/advertiser/dashboard/dashboard.js"),
          adv_partners: join(INPUT_DIR, "/js/dashboard/advertiser/partners/partners.js"),
          adv_projects: join(INPUT_DIR, "/js/dashboard/advertiser/projects/projects.js"),
          adv_requisites: join(INPUT_DIR, "/js/dashboard/advertiser/requisites/requisites.js"),
          adv_sales: join(INPUT_DIR, "/js/dashboard/advertiser/sales/sales.js"),
          adv_settings: join(INPUT_DIR, "/js/dashboard/advertiser/settings/settings.js"),

          // Партнёр
          partner_dashboard: join(INPUT_DIR, "/js/dashboard/partner/dashboard/dashboard.js"),
          partner_offers: join(INPUT_DIR, "/js/dashboard/partner/offers/offers.js"),
          partner_connections: join(INPUT_DIR, "/js/dashboard/partner/connections/connections.js"),
          partner_notifications: join(INPUT_DIR,"/js/dashboard/partner/notifications/notifications.js"),
          partner_platforms: join(INPUT_DIR, "/js/dashboard/partner/platforms/platforms.js"),
          partner_links: join(INPUT_DIR, "/js/dashboard/partner/links/links.js"),
          partner_payments: join(INPUT_DIR, "/js/dashboard/partner/payments/payments.js"),
          partner_settings: join(INPUT_DIR, "/js/dashboard/partner/settings/settings.js"),

          // Менеджер
          manager_dashboard: join(INPUT_DIR, "/js/dashboard/manager/dashboard/dashboard.js"),
          manager_projects: join(INPUT_DIR, "/js/dashboard/manager/projects/projects.js"),
          manager_platforms: join(INPUT_DIR, "/js/dashboard/manager/platforms/platforms.js"),
          manager_users: join(INPUT_DIR, "/js/dashboard/manager/users/users.js"),
          manager_partners: join(INPUT_DIR, "/js/dashboard/manager/partners/partners.js"),
          manager_advertisers: join(INPUT_DIR, "/js/dashboard/manager/advertisers/advertisers.js")
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
