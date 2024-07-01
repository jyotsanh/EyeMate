import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/user/register/';
const API_URL_login = 'http://127.0.0.1:8000/api/user/login/';

// Function to register a new user
export const registerUser = async (userData) => {
  try {
    const response = await axios.post(API_URL, userData, {
      withCredentials: true, // This is necessary for cookies to be set
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};
export const loginUser = async (userData) => {
  try {
    const response = await axios.post(API_URL_login, userData, {
      withCredentials: true, // This is necessary for cookies to be set
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

