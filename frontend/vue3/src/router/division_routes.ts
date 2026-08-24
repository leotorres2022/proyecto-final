const division_routes = [
  {
    path: '/torneos/division',
    component: () => import('@/views/DivisionView.vue'),
    
    children: [
      {
        path: '', 
        name: 'division_home', 
        component: () => import('@/components/torneos_division/DivisionHome.vue'),
      },
      {
        path: 'list', 
        name: 'division_list', 
        component: () => import('@/components/torneos_division/DivisionList.vue'),
      },
    ]
  }
]


export default division_routes
