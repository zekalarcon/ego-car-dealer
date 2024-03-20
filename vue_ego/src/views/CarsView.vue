<template>
  <div class="cars w-[90%] mx-auto">
    <h1 class="text-center text-[30px] font-bold m-5">Cars</h1>

    <div class="sticky top-20 z-50" v-if="loadingCars">
      <div role="status">
        <svg aria-hidden="true"
          class="absolute bottom-5 w-/10 h-10 text-gray-200 animate-spin dark:text-black fill-blue-500"
          viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
            fill="currentColor" />
          <path
            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
            fill="currentFill" />
        </svg>
        <span class="sr-only">Loading...</span>
      </div>
    </div>

    <div class="flex flex-wrap justify-center mb-10 mx-5">
      <SearchComp @query="searchQuery($event)" @getAll="getCars" />
    </div>

    <div class="h-[560px] lg:h-[500px] overflow-y-scroll">
      <table class="border-collapse w-full mx-auto">
        <thead>
          <tr>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Id</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Available</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Title</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Category</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Year</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Price</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Color</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Doors</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Engine</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Created</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
              Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="car in cars" :key="car.id"
            class="bg-white lg:hover:bg-gray-100 flex lg:table-row flex-row lg:flex-row flex-wrap lg:flex-no-wrap mb-10 lg:mb-0">
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b block lg:table-cell relative lg:static">
              <span class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Id</span>
              {{ car.id }}
            </td>
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b text-center block lg:table-cell relative lg:static">
              <span
                class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Available</span>
              <svg v-if="car.available" class="h-8 w-8 text-green-500 mx-auto" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else class="h-8 w-8 text-red-500 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>

            </td>
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b text-center block lg:table-cell relative lg:static">
              <span
                class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Title</span>
              {{ car.title }}
            </td>
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b text-center block lg:table-cell relative lg:static">
              <span
                class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Category</span>
              {{ car.category }}
            </td>
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b text-center block lg:table-cell relative lg:static">
              <span
                class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Year</span>
              {{ car.year }}
            </td>
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b text-center block lg:table-cell relative lg:static">
              <span
                class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Price</span>
              {{ car.price }}
            </td>
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b text-center block lg:table-cell relative lg:static">
              <span
                class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Color</span>
              {{ car.color }}
            </td>
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b text-center block lg:table-cell relative lg:static">
              <span
                class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Doors</span>
              {{ car.doors }}
            </td>
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b text-center block lg:table-cell relative lg:static">
              <span
                class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Engine</span>
              {{ car.engine }}
            </td>
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b text-center block lg:table-cell relative lg:static">
              <span
                class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Created</span>
              {{ car.get_created }}
            </td>
            <td
              class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b text-center block lg:table-cell relative lg:static">
              <span
                class="lg:hidden absolute top-0 left-0 bg-blue-200 px-2 py-1 text-xs font-bold uppercase">Actions</span>
              <a href="#" @click="carModal" class="text-blue-400 hover:text-blue-600 underline"
                :data-id="car.id">Edit</a>
              <a href="#" @click="deleteCar" class="text-red-500 hover:text-red-700 underline pl-6"
                :data-id="car.id">Delete</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex justify-center mt-2">
      <div v-if="prev" class="mx-2 cursor-pointer">
        <a href="#" @click="changePage('prev')" class="text-black hover:text-blue-700">&laquo; Prev</a>
      </div>
      <div v-if="next" class="mx-2 cursor-pointer">
        <a href="#" @click="changePage('next')" class="text-black hover:text-blue-700">Next &raquo;</a>
      </div>
    </div>

    <button @click="carModal" data-id="new-car"
      class="sticky bottom-0 lg:static transition-all mt-3 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      type="button">
      Add car
    </button>

    <div class="flex flex-wrap justify-center mb-10">
      <AddCategoryComp class="mx-5" />
      <AddColorComp class="mx-5" />
    </div>

    <transition name="slide-fade">
      <AddCarComp v-show="this.$store.state.showModalEditCar"
        @close-modal="this.$store.state.showModalEditCar = false; carId = ''" @getCars="getCars()" :trigger="carId"
        info="" />
    </transition>
  </div>
</template>

<script>
import axios from 'axios'
import AddCarComp from '@/components/AddCarComp'
import AddCategoryComp from '@/components/AddCategoryComp'
import AddColorComp from '@/components/AddColorComp'
import SearchComp from '@/components/SearchComp'

export default {
  name: 'BuscarView',
  data() {
    return {
      cars: [],
      search: '',
      counter: 1,
      carId: '',
      next: false,
      prev: false,
      page: 1,
      loadingCars: false
    }
  },
  components: {
    AddCarComp,
    AddCategoryComp,
    AddColorComp,
    SearchComp
  },
  mounted() {
    document.title = 'Cars | Ego Car Dealer'
    this.getCars();
  },
  methods: {
    changePage(e) {
      let info = e
      if (info == 'prev') {
        this.page--
      } else {
        this.page++
      }

      if (this.page < 1) {
        this.page = 1
      }
      this.getCars()
    },
    async deleteCar(e) {
      // set loading to true
      this.loadingCars = true
      // create data object
      let data = {
        info: 'delete-car',
        id: e.target.dataset.id
      }

      // send post request to server
      await axios
        .post('/api/v1/cars/crud/', data)
        .then(response => {
          // get cars from server
          this.getCars()
        })
        .catch(error => {
          console.log(error)
        })

      // set loading to false
      this.loadingCars = false
    },
    carModal(e) {
      // Get the carId from the data-id attribute of the car modal
      this.carId = e.target.dataset.id
      // Log the carId to the console
      console.log(this.carId)
    },
    async searchQuery(e) {
      console.log('query', e)
      // set loading to true
      this.loadingCars = true

      await axios
        .get(`/api/v1/cars/search/?q=${e}`)
        .then(response => {
          // Check if there is a next page
          if (response.data.next) {
            this.next = true
          } else {
            this.next = false
          }

          // Check if there is a previous page
          if (response.data.previous) {
            this.prev = true
          } else {
            this.prev = false
          }

          // Set the cars to the response data
          this.cars = response.data.results

        })
        .catch(error => {
          console.log(JSON.stringify(error))
        })

      this.loadingCars = false
    },
    async getCars() {
      // Set loadingCars to true to indicate that the request is in progress
      this.loadingCars = true
      // Create an object to pass to the API call
      let data = {
        contador: this.counter
      }
      // Make the API call
      await axios
        .get(`/api/v1/cars/?p=${this.page}`)
        .then(response => {
          console.log(response)
          // Check if there is a next page
          if (response.data.next) {
            this.next = true
          } else {
            this.next = false
          }

          // Check if there is a previous page
          if (response.data.previous) {
            this.prev = true
          } else {
            this.prev = false
          }

          // Set the cars to the response data
          this.cars = response.data.results

        })
        .catch(error => {
          // If the API call returns a 401, remove the token and push to the gestion page
          if (error.response.status === 401) {
            localStorage.removeItem("token")
            localStorage.removeItem("username")
            this.$store.commit('removeToken')
            this.$router.push('/')
          }
          console.log(error)
        })

      // Set loadingCars to false to indicate that the request is complete
      this.loadingCars = false
    }
  }
}
</script>

<style>
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>