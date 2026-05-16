const division_routes = [
  {
    path: '/torneos/division',
    component: () => import('@/views/DivisionView.vue'),
    children: [
      {
        path: '', // IMPORTANTE: Al estar vacío, este es el componente por defecto
        name: 'division_home', 
        component: () => import('@/components/torneos_division/DivisionHome.vue'),
      },
      {
        path: 'list', // Esta es la de las tablas
        name: 'division_list', 
        component: () => import('@/components/torneos_division/DivisionList.vue'),
      },
    ]
  }
]


export default division_routes
