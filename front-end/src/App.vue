<script setup lang="ts">
import {onMounted} from "vue";
import {useStore} from "./store/useStore";
import {AddressBook} from "./assets/types";
import UserParser from "./components/utils/UserParser.vue";
import ReceiverSelector from "./components/ReceiverSelector.vue";
import SenderSelector from "./components/SenderSelector.vue";
import TextInputForm from "./components/utils/TextInputForm.vue";
import DateTimeRangePicker from "./components/utils/DateTimeRangePicker.vue";
import CalendarCreator from "./components/CalendarCreator.vue";

const store = useStore();

onMounted(async () => {
  store.accessToken = (await (await fetch((import.meta.env.VITE_BACKEND_URL ?? "") + "/access-token/")).json())["accessToken"] as string;
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
        <TextInputForm v-model:value="store.calendar.title" label="日程标题:" placeholder="请输入日程标题"/>
      </n-gi>
      <n-gi span="2">
        <TextInputForm v-model:value="store.calendar.content" :textarea="true" :required="false" label="日程内容:" placeholder="请输入日程内容"/>
      </n-gi>
    </n-grid>

    <n-divider/>

    <n-space justify="center">
      <DateTimeRangePicker v-model:value="store.calendar.timeRange" label="时间安排"/>
    </n-space>

    <CalendarCreator/>
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
