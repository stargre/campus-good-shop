import { BASE_URL, SERVER_ORIGIN } from '/@/store/constants'

export function getImageUrl(s: string | undefined | null): string {
  if (!s) return ''
  const path = String(s)
  if (/^https?:\/\//.test(path)) return path
  if (path.startsWith('/upload/') || path.startsWith('upload/')) {
    const p = path.startsWith('/') ? path : `/${path}`
    return `${SERVER_ORIGIN}${p}`
  }
  const p = path.startsWith('/') ? path : `/${path}`
  return `${BASE_URL}${p}`
}
