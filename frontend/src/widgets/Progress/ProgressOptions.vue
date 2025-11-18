<script setup>
import InputWithTabs from '@/components/Controls/InputWithTabs.vue'
import { FIELDTYPES } from '@/utils'
import { computed } from 'vue'
import { __ } from "@/translation";
const emit = defineEmits(['update:modelValue'])
const props = defineProps({
	modelValue: { type: Object, required: true },
	columns: { type: Array, required: true },
})

const options = computed({
	get: () => props.modelValue,
	set: (value) => emit('update:modelValue', value),
})

const valueOptions = computed(() => {
	return props.columns
		?.filter((column) => FIELDTYPES.NUMBER.includes(column.type))
		.map((column) => ({
			label: column.label,
			value: column.label,
			description: column.type,
		}))
})

if (!options.value.targetType) {
	options.value.targetType = 'Column'
}
</script>

<template>
	<div class="space-y-4">
		<FormControl
			type="text"
			:label="__('Title')"
			class="w-full"
			v-model="options.title"
			:placeholder="__('Title')"
		/>
		<div>
			<label class="mb-1.5 block text-xs text-gray-600">Progress Column</label>
			<Autocomplete
				:options="valueOptions"
				:modelValue="options.progress"
				@update:modelValue="options.progress = $event?.value"
			/>
		</div>
		<div>
			<label class="mb-1.5 block text-xs text-gray-600">Target</label>
			<InputWithTabs
				:value="options.targetType"
				:tabs="{
					Column: options.targetType === 'Column',
					Value: options.targetType === 'Value',
				}"
				@tab-change="options.targetType = $event"
			>
				<template #inputs>
					<div class="w-full">
						<Autocomplete
							v-if="options.targetType === 'Column'"
							:placeholder="__('Select a column...')"
							:options="valueOptions"
							:modelValue="options.target"
							@update:modelValue="options.target = $event?.value"
						/>
						<FormControl
							v-if="options.targetType === 'Value'"
							v-model="options.target"
							:placeholder="__('Enter a value...')"
							type="number"
						/>
					</div>
				</template>
			</InputWithTabs>
		</div>
		<FormControl
			:label="__('Prefix')"
			type="text"
			v-model="options.prefix"
			:placeholder="__('Enter a prefix...')"
		/>
		<FormControl
			:label="__('Suffix')"
			type="text"
			v-model="options.suffix"
			:placeholder="__('Enter a suffix...')"
		/>
		<FormControl
			:label="__('Decimals')"
			type="number"
			v-model="options.decimals"
			:placeholder="__('Enter a number...')"
		/>
		<Checkbox v-model="options.shorten" :label="__('Shorten Numbers')" />
	</div>
</template>
