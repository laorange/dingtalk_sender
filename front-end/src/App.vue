<script setup lang="ts">
import {onMounted} from "vue";
import {useStore} from "./store/useStore";
import {AddressBook} from "./assets/types";
import UserParser from "./components/UserParser.vue";
import ReceiverSelector from "./components/ReceiverSelector.vue";
import SenderSelector from "./components/SenderSelector.vue";

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
    <n-grid x-gap="20" y-gap="40" cols="1 800:2">
      <n-gi>
        <UserParser/>
      </n-gi>
      <n-gi>
        <ReceiverSelector/>
      </n-gi>
      <n-gi>
        <SenderSelector/>
      </n-gi>
      <n-gi>
        <n-form-item label="日程标题:" :required="true" label-placement="left" :show-feedback="false">
          <n-input v-model:value="store.calendar.title" placeholder="请输入日程标题"></n-input>
        </n-form-item>
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
