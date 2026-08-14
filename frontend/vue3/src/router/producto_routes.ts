const producto_routes = [
  {
    path: '/productos',
    name: 'productos',
    component: () => import('../views/ProductosView.vue'),
    children: [
      {
        path: '',
        name: 'productos_list',
        component: () => import('../components/productos/ProductosList.vue'),
      },
      {
        path: ':id/update',
        name: 'productos_update',
        component: () => import('../components/productos/ProductosUpdate.vue'),
      },
      {
        path: '',
        name: 'productos_create',
        component: () => import('../components/productos/ProductosCreate.vue'),
      },
      {
        path: ':id/show',
        name: 'productos_show',
        component: () => import('../components/productos/ProductosShow.vue'),
      },

    ]
  }
]

export default producto_routes
