const tienda_routes = [
  {
    path: '/tienda',
    name: 'tienda',
    component: () => import('../views/TiendaView.vue') ,
    meta: {
      requiresAuth: true
    },
    
   }
]

export default tienda_routes
