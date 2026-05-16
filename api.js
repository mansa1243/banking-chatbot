import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getBalance = async (user_id) => {
  const res = await API.post("/chat", {
    message: "show balance",
    user_id,
  });

  return res.data;
};