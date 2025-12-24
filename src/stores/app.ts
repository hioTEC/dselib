import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Subject, UIState, SubjectMeta } from '@/types'

// Constants matching the original configuration
const SUBJECT_META: Record<string, SubjectMeta> = {
  'Chinese History': { zh: '中國歷史', en: 'Chinese History', displayKey: 'chi_hist', category: 'Arts', icon: 'temple_buddhist' },
  'Chinese': { zh: '中文', en: 'Chinese', displayKey: 'chi', category: 'Core', icon: 'history_edu' },
  'English': { zh: '英文', en: 'English', displayKey: 'eng', category: 'Core', icon: 'translate' },
  'Mathematics M1': { zh: '微積分與統計 (M1)', en: 'Maths (M1)', displayKey: 'm1', category: 'Science', icon: 'pie_chart' },
  'Mathematics M2': { zh: '代數與微積分 (M2)', en: 'Maths (M2)', displayKey: 'm2', category: 'Science', icon: 'functions' },
  'Mathematics': { zh: '數學', en: 'Mathematics', displayKey: 'm0', category: 'Core', icon: 'calculate' },
  'Citizenship': { zh: '公民與社會發展', en: 'Citizenship', displayKey: 'cs', category: 'Core', icon: 'public' },
  'Liberal Studies': { zh: '通識教育', en: 'Liberal Studies', displayKey: 'ls', category: 'Arts', icon: 'newspaper' },
  'Physics': { zh: '物理', en: 'Physics', displayKey: 'phy', category: 'Science', icon: 'electric_bolt' },
  'Chemistry': { zh: '化學', en: 'Chemistry', displayKey: 'chem', category: 'Science', icon: 'science' },
  'Biology': { zh: '生物', en: 'Biology', displayKey: 'bio', category: 'Science', icon: 'biotech' },
  'ICT': { zh: '資訊及通訊科技', en: 'ICT', displayKey: 'ict', category: 'Science', icon: 'computer' },
  'BAFS': { zh: '企業、會計與財務概論', en: 'BAFS', displayKey: 'bafs', category: 'Commerce', icon: 'business_center' },
  'Economics': { zh: '經濟', en: 'Economics', displayKey: 'econ', category: 'Commerce', icon: 'trending_up' },
  'History': { zh: '世界歷史', en: 'History', displayKey: 'hist', category: 'Arts', icon: 'public' },
  'Geography': { zh: '地理', en: 'Geography', displayKey: 'geog', category: 'Arts', icon: 'landscape' },
  'Tourism': { zh: '旅遊與款待', en: 'Tourism', displayKey: 'tourism', category: 'Arts', icon: 'flight_takeoff' }
}

const CATEGORY_MAP: Record<string, string> = {
  'Core': '必修',
  'Science': '理科',
  'Commerce': '商科',
  'Arts': '文科',
  'Technology': '科技',
  'Others': '其他'
}

const ORDER_CONFIG: Record<string, string[]> = {
  'Core': ['Chinese', 'English', 'Mathematics', 'Citizenship'],
  'Science': ['Physics', 'Chemistry', 'Biology', 'Mathematics M1', 'Mathematics M2', 'ICT'],
  'Commerce': ['Economics', 'BAFS'],
  'Arts': ['History', 'Chinese History', 'Tourism', 'Geography', 'Liberal Studies']
}

const CATEGORY_ORDER = ['Core', 'Science', 'Commerce', 'Arts', 'Others']

