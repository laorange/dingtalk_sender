<script setup lang="ts">
import {useRouter} from "vue-router";
import CopyrightDiv from "../components/CopyrightDiv.vue";

const router = useRouter();
</script>

<template>
  <main>
    <h1>基于钉钉的批量通知程序</h1>

    <n-space justify="center">
      <n-button @click="router.push({name:'create-calendar'})" type="success">新建日程</n-button>
      <n-button @click="router.push({name:'create-bulletin'})" type="info">新建公告</n-button>
    </n-space>

    <CopyrightDiv/>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  align-items: center;
  min-height: 80vh;
}
</style>
