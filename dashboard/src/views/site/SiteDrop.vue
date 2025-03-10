<template>
	<div class="shrink-0">
		<slot v-bind="{ showDialog }"></slot>
		<FrappeUIDialog :options="{ title: 'Drop Site' }" v-model="dialogOpen">
			<template v-slot:body-content>
				<p class="text-base">
					Are you sure you want to drop your site? The site will be archived and
					all of its files and Offsite Backups will be deleted. This action
					cannot be undone.
				</p>
				<p class="mt-4 text-base">
					Please type
					<span class="font-semibold">{{ site.name }}</span> to confirm.
				</p>
				<Input type="text" class="mt-4 w-full" v-model="confirmSiteName" />
				<div class="mt-4">
					<Input
			 			v-show="!site.archive_failed"
						id="auto-update-checkbox"
						v-model="forceDrop"
						type="checkbox"
						label="Force"
					/>
				</div>
				<ErrorMessage class="mt-2" :error="$resources.dropSite.error" />
			</template>

			<template v-slot:actions>
				<div>
					<Button @click="dialogOpen = false"> Cancel </Button>
					<Button
						class="ml-3"
						appearance="danger"
						@click="$resources.dropSite.submit()"
						:loading="$resources.dropSite.loading"
					>
						{{ site.archive_failed ? 'Force Drop Site' : 'Drop Site' }}
					</Button>
				</div>
			</template>
		</FrappeUIDialog>
	</div>
</template>

<script>
export default {
	name: 'SiteDrop',
	props: ['site'],
	data() {
		return {
			dialogOpen: false,
			confirmSiteName: null,
			forceDrop: false
		};
	},
	resources: {
		dropSite() {
			return {
				method: 'press.api.site.archive',
				params: {
					name: this.site?.name,
					force: this.site.archive_failed == true ? true : this.forceDrop
				},
				onSuccess() {
					this.dialogOpen = false;
					this.$router.push('/sites');
				},
				validate() {
					if (this.site?.name !== this.confirmSiteName) {
						return 'Please type the site name to confirm';
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
