<template>
  <div @dragover.prevent @dragenter.prevent @dragstart.prevent @drop.prevent="uploadImage($event, this.inf)"
    class="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">

    <div class="text-center">

      <div class="mt-4 flex text-sm leading-6 text-gray-600">
        <label
          class="relative cursor-pointer rounded-md font-semibold text-indigo-600 focus-within:outline-none hover:text-purple-500">
          <span>Upload a file</span>
          <input @change="uploadImage($event, this.inf)" accept="image/jpeg,image/png,image/webp" type="file"
            class="sr-only img-input">
        </label>
        <p class="pl-1">or drag and drop</p>
      </div>
      <p class="text-xs leading-5 text-gray-600">PNG, JPG, WEBP</p>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ImageUploadModal',
  data() {
    return {
      image: {
        id: 0,
        data: '',
        url: '',
        file: ''
      },
    }
  },
  props: {
    inf: String,
    id: Number
  },
  mounted() {
  },
  methods: {
    uploadImage(e, info) {
      let currentImage
      try {
        // Get the image from the event target
        currentImage = e.target.files[0];
      } catch {
        // Get the image from the data transfer object
        currentImage = e.dataTransfer.files[0];
      }

      // Log the image to the console
      console.log(currentImage)
      // Set the file property of the image object to the current image
      this.image.file = currentImage
      // Set the url property of the image object to a URL object
      this.image.url = URL.createObjectURL(currentImage);
      // Set the id property of the image object to the id of the image object
      this.image.id = this.id
      // Set the data property of the image object to the info parameter
      this.image.data = info

      // Log the info parameter to the console
      console.log('inf', info)
      // Clear the value of the image input
      $('.img-input').val("")
      // Emit the image object
      this.$emit('getImage', this.image)
    }
  }
}
</script>