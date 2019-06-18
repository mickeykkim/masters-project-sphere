import axios from 'axios';
import AuthService from '../auth/AuthService';
const API_URL = 'http://localhost:8000';

export class APIService{
   constructor(){

   }

   getPatientData() {
      const url = `${API_URL}/patient/`;
      return axios.get(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }}).then(response => response.data);
   }

   getPatientDataByID(pk) {
      const url = `${API_URL}/patient/${pk}`;
      return axios.get(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }}).then(response => response.data);
   }

   getProductsByURL(link){
      const url = `${API_URL}${link}`;
      return axios.get(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }}).then(response => response.data);
   }

   deletePatientData(patient){
      const url = `${API_URL}/patient/${patient.pk}`;
      return axios.delete(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }});
   }

   createPatientData(patient){
      const url = `${API_URL}/patient/`;
      const headers = {Authorization: `Bearer ${AuthService.getAuthToken()}`};
      return axios.post(url, patient, {headers: headers});
   }

   updateProduct(patient){
      const url = `${API_URL}/patient/${patient.pk}`;
      const headers = {Authorization: `Bearer ${AuthService.getAuthToken()}`};
      return axios.put(url, patient, {headers: headers});
   }
}