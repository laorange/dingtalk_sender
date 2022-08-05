<script setup lang="ts">
import ApiFetcher from "./components/utils/ApiFetcher.vue";
import {useStore} from "./store/useStore";

const store = useStore();
</script>

<template>
  <n-dialog-provider>
    <n-message-provider>
      <n-spin :show="store.isLoading">

        <router-view/>
        <ApiFetcher/>

      </n-spin>
    </n-message-provider>
  </n-dialog-provider>
</template>

<style>
h1 {
  text-align: center;
}

main {
  margin: 20px 10vw;
}
</style>
