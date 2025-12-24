/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Global type definitions
declare global {
  interface Window {
    JSZip: any
    saveAs: any
  }
}

export {}