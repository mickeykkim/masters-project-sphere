import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import Patients from '@/components/Patients'
import PatientCreate from '@/components/PatientCreate'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'root',
      component: Main
    },
    {
      path: '/patients',
      name: 'Patients',
      component: Patients
    },
    {
      path: '/patients/:pk',
      name: 'PatientCreate',
      component: PatientCreate
    }
  ]
})
