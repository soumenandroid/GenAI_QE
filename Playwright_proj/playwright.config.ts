import { defineConfig, devices, PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
  testMatch: ["tests/mcp_server.ts"],
  timeout: 120_000,
  use: {
    headless: false,
    screenshot: "only-on-failure",
    video: "on"
  },
  reporter: [['html', {
    open: "always"
  }]],
}

export default config