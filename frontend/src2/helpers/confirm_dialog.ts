import ConfirmDialog from '../components/ConfirmDialog.vue'
import { VNode, h, ref } from 'vue'
import { __ } from '@/translation'

export const dialogs = ref<VNode[]>([])

export function confirmDialog({
	title = 'Untitled',
	message = '',
	primaryActionLabel = __('Confirm'),
	theme = 'gray',
	fields = [],
	onSuccess = () => {},
}) {
	const component = h(ConfirmDialog, {
		title,
		message,
		theme,
		fields,
		onSuccess,
		primaryActionLabel,
	})
	dialogs.value.push(component)
}
