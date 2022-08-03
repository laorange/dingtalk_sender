<script setup lang="ts">


const handlers = {
  submit() {
    fetch(`https://api.dingtalk.com/v1.0/calendar/users/{publisherUserUnionId}/calendars/primary/events`)
  },
};
</script>

<template>
  <n-button @click="handlers.submit()">发送</n-button>
</template>

<style scoped>

</style>
