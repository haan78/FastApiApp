<template>
  <div>
    <button>Selam</button>
  </div>
  
</template>
<script>
export default {
  name: 'Main',
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
