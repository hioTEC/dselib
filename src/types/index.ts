// Subject and exam types
export interface SubjectMeta {
  zh: string
  en: string
  displayKey?: string
  category: 'Core' | 'Science' | 'Commerce' | 'Arts' | 'Technology' | 'Others'
  icon: string
}

export interface ExamFile {
  name: string
  path: string
  type?: 'paper' | 'marking' | 'report' | 'audio'
  year?: string
}

export interface YearData {
  display: string
  languages: Record<string, {
    files: ExamFile[]
  }>
}

export interface ExamData {
  years: Record<string, YearData>
}

export interface Subject {
  key: string
  name: string
  exams?: Record<string, ExamData>
  files?: ExamFile[]
  years_summary?: Record<string, {
    min: number
    max: number
  }>
}

// UI State types
export interface UIState {
  isDarkMode: boolean
  language: 'zh' | 'en'
  currentSubject: Subject | null
  examType: 'dse' | 'ce' | 'al'
  mobileMenuOpen: boolean
  loading: boolean
  error: string | null
  downloadingYear: string | null
}

// Component Props types
export interface SubjectCardProps {
  subject: Subject
  isActive: boolean
  onClick: () => void
}

export interface FileListProps {
  subject: Subject
  examType: string
  language: string
  files: ExamFile[]
  downloadingYear: string | null
  onDownload: (yearData: { year: string; files: ExamFile[] }) => void
}

// API Response types
export interface IndexData {
  subjects: Subject[]
}

// Configuration types
export interface AppConfig {
  categoryOrder: string[]
  examTypes: string[]
  languages: string[]
  subjectMeta: Record<string, SubjectMeta>
  categoryMap: Record<string, string>
  orderConfig: Record<string, string[]>
}