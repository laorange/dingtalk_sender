<script setup lang="ts">
import UserSelector from "./components/UserSelector.vue";
import {onMounted} from "vue";
import {useStore} from "./store/useStore";
import {AddressBook} from "./assets/types";
import UserParser from "./components/UserParser.vue";

const store = useStore();

onMounted(async () => {
  store.accessToken = await (await fetch((import.meta.env.VITE_BACKEND_URL ?? "") + "/access-token/")).json() as string;
  store.addressBook = await (await fetch((import.meta.env.VITE_BACKEND_URL ?? "") + "/address-book/")).json() as AddressBook;
});
</script>

<template>
  <header>
    <h1>钉钉通知程序</h1>
  </header>

  <main>
    <n-grid x-gap="20" cols="1 800:2">
      <n-gi>
        <UserParser/>
      </n-gi>
      <n-gi>
        <UserSelector/>
      </n-gi>
    </n-grid>
  </main>

</template>

<style>
h1 {
  text-align: center;
}

main {
  margin: 0 10vw;
}
</style>
