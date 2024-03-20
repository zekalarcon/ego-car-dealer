<template>
  <div>
    <div class="lg:w-40 w-full relative mb-3">
      <input v-model="query" type="text" id="query" required
        class="block w-full rounded-md border-0 p-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6">

      <span v-if="errorQuery">
        <p class="absolute text-red-600">{{ errorQuery }}</p>
      </span>
    </div>

    <div class="relative">
      <button @click="search()"
        class="transition-all mt-3 lg:w-40 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        type="button">
        Search
      </button>
      <div class="absolute top-14 left-5">
        <a href="#" v-if="seeAll" @click="this.$emit('getAll'); seeAll = !seeAll"
          class="text-blue-400 hover:text-blue-600">See all</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Search',
  data() {
    return {
      query: '',
      errorQuery: '',
      seeAll: false
    }
  },
  methods: {
    search() {
      if (!this.query) {
        // Set error message
        this.errorQuery = 'Required';
        // Set timeout to clear error message
        setTimeout(() => this.errorQuery = '', 2000)
      }

      // Check if errorCategory is empty
      if (!this.errorQuery) {
        console.log('q', this.query)
        this.$emit('query', this.query);
        this.seeAll = true;
        // Clear input value
        this.query = '';
      }
    }
  }
}
</script>