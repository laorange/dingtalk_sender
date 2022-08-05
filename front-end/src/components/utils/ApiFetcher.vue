<script setup lang="ts">
import {useStore} from "../../store/useStore";
import {onMounted} from "vue";
import {AddressBook} from "../../assets/types";
import {useMessage} from "naive-ui";

const store = useStore();
const message = useMessage();

const handlers = {
  async fetchAccessToken() {
    store.accessToken = (await (await fetch((import.meta.env.VITE_BACKEND_URL ?? "") + "/access-token/")).json())["accessToken"] as string;
  },
  async fetchAddressBook() {
    store.addressBook = await (await fetch((import.meta.env.VITE_BACKEND_URL ?? "") + "/address-book/")).json() as AddressBook;
  },
};

onMounted(async () => {
  try {
    store.isLoading = true;
    await handlers.fetchAccessToken();
    await handlers.fetchAddressBook();
  } catch (e) {
    message.error("请求数据失败！请检查后端服务是否已被关闭");
  } finally {
    store.isLoading = false;
  }

  setInterval(() => handlers.fetchAccessToken(), 1000 * 60 * 5); // 每5分钟刷新一次accessToken
});
</script>

<template>

</template>

<style scoped>

</style>
