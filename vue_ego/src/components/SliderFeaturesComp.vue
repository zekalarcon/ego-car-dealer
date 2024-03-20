<template>
  <div class="flex flex-wrap gap-4">
    <div v-for="item in items" :key="item.id" class="w-[200px] max-[700px]:w-full">
      <div class="w-40 max-[700px]:w-full relative">
        <label for="title-slider" class="block text-sm font-medium leading-6 text-gray-900">Title</label>
        <input v-model="item.title" type="text" id="title-slider"
          class="block w-full rounded-md border-0 p-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6">

        <span v-if="item.title_error">
          <p class="absolute text-red-600">{{ item.title_error }}</p>
        </span>
      </div>

      <div class="col-span-full mt-5 relative">
        <label for="description" class="block text-sm font-medium leading-6 text-gray-900">Description</label>
        <div class="">
          <textarea v-model="item.description" id="description" rows="3"
            class="block w-full rounded-md border-0 p-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"></textarea>
        </div>

        <span v-if="item.description_error">
          <p class="absolute text-red-600">{{ item.description_error }}</p>
        </span>
      </div>

      <div class="flex flex-wrap justify-center mt-4">
        <div class=" p-1 relative">
          <label for="slider-feature-image" class="block text-sm font-medium leading-6 text-gray-900">Image</label>
          <div class="mt-2">
            <a v-if="item.get_image" :href="item.get_image" target="_blank"><img :src="item.get_thumbnail" alt=""
                id="slider-feature-image" class="w-[200px] h-[100px] object-cover mx-auto"></a>
            <img v-else :src="require('@/assets/images/addImage.webp')" alt="" id="slider-feature-image"
              class="w-[200px] h-[100px] object-cover mx-auto">
          </div>

          <ImageUpload @getImage="getImage($event)" :inf="info" :id="item.id" />

          <span v-if="item.image_error">
            <p class="absolute text-red-600">{{ item.image_error }}</p>
          </span>

          <button @click="this.$emit('deleteItem', { 'info': info, 'id': item.id })"
            class="transition-all mt-6 w-full bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button">
            Delete
          </button>
        </div>
      </div>
    </div>

    <button @click="this.$emit('addItem', info)"
      class="transition-all w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      type="button">
      Add {{ info }}
    </button>

  </div>
</template>

<script>
import ImageUpload from '@/components/ImageUploadComp.vue'

export default {
  name: 'SliderFeatures',
  data() {
    return {
    }
  },
  components: {
    ImageUpload
  },
  props: {
    items: Array,
    info: String
  },
  mounted() {
  },
  methods: {
    getImage(e) {
      //emit an event to get an image
      this.$emit('getImage', e)
    }
  }
}
</script>