<template>
	<div class="shrink-0">
		<slot v-bind="{ showDialog }"></slot>
		<FrappeUIDialog :options="{ title: 'Drop Bench' }" v-model="dialogOpen">
			<template v-slot:body-content>
				<p class="text-base">
					Are you sure you want to drop this bench? All the sites on this bench
					should be dropped manually before dropping the bench. This action
					cannot be undone.
				</p>
				<p class="mt-4 text-base">
					Please type
					<span class="font-semibold">{{ bench.title }}</span> to confirm.
				</p>
				<Input type="text" class="mt-4 w-full" v-model="confirmBenchName" />
				<ErrorMessage class="mt-2" :error="$resources.dropBench.error" />
			</template>

			<template v-slot:actions>
				<Button @click="dialogOpen = false"> Cancel </Button>
				<Button
					class="ml-3"
					appearance="danger"
					@click="$resources.dropBench.submit()"
					:loading="$resources.dropBench.loading"
				>
					Drop Bench
				</Button>
			</template>
		</FrappeUIDialog>
	</div>
</template>

<script>
export default {
	name: 'BenchDrop',
	props: ['bench'],
	data() {
		return {
			dialogOpen: false,
			confirmBenchName: null
		};
	},
	resources: {
		dropBench() {
			return {
				method: 'press.api.bench.archive',
				params: {
					name: this.bench?.name
				},
				onSuccess() {
					this.dialogOpen = false;
					this.$router.push('/sites');
				},
				validate() {
					if (this.bench?.title !== this.confirmBenchName) {
						return 'Please type the bench name correctly to confirm';
					}
				}
			};
		}
	},
	methods: {
		showDialog() {
			this.dialogOpen = true;
		}
	}
};
</script>
