<template>
  <div class="flex items-center justify-center h-screen text-center bg-stone-300" id="login-view">
    <div class="text-center">
      <div role="status" v-if="this.$store.state.isLoading">
        <svg aria-hidden="true" class="inline w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
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

    <div class="w-[300px] mx-auto bg-slate-400 mx-10" id="login-div">
      <h1 class="title py-5 mx-10 font-bold">EGO CAR DEALER</h1>

      <div id="username-div" class="mb-4 mx-5">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
          Username
        </label>
        <input v-model="username"
          class="rounded w-[70%] py-2 px-3 mb-1 text-gray-700 focus:outline-none focus:shadow-outline" id="username"
          type="email" placeholder="example@gmail.com">

        <span v-if="errorUser">
          <p class="absolute left-0 right-0 text-red-600">{{ errorUser }}</p>
        </span>
      </div>

      <div id="password-div" class="mx-5 my-5">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
          Password
        </label>
        <input v-on:keyup.enter="onEnter" v-model="password"
          class="rounded w-[70%] py-2 px-3 mb-1 text-gray-700 focus:outline-none focus:shadow-outline" id="password"
          type="password" placeholder="******************">

        <span v-if="errorPassword">
          <p class="absolute left-0 right-0 text-red-600">{{ errorPassword }}</p>
        </span>
      </div>

      <div class="py-5 mx-10" id="button-submit">
        <button @click="Login"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="button">
          Log In
        </button>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'IniciarSesionView',
  data() {
    return {
      username: '',
      password: '',
      errorUser: '',
      errorPassword: '',
      login: true,
    }
  },
  mounted() {
    document.title = 'Log In | EGO Car Dealer'
    this.logged()
  },
  methods: {
    onEnter() {
      this.Login()
    },
    logged() {
      // Check if user is authenticated
      if (this.$store.state.isAuthenticated == true) {
        // Set the path to the route query or default to /cars
        const toPath = this.$route.query.to || '/cars'
        // Push the path to the router
        this.$router.push(toPath)
      }
    },
    async Login(e) {
      // Check if username is empty
      if (!this.username) {
        // Set error message
        this.errorUser = 'Required';
        // Set timeout to clear error message
        setTimeout(() => this.errorUser = '', 2000)
      }
      // Check if password is empty
      if (!this.password) {
        // Set error message
        this.errorPassword = 'Required';
        // Set timeout to clear error message
        setTimeout(() => this.errorPassword = '', 2000)
      }

      // Check if errorUser and errorPassword are empty
      if (!this.errorUser && !this.errorPassword) {
        // Set authorization header
        axios.defaults.headers.common["Authorization"] = ""
        // Remove token from local storage
        localStorage.removeItem("token")
        // Set loading to true
        this.$store.commit('setIsLoading', true)
        // Create data object
        const data = {
          username: this.username,
          password: this.password,
        }

        // Make post request
        axios
          .post("/api/v1/login/", data)
          .then(response => {
            // Check if response is user not found
            if (response.data == 'user not found') {
              // Set error message
              this.errorUser = ('User not found')
              // Set timeout to clear error message
              setTimeout(() => this.errorUser = '', 2000)
              // Check if response is wrong password or username
            } else if (response.data == 'wrong password or username') {
              // Set error message
              this.errorPassword = ('Wrong password or username')
              // Set timeout to clear error message
              setTimeout(() => this.errorPassword = '', 2000)
              // Check if response is token
            } else if (response.data.token) {
              // Set token
              const token = response.data['token']
              // Set timeLogin
              const timeLogin = response.data['expiry']
              // Set token in store
              this.$store.commit('setToken', token)
              // Set timeLogin in store
              this.$store.commit('setTimeLogin', timeLogin)
              // Set authorization header
              axios.defaults.headers.common["Authorization"] = "Token " + token
              // Set token in local storage
              localStorage.setItem("token", token)
              // Set timeLogin in local storage
              localStorage.setItem("timeLogin", timeLogin)
              // Set username in local storage
              localStorage.setItem("username", this.username)
              // Set path to redirect to
              const toPath = this.$route.query.to || '/cars'
              // Push to path
              this.$router.push(toPath)
            }
          })
          .catch(error => {
            // Set errors to empty array
            this.errors = []
            // Check if error is response
            if (error.response) {
              // Loop through response data
              for (const property in error.response.data) {
                // Check if response data is unable to log in with provided credentials
                if (error.response.data[property] == 'Unable to log in with provided credentials.')
                  // Set error message
                  this.errorPassword = error.response.data[property]
                // Set timeout to clear error message
                setTimeout(() => this.errorPassword = '', 2000)
              }
              // Check if error is error
            } else {
              // Log error
              console.log(JSON.stringify(error))
            }
          })

        // Set loading to false
        this.$store.commit('setIsLoading', false)
      }
    }
  }
}
</script>

<style></style>