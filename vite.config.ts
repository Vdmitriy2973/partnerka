import { defineConfig, loadEnv } from "vite";
import { resolve, join } from "path";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig((mode) => {
  const env = loadEnv(mode, process.cwd(), "");

  const CORE_INPUT_DIR = "./apps/core/assets/js";
  const ADVERTISERS_INPUT_DIR = "./apps/advertisers/assets/js";
  const PARTNERS_INPUT_DIR = "./apps/partners/assets/js";
  const MANAGERS_INPUT_DIR = "./apps/managers/assets/js"

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
          home: join(CORE_INPUT_DIR, "/main/index.js"),
          auth: join(CORE_INPUT_DIR,'/auth/auth.js'),

          // Рекламодатель
          advertiser_dashboard: join(ADVERTISERS_INPUT_DIR, "/dashboard/dashboard.js"),
          advertiser_partners: join(ADVERTISERS_INPUT_DIR, "/partners/partners.js"),
          advertiser_projects: join(ADVERTISERS_INPUT_DIR, "/projects/projects.js"),
          advertiser_requisites: join(ADVERTISERS_INPUT_DIR, "/requisites/requisites.js"),
          advertiser_sales: join(ADVERTISERS_INPUT_DIR, "/sales/sales.js"),
          advertiser_notifications: join(ADVERTISERS_INPUT_DIR, "/notifications/notifications.js"),
          advertiser_settings: join(ADVERTISERS_INPUT_DIR, "/settings/settings.js"),

          // Партнёр
          partner_dashboard: join(PARTNERS_INPUT_DIR, "/dashboard/dashboard.js"),
          partner_stats:join(PARTNERS_INPUT_DIR,'/stats/stats.js'),
          partner_offers: join(PARTNERS_INPUT_DIR, "/offers/offers.js"),
          partner_connections: join(PARTNERS_INPUT_DIR, "/connections/connections.js"),
          partner_notifications: join(PARTNERS_INPUT_DIR, "/notifications/notifications.js"),
          partner_platforms: join(PARTNERS_INPUT_DIR, "/platforms/platforms.js"),
          partner_links: join(PARTNERS_INPUT_DIR, "/links/links.js"),
          partner_payments: join(PARTNERS_INPUT_DIR, "/payments/payments.js"),
          partner_settings: join(PARTNERS_INPUT_DIR, "/settings/settings.js"),

          // Менеджер
          manager_dashboard: join(MANAGERS_INPUT_DIR, "/dashboard/dashboard.js"),
          manager_projects: join(MANAGERS_INPUT_DIR, "/projects/projects.js"),
          manager_platforms: join(MANAGERS_INPUT_DIR, "/platforms/platforms.js"),
          manager_users: join(MANAGERS_INPUT_DIR, "/users/users.js"),
          manager_partners: join(MANAGERS_INPUT_DIR, "/partners/partners.js"),
          manager_advertisers: join(MANAGERS_INPUT_DIR, "/advertisers/advertisers.js"),
          manager_reviews:join(MANAGERS_INPUT_DIR,"/reviews/reviews.js"),

          // Статические страницы
          static_page_core_app: join(CORE_INPUT_DIR, "/static-pages/static_page.js"),
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
