<script setup lang="ts">
import UserParser from "../components/utils/UserParser.vue";
import ReceiverSelector from "../components/ReceiverSelector.vue";
import SenderSelector from "../components/SenderSelector.vue";
import TextInputForm from "../components/utils/TextInputForm.vue";
import {useStore} from "../store/useStore";
import DateTimeRangePicker from "../components/utils/DateTimeRangePicker.vue";
import CalendarButton from "../components/CalendarButton.vue";

const store = useStore();
</script>

<template>
  <h1>新建日程</h1>

  <main>
    <n-grid x-gap="20" y-gap="40" cols="1 800:2">
      <n-gi>
        <UserParser/>
      </n-gi>
      <n-gi>
        <ReceiverSelector/>
      </n-gi>
      <n-gi>
        <SenderSelector placeholder="选择发布者(需要具有日程发布权限)"/>
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
      <DateTimeRangePicker label="时间安排"/>
    </n-space>

    <CalendarButton/>
  </main>
</template>

<style scoped>

</style>
