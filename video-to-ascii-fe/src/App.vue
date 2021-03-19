<template>
  <div id="app">
    <Title class="animatedfTitle" />
    <div class="flex w-full items-center text-center" id="app">
      <div
        class="p-12 border border-gray-300"
        @dragover="dragover"
        @dragleave="dragleave"
        @drop="drop"
      >
        <input
          type="file"
          multiple
          name="fields[assetsFieldHandle][]"
          id="assetsFieldHandle"
          class="w-px h-px opacity-0 overflow-hidden absolute"
          @change="onChange"
          ref="file"
          accept=".pdf,.jpg,.jpeg,.png"
        />

        <label for="assetsFieldHandle" class="block cursor-pointer">
          <div>
            Explain to our users they can drop files in here or
            <span class="underline">click here</span> to upload their files
          </div>
        </label>
        <ul class="mt-4" v-if="this.filelist.length" v-cloak>
          <li class="text-sm p-1" v-for="file in filelist" v-bind:key="file.id">
            ${ file.name }<button
              class="ml-2"
              type="button"
              @click="remove(filelist.indexOf(file))"
              title="Remove file"
            >
              remove
            </button>
          </li>
        </ul>
        <b-button>Button</b-button>
      </div>
    </div>
  </div>
</template>

<script>
import Title from "./components/Title.vue";

export default {
  name: "App",
  components: {
    Title,
  },
  delimiters: ["${", "}"], // Avoid Twig conflicts
  data: function () {
    return {
      filelist: [], // Store our uploaded files
    };
  },
  methods: {
    onChange() {
      this.filelist = [...this.$refs.file.files];
    },
    remove(i) {
      this.filelist.splice(i, 1);
    },
    dragover(event) {
      event.preventDefault();
      // Add some visual fluff to show the user can drop its files
      if (!event.currentTarget.classList.contains("bg-green-300")) {
        event.currentTarget.classList.remove("bg-gray-100");
        event.currentTarget.classList.add("bg-green-300");
      }
    },
    dragleave(event) {
      // Clean up
      event.currentTarget.classList.add("bg-gray-100");
      event.currentTarget.classList.remove("bg-green-300");
    },
    drop(event) {
      event.preventDefault();
      this.$refs.file.files = event.dataTransfer.files;
      this.onChange(); // Trigger the onChange event manually
      // Clean up
      event.currentTarget.classList.add("bg-gray-100");
      event.currentTarget.classList.remove("bg-green-300");
    },
  },
};
</script>

<style>
@import "https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/1.1.4/tailwind.min.css";
</style>

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

[v-cloak] {
  display: none;
}
</style>
