/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

var fuelGasRouter = {
  path: '/fuel-gas',
  component: Layout,
  redirect: '/fuel-gas/market/pm',
  name: 'FuelGas',
  meta: { title: 'fuelGas', icon: 'burn', fa: true },
  children: [
    {
      path: 'market',
      component: () => import('@/views/fuel-gas/market/'),
      name: 'Market',
      meta: { title: 'Market', icon: 'balance-scale', fa: true },
      redirect: '/fuel-gas/market/pm',
      children: [
        {
          path: 'pm',
          component: () => import('@/views/fuel-gas/market/pm'),
          name: 'pm',
          meta: { title: 'pm', icon: 'poll', fa: true }
        }
      ]
    },
    {
      path: 'oc',
      component: () => import('@/views/fuel-gas/oc'),
      name: 'oc',
      meta: { title: 'oc', icon: 'poll', fa: true }
    },
    {
      path: 'og',
      component: () => import('@/views/fuel-gas/og'),
      name: 'og',
      meta: { title: 'og', icon: 'poll', fa: true }
    },
    {
      path: 'gasInventory',
      component: () => import('@/views/fuel-gas/inventory'),
      name: 'gasInventory',
      meta: { title: 'gasInventory', icon: 'poll', fa: true }
    },
    {
      path: 'gpin',
      component: () => import('@/views/fuel-gas/gpin'),
      name: 'gpin',
      meta: { title: 'gpin', icon: 'poll', fa: true }
    }
  ]
}
if (process.env.VUE_APP_PUBLIC === 'false') {
  fuelGasRouter.children.push(
    {
      path: 'daggi',
      component: () => import('@/views/fuel-gas/daggi'),
      name: 'daggi',
      meta: { title: 'daggi', icon: 'poll', fa: true }
    }
  )
  fuelGasRouter.children.push(
    {
      path: 'idp',
      component: () => import('@/views/fuel-gas/idp'),
      name: 'idp',
      meta: { title: 'idp', icon: 'poll', fa: true }
    }
  )
  fuelGasRouter.children.push(
    {
      path: 'edp',
      component: () => import('@/views/fuel-gas/edp'),
      name: 'edp',
      meta: { title: 'edp', icon: 'poll', fa: true }
    }
  )
  fuelGasRouter.children.push(
    {
      path: 'rc',
      component: () => import('@/views/fuel-gas/rc'),
      name: 'rc',
      meta: { title: 'rc', icon: 'poll', fa: true }
    }
  )
  fuelGasRouter.children.push(
    {
      path: 'dp',
      component: () => import('@/views/fuel-gas/dp'),
      name: 'dp',
      meta: { title: 'dp', icon: 'poll', fa: true }
    }
  )
  fuelGasRouter.children.push(
    {
      path: 'mc',
      component: () => import('@/views/fuel-gas/mc'),
      name: 'mc',
      meta: { title: 'mc', icon: 'poll', fa: true }
    }
  )
  fuelGasRouter.children.push(
    {
      path: 'contractNetwork',
      component: () => import('@/views/fuel-gas/contract-network'),
      name: 'contractNetwork',
      meta: { title: 'contractNetwork', icon: 'poll', fa: true }
    }
  )
}

export default fuelGasRouter
