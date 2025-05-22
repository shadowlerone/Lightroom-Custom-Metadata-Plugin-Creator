<template>
	<div class="notification">
		<button class="delete"></button>
		<slot>An error occurred</slot>
	</div>
</template>
<script setup>
import { ref, computed, onMounted, onBeforeUpdate, onBeforeMount } from 'vue';
import { to_id } from '../utils.js'

const props = defineEmits({'show':Boolean})

</script>