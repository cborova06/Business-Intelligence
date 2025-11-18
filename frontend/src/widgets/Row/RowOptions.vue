<script setup>
import AxisChartOptions from '@/widgets/AxisChart/AxisChartOptions.vue'
import { __ } from "@/translation";
const options = defineModel()
const props = defineProps({
	columns: { type: Array, required: true },
})
</script>

<template>
	<div class="space-y-4">
		<AxisChartOptions seriesType="bar" v-model:options="options" :columns="props.columns" />
		<Checkbox v-model="options.stack" :label="__('Stack Values')" />
		<Checkbox v-model="options.roundedBars" :label="__('Rounded Bars')" />
		<Checkbox v-model="options.show_data_labels" :label="__('Show Data Labels')" />
	</div>
</template>
