import { instance  as axios } from "@/plugins/axios"
class ApiService {
  static async getAll(url: string) {
    const response = await axios.get(url);
    return response.data
  }
static async get(endpoint: string, params?: object) {
    try {
       
        const response = await axios.get(endpoint, { params });
        return response.data;
    } catch (error) {
        throw error;
    }
}

static async create (url: string, data: object) {
  try {
    const response = await axios.post(url, data);
    if (response) {
      return response.data
    }
  } catch (error) {
    return error
  }
}

static async update (url: string, id: number, data: object) {
  try {
    const response = await axios.patch(`${url}${id}/`, data);
    if (response) {
      return response.data
    }
  } catch (error) {
    return error
  }
}
static async destroy (url: string, id: number) {
    try {
      const response = await axios.delete(`${url}${id}/`);
      if (response) {
        return response.data
      }
    } catch (error) {
      return error;
    }
  }

 static async destroyUrl(endpoint: string) {
  const response = await axios.delete(endpoint)
  return response.data
}
}

export default ApiService
