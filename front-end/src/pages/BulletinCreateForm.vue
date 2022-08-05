<script setup lang="ts">
import UserParser from "../components/utils/UserParser.vue";
import ReceiverSelector from "../components/ReceiverSelector.vue";
import SenderSelector from "../components/SenderSelector.vue";
import TextInputForm from "../components/utils/TextInputForm.vue";
import {useStore} from "../store/useStore";
import BulletinButton from "../components/BulletinButton.vue";

const store = useStore();
</script>

<template>
  <h1>新建公告</h1>

  <main>
    <n-grid x-gap="20" y-gap="40" cols="1 800:2">
      <n-gi>
        <UserParser/>
      </n-gi>
      <n-gi>
        <ReceiverSelector/>
      </n-gi>
      <n-gi>
        <SenderSelector placeholder="选择发布者(需要具有公告发布权限)"/>
      </n-gi>
      <n-gi>
        <TextInputForm v-model:value="store.bulletin.title" label="公告标题:" placeholder="请输入公告标题"/>
      </n-gi>
      <n-gi span="2">
        <TextInputForm v-model:value="store.bulletin.content" :textarea="true" :required="false" label="公告内容:" placeholder="请输入公告内容"/>
      </n-gi>
    </n-grid>
  </main>

  <BulletinButton/>
</template>

<style scoped>

</style>
