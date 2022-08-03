<script setup lang="ts">
import {useStore} from "../store/useStore";
import UserSelector from "./UserSelector.vue";

const store = useStore();
</script>

<template>
  <UserSelector v-model:users="store.senderUnionId" :multiple="false" :clearable="false" placeholder="选择通知发布者(需要具有发布日程权限)" label="发布者:"/>
</template>

<style scoped>

</style>
