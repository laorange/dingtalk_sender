<script setup lang="ts">
import {useStore} from "../store/useStore";
import UserSelector from "./UserSelector.vue";

defineProps<{ placeholder: string }>();

const store = useStore();
</script>

<template>
  <UserSelector v-model:value="store.senderDeptUnionId" :multiple="false" :clearable="false" :placeholder="placeholder" label="发布者:"/>
</template>

<style scoped>

</style>
