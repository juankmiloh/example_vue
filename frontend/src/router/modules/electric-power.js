/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

var marketPowerChildren = [
  {
    path: 'ihh',
    component: () => import('@/views/electric-power/market-power/ihh/complete'),
    name: 'ihh',
    meta: { title: 'ihh', icon: 'poll', fa: true }
  },
  {
    path: 'ihh_c',
    component: () => import('@/views/electric-power/market-power/ihh/capacity'),
    name: 'ihh_c',
    meta: { title: 'capacity', icon: 'poll', fa: true }
  },
  {
    path: 'ihh_g',
    component: () => import('@/views/electric-power/market-power/ihh/generation'),
    name: 'ihh_g',
    meta: { title: 'generation', icon: 'poll', fa: true }
  },
  {
    path: 'ihh_dr',
    component: () => import('@/views/electric-power/market-power/ihh/realDisponibility'),
    name: 'ihh_dr',
    meta: { title: 'realDisponibility', icon: 'poll', fa: true }
  },
  {
    path: 'ihh_dd',
    component: () => import('@/views/electric-power/market-power/ihh/declaredDisponibility'),
    name: 'ihh_dd',
    meta: { title: 'declaredDisponibility', icon: 'poll', fa: true }
  },
  {
    path: 'trsd',
    component: () => import('@/views/electric-power/market-power/trsd'),
    name: 'trsd',
    meta: { title: 'trsd', icon: 'poll', fa: true }
  },
  {
    path: 'pivotal',
    component: () => import('@/views/electric-power/market-power/pivotal'),
    name: 'pivotal',
    meta: { title: 'pivotal', icon: 'poll', fa: true }
  },
  {
    path: 'pivotal3d',
    component: () => import('@/views/electric-power/market-power/pivotal3d'),
    name: 'pivotal3d',
    meta: { title: 'pivotal3d', icon: 'poll', fa: true }
  },
  {
    path: 'fpp',
    component: () => import('@/views/electric-power/market-power/fpp'),
    name: 'fpp',
    meta: { title: 'fpp', icon: 'poll', fa: true }
  }
]

var marketReliabilitiesChildren = [
  {
    path: 'icoef',
    component: () => import('@/views/electric-power/market-power/icoef'),
    name: 'icoef',
    meta: { title: 'icoef', icon: 'poll', fa: true }
  },
  {
    path: 'icoef-cober',
    component: () => import('@/views/electric-power/market-power/icoef-cober'),
    name: 'icoefCober',
    meta: { title: 'icoefCober', icon: 'poll', fa: true }
  }

]

if (process.env.VUE_APP_PUBLIC === 'false') {
  marketReliabilitiesChildren.push(
    {
      path: 'iar',
      component: () => import('@/views/electric-power/market-power/iar'),
      name: 'iar',
      meta: { title: 'iar', icon: 'poll', fa: true }
    }
  )
  marketReliabilitiesChildren.push(
    {
      path: 'iag',
      component: () => import('@/views/electric-power/market-power/iag'),
      name: 'iag',
      meta: { title: 'iag', icon: 'poll', fa: true }
    }
  )
}
/*
if (process.env.VUE_APP_PUBLIC === 'false') {
  marketPowerChildren.push(
    {
      path: 'pivotal3d',
      component: () => import('@/views/electric-power/market-power/pivotal3d'),
      name: 'pivotal3d',
      meta: { title: 'pivotal3d', icon: 'poll', fa: true }
    }
  )
}
*/
var electricPowerRouter = {
  path: '/electric-power',
  component: Layout,
  redirect: '/electric-power/market-power/ihh',
  name: 'ElectricPower',
  meta: { title: 'electricPower', icon: 'lightbulb', fa: true },
  children: [
    {
      path: 'market-power',
      component: () => import('@/views/electric-power/market-power/'),
      name: 'MarketPower',
      meta: { title: 'Concentration', icon: 'balance-scale', fa: true },
      redirect: '/electric-power/market-power/ihh',
      children: marketPowerChildren
    },
    {
      path: 'market-operations',
      component: () => import('@/views/electric-power/market-power/'),
      name: 'Operation',
      meta: { title: 'Operation', icon: 'balance-scale', fa: true },
      redirect: '/electric-power/market-power/ihh',
      children: [
        {
          path: 'grgp',
          component: () => import('@/views/electric-power/market-power/grgp'),
          name: 'grgp',
          meta: { title: 'grgp', icon: 'poll', fa: true }
        },
        {
          path: 'grgpa',
          component: () => import('@/views/electric-power/market-power/grgpa'),
          name: 'grgpa',
          meta: { title: 'grgpa', icon: 'poll', fa: true }
        }
      ]
    },
    {
      path: 'market-reliabilities',
      component: () => import('@/views/electric-power/market-power/'),
      name: 'Reliability',
      meta: { title: 'Reliability', icon: 'balance-scale', fa: true },
      redirect: '/electric-power/market-power/icoef',
      children: marketReliabilitiesChildren
    },
    {
      path: 'pb',
      component: () => import('@/views/electric-power/offer-prices/stock-prices'),
      name: 'pb',
      meta: { title: 'stockPrice', icon: 'poll', fa: true }
    },
    {
      path: 'op',
      component: () => import('@/views/electric-power/offer-prices/offer-prices'),
      name: 'op',
      meta: { title: 'offerPrice', icon: 'poll', fa: true }
    }
  ]
}

export default electricPowerRouter
