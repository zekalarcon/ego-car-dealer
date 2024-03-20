<template>

  <div
    class="fixed flex flex-wrap justify-center content-center z-[999] top-0 bottom-0 left-0 right-0 h-full bg-[#34343449]"
    @click="this.$emit('close-modal'); cleanFields()">
    <div
      class="px-10 py-5 mx-5 h-[700px] max-[1000px]:h-[70%] max-w-[1000px] overflow-y-scroll rounded-lg bg-slate-100 text-left shadow-xl scroll-smooth"
      id="car-information-modal" @click.stop>
      <h1 class="text-center text-2xl font-semibold leading-7 text-gray-900">{{ title }}</h1>
      <hr class="mb-5 mt-2">

      <div v-if="modalCarLoading" role="status" class="absolute -translate-x-1/2 -translate-y-1/2 top-2/4 left-1/2">
        <svg aria-hidden="true" class="w-10 h-10 text-black animate-spin dark:text-black fill-blue-500"
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

      <div id="main-edit">
        <div class="flex flex-wrap gap-4 my-5">
          <div class="">
            <label for="available" class="block text-sm font-medium leading-6 text-gray-900">Available</label>
            <input v-model="car.available" id="available" type="checkbox"
              class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600">
          </div>

          <div class="w-40 max-[700px]:w-full relative">
            <label for="title" class="block text-sm font-medium leading-6 text-gray-900">Title</label>
            <input v-model="car.title" type="text" id="title" required
              class="block w-full rounded-md border-0 p-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6">

            <span v-if="error.title">
              <p class="absolute text-red-600">{{ error.title }}</p>
            </span>
          </div>

          <div class="w-40 max-[700px]:w-full relative">
            <label for="secondary-title" class="block text-sm font-medium leading-6 text-gray-900">Secondary
              Title</label>
            <input v-model="car.secondary_title" type="text" id="secondary-title" required
              class="block w-full rounded-md border-0 p-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6">

            <span v-if="error.secondary_title">
              <p class="absolute text-red-600">{{ error.secondary_title }}</p>
            </span>
          </div>

          <div class="w-40 max-[700px]:w-full relative">
            <label for="description-title" class="block text-sm font-medium leading-6 text-gray-900">Title
              Description</label>
            <input v-model="car.description_title" type="text" id="description-title" required
              class="block w-full rounded-md border-0 p-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6">

            <span v-if="error.description_title">
              <p class="absolute text-red-600">{{ error.description_title }}</p>
            </span>
          </div>

          <div class="w-40 max-[700px]:w-full relative">
            <label for="price" class="block text-sm font-medium leading-6 text-gray-900">Price</label>
            <input v-model="car.price" type="number" id="price" required
              class="block w-full rounded-md border-0 p-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6">

            <span v-if="error.price">
              <p class="absolute text-red-600">{{ error.price }}</p>
            </span>
          </div>
        </div>

        <div class="col-span-full mb-5 relative">
          <label for="description" class="block text-sm font-medium leading-6 text-gray-900">Description</label>
          <div class="">
            <textarea v-model="car.description" id="description" required rows="3"
              class="block w-full rounded-md border-0 p-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"></textarea>
          </div>

          <span v-if="error.description">
            <p class="absolute text-red-600">{{ error.description }}</p>
          </span>
        </div>

        <div class="flex flex-wrap gap-4 mt-2">
          <div class="w-40 relative">
            <label for="category" class="block text-sm font-medium leading-6 text-gray-900">Category</label>
            <div class="mt-2">
              <select v-model="car.category" id="category"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-xs sm:text-sm sm:leading-6">
                <option v-for="category in categories" :key="category.id">{{ category.name }}</option>
              </select>
            </div>

            <span v-if="error.category">
              <p class="absolute text-red-600">{{ error.category }}</p>
            </span>
          </div>

          <div class="w-40 relative">
            <label for="year" class="block text-sm font-medium leading-6 text-gray-900">Year</label>
            <div class="mt-2">
              <select v-model="car.year" id="year"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-xs sm:text-sm sm:leading-6">
                <option v-for="year in years" :key="year">{{ year }}</option>
              </select>
            </div>

            <span v-if="error.year">
              <p class="absolute text-red-600">{{ error.year }}</p>
            </span>
          </div>

          <div class="w-40 relative">
            <label for="color" class="block text-sm font-medium leading-6 text-gray-900">Color</label>
            <div class="mt-2">
              <select v-model="car.color" id="color"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 m:max-w-xs sm:text-sm sm:leading-6">
                <option v-for="color in colors" :key="color.id">{{ color.name }}</option>
              </select>
            </div>

            <span v-if="error.color">
              <p class="absolute text-red-600">{{ error.color }}</p>
            </span>
          </div>

          <div class="w-40 relative">
            <label for="doors" class="block text-sm font-medium leading-6 text-gray-900">Doors</label>
            <div class="mt-2">
              <select v-model="car.doors" id="doors"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-xs sm:text-sm sm:leading-6">
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5</option>
              </select>
            </div>

            <span v-if="error.doors">
              <p class="absolute text-red-600">{{ error.doors }}</p>
            </span>
          </div>

          <div class="w-40 relative">
            <label for="engine" class="block text-sm font-medium leading-6 text-gray-900">Engine</label>
            <div class="mt-2">
              <select v-model="car.engine" id="engine"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-xs sm:text-sm sm:leading-6">
                <option>nafta</option>
                <option>diesel</option>
                <option>electrico</option>
              </select>
            </div>

            <span v-if="error.engine">
              <p class="absolute text-red-600">{{ error.engine }}</p>
            </span>
          </div>
        </div>

        <div class="flex flex-wrap justify-center mt-4">
          <div class="p-1 relative">
            <label for="main-image" class="block text-sm font-medium leading-6 text-gray-900">Main
              image</label>
            <div class="mt-2">
              <a v-if="url_main_image" :href="url_main_image" target="_blank"><img :src="url_main_thumbnail"
                  class="w-[200px] h-[100px] object-contain mx-auto" alt="" id="main-image"></a>
              <img v-else :src="require('@/assets/images/addImage.webp')" alt="" id="first-image"
                class="w-[200px] h-[100px] object-contain mx-auto">
            </div>

            <ImageUpload @getImage="getImage($event)" inf="main" :id=0 />

            <span v-if="error.main_image">
              <p class="absolute text-red-600">{{ error.main_image }}</p>
            </span>
          </div>

          <div class=" p-1 relative">
            <label for="secondary-image" class="block text-sm font-medium leading-6 text-gray-900">Secondary
              image</label>
            <div class="mt-2">
              <a v-if="url_secondary_image" :href="url_secondary_image" target="_blank"><img
                  :src="url_secondary_thumbnail" class="w-[200px] h-[100px] object-contain mx-auto" alt=""></a>
              <img v-else :src="require('@/assets/images/addImage.webp')" alt="" id="second-image"
                class="w-[200px] h-[100px] object-contain mx-auto">
            </div>

            <ImageUpload @getImage="getImage($event)" inf="secondary" :id=0 />

            <span v-if="error.secondary_image">
              <p class="absolute text-red-600">{{ error.secondary_image }}</p>
            </span>
          </div>
        </div>
      </div>

      <div id="slider-edit">
        <hr class="mb-2 mt-10">
        <h1 class="text-center text-xl  font-semibold leading-7 text-gray-900">Slider</h1>
        <hr class="mb-5 mt-2">

        <SliderFeatures :items="car.slider" info="slider" @addItem="addItem('slider')" @deleteItem="deleteItem($event)"
          @getImage="getImage($event)" />

      </div>

      <div id="features-edit">
        <hr class="mb-2 mt-10">
        <h1 class="text-center text-xl  font-semibold leading-7 text-gray-900">Features</h1>
        <hr class="mb-5 mt-2">

        <SliderFeatures :items="car.features" info="features" @addItem="addItem('feature')"
          @deleteItem="deleteItem($event)" @getImage="getImage($event)" />
      </div>

      <hr class="my-10">
      <button @click="this.$emit('close-modal')"
        class="w-full mb-2 bg-red-700 hover:bg-red-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        type="button">
        Cancel
      </button>
      <button @click="saveCar"
        class="w-full bg-green-700 hover:bg-green-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        type="button">
        Save
      </button>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
