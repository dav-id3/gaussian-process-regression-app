import { MlApi } from "./generated/api";

import axios from "axios";

const API_BASE_URL = process.env.API_BASE_URL || "http://localhost:8000";

const MlApiClient = new AccountApi(undefined, API_BASE_URL, axios);

export { MlApiClient };