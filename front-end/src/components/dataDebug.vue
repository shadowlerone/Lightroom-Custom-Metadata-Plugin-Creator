<template>
	<pre><code>{{ JSON.stringify(data, null, 4) }}</code></pre>
</template>
<script setup>
	const props = defineProps('data')
</script>