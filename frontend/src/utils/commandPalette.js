import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { __ } from "@/translation";
const commandPalette = reactive({
	isOpen: false,
	commands: [],
	open,
	close,
	search,
})

function open() {
	commandPalette.isOpen = true
}
function close() {
	commandPalette.isOpen = false
}
function search(searchTerm) {
	return commandPalette.commands.filter((command) => {
		return command.title.toLowerCase().includes(searchTerm.toLowerCase())
	})
}

function initNavigationCommands(commandPalette) {
	const router = useRouter()
	commandPalette.commands = []
	commandPalette.commands.push({
		title: __('Query'),
		description: __('Go to query list'),
		icon: 'arrow-right',
		action: () => {
			router.push('/query')
		},
	})
	commandPalette.commands.push({
		title: __('Dashboard'),
		description: __('Go to dashboard list'),
		icon: 'arrow-right',
		action: () => {
			router.push('/dashboard')
		},
	})
	commandPalette.commands.push({
		title: __('Data Source'),
		description: __('Go to data source list'),
		icon: 'arrow-right',
		action: () => {
			router.push('/data-source')
		},
	})
	commandPalette.commands.push({
		title: __('Settings'),
		description: __('Go to settings'),
		icon: 'arrow-right',
		action: () => {
			router.push('/settings')
		},
	})
}

export default function useCommandPalette() {
	initNavigationCommands(commandPalette)
	return commandPalette
}
