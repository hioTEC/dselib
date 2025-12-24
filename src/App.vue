<template>
  <div class="flex min-h-screen bg-white dark:bg-black text-gray-800 dark:text-gray-100 font-sans antialiased selection:bg-black selection:text-white transition-colors duration-300">
    <!-- Sidebar -->
    <aside
      class="w-64 fixed inset-y-0 left-0 bg-white dark:bg-black border-r border-gray-100 dark:border-gray-800 overflow-y-auto z-50 scrollbar-thin transition-transform duration-300"
      :class="mobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'">
      <div class="p-6">
        <!-- Logo area -->
        <div class="flex justify-between items-center mb-8">
          <div class="font-bold text-2xl tracking-tighter cursor-pointer" @click="goHome">
            <span class="border-b-2 border-black dark:border-white">DSE</span> Lib
          </div>
          <!-- Close button for mobile -->
          <button 
            class="md:hidden text-gray-400 dark:text-gray-500 hover:text-black dark:hover:text-white"
            @click="mobileMenuOpen = false">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <!-- Subject Categories -->
        <div class="space-y-8">
          <template v-for="catKey in categoryOrder" :key="catKey">
            <div v-if="groupedSubjects[catKey] && groupedSubjects[catKey].length > 0">
              <h3 class="text-xs font-medium text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-3">
                {{ mapCategoryName(catKey) }}
              </h3>
              <ul class="space-y-1">
                <li v-for="sub in groupedSubjects[catKey]" :key="sub.key">
                  <div @click="selectSubject(sub)"
                    class="flex items-center gap-3 px-2 py-2 rounded-lg cursor-pointer transition-colors duration-200 group"
                    :class="currentSubject && currentSubject.key === sub.key 
                      ? 'bg-gray-100 dark:bg-gray-900 text-black dark:text-white font-semibold' 
                      : 'text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-900 hover:text-black dark:hover:text-white'">
                    <span class="material-symbols-rounded w-6 flex justify-center items-center transition-colors"
                      :class="currentSubject && currentSubject.key === sub.key 
                        ? 'text-black dark:text-white' 
                        : 'text-gray-400 dark:text-gray-500 group-hover:text-black dark:group-hover:text-white'">
                      {{ getMeta(sub.name).icon }}
                    </span>
                    <span class="text-sm">{{ getMeta(sub.name).zh }}</span>
                  </div>
                </li>
              </ul>
            </div>
          </template>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 md:ml-64 p-8 md:p-12 lg:p-16 relative">
      <!-- Mobile Toggle -->
      <button 
        class="md:hidden absolute top-4 left-4 p-2 text-gray-600 hover:text-black dark:hover:text-white"
        @click="mobileMenuOpen = !mobileMenuOpen">
        <i class="fas fa-bars text-xl"></i>
      </button>

      <!-- Theme Toggle -->
      <div class="absolute top-8 right-8 flex items-center gap-4">
        <button @click="toggleDarkMode"
          class="text-gray-400 dark:text-gray-500 hover:text-black dark:hover:text-white flex items-center transition">
          <span class="material-symbols-rounded text-lg">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</span>
        </button>
      </div>

      <!-- Content Area -->
      <div class="max-w-3xl mx-auto mt-8">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-20">
          <span class="material-symbols-rounded animate-spin text-4xl text-gray-300 dark:text-gray-600">
            progress_activity
          </span>
        </div>

        <!-- Error State -->
        <div v-if="error" class="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-lg mb-8 text-sm">
          {{ error }}
        </div>

        <!-- Home View -->
        <div v-if="!currentSubject && !loading">
          <header class="mb-12">
            <h1 class="text-3xl font-bold mb-4 tracking-tight">{{ uiText.title }}</h1>
            <p class="text-gray-400 dark:text-gray-500 text-sm">{{ uiText.disclaimer }}</p>
          </header>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="sub in displayList" :key="sub.key" @click="selectSubject(sub)"
              class="group border border-gray-100 dark:border-gray-800 rounded-xl p-6 hover:border-gray-300 dark:hover:border-gray-700 transition-all cursor-pointer bg-white dark:bg-gray-900 hover:shadow-sm">
              <div class="flex items-start justify-between mb-4">
                <div class="flex items-center gap-3">
                  <span class="material-symbols-rounded text-2xl text-gray-800 dark:text-gray-200">
                    {{ getMeta(sub.name).icon }}
                  </span>
                  <div>
                    <h3 class="font-bold text-lg">{{ getMeta(sub.name).en }}</h3>
                    <p class="text-xs text-gray-400 dark:text-gray-500">{{ getMeta(sub.name).zh }}</p>
                  </div>
                </div>
              </div>
              <div class="text-xs text-gray-400 dark:text-gray-500 font-mono">
                {{ getYearRange(sub) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Subject View -->
        <div v-if="currentSubject">
          <!-- Breadcrumb -->
          <div class="text-xs text-gray-400 dark:text-gray-500 mb-6 flex items-center gap-2">
            <span class="cursor-pointer hover:text-black dark:hover:text-white" @click="goHome">
              {{ uiText.all }}
            </span>
            <span class="material-symbols-rounded text-[16px] flex items-center">chevron_right</span>
            <span>{{ getMeta(currentSubject.name).displayKey || getMeta(currentSubject.name).en }}</span>
          </div>

          <!-- Header -->
          <header class="mb-16">
            <div class="flex justify-between items-start mb-4">
              <h1 class="text-4xl font-extrabold tracking-tight">
                {{ language === 'en' ? getMeta(currentSubject.name).en : getMeta(currentSubject.name).zh }}
              </h1>
            </div>
            <p class="text-gray-400 dark:text-gray-400 text-sm font-mono mb-6">
              {{ getYearRange(currentSubject) }}
            </p>

            <!-- Controls -->
            <div class="flex items-center gap-4 min-h-[32px]">
              <!-- Exam Type Buttons -->
              <div class="flex gap-2">
                <template v-for="exam in getAvailableExams(currentSubject)" :key="exam">
                  <button @click="switchExamType(exam)"
                    :class="examType === exam 
                      ? 'bg-gray-100 dark:bg-gray-700 text-black dark:text-white' 
                      : 'text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-black dark:hover:text-white'"
                    class="px-3 py-1 text-xs font-bold rounded transition">
                    {{ exam.toUpperCase() }}
                  </button>
                </template>
              </div>
              
              <!-- Language Toggle -->
              <div v-if="getAvailableLanguages(currentSubject).length > 1" class="flex items-center bg-gray-100 dark:bg-gray-800 rounded-lg p-1 transition-colors">
                <button @click="switchLanguage('zh')"
                  :class="language === 'zh' 
                    ? 'bg-white dark:bg-gray-700 text-black dark:text-white shadow-sm' 
                    : 'text-gray-500 dark:text-gray-400 hover:text-black dark:hover:text-white'"
                  class="px-3 py-1 text-xs font-semibold rounded-md transition">中</button>
                <button @click="switchLanguage('en')"
                  :class="language === 'en' 
                    ? 'bg-white dark:bg-gray-700 text-black dark:text-white shadow-sm' 
                    : 'text-gray-500 dark:text-gray-400 hover:text-black dark:hover:text-white'"
                  class="px-3 py-1 text-xs font-medium rounded-md transition">EN</button>
              </div>
              
              <!-- Placeholder -->
              <div v-else class="w-20 h-8"></div>
            </div>
          </header>

          <!-- File List -->
          <div class="space-y-2">
            <div v-for="yearData in sortedYears" :key="yearData.year"
              class="flex flex-col md:flex-row md:items-start gap-4 group w-full transition-colors rounded-lg p-2 border-b border-gray-50 dark:border-gray-800 last:border-0">
              <!-- Year Column -->
              <div class="w-24 md:w-32 font-mono font-bold text-sm md:text-base text-gray-800 dark:text-gray-200 shrink-0 whitespace-nowrap text-left flex items-center h-[29px]">
                {{ formatYearLabel(yearData.year) }}
              </div>

              <!-- Files Column -->
              <div class="flex-1 min-w-0">
                <div class="flex flex-wrap gap-3 items-center">
                  <a v-for="file in yearData.files" :key="file.path" 
                     :href="resolveFilePath(file.path)" target="_blank"
                    class="px-3 py-1.5 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 text-xs font-medium rounded text-gray-700 dark:text-gray-300 transition-colors whitespace-nowrap max-w-[100px] overflow-hidden text-ellipsis">
                    {{ getShortFileName(file.name) }}
                  </a>
                  
                  <!-- Download Button -->
                  <button
                    @click="downloadYear(yearData)"
                    :disabled="downloadingYear === yearData.year"
                    class="ml-auto py-1.5 px-3 bg-black dark:bg-gray-800 text-white text-xs font-bold rounded hover:bg-gray-800 dark:hover:bg-gray-700 transition flex items-center justify-center gap-1 disabled:opacity-50 min-w-[64px]">
                    <span class="material-symbols-rounded text-sm">download</span>
                    <span class="text-xs" v-if="downloadingYear === yearData.year">...</span>
                    <span class="text-xs" v-else>下载</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAppStore } from '@/stores/app'

const store = useAppStore()

// Store bindings
const {
  rawData,
  currentSubject,
  mobileMenuOpen,
  examType,
  language,
  isDarkMode,
  downloadingYear,
  loading,
  error,
  uiText,
  groupedSubjects,
  displayList,
  sortedYears,
  loadData,
  selectSubject,
  switchExamType,
  switchLanguage,
  goHome,
  toggleDarkMode,
  downloadYear,
  getMeta,
  mapCategoryName,
  getYearRange,
  getShortFileName,
  resolveFilePath,
  formatYearLabel,
  getAvailableExams,
  getAvailableLanguages,
  registerServiceWorker,
} = store

// Constants
const categoryOrder = ['Core', 'Science', 'Commerce', 'Arts', 'Others']

// Lifecycle
onMounted(() => {
  loadData()
  registerServiceWorker()
})
</script>

<style scoped>
/* Custom scrollbar for sidebar */
.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: #e5e7eb;
  border-radius: 20px;
}

.dark .scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: #374151;
}

/* Material Symbols styling */
.material-symbols-rounded {
  font-family: 'Material Symbols Rounded';
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  display: inline-block;
  line-height: 1;
  text-transform: none;
  letter-spacing: normal;
  word-wrap: normal;
  white-space: nowrap;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  -moz-osx-font-smoothing: grayscale;
  font-size: 20px;
}
</style>