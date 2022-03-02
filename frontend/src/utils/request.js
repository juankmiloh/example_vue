import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  withCredentials: true,
  timeout: 100000
})
// request interceptor
service.interceptors.request.use(
  config => {
    // Do something before request is sent
    store.dispatch('app/setLoading')
    if (store.getters.token) {
      config.headers['X-Token'] = getToken()
    }
    return config
  },
  error => {
    // Do something with request error
    store.dispatch('app/claearLoading')
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get information such as headers or status
   * Please return  response => response
  */
  response => {
    const res = response.data
    store.dispatch('app/claearLoading')
    return res
  },
  error => {
    store.dispatch('app/claearLoading')
    console.log('err' + error) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
