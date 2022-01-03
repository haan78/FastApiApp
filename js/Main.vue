<template>
  <div>
    <button>Selam</button>
    <el-button type="success" :icon="Star"></el-button>
  </div>
  
</template>
<style>
@import "element-plus/theme-chalk/index.css";
</style>
<script>
import {
  Star
} from '@element-plus/icons-vue'
export default {
  name: 'Main',
  data() {
    return {
      "Star":Star
    }
  },
  created() {
    console.log(document.cookie);
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
