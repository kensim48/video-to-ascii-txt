<template>
  <div id="app">
    <div v-if="applicationState == 0">
      <Title class="animatedfTitle" />
      <div class="flex w-full items-center text-center" id="app">
        <div class="p-12">
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
              <div v-if="this.filelist.length">
                {{ filelist[0].name }}
                <br />
                Drag another file or
                <span class="underline">click here</span> to replace
              </div>
              <div v-else>
                Drag and drop an .mp4 here or
                <span class="underline">click here</span> to upload your file
                <br />
                [file size less than X and length less than Y]
              </div>
            </label>
          </div>
          <v-btn
            class="my-5"
            block
            :disabled="!this.filelist.length"
            @click="submitFile()"
            >Submit</v-btn
          >
        </div>
      </div>
    </div>
    <div v-else-if="applicationState == 1">
      <Loading class="animatedLoading" />
    </div>
    <div v-else-if="applicationState == 2">
      <iframe
        :src="iframeUrl"
        style="position: absolute; height: 100%; width: 100%; border: none"
      ></iframe>
    </div>
  </div>
</template>

<script>
import Title from "./components/Title.vue";
import Loading from "./components/Loading.vue";
import axios from "axios";

export default {
  name: "App",
  components: {
    Title,
    Loading,
  },
  delimiters: ["${", "}"], // Avoid Twig conflicts
  data: function () {
    return {
      filelist: [], // Store our uploaded files
      applicationState: 0,
      iframeUrl: "",
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
        event.currentTarget.classList.add("bg-green-300");
      }
    },
    dragleave(event) {
      // Clean up
      event.currentTarget.classList.remove("bg-green-300");
    },
    drop(event) {
      if (this.filelist.length > 0) this.remove(0);
      event.preventDefault();
      this.$refs.file.files = event.dataTransfer.files;
      this.onChange(); // Trigger the onChange event manually
      event.currentTarget.classList.remove("bg-green-300");
    },
    submitFile() {
      console.log("submitted");
      let formData = new FormData();
      formData.append("file", this.filelist[0]);
      this.applicationState = 1;
      let self = this;
      axios
        .post(
          "https://video-to-ascii-file-processing-niuary44ca-de.a.run.app",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then(function (response) {
          console.log(JSON.stringify(response.data));
          self.applicationState = 2;
          self.iframeUrl = response.data.url_result;
        })
        .catch(function (error) {
          console.log(error);
        });
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
  font-family: "Lucida Console", "Courier New", serif;
  /* margin-top: 60px; */
}

/* Extra small devices (phones, 600px and down) */
@media only screen and (max-width: 600px) {
  .animatedfTitle {
    display: inline-block;
    font-size: 0.8vw;
  }
  .animatedLoading {
    display: inline-block;
    font-size: 0.8vw;
  }
}

/* Small devices (portrait tablets and large phones, 600px and up) */
@media only screen and (min-width: 600px) {
  .animatedfTitle {
    display: inline-block;
    font-size: 0.4vw;
  }
  .animatedLoading {
    display: inline-block;
    font-size: 0.3vw;
  }
}

[v-cloak] {
  display: none;
}
</style>
