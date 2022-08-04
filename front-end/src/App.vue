<script setup lang="ts">
import ApiFetcher from "./components/utils/ApiFetcher.vue";

</script>

<template>
  <header>
    <h1>基于钉钉的批量通知程序</h1>
  </header>

  <router-view/>

  <ApiFetcher/>
</template>

<style>
h1 {
  text-align: center;
}

main {
  margin: 20px 10vw;
}
</style>
