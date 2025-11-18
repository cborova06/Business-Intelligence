import { createResource } from 'frappe-ui'
import type { App } from 'vue'

function getTranslatedMessage(message: string): string {
	const translatedMessages = ((
		'translatedMessages' in window ? (window as any)['translatedMessages'] : null
	) ?? {}) as Record<string, string>
	return translatedMessages[message] || message
}

function translate(message: string): string
function translate(message: string, ...args: (string | number)[]): string
function translate(message: string, ...args: (string | number)[]): string {
	const translatedMessage = getTranslatedMessage(message)
	if (!args.length) {
		return translatedMessage
	}
	return translatedMessage.replace(/\{(\d+)\}/g, (match, index) => {
		return typeof args[index] !== 'undefined' ? String(args[index]) : match
	})
}

export const __ = translate

function fetchTranslations() {
	createResource({
		url: 'insights.api.general.get_translations',
		method: 'GET',
		cache: 'insights_translations',
		auto: true,
		transform(data: Record<string, string>) {
			;(window as any).translatedMessages = data
		},
	})
}

export function translationPlugin(app: App<Element>) {
	app.config.globalProperties.__ = translate
	const win = window as any
	win.__ = translate
	if (!win.translatedMessages) {
		fetchTranslations()
	}
}

declare module '@vue/runtime-core' {
	interface ComponentCustomProperties {
		__ : typeof translate
	}
}

