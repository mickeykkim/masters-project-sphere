'use strict'

import axios from 'axios'
import store from '@/store/store'

const API_URL = 'http://localhost:8000';

export class APIService{
  constructor(){

  }

  getPatientData() {
    const url = `${API_URL}/patient/`;
    return axios.get(url, { headers: {Authorization: `Bearer ${store.state.token}`}}).then(response => response.data);
  }

  getPatientDataByID(pk) {
    const url = `${API_URL}/patient/${pk}`;
    return axios.get(url, { headers: {Authorization: `Bearer ${store.state.token}`}}).then(response => response.data);
  }

  getPatientDataByURL(link){
    const url = `${API_URL}${link}`;
    return axios.get(url, { headers: {Authorization: `Bearer ${store.state.token}`}}).then(response => response.data);
  }

  deletePatientData(patient){
    const url = `${API_URL}/patient/${patient.pk}`;
    return axios.delete(url, { headers: {Authorization: `Bearer ${store.state.token}`}});
  }

  createPatientData(patient){
    const url = `${API_URL}/patient/`;
    const headers = {Authorization: `Bearer ${store.state.token}`};
    return axios.post(url, patient, {headers: headers});
  }

  updateProduct(patient){
    const url = `${API_URL}/patient/${patient.pk}`;
    const headers = {Authorization: `Bearer ${store.state.token}`};
    return axios.put(url, patient, {headers: headers});
  }
}

export default() => {
  return axios.create({
    baseURL: `${API_URL}`,
    headers: {
      Authorization: `Bearer ${store.state.token}`
    }
  })
}
