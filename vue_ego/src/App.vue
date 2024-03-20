<template>
  <button v-if="this.$store.state.isAuthenticated" @click="logout"
    class="w-full top-0 bg-red-700 hover:bg-red-800 text-white font-bold py-2 px-4 focus:outline-none focus:shadow-outline"
    type="button">
    Log out
  </button>

  <router-view v-slot="{ Component }">
    <component :is="Component" :key="$route.path" />
  </router-view>
</template>

<script>
import axios from 'axios'

export default {
  beforeCreate() {
    // Initialize the store
    this.$store.commit('initializeStore')

    // Check if the user is logged in
    if (this.$store.state.token != '') {
      // Get the token and expiration time from the store
      const token = this.$store.state.token
      const ex_time = new Date(this.$store.state.timeLogin)

      // Check if the token has expired
      if (ex_time.getTime() <= new Date().getTime()) {
        // If the token has expired, remove the token from the store and local storage
        axios.defaults.headers.common['Authorization'] = ""
        localStorage.removeItem("token")
        localStorage.removeItem("username")
        this.$store.commit('removeToken')
        // Redirect the user to the home page
        this.$router.push('/')
      } else {
        // If the token has not expired, add the token to the authorization header
        axios.defaults.headers.common['Authorization'] = "Token " + token
      }
    } else {
      // If the user is not logged in, remove the authorization header
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted() {
    //console.log = function() {}   
  },
  methods: {
    async logout() {
      //Send a POST request to the logout endpoint
      await axios
        .post("/api/v1/logout/")
        //If the request is successful, remove the token and username from local storage, remove the token from the store, and push the user to the home page
        .then(response => {
          localStorage.removeItem("token")
          localStorage.removeItem("username")
          this.$store.commit('removeToken')
          axios.defaults.headers.common["Authorization"] = ""
          this.$router.push('/')
        })
        //If the request fails, log the error
        .catch(error => {
          console.log(JSON.stringify(error))
        })
    },
  }
};
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');

</style>
