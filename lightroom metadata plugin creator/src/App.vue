<script setup>
import MetaField from "./components/MetaField.vue";
import { ref, reactive, computed } from 'vue';
import { sanitize, to_id } from './utils.js'

let advanced = ref(false)

let plugin_name = ref('Test Plugin')

let plugin_id = computed(() => {
	return to_id(plugin_name.value)
})

let full_plugin_id_string = computed(() => {
	return `shadowlerone.${plugin_id.value}.Metadata`
})

function add_field() {
	console.log("Not implemented")
}

let metadata_fields = ref([''])
// let metadata_field_count = ref(1)
let data = ref({
	'name': plugin_name,
	'mfields': metadata_fields
})

async function downloadFile() {
	let headers = {
		// mode: 'cors',
		cache: 'no-cache',
		"Content-Type": "application/json",
	}
	try {
		console.debug("Sending request")
		let response = await fetch("http://localhost:5000/generate", {
			method: "POST",
			body: JSON.stringify(data.value),
			headers: headers
		})
		console.debug("attempting download")
		await forceDownload(await response.blob())
	} catch (e) {
		console.error("error occurred")
		throw new Error(e)
	}
}

async function forceDownload(blob) {
	window.console.log(blob)
	const a = document.createElement('a')
	a.style.display = 'none'
	document.body.appendChild(a)
	a.href = URL.createObjectURL(blob)
	a.setAttribute('download', `${plugin_name.value}.lrplugin.zip`)
	a.click()
	window.URL.revokeObjectURL(a.href)
	document.body.removeChild(a)
}
</script>

<template>

	<h1 class="title is-1">Lightroom Metadata Plugin Generator</h1>

	<form class="panel">
		<h2 class="panel-heading"> {{ plugin_name }}
			<template v-if="advanced">(id: {{ full_plugin_id_string }})</template>
		</h2>
		<div class="panel-block">
			<div class="control">
				<div class="field">
					<label class="checkbox">
						<input class="checkbox" type="checkbox" v-model="advanced" />
						Advance Mode
					</label>
				</div>
			</div>
		</div>
		<div class="panel-block">
			<div class="control">
				<div class="field">
					<label class="label">
						Plugin Name
					</label>
					<div class="control">
						<input class="input" type="text" placeholder="Plugin Name" v-model="plugin_name">
					</div>
				</div>
			</div>
		</div>

		<div class="panel-block">
			<div class="control">
				<div id="metadata-fields" class="field">
					<!-- <h2 class="title is-2">Fields</h2> -->
					<label class="label">Fields</label>
					<template v-for="(_, index) in metadata_fields">
						<MetaField :pluginId="full_plugin_id_string" :index="index" :advanced="advanced"
							v-model="metadata_fields" />
					</template>
				</div>
				<div class="field">
					<button class="button" @click.prevent="metadata_fields.push('')">Add Metadata field</button>
				</div>
			</div>
		</div>



		<div class="panel-block">
			<div class="control">
				<div class="field is-grouped">
					<div class="control">
						<button @click.prevent="downloadFile()" class="button is-link">Generate</button>
					</div>
					<div class="control">
						<button class="button is-link is-light">Cancel</button>
					</div>
				</div>
			</div>
		</div>


	</form>
	<!-- <template v-if="advanced == true">
		{{ data }}
	</template> -->

</template>

<style scoped></style>
