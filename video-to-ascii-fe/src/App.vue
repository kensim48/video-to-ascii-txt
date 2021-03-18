<template>
  <div id="app">
    <Title class="animatedfTitle" msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
import Title from "./components/Title.vue";

export default {
  name: "App",
  components: {
    Title,
  },
};
</script>

<style>
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center; */
  background-color: black;
  color: white;
  /* margin-top: 60px; */
}

/* Extra small devices (phones, 600px and down) */
@media only screen and (max-width: 600px) {
  .animatedfTitle {
    display: inline-block;
    font-size: 0.8vw;
    /* width: 50%; */
  }
}

/* Small devices (portrait tablets and large phones, 600px and up) */
@media only screen and (min-width: 600px) {
  .animatedfTitle {
    display: inline-block;
    font-size: 0.4vw;
    /* width: 50%; */
  }
}
</style>
