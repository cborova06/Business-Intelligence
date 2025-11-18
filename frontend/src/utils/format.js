import dayjs from './dayjs'
import { __ } from "@/translation";
export const dateFormats = [
	{ label: __('January 12, 2020 1:14 PM'), value: 'Minute' },
	{ label: __('January 12, 2020 1:00 PM'), value: 'Hour' },
	{ label: __('1:00 PM'), value: 'Hour of Day' },
	{ label: __('12th January, 2020'), value: 'Day' },
	{ label: __('12th Jan, 20'), value: 'Day Short' },
	{ label: __('12th January, 2020'), value: 'Week' },
	{ label: __('January, 2020'), value: 'Month' },
	{ label: __('Jan 20'), value: 'Mon' },
	{ label: __('Q1, 2020'), value: 'Quarter' },
	{ label: '2020', value: 'Year' },
	{ label: __('Monday'), value: 'Day of Week' },
	{ label: __('January'), value: 'Month of Year' },
	{ label: 'Q1', value: 'Quarter of Year' },
]

export function getFormattedDate(date, dateFormat) {
	if (!date) return ''

	if (dateFormat === 'Day of Week') {
		return date
	}

	if (dateFormat === 'Month of Year') {
		if (isNaN(date)) return date
		return dayjs(date, 'MM').format('MMMM')
	}

	if (dateFormat === 'Quarter of Year') {
		return `Q${date}`
	}

	if (dateFormat === 'Hour of Day') {
		return dayjs(date, 'HH:mm').format('h:mm A')
	}

	const dayjsFormat = {
		Minute: 'MMMM D, YYYY h:mm A',
		Hour: 'MMMM D, YYYY h:00 A',
		Day: 'MMMM D, YYYY',
		Week: 'MMM Do, YYYY',
		Mon: 'MMM YY',
		Month: 'MMMM, YYYY',
		Year: 'YYYY',
		Quarter: '[Q]Q, YYYY',
		'Day Short': 'Do MMM, YY',
	}[dateFormat]

	if (!dayjsFormat) return date
	return dayjs(date).format(dayjsFormat)
}
