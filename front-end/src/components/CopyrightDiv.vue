<script setup lang="ts">
import packageJson from "../../package.json";
</script>

<template>
  <div class="copyright-div">
    <div><a href="https://github.com/laorange/dingtalk_sender">v{{ packageJson.version }}</a> |
      Released under <a href="https://spdx.org/licenses/AGPL-3.0-only.html">AGPL-3.0 License</a></div>
    <div>Copyright © 2022 <a href="https://github.com/laorange">GitHub@laorange</a></div>
  </div>
</template>

<style scoped>
.copyright-div {
  font-size: xx-small;
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

a:link, a:visited {
  text-decoration: none;
  color: black;
}
</style>
