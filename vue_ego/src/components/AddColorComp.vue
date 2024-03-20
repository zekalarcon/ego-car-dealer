<template>
  <div>
    <h1 class="text-center text-[30px] font-bold mt-10 mb-5">Colors</h1>

    <div class="w-40 max-[700px]:w-full relative mb-3">
      <label for="add-color" class="block text-sm font-medium leading-6 text-gray-900">Color</label>
      <input v-model="color" type="text" id="add-color" required
        class="block w-full rounded-md border-0 p-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6">

      <span v-if="errorColor">
        <p class="absolute text-red-600">{{ errorColor }}</p>
      </span>
    </div>

    <button @click="addColor"
      class="transition-all mt-3 lg:w-40 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      type="button">
      Add color
    </button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      color: '',
      errorColor: ''
    };
  },
  methods: {
    async addColor() {
      if (!this.color) {
        // Set error message
        this.errorColor = 'Required';
        // Set timeout to clear error message
        setTimeout(() => this.errorColor = '', 2000)
      }

      // Check if errorColor is empty
      if (!this.errorColor) {
        const data = {
          name: this.color
        }
        await axios
          .post('/api/v1/cars/color/', data)
          .then(response => {
            this.color = ''
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