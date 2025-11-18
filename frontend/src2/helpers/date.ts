declare const window: any

export function formatTimeAgo(date: string | Date | null | undefined): string {
	if (!date) return ''

	const frappe = window?.frappe

	// Prefer Frappe's prettyDate, which is already localized via __()
	if (frappe?.datetime?.prettyDate) {
		return frappe.datetime.prettyDate(date)
	}

	// Fallback: simple Turkish human‑friendly formatting
	const d = typeof date === 'string' ? new Date(date) : date
	if (isNaN(d.getTime())) return ''

	const diffMs = Date.now() - d.getTime()
	const diffSec = Math.round(diffMs / 1000)
	const diffMin = Math.round(diffSec / 60)
	const diffHr = Math.round(diffMin / 60)
	const diffDay = Math.round(diffHr / 24)

	if (diffSec < 45) return 'az önce'
	if (diffMin < 2) return '1 dakika önce'
	if (diffMin < 45) return `${diffMin} dakika önce`
	if (diffHr < 2) return '1 saat önce'
	if (diffHr < 24) return `${diffHr} saat önce`
	if (diffDay < 2) return 'dün'
	if (diffDay < 30) return `${diffDay} gün önce`

	const diffMonth = Math.round(diffDay / 30)
	if (diffMonth < 2) return '1 ay önce'
	if (diffMonth < 12) return `${diffMonth} ay önce`

	const diffYear = Math.round(diffMonth / 12)
	if (diffYear < 2) return '1 yıl önce'
	return `${diffYear} yıl önce`
}
