// configures axios client not to throw error when status code indicate failure
import axios from "axios";
import { config } from "process";

const client = axios.create({
  validateStatus: (status: number) => true,
  withCredentials: true,
  timeout: Number(process.env.TIME_OUT),
});

client.interceptors.response.use((config) => config);
client.interceptors.request.use(
  (response) => response,
  (err) => err.response
);

export default client;