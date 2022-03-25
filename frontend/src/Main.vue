<template>
  <div>
    <input v-model="v1" />
    <el-icon>
      <Search/>
    </el-icon>
    <el-icon>
      <Edit/>
    </el-icon>
    <el-date-picker v-model="v2" placeholder="" format="DD/MM/YYYY" value-format="YYYY-MM-DDTHH:mm:ss.SSSZ"></el-date-picker>
    <el-button type="primary">OK2</el-button>
  </div>
</template>
<style>
@import "~element-plus/theme-chalk/index.css";
</style>
<script>
import { Search,Edit } from "@element-plus/icons-vue";
export default {
  name: 'Main',
  components:{ Search,Edit },
  data() {
    return {
      
      v1:"qqqqq",
      v2:null
      
    }
  },
  created() {
    //console.log(document.cookie);
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
