import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/students',
    children: [
      {
        path: 'students',
        component: () => import('@/views/astudents/index'),
        name: 'students',
        meta: { title: '学生管理', icon: 'people', affix: true }
      }
    ]
  },
  {
    path: '/class',
    component: Layout,
    redirect: '/classes',
    children: [
      {
        path: 'classes',
        component: () => import('@/views/aclasses/index'),
        name: 'classes',
        meta: { title: '班级管理', icon: 'tree-table', affix: true }
      }
    ]
  },
  {
    path: '/check',
    component: Layout,
    redirect: '/check',
    children: [
      {
        path: 'check',
        component: () => import('@/views/acheck/index'),
        name: 'check',
        meta: { title: '考勤管理', icon: 'dashboard', affix: true }
      }
    ]
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
