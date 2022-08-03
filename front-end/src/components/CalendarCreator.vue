<script setup lang="ts">

import {useStore} from "../store/useStore";
import dayjs from "dayjs";
import {computed} from "vue";

const store = useStore();

const whetherCanSend = computed<boolean>(() => {
  return !!store.senderDeptUnionId
      && !!store.receiverDeptUnionIdArray.length
      && !!store.calendar.title;
});

const handlers = {
  async submit() {
    await fetch(`https://api.dingtalk.com/v1.0/calendar/users/${store.senderDeptUnionId?.split(",")[1]}/calendars/primary/events`, {
      method: "POST",
      headers: {"x-acs-dingtalk-access-token": store.accessToken},
      body: JSON.stringify({
        summary: store.calendar.title,
        description: store.calendar.content,
        isAllDay: false,
        start: {
          dateTime: dayjs(store.calendar.timeRange[0]).format("YYYY-MM-DDTHH:mm:ss+08:00"),
          timeZone: "Asia/Shanghai",
        },
        end: {
          dateTime: dayjs(store.calendar.timeRange[1]).format("YYYY-MM-DDTHH:mm:ss+08:00"),
          timeZone: "Asia/Shanghai",
        },
        reminders: [],
        attendees: store.receiverDeptUnionIdArray.map(du => {
          return {id: du.split(",")[1], isOptional: false};
        }),
      }),
    });
  },
};
</script>

<template>
  <n-divider/>

  <n-space justify="center">
    <n-button @click="handlers.submit()" :disabled="!whetherCanSend" :type="whetherCanSend?`success`:`warning`" size="large">发送</n-button>
  </n-space>
</template>

<style scoped>

</style>