import ImageUpload from '@/components/ImageUploadComp.vue'
import SliderFeatures from '@/components/SliderFeaturesComp.vue'

export default {
  name: 'SettingsEmpleadoModal',
  props: {
    trigger: String,
  },
  data() {
    return {
      car: {
        id: '',
        available: false,
        title: '',
        category: '',
        secondary_title: '',
        description_title: '',
        description: '',
        year: '',
        color: '',
        doors: '',
        engine: '',
        price: '',
        main_image: '',
        secondary_image: '',
        slider: [],
        features: []
      },
      error: {
        available: '',
        title: '',
        category: '',
        secondary_title: '',
        description_title: '',
        description: '',
        year: '',
        color: '',
        doors: '',
        engine: '',
        price: '',
        main_image: '',
        secondary_image: ''
      },
      categories: [],
      years: [],
      colors: [],
      url_main_image: '',
      url_secondary_image: '',
      url_main_thumbnail: '',
      url_secondary_thumbnail: '',
      info: '',
      title: '',
      modalCarLoading: false
    }
  },
  components: {
    ImageUpload,
    SliderFeatures
  },
  watch: {
    trigger: function (newVal, oldVal) {
      // Scroll to the top of the modal when the trigger is changed
      $('#car-information-modal').scrollTop(0)
      // If the new trigger is 'new-car'
      if (newVal == 'new-car') {
        // Set the title to 'Create car'
        this.title = 'Create car'
        // Clean the fields
        this.cleanFields()
        // Set the info to 'new-car'
        this.info = newVal
        // Set a timeout of 200 milliseconds before setting the showModalEditCar state to true
        setTimeout(() => {
          this.$store.state.showModalEditCar = true
        }, 200)
      }
      // If the new trigger is not 'new-car'
      else if (newVal) {
        // Set the title to 'Edit car'
        this.title = 'Edit car'
        // Set the car id to the new trigger
        this.car.id = newVal
        // Set the info to an empty string
        this.info = ''
        // Get the car details
        this.getCarDetails()
        // Set a timeout of 200 milliseconds before setting the showModalEditCar state to true
        setTimeout(() => {
          this.$store.state.showModalEditCar = true
        }, 200)
      }
    }
  },
  methods: {
    async deleteItem(e) {
      // set the loading state to true
      this.modalCarLoading = true
      // create an object to store the data to be sent to the API
      let data = {
        info: e.info,
        id: e.id
      }
      // send a post request to the API
      await axios
        .post('/api/v1/cars/crud/', data)
        // if the request is successful
        .then(response => {
          // if the response is 'query does not exist'
          if (response.data == 'query does not exist') {
            // loop through the car object
            for (let i = 0; i < this.car[e.info].length; i++) {
              // if the id of the car object matches the id of the item to be deleted
              if (this.car[e.info][i]['id'] == e.id) {
                // remove the item from the car object
                this.car[e.info].splice(i, 1);
                // break out of the loop
                break
              }
            }
            // if the request is successful
          } else {
            // log the response data
            console.log('delete', response.data)
            // call the getCarDetails function
            this.getCarDetails()
          }
        })
        // if the request fails
        .catch(error => {
          // log the error
          console.log(error)
        })
      // set the loading state to false
      this.modalCarLoading = false
    },
    addItem(e) {
      //Create an item object to store the data
      let item = {
        //Set the id to the length of the slider + 1
        id: this.car.slider.length + 1,
        //Set the car id
        car: this.car.id,
        //Set the title to an empty string
        title: '',
        //Set the description to an empty string
        description: '',
        //Set the image to an empty string
        get_image: '',
        //Set the thumbnail to an empty string
        get_thumbnail: '',
        //Set the image to an empty string
        image: '',
        //Set the title error to an empty string
        title_error: '',
        //Set the description error to an empty string
        description_error: '',
        //Set the image error to an empty string
        image_error: '',
      }

      //Check if the item is a slider item
      if (e === 'slider') {
        //Push the item to the slider array
        this.car.slider.push(item);
      } else {
        //Push the item to the features array
        this.car.features.push(item);
      }
    },
    getImage(e) {
      // Check if the data is main
      if (e.data === 'main') {
        // Set the main image and url
        this.car.main_image = e.file;
        this.url_main_thumbnail = e.url;
        this.url_main_image = e.url;
        // Check if the data is secondary
      } else if (e.data === 'secondary') {
        // Set the secondary image and url
        this.car.secondary_image = e.file;
        this.url_secondary_thumbnail = e.url;
        this.url_secondary_image = e.url;
        // Check if the data is not main or secondary
      } else {
        // Log the data
        console.log('data', e.data)
        // Set the data
        let data = e.data;
        // Loop through the car
        this.car[data].forEach(element => {
          // Log the element
          console.log('element', element)
          // Check if the id matches
          if (element.id === e.id) {
            // Set the get image, get thumbnail, and image
            element.get_image = e.url;
            element.get_thumbnail = e.url;
            element.image = e.file;
          }
        });
      }
    },
    getYears() {
      // Get the current year
      let year = new Date().getFullYear();
      // Create an empty array to store the years
      let y = [];
      // Loop through the years from 1950 to the current year
      for (let i = 1950; i <= year; i++) {
        // Push each year to the array
        y.push(i);
      }
      // Set the years property to the array of years
      this.years = y;
    },
    async getColors() {
      // make an API call to the server to get the list of colors
      await axios
        .get('/api/v1/cars/colors/')
        .then(response => {
          // set the colors property of the component to the response data
          this.colors = response.data;
        })
        .catch(error => {
          // log the error to the console
          console.log(error);
        })
    },
    async getCategories() {
      // make an API call to the specified endpoint
      await axios
        .get('/api/v1/cars/categories/')
        // if the API call is successful, set the response data to the categories property
        .then(response => {
          this.categories = response.data;
        })
        // if the API call fails, log the error
        .catch(error => {
          console.log(error);
        })
    },
    async getCarDetails() {
      // set loading to true
      this.modalCarLoading = true
      // create data object to pass to axios
      const data = {
        info: 'car-data',
        id: this.car.id
      }

      // send post request to /api/v1/cars/crud/ with data object
      await axios
        .post('/api/v1/cars/crud/', data)
        .then(response => {
          // log response data
          console.log(response.data)
          // set car data from response
          this.car.id = response.data['id'];
          this.car.available = response.data['available'];
          this.car.title = response.data['title'];
          this.car.category = response.data['category'];
          this.car.secondary_title = response.data['secondary_title'];
          this.car.description_title = response.data['description_title'];
          this.car.description = response.data['description'];
          this.car.year = response.data['year'];
          this.car.color = response.data['color'];
          this.car.doors = response.data['doors'];
          this.car.engine = response.data['engine'];
          this.car.price = parseInt(response.data['price']);
          this.car.slider = response.data['slider'];
          this.car.features = response.data['feature'];

          // loop through slider and set image, title, description, and image_error to empty string
          this.car.slider.forEach(element => {
            element.image = '';
            element.title_error = '';
            element.description_error = '';
            element.image_error = '';
          });
          // loop through features and set image, title, description, and image_error to empty string
          this.car.features.forEach(element => {
            element.image = '';
            element.title_error = '';
            element.description_error = '';
            element.image_error = '';
          });
          // set main image, secondary image, main thumbnail, and secondary thumbnail from response
          this.url_main_image = response.data['get_main_image'];
          this.url_secondary_image = response.data['get_secondary_image'];
          this.url_main_thumbnail = response.data['get_main_thumbnail'];
          this.url_secondary_thumbnail = response.data['get_secondary_thumbnail'];
          // call getCategories, getColors, and getYears functions
          this.getCategories();
          this.getColors();
          this.getYears();
          // log car data
          console.log(this.car)
          // log main thumbnail and secondary thumbnail
          console.log(this.url_main_thumbnail)
          console.log(this.url_secondary_thumbnail)
        })
        // if there is an error, log it
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

      // set loading to false
      this.modalCarLoading = false
    },
    async saveCar(e) {
      // set modalCarLoading to true
      this.modalCarLoading = true
      $('#car-information-modal').scrollTop(0)
      // set slider and features to '-'
      let slider = '-'
      let features = '-'

      // loop through car object
      Object.entries(this.car).forEach(([key, value]) => {
        // if value is null or empty
        if (value === null || value === '') {
          // if info is new-car
          if (this.info === 'new-car') {
            // set error to required
            this.error[key] = 'Required';
            // set timeout to clear error
            setTimeout(() => this.error[key] = '', 4000)
          } else {
            // if key is not main_image or secondary_image
            if (key != 'main_image' && key != 'secondary_image') {
              // log key and value
              console.log('k', key, value)
              // set error to required
              this.error[key] = 'Required';
              // set timeout to clear error
              setTimeout(() => this.error[key] = '', 4000)
            }
          }
        }

        // if key is slider or features
        if (key === 'slider' || key === 'features') {
          // loop through value
          value.forEach(element => {
            // loop through element
            Object.entries(element).forEach(([k, v]) => {
              // if k is get_image
              if (k == 'get_image') {
                // if v is null or empty
                if (v === null || v === '') {
                  // set image_error to required
                  element.image_error = 'Required';
                  // set timeout to clear image_error
                  setTimeout(() => element.image_error = '', 4000)
                }
              }

              // if v is null or empty
              if (v === null || v === '') {
                // if k is title
                if (k == 'title') {
                  // set title_error to required
                  element.title_error = 'Required';
                  // set timeout to clear title_error
                  setTimeout(() => element.title_error = '', 4000)
                }
                // if k is description
                if (k == 'description') {
                  // set description_error to required
                  element.description_error = 'Required';
                  // set timeout to clear description_error
                  setTimeout(() => element.description_error = '', 4000)
                }
              }
            })
          });
        }
      });


      // if slider is empty
      if (this.car.slider.length == 0) {
        // set slider to ''
        slider = ''
      } else {
        // loop through slider
        this.car.slider.forEach(element => {
          // if title_error, description_error and image_error are all empty
          if (!element.title_error && !element.description_error && !element.image_error) {
            // set slider to ''
            slider = '';
          }
        })
      }

      // if features is empty
      if (this.car.features.length == 0) {
        // set features to ''
        features = ''
      } else {
        // loop through features
        this.car.features.forEach(element => {
          // if title_error, description_error and image_error are all empty
          if (!element.title_error && !element.description_error && !element.image_error) {
            // set features to ''
            features = '';
          }
        })
      }

      // if error is empty
      if (!this.error.title && !this.error.secondary_title &&
        !this.error.description_title && !this.error.description &&
        !this.error.main_image && !this.error.secondary_image &&
        !slider && !features) {

        // create form data
        let formData = new FormData();

        // loop through car object
        Object.entries(this.car).forEach(([key, value]) => {
          // if key is slider or features
          if (key == 'slider' || key == 'features') {
            // set counter to 0
            let counter = 0;
            // loop through value
            value.forEach(element => {
              // loop through element
              Object.entries(element).forEach(([k, v]) => {
                // if v is instance of file
                if (v instanceof File) {
                  // append to form data
                  formData.append(key.concat('-images'), v, key.concat('-' + counter));
                  // set element[k] to true
                  element[k] = true;
                }
                // if k is get_image, get_thumbnail or get_created
                if (k == 'get_image' || k == 'get_thumbnail' || k == 'get_created') {
                  // delete element[k]
                  delete element[k];
                }
              })
              // append to form data
              formData.append(key, JSON.stringify(element));
              // increment counter
              counter++;
            })
          } else {
            // append to form data
            formData.append(key, value);
          }
        })

        // if info is defined
        if (this.info) {
          // append info to form data
          formData.append('info', this.info);
        } else {
          // append info to form data
          formData.append('info', 'update');
        }

        // send put request
        await axios
          .put('/api/v1/cars/crud/', formData)
          .then(response => {
            // emit close-modal
            this.$emit('close-modal');
            // emit getCars
            this.$emit('getCars')
            // clean fields
            this.cleanFields();
            // if info is defined
            if (this.info) {
              // emit getCars
              this.$emit('getCars')
            }
          })
          .catch(error => {
            // log error
            console.log(error)
          })
      }
      // set modalCarLoading to false
      this.modalCarLoading = false
    },
    cleanFields() {
      setTimeout(() => {
        this.car.id = '';
        this.car.available = false;
        this.car.title = '';
        this.car.category = '';
        this.car.secondary_title = '';
        this.car.description_title = '';
        this.car.description = '';
        this.car.year = '';
        this.car.color = '';
        this.car.doors = '';
        this.car.engine = '';
        this.car.price = '';
        this.car.main_image = '';
        this.car.secondary_image = '';
        this.car.slider = [];
        this.car.features = [];

        this.url_main_image = '';
        this.url_main_thumbnail = '';
        this.url_secondary_image = '';
        this.url_secondary_thumbnail = '';
        this.getCategories();
        this.getColors();
        this.getYears();
      }, 500)
    }
  }
}
</script>

<style lang="scss"></style>
