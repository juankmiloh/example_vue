import request from '@/utils/request'

export function searchUser(name) {
  return request({
    url: '/search/user',
    method: 'get',
    params: { name }
  })
}

export function transactionList(query) {
  return request({
    url: '/transaction/list',
    method: 'get',
    params: query
  })
}

export function getIndicator(id, query) {
  return request({
    url: `/indicadores/${id}`,
    method: 'get',
    params: query
  })
}

export function getLastDate(id) {
  return request({
    url: '/indicadores/indicador',
    method: 'get',
    params: { 'nombre': id }
  })
}
