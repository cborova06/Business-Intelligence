<script setup lang="ts">
import { ref } from 'vue'
import useTeamStore from './teams'
import { __ } from "@/translation";
const show = defineModel()
const teamStore = useTeamStore()
const newTeamName = ref('')
</script>

<template>
	<Dialog
		v-model="show"
		:options="{
			title: 'Create Team',
			actions: [
				{
					label: 'Create',
					variant: 'solid',
					disabled: !newTeamName || teamStore.creatingTeam,
					loading: teamStore.creatingTeam,
					onClick: () => {
						teamStore.createTeam(newTeamName).then(() => {
							newTeamName = ''
							show = false
						})
					},
				},
			],
		}"
	>
		<template #body-content>
			<div class="flex flex-col gap-4">
				<FormControl :label="__('Team Name')" v-model="newTeamName" autocomplete="off" />
			</div>
		</template>
	</Dialog>
</template>