export const useAppStore = defineStore('app', () => {
  // State
  const rawData = ref<Subject[]>([])
  const currentSubject = ref<Subject | null>(null)
  const mobileMenuOpen = ref(false)
  const examType = ref<'dse' | 'ce' | 'al'>('dse')
  const language = ref<'zh' | 'en'>('zh')
  const isDarkMode = ref(false)
  const downloadingYear = ref<string | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)
  const isSwitching = ref(false)

  // Computed
  const uiText = computed(() => {
    const texts = {
      zh: {
        title: '过往试卷',
        disclaimer: '本網站為學習資源交流平台，只作為學習用途，而非商業用途。若上載之內容涉及版權，請即與我們聯絡。',
        all: '全部'
      },
      en: {
        title: 'Past Papers',
        disclaimer: 'This website is a learning resource exchange platform for educational purposes only, not for commercial use. Please contact us immediately if uploaded content involves copyright issues.',
        all: 'All'
      }
    }
    return texts[language.value] || texts.zh
  })

  const groupedSubjects = computed(() => {
    const groups: Record<string, Subject[]> = {
      'Core': [], 'Science': [], 'Commerce': [], 'Arts': [], 'Others': []
    }

    const getKey = (name: string) => {
      for (const k in SUBJECT_META) {
        if (name === k || name.includes(k)) return k
      }
      return 'Other'
    }

    rawData.value.forEach(sub => {
      const meta = getMeta(sub.name)
      const cat = meta.category || 'Others'
      if (!groups[cat]) groups[cat] = []
      groups[cat].push(sub)
    })

    // Sort items within groups
    Object.keys(ORDER_CONFIG).forEach(cat => {
      if (groups[cat]) {
        const orderList = ORDER_CONFIG[cat]
        groups[cat].sort((a, b) => {
          const keyA = getKey(a.name)
          const keyB = getKey(b.name)
          const idxA = orderList.indexOf(keyA)
          const idxB = orderList.indexOf(keyB)
          return (idxA === -1 ? 999 : idxA) - (idxB === -1 ? 999 : idxB)
        })
      }
    })

    return groups
  })

  const displayList = computed(() => {
    let list: Subject[] = []
    CATEGORY_ORDER.forEach(cat => {
      if (groupedSubjects.value[cat]) {
        list = list.concat(groupedSubjects.value[cat])
      }
    })
    return list
  })

  const sortedYears = computed(() => {
    if (!currentSubject.value) return []

    const yearsMap: Record<string, any[]> = {}
    const targetLang = language.value === 'zh' ? 'chi' : 'eng'

    // Use structured 'exams' data
    if (currentSubject.value.exams) {
      const examData = currentSubject.value.exams[examType.value]
      if (examData && examData.years) {
        Object.values(examData.years).forEach(yearData => {
          const y = yearData.display
          let langData = null

          // Try target language first
          if (yearData.languages && yearData.languages[targetLang]) {
            langData = yearData.languages[targetLang]
          }
          // Fallback: If only one language available
          else if (yearData.languages && Object.keys(yearData.languages).length > 0) {
            const availableLangs = Object.keys(yearData.languages)
            if (availableLangs.length === 1) {
              langData = yearData.languages[availableLangs[0]]
            }
          }

          if (langData && langData.files) {
            if (!yearsMap[y]) yearsMap[y] = []
            langData.files.forEach((f: any) => {
              yearsMap[y].push({ ...f, year: y })
            })
          }
        })
      }
    }
    // Fallback for flat 'files' array
    else if (currentSubject.value.files) {
      currentSubject.value.files.forEach(f => {
        const path = (f.path || '').toLowerCase()
        if (!path.includes(`/${examType.value}/`)) return
        if (!path.includes(`/${targetLang}/`)) return

        const y = f.year || 'Unknown'
        if (!yearsMap[y]) yearsMap[y] = []
        yearsMap[y].push(f)
      })
    }

    // Sort years
    const sortedKeys = Object.keys(yearsMap).sort((a, b) => {
      const isSpecial = (y: string) => {
        const ly = y.toLowerCase()
        return ly.includes('sp') || ly.includes('pp') || ly.includes('sample') || ly.includes('practice')
      }
      const aSpecial = isSpecial(a)
      const bSpecial = isSpecial(b)
      
      if (aSpecial && !bSpecial) return 1
      if (!aSpecial && bSpecial) return -1
      if (aSpecial && bSpecial) return b.localeCompare(a)
      
      return b.localeCompare(a)
    })

    return sortedKeys.map(y => ({
      year: y,
      files: yearsMap[y].sort((a, b) => {
        const wA = fileWeight(a)
        const wB = fileWeight(b)
        if (wA !== wB) return wA - wB
        return a.name.toLowerCase().localeCompare(b.name.toLowerCase())
      })
    }))
  })

  // Actions
  async function loadData() {
    loading.value = true
    error.value = null

    const protocol = window.location.protocol
    if (protocol === 'file:') {
      error.value = "本页面以文件方式打开（file://），浏览器会拦截数据读取。请用本地 HTTP 服务访问：\npython -m http.server -d frontend 8000\n然后打开：http://localhost:8000/"
      loading.value = false
      return
    }

    const url = './public/data/index.json'

    try {
      const res = await fetch(url, { cache: 'no-store' })
      if (!res.ok) {
        throw new Error(`Failed to load index.json (HTTP ${res.status})`)
      }

      const data = await res.json()
      if (!data || !Array.isArray(data.subjects)) {
        throw new Error('index.json schema mismatch: expected { subjects: [] }')
      }

      rawData.value = data.subjects
    } catch (e: any) {
      error.value = `Failed to fetch index.json: ${e?.message || e}`
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  function selectSubject(sub: Subject) {
    currentSubject.value = sub
    mobileMenuOpen.value = false
    examType.value = 'dse'
    language.value = 'zh'
    window.scrollTo(0, 0)
  }

  async function switchExamType(exam: 'dse' | 'ce' | 'al') {
    if (examType.value === exam || isSwitching.value) return
    
    isSwitching.value = true
    const contentArea = document.querySelector('main > div')
    if (contentArea) {
      contentArea.setAttribute('style', 'background-color: #ffffff')
      setTimeout(() => {
        examType.value = exam
        setTimeout(() => {
          contentArea.removeAttribute('style')
          isSwitching.value = false
        }, 150)
      }, 150)
    } else {
      examType.value = exam
      isSwitching.value = false
    }
  }

  async function switchLanguage(lang: 'zh' | 'en') {
    if (language.value === lang || isSwitching.value) return
    
    isSwitching.value = true
    const contentArea = document.querySelector('main > div')
    if (contentArea) {
      contentArea.setAttribute('style', 'background-color: #ffffff')
      setTimeout(() => {
        language.value = lang
        setTimeout(() => {
          contentArea.removeAttribute('style')
          isSwitching.value = false
        }, 150)
      }, 150)
    } else {
      language.value = lang
      isSwitching.value = false
    }
  }

  function goHome() {
    currentSubject.value = null
    mobileMenuOpen.value = false
  }

  function toggleDarkMode() {
    isDarkMode.value = !isDarkMode.value
    if (isDarkMode.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Helper functions
  function getMeta(name: string): SubjectMeta {
    if (SUBJECT_META[name]) {
      return SUBJECT_META[name]
    }
    
    for (const key in SUBJECT_META) {
      if (name === key ||
          (name.includes(key) && (key.length >= name.length * 0.6 || name.includes(key + ' ') || name.includes(' ' + key)))) {
        return SUBJECT_META[key]
      }
    }
    return { zh: name, en: name, category: 'Others', icon: 'folder' }
  }

  function mapCategoryName(cat: string): string {
    return CATEGORY_MAP[cat] || cat
  }

  function getYearRange(sub: Subject): string {
    if (sub.years_summary && sub.years_summary.dse) {
      return `${sub.years_summary.dse.min}-${sub.years_summary.dse.max}`
    }
    if (sub.years_summary && sub.years_summary.ce) {
      return `${sub.years_summary.ce.min}-${sub.years_summary.ce.max}`
    }
    return '1980-2025'
  }

  function fileWeight(file: any): number {
    const name = (file.name || '').toLowerCase()
    if (name.includes('p1a')) return 10
    if (name.includes('p1b')) return 20
    if (name.includes('p1')) return 30
    if (name.includes('p2')) return 40
    if (name.includes('p3')) return 50
    if (name.includes('p4')) return 60
    if (name.includes('p5')) return 70
    if (name.includes('ans') || file.type === 'marking') return 80
    if (name.includes('per') || file.type === 'report') return 90
    return 999
  }

  function getShortFileName(name: string): string {
    if (!name) return ''
    const n = name.toLowerCase()
    
    // HYC Mock paper handling
    if (n.includes('mock ms1')) return 'ans1'
    if (n.includes('mock ms2')) return 'ans2'
    if (n.includes('mock ms')) return 'ans'
    if (n.includes('mock p1')) return 'p1'
    if (n.includes('mock p2')) return 'p2'
    if (n.includes('mock p3')) return 'p3'
    
    if (n.includes("paper 1")) return "p1"
    if (n.includes("paper 2")) return "p2"
    if (n.includes("paper 3")) return "p3"
    
    // Remove common prefixes
    const parts = name.split('_')
    let cleanName = parts[parts.length - 1]
    
    // Remove extension
    if (cleanName.toLowerCase().endsWith('.pdf')) {
      cleanName = cleanName.substring(0, cleanName.length - 4)
    }
    return cleanName
  }

  function resolveFilePath(p: string): string {
    if (!p) return '/#'
    return p.startsWith('/') ? p : '/' + p
  }

  function formatYearLabel(year: string): string {
    if (year && year.toLowerCase().includes('sample')) {
      return 'SP'
    }
    if (year && year.toLowerCase().includes('practice')) {
      return 'PP'
    }
    return year
  }

  async function downloadYear(yearData: { year: string; files: any[] }) {
    if (!window.JSZip || !window.saveAs) {
      alert('JSZip/FileSaver 未加载，无法打包下载')
      return
    }
    
    downloadingYear.value = yearData.year
    try {
      const zip = new window.JSZip()
      for (const file of yearData.files) {
        const url = resolveFilePath(file.path)
        try {
          const res = await fetch(url)
          if (!res.ok) continue
          const blob = await res.blob()
          zip.file(file.name, blob)
        } catch (e) {
          console.warn('download skip', url, e)
        }
      }
      const content = await zip.generateAsync({ type: 'blob' })
      const subjKey = (currentSubject.value && currentSubject.value.key) || 'papers'
      window.saveAs(content, `${subjKey}_${yearData.year}.zip`)
    } catch (e) {
      alert('打包下载失败，请稍后重试')
      console.error(e)
    } finally {
      downloadingYear.value = null
    }
  }

  function getAvailableExams(subject: Subject): string[] {
    if (!subject) return ['dse', 'ce', 'al']

    const available: string[] = []
    const allExams = subject.exams ? Object.keys(subject.exams) : ['dse', 'ce', 'al']

    if (subject.exams) {
      allExams.forEach(exam => {
        if (subject.exams![exam] && subject.exams![exam].years) {
          const hasFiles = Object.values(subject.exams![exam].years).some(yearData => {
            if (yearData.languages) {
              return Object.values(yearData.languages).some(langData => {
                return langData.files && langData.files.length > 0
              })
            }
            return false
          })
          if (hasFiles) available.push(exam)
        }
      })
    } else if (subject.files) {
      allExams.forEach(exam => {
        const hasFiles = subject.files!.some(f => {
          const path = (f.path || '').toLowerCase()
          return path.includes(`/${exam}/`)
        })
        if (hasFiles) available.push(exam)
      })
    }
    
    return available.length > 0 ? available : ['dse', 'ce', 'al']
  }

  function getAvailableLanguages(subject: Subject): string[] {
    if (!subject) return ['zh', 'en']
    
    const available: string[] = []
    const allLangs = ['chi', 'eng']
    
    if (subject.exams) {
      const examData = subject.exams[examType.value]
      if (examData && examData.years) {
        allLangs.forEach(lang => {
          const hasFiles = Object.values(examData.years).some(yearData => {
            if (yearData.languages && yearData.languages[lang]) {
              return yearData.languages[lang].files && yearData.languages[lang].files.length > 0
            }
            return false
          })
          if (hasFiles) available.push(lang)
        })
      }
    } else if (subject.files) {
      allLangs.forEach(lang => {
        const hasFiles = subject.files!.some(f => {
          const path = (f.path || '').toLowerCase()
          return path.includes(`/${lang}/`)
        })
        if (hasFiles) available.push(lang)
      })
    }
    
    return available.length > 0 ? available : ['chi', 'eng']
  }

  function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js')
        .then(function(registration) {
          console.log('ServiceWorker registration successful')
        })
        .catch(function(err) {
          console.log('ServiceWorker registration failed')
        })
    }
  }

  return {
    // State
    rawData,
    currentSubject,
    mobileMenuOpen,
    examType,
    language,
    isDarkMode,
    downloadingYear,
    loading,
    error,
    isSwitching,
    
    // Computed
    uiText,
    groupedSubjects,
    displayList,
    sortedYears,
    
    // Actions
    loadData,
    selectSubject,
    switchExamType,
    switchLanguage,
    goHome,
    toggleDarkMode,
    downloadYear,
    
    // Helper functions
    getMeta,
    mapCategoryName,
    getYearRange,
    getShortFileName,
    resolveFilePath,
    formatYearLabel,
    getAvailableExams,
    getAvailableLanguages,
    registerServiceWorker,
  }
})