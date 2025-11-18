import router from '@/router'
import { call } from 'frappe-ui'
import { reactive, ref } from 'vue'
import { confirmDialog } from '../helpers/confirm_dialog'
import { createToast } from '../helpers/toasts'
import { WorkbookListItem } from '../types/workbook.types'
import { formatTimeAgo } from '../helpers/date'
import { __ } from '@/translation'

const workbooks = ref<WorkbookListItem[]>([])

const loading = ref(false)
async function getWorkbooks(search_term?: string, limit: number = 100) {
	loading.value = true
	workbooks.value = await call('insights.api.workbooks.get_workbooks', {
		search_term,
		limit,
	})
	workbooks.value = workbooks.value.map((workbook: any) => ({
		...workbook,
		created_from_now: formatTimeAgo(workbook.creation),
		modified_from_now: formatTimeAgo(workbook.modified),
	}))
	loading.value = false
	return workbooks.value
}

function importWorkbook(workbook: any) {
	confirmDialog({
		title: __('Import Workbook'),
		message: __('Are you sure you want to import this workbook?'),
		onSuccess: () => {
			call('insights.api.workbooks.import_workbook', { workbook }).then((name: string) => {
				getWorkbooks().then(() => {
					createToast({
						message: __('Workbook imported successfully'),
						variant: 'success',
					})
				})
				router.push(`/workbook/${name}`)
			})
		},
	})
}

export default function useWorkbookListItemStore() {
	if (!workbooks.value.length) {
		getWorkbooks()
	}

	return reactive({
		workbooks,
		loading,
		getWorkbooks,
		importWorkbook
	})
}
