<template>
	<div>
		<Form
			class="mt-4"
			:fields="fields"
			:modelValue="address"
			@update:modelValue="$emit('update:address', $event)"
		/>
		<div class="mt-4" v-show="address.country == 'India'">
			<span class="mb-2 block text-sm leading-4 text-gray-700">
				GSTIN
			</span>
			<Input
		 		v-if="gstApplicable"
				type="text"
				v-model="address.gstin"
				:disabled="!gstApplicable"
			/>
			<Button
				v-if="gstApplicable"
				class="mt-2"
				@click="
					update('gstin', 'Not Applicable');
					gstApplicable = false;
				"
			>
				I don't have a GSTIN
			</Button>
			<Button
				v-else
				class="mt-2"
				@click="
					update('gstin', '');
					gstApplicable = true;
				"
			>
				Add a GSTIN
			</Button>
		</div>
	</div>
</template>

<script>
import Form from '@/components/Form.vue';

export default {
	name: 'AddressForm',
	props: ['address'],
	emits: ['update:address'],
	components: {
		Form
	},
	data() {
		return {
			gstApplicable: true
		};
	},
	resources: {
		countryList: {
			method: 'press.api.account.country_list',
			auto: true,
			onSuccess() {
				let country = this.countryList.find(
					d => d.label === this.$account.team.country
				);
				if (country) {
					this.update('country', country.value);
				}
			}
		},
		indianStates: {
			method: 'press.api.billing.indian_states'
		}
	},
	watch: {
		'address.country': {
			handler(value) {
				if (value === 'India') {
					this.$resources.indianStates.fetch();
					this.update('state', '');
				}
			},
			immediate: true
		}
	},
	methods: {
		update(key, value) {
			this.$emit('update:address', {
				...this.address,
				[key]: value
			});
		},
		async validateValues() {
			let { country } = this.address;
			let is_india = country == 'India';
			let values = this.fields
				.flat()
				.filter(df => df.fieldname != 'gstin' || is_india)
				.map(df => this.address[df.fieldname]);

			if (!values.every(Boolean)) {
				return 'Please fill required values';
			}

			try {
				await this.$call('press.api.billing.validate_gst', {
					address: this.address
				});
			} catch (error) {
				return error.messages.join('\n');
			}
		}
	},
	computed: {
		countryList() {
			return (this.$resources.countryList.data || []).map(d => ({
				label: d.name,
				value: d.name
			}));
		},
		indianStates() {
			return (this.$resources.indianStates.data || []).map(d => ({
				label: d,
				value: d
			}));
		},
		fields() {
			return [
				{
					fieldtype: 'Select',
					label: 'Country',
					fieldname: 'country',
					options: this.countryList,
					required: 1
				},
				{
					fieldtype: 'Data',
					label: 'Address',
					fieldname: 'address',
					required: 1
				},
				[
					{
						fieldtype: 'Data',
						label: 'City',
						fieldname: 'city',
						required: 1
					},
					{
						fieldtype: this.address.country === 'India' ? 'Select' : 'Data',
						label: 'State / Province / Region',
						fieldname: 'state',
						required: 1,
						options: this.address.country === 'India' ? this.indianStates : null
					},
					{
						fieldtype: 'Data',
						label: 'Postal Code',
						fieldname: 'postal_code',
						required: 1
					}
				]
			];
		}
	}
};
</script>
