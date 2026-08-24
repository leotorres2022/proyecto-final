const producto_routes = [
  {
    path: '/productos',
    name: 'productos',
    component: () => import('../views/ProductosView.vue'),
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '',
        name: 'productos_list',
        component: () => import('../components/producto/ProductoList.vue'),
      },
      {
        path: ':id/update',
        name: 'productos_update',
        component: () => import('../components/producto/ProductoUpdate.vue'),
      },
      {
        path: 'create',
        name: 'productos_create',
        component: () => import('../components/producto/ProductoCreate.vue'),
      },
      {
        path: ':id/show',
        name: 'productos_show',
        component: () => import('../components/producto/ProductoShow.vue'),
      },

      {
        path: 'stock',
        name: 'stock_list',
        component: () => import('../components/producto/StockList.vue'),  
      }

    ]
  }
]

export default producto_routes
