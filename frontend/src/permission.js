import router from './router'
import store from './store'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style

NProgress.configure({ showSpinner: false }) // NProgress Configuration

// const whiteList = ['/login', '/auth-redirect'] // no redirect whitelist

router.beforeEach(async(to, from, next) => {
  // start progress bar
  NProgress.start()

  const hasRoles = store.getters.roles && store.getters.roles.length > 0
  if (hasRoles) {
    next()
  } else {
    // acceso total para todos los usuarios
    const { roles } = await store.dispatch('user/setDefaultUser')
    const accessRoutes = await store.dispatch('permission/generateRoutes', roles)
    router.addRoutes(accessRoutes)
    next({ ...to, replace: true })
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
