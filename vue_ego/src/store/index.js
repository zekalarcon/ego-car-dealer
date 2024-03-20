import { createStore } from 'vuex'

export default createStore({
  state: {
    isLoading: false,
    isAuthenticated: false,
    token: '',
    timeLogin:'',
    showModalEditCar: false
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
          state.token = localStorage.getItem('token')
          state.isAuthenticated = true
          state.timeLogin = localStorage.getItem('timeLogin')
      } else {
          state.token = ''
          state.isAuthenticated = false
          state.timeLogin = ''
      } 
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },  
    removeToken(state) {
      state.token = ''
      state.isAuthenticated = false
    },
    setTimeLogin(state, timeLogin) {
      state.timeLogin = timeLogin
    }
  },
  actions: {
  },
  modules: {
  }
})
