<template>
  <div>
    <h1 class="text-center text-[30px] font-bold mt-10 mb-5">Categories</h1>

    <div class="lg:w-40 w-full relative mb-3">
      <label for="add-category" class="block text-sm font-medium leading-6 text-gray-900">Category</label>
      <input v-model="category" type="text" id="add-category" required
        class="block w-full rounded-md border-0 p-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6">

      <span v-if="errorCategory">
        <p class="absolute text-red-600">{{ errorCategory }}</p>
      </span>
    </div>

    <button @click="addCategory"
      class="transition-all mt-3 lg:w-40 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      type="button">
      Add category
    </button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      category: '',
      errorCategory: ''
    };
  },
  methods: {
    async addCategory() {
      if (!this.category) {
        // Set error message
        this.errorCategory = 'Required';
        // Set timeout to clear error message
        setTimeout(() => this.errorCategory = '', 2000)
      }

      // Check if errorCategory is empty
      if (!this.errorCategory) {
        const data = {
          name: this.category
        }
        await axios
          .post('/api/v1/cars/category/', data)
          .then(response => {
            this.category = ''
            console.log(response.data)
          })
          .catch(error => {
            console.log(error)
          })
      }
    }
  }
};
</script>